import os
import pytest
from PIL import Image, ImageDraw, ImageFont
from app.services.ocr_service import OCRService

def test_ocr_image_processing(tmp_path):
    # Create a synthetic image containing readable text
    img_path = str(tmp_path / "test_receipt.png")
    img = Image.new("RGB", (400, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 30), "INVOICE #99823 TOTAL $10,000", fill=(0, 0, 0))
    img.save(img_path)

    res = OCRService.process_image_file(img_path, "test_receipt.png")
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]["page_number"] == 1
    assert "ocr_provider" in res[0]
    assert "raw_content" in res[0]
    assert len(res[0]["raw_content"]) > 0

def test_ocr_unsupported_file_extension():
    res = OCRService.process_image_file("file.txt", "file.txt")
    assert res == []
