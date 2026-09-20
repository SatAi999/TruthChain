import os
import logging
from typing import List, Dict, Any, Optional
from PIL import Image
from app.core.security import sanitize_document_text

logger = logging.getLogger("truthchain.ocr")

class OCRService:
    @classmethod
    def process_image_file(cls, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """
        Executes deployment-safe OCR on an image file (PNG, JPG, JPEG, WEBP).
        Uses rapidocr (pure Python ONNX runtime) or pytesseract fallback.
        Returns: List of parsed document dicts with page, text, bounding_box, confidence.
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
            return []

        ocr_text = ""
        ocr_confidence = 0.92
        ocr_provider = "RapidOCR (ONNX Runtime)"

        # 1. Try RapidOCR (Pure Python, zero system binary dependency)
        try:
            from rapidocr import RapidOCR
            engine = RapidOCR()
            result, _ = engine(file_path)
            if result:
                lines = [line[1] for line in result if line and len(line) > 1]
                ocr_text = "\n".join(lines)
        except Exception as e:
            logger.warning(f"RapidOCR processing failed: {e}. Trying pytesseract fallback...")

        # 2. Pytesseract Fallback if installed
        if not ocr_text:
            try:
                import pytesseract
                img = Image.open(file_path)
                ocr_text = pytesseract.image_to_string(img)
                ocr_provider = "Tesseract OCR"
            except Exception as e:
                logger.warning(f"Pytesseract fallback failed: {e}")

        # 3. Handle image content fallback
        if not ocr_text:
            ocr_text = f"[SCANNED DOCUMENT IMAGE: {filename} - Text extraction unavailable]"
            ocr_confidence = 0.50

        clean_text = sanitize_document_text(ocr_text)

        return [{
            "page_number": 1,
            "section_name": f"OCR Extracted Layer ({ocr_provider})",
            "raw_content": clean_text,
            "ocr_provider": ocr_provider,
            "ocr_confidence": ocr_confidence
        }]

    @classmethod
    def process_scanned_pdf(cls, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """
        Processes scanned PDFs by rendering pages to images and executing RapidOCR.
        """
        docs = []
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(file_path)
            for page_idx, page in enumerate(pdf, start=1):
                text_page = page.get_textpage()
                text = text_page.get_text_range().strip()
                
                if text:
                    # Text PDF - use text layer directly
                    docs.append({
                        "page_number": page_idx,
                        "section_name": f"Page {page_idx}",
                        "raw_content": sanitize_document_text(text),
                        "ocr_provider": "Native PDF Text Layer",
                        "ocr_confidence": 1.0
                    })
                else:
                    # Image-only scanned page - render to image and OCR
                    pil_image = page.render(scale=2).to_pil()
                    tmp_img_path = f"tmp_page_{page_idx}.png"
                    pil_image.save(tmp_img_path)
                    try:
                        ocr_res = cls.process_image_file(tmp_img_path, tmp_img_path)
                        if ocr_res:
                            docs.append({
                                "page_number": page_idx,
                                "section_name": f"Scanned Page {page_idx} (OCR)",
                                "raw_content": ocr_res[0]["raw_content"],
                                "ocr_provider": ocr_res[0]["ocr_provider"],
                                "ocr_confidence": ocr_res[0]["ocr_confidence"]
                            })
                    finally:
                        if os.path.exists(tmp_img_path):
                            os.remove(tmp_img_path)
        except Exception as e:
            logger.error(f"Scanned PDF processing failed: {e}")

        return docs
