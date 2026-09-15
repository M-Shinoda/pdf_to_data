"""pdf-inspector で source_pdf 内のPDFをMarkdownに変換し、output/ に保存する。

使い方:
    source .venv/bin/activate
    python run.py [PDFファイル名]   # 省略時は assets_com_9ji_kotuanzen.pdf
"""

import sys
from pathlib import Path

import pdf_inspector

SOURCE_DIR = Path(__file__).parent.parent / "source_pdf"
OUTPUT_DIR = Path(__file__).parent / "output"


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "assets_com_9ji_kotuanzen.pdf"
    pdf_path = SOURCE_DIR / filename
    output_path = OUTPUT_DIR / (pdf_path.stem + ".md")

    classification = pdf_inspector.classify_pdf(str(pdf_path))
    print(f"pdf_type={classification.pdf_type} pages={classification.page_count} "
          f"confidence={classification.confidence:.2f}")

    result = pdf_inspector.process_pdf(str(pdf_path))
    print(f"processing_time_ms={result.processing_time_ms}")
    print(f"page_count={result.page_count}")
    print(f"is_complex_layout={result.is_complex_layout}")
    print(f"pages_needing_ocr={result.pages_needing_ocr}")
    print(f"pages_with_tables={result.pages_with_tables}")
    print(f"has_encoding_issues={result.has_encoding_issues}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path.write_text(result.markdown, encoding="utf-8")
    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
