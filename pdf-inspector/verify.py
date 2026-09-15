"""抽出結果の精度を確認するための検証スクリプト。

自動でわかる範囲(構造的な整合性)をチェックし、目視確認が必要なページは
画像としてレンダリングして output/page_renders/ に保存する。

チェック内容:
  1. ページ数の一致 (pdf-inspector が報告した page_count と実際の PDF ページ数)
  2. pdf-inspector 自身の診断 (has_encoding_issues, confidence, pages_needing_ocr)
  3. 画像/グラフ領域の検出数 vs 実際の埋め込み画像・ベクター描画オブジェクト数(ページ単位)
     -> 大きく食い違うページは検出漏れ/誤検出の疑いがあるとして警告し、目視用に全ページを画像化する
  4. 表・複数カラムが検出されたページも同様に画像化(表の列ズレ等は自動チェックできないため)

使い方:
    source .venv/bin/activate
    python verify.py [PDFファイル名]
"""

import sys
from pathlib import Path

import pdf_inspector
import pymupdf

SOURCE_DIR = Path(__file__).parent.parent / "source_pdf"
OUTPUT_DIR = Path(__file__).parent / "output"


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "assets_com_9ji_kotuanzen.pdf"
    pdf_path = SOURCE_DIR / filename

    result = pdf_inspector.process_pdf(str(pdf_path))
    items = pdf_inspector.extract_text_with_positions(str(pdf_path))

    doc = pymupdf.open(str(pdf_path))
    actual_page_count = doc.page_count

    print("=== 1. ページ数の一致 ===")
    match = "OK" if result.page_count == actual_page_count else "NG"
    print(f"[{match}] pdf-inspector={result.page_count} / 実際={actual_page_count}")

    print("\n=== 2. pdf-inspector自身の診断 ===")
    print(f"confidence={result.confidence:.2f}")
    print(f"has_encoding_issues={result.has_encoding_issues}")
    print(f"pages_needing_ocr={result.pages_needing_ocr}")

    print("\n=== 3. 画像/グラフ領域の検出数 vs 実際のオブジェクト数(ページ単位) ===")
    detected_by_page: dict[int, int] = {}
    for it in items:
        if it.item_type == "image":
            detected_by_page[it.page] = detected_by_page.get(it.page, 0) + 1

    pages_to_render: set[int] = set()
    all_pages = sorted(set(detected_by_page) | set(result.pages_with_tables))
    for page_no in all_pages:
        page = doc[page_no - 1]
        actual_images = len(page.get_images(full=True))
        actual_drawings = len(page.get_drawings())
        detected = detected_by_page.get(page_no, 0)
        has_table = page_no in result.pages_with_tables
        note = []
        # 目安: 検出0件なのに実際は画像/描画がある場合は見逃しの疑い
        if detected == 0 and (actual_images > 0 or actual_drawings > 5):
            note.append("検出漏れの疑い")
            pages_to_render.add(page_no)
        if has_table:
            note.append("表あり(要目視)")
            pages_to_render.add(page_no)
        print(
            f"page={page_no:>3} 検出={detected} 実画像={actual_images} "
            f"ベクター描画={actual_drawings} {' / '.join(note)}"
        )

    print(f"\n=== 4. 目視確認用にページ画像を保存 ({len(pages_to_render)}ページ) ===")
    render_dir = OUTPUT_DIR / "page_renders" / pdf_path.stem
    render_dir.mkdir(parents=True, exist_ok=True)
    for page_no in sorted(pages_to_render):
        page = doc[page_no - 1]
        pix = page.get_pixmap(dpi=150)
        out_path = render_dir / f"page{page_no:03d}.png"
        pix.save(out_path)
        print(f"saved: {out_path}")

    doc.close()
    print(
        f"\n上記ページ画像を output/{pdf_path.stem}.md の該当箇所と見比べて、"
        "表のズレや文字化けがないか目視確認してください。"
    )


if __name__ == "__main__":
    main()
