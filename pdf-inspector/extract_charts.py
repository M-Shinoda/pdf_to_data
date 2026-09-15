"""ベクター描画のグラフ(Excel等で作成されたチャート)を検出して画像として切り出す。

pdf-inspector の extract_text_with_positions() が item_type='image' として
検出するのは埋め込みラスター画像のみで、色塗りされたベクター描画チャート
(棒グラフ/折れ線グラフなど)は拾えない(verify.py で確認済みの既知の弱点)。

そこで pymupdf の get_drawings() を直接使い、
  「白背景で塗りつぶされた、ある程度大きい矩形」 = グラフ全体の外枠
というヒューリスティックでチャート領域を検出する。
Excel/PowerPoint由来のグラフはプロットエリアの外側に白い背景枠を持つことが
多く、この矩形をクロップ範囲としてそのまま使えば、タイトル・凡例・軸ラベル
を含めてグラフ全体を画像化できる(pdf-inspectorの画像検出と違い、座標変換も不要
= get_drawings()の rect と get_pixmap(clip=...)の clip は同じ座標系)。

表の罫線(セル単位の小さい塗りつぶし)は面積が小さいため MIN_AREA で除外される。
ただし白背景の大きい装飾ボックス等を誤検出する可能性はあるので、保存された
画像は目視で確認すること。

使い方:
    source .venv/bin/activate
    python extract_charts.py [PDFファイル名] [MIN_AREA] [DPI]
"""

import sys
from pathlib import Path

import pymupdf

SOURCE_DIR = Path(__file__).parent.parent / "source_pdf"
OUTPUT_DIR = Path(__file__).parent / "output" / "charts"

WHITE = (1.0, 1.0, 1.0)


def find_chart_rects(page: pymupdf.Page, min_area: float) -> list[pymupdf.Rect]:
    candidates = []
    for d in page.get_drawings():
        if d.get("fill") != WHITE:
            continue
        r = d["rect"]
        area = r.width * r.height
        if area >= min_area:
            candidates.append(r)

    # 他の候補に完全に包含される矩形は除外(同じチャートの内側の白領域等の重複防止)
    result = []
    for r in candidates:
        if not any(other != r and other.contains(r) for other in candidates):
            result.append(r)
    return result


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "assets_com_9ji_kotuanzen.pdf"
    min_area = float(sys.argv[2]) if len(sys.argv) > 2 else 20000.0
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    pdf_path = SOURCE_DIR / filename

    doc = pymupdf.open(str(pdf_path))
    out_dir = OUTPUT_DIR / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for page_index in range(doc.page_count):
        page = doc[page_index]
        rects = find_chart_rects(page, min_area)
        for i, r in enumerate(rects, start=1):
            pix = page.get_pixmap(clip=r, dpi=dpi)
            out_path = out_dir / f"page{page_index + 1:03d}_{i:02d}.png"
            pix.save(out_path)
            print(f"page={page_index + 1} rect={r} -> {out_path}")
            total += 1

    doc.close()
    print(f"\n合計 {total} 件のグラフ候補を保存しました -> {out_dir}")
    print("表の背景色や装飾枠が誤検出される場合があるため、目視で確認してください。")


if __name__ == "__main__":
    main()
