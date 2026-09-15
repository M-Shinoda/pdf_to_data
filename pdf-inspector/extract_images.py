"""pdf-inspector で検出した画像/グラフ領域を、PyMuPDFでページごと切り出してPNG保存する。

pdf-inspector自体は画像データを直接取り出すAPIを持たない（テキスト/レイアウト抽出ライブラリのため）。
そこで、
  1. pdf_inspector.extract_text_with_positions() で item_type='image' の領域（座標）を検出
  2. pymupdf でページをレンダリングし、その座標でクロップしてPNG化
という2段構成にする。ラスター画像（写真等）・ベクター描画（Excel等のグラフ）のどちらも
同じ方法で画像化できる（レンダリング後のピクセルを切り出すだけなので、埋め込み画像かどうかを問わない）。

使い方:
    source .venv/bin/activate
    python extract_images.py [PDFファイル名] [DPI]
"""

import sys
from pathlib import Path

import pdf_inspector
import pymupdf

SOURCE_DIR = Path(__file__).parent.parent / "source_pdf"
OUTPUT_DIR = Path(__file__).parent / "output" / "images"


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "assets_com_9ji_kotuanzen.pdf"
    dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    pdf_path = SOURCE_DIR / filename

    items = pdf_inspector.extract_text_with_positions(str(pdf_path))
    image_items = [it for it in items if it.item_type == "image"]
    print(f"検出された画像/グラフ領域: {len(image_items)}件")

    doc = pymupdf.open(str(pdf_path))
    out_dir = OUTPUT_DIR / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, it in enumerate(image_items, start=1):
        page = doc[it.page - 1]  # pdf_inspector は1-indexed, pymupdfは0-indexed
        page_height = page.rect.height

        # pdf-inspector の座標系(左下原点,y上向き) -> pymupdf の座標系(左上原点,y下向き) に変換
        y_top = page_height - it.y - it.height
        clip = pymupdf.Rect(it.x, y_top, it.x + it.width, y_top + it.height)

        pix = page.get_pixmap(clip=clip, dpi=dpi)
        out_path = out_dir / f"page{it.page:03d}_{i:02d}.png"
        pix.save(out_path)
        print(f"page={it.page} bbox=({it.x:.0f},{it.y:.0f},{it.width:.0f},{it.height:.0f}) -> {out_path}")

    doc.close()


if __name__ == "__main__":
    main()
