import re
import os
from fastapi import HTTPException
from app.core.config import settings

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes uploaded filenames to prevent path traversal attacks.
    Strips path separators and restricts to safe alphanumeric, dot, dash, underscore characters.
    """
    cleaned = os.path.basename(filename)
    return re.sub(r'[^a-zA-Z0-9_\.\-]', '_', cleaned)

def validate_file_upload(filename: str, file_size_bytes: int = 0):
    """
    Validates file extension and size limits for safe document ingestion.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed extensions: {', '.join(sorted(settings.ALLOWED_EXTENSIONS))}"
        )
    
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

def sanitize_document_text(text: str) -> str:
    """
    Defends against prompt injection in uploaded document content.
    Strips adversarial instructions trying to override system prompts or declare claims true.
    """
    if not text:
        return ""
    
    injection_patterns = [
        r"(?i)ignore\s+all\s+(previous\s+)?instructions",
        r"(?i)you\s+are\s+now\s+a",
        r"(?i)system\s+prompt:",
        r"(?i)declare\s+this\s+claim\s+true",
        r"(?i)override\s+verdict",
        r"(?i)set\s+verdict\s+to\s+supported",
        r"(?i)disregard\s+contradictions"
    ]
    
    cleaned_text = text
    for pattern in injection_patterns:
        cleaned_text = re.sub(pattern, "[FILTERED_INSTRUCTION_ATTEMPT]", cleaned_text)
    
    return cleaned_text

def format_document_for_llm(doc_name: str, content: str, page: int = 1) -> str:
    """
    Wraps document content in isolated XML-like data blocks to prevent prompt injection execution.
    """
    safe_content = sanitize_document_text(content)
    return f"""<DOCUMENT_CONTENT_BLOCK>
<METADATA>
  <NAME>{doc_name}</NAME>
  <PAGE>{page}</PAGE>
</METADATA>
<CONTENT>
{safe_content}
</CONTENT>
</DOCUMENT_CONTENT_BLOCK>"""
