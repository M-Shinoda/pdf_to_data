"""markitdown で source_pdf 内のPDFをMarkdownに変換し、output/ に保存する。

使い方:
    source .venv/bin/activate
    python run.py [PDFファイル名]   # 省略時は assets_com_9ji_kotuanzen.pdf
"""

import sys
from pathlib import Path

from markitdown import MarkItDown

SOURCE_DIR = Path(__file__).parent.parent / "source_pdf"
OUTPUT_DIR = Path(__file__).parent / "output"


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "assets_com_9ji_kotuanzen.pdf"
    pdf_path = SOURCE_DIR / filename
    output_path = OUTPUT_DIR / (pdf_path.stem + ".md")

    md = MarkItDown()
    result = md.convert(str(pdf_path))

    print(f"title={result.title}")
    print(f"text_content length={len(result.text_content)}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path.write_text(result.text_content, encoding="utf-8")
    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
