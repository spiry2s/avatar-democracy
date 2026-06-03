"""
Text extraction from bill sources: raw text, URLs, and uploaded PDFs.
"""

from __future__ import annotations

import io
import re


def extract_text(source: str | bytes, source_type: str) -> str:
    """
    Extract plain text from a bill source.

    Args:
        source: The bill source — str for text/url, bytes for pdf.
        source_type: One of "text", "url", "pdf".

    Returns:
        Extracted plain text.

    Raises:
        ValueError: If extraction fails or source_type is unknown.
    """
    if source_type == "text":
        return source if isinstance(source, str) else source.decode("utf-8", errors="replace")

    if source_type == "url":
        return _extract_from_url(source)

    if source_type == "pdf":
        content = source if isinstance(source, bytes) else source.encode("latin-1")
        return _extract_from_pdf(content)

    raise ValueError(f"Unknown source_type: {source_type!r}. Expected 'text', 'url', or 'pdf'.")


def _extract_from_url(url: str) -> str:
    """Fetch a URL and extract text. Handles HTML and PDF responses."""
    try:
        import httpx
    except ImportError as e:
        raise ImportError("httpx is required for URL extraction: pip install httpx") from e

    with httpx.Client(follow_redirects=True, timeout=30) as client:
        response = client.get(url, headers={"User-Agent": "BillAnalyzer/0.1"})
        response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()

    if "pdf" in content_type:
        return _extract_from_pdf(response.content)

    return _extract_from_html(response.text)


def _extract_from_html(html: str) -> str:
    """Strip HTML tags and return readable text."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
    except ImportError:
        # Fallback: crude tag stripping
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"&[a-z]+;", " ", text)

    # Collapse whitespace
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def _extract_from_pdf(content: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        import pypdf
    except ImportError as e:
        raise ImportError("pypdf is required for PDF extraction: pip install pypdf") from e

    reader = pypdf.PdfReader(io.BytesIO(content))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())

    if not pages:
        raise ValueError("Could not extract any text from the PDF. It may be a scanned image.")

    return "\n\n".join(pages)
