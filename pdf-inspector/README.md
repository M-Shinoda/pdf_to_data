# pdf-inspector

[pdf-inspector](https://pypi.org/project/pdf-inspector/) を使い、`source_pdf/` 内のPDFをMarkdownに変換する。加えて、PyMuPDF（pymupdf）を使った画像・グラフの切り出しと、変換精度を確認するための検証スクリプトを含む。

## 技術スタック

- Python 3.13
- [pdf-inspector](https://pypi.org/project/pdf-inspector/) 1.19.0 — PDF分類・PDF→Markdown変換・レイアウト情報（テキスト/画像位置、表、OCR要否など）の抽出
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) (pymupdf) 1.28.2 — ページのレンダリング、座標指定でのクロップ・PNG保存、ベクター描画（グラフ）の検出
- 仮想環境: venv（`.venv/`）

## スクリプト構成

- [run.py](run.py) — PDFを分類・変換し、Markdownとして `output/` に保存するメインスクリプト
- [extract_images.py](extract_images.py) — pdf-inspectorが検出した画像/グラフ領域をpymupdfでクロップし、PNGとして `output/images/` に保存（埋め込みラスター画像向け）
- [extract_charts.py](extract_charts.py) — pymupdfの `get_drawings()` を使い、白背景で塗りつぶされた矩形をヒューリスティックにグラフ領域として検出し、`output/charts/` にPNG保存（Excel/PowerPoint由来のベクター描画チャート向け。pdf-inspectorの画像検出では拾えない弱点を補う）
- [verify.py](verify.py) — 変換結果の精度を自動チェックし、目視確認が必要なページを `output/page_renders/` に画像として保存する検証スクリプト

## 実行方法

```bash
cd pdf-inspector
source .venv/bin/activate

# PDF→Markdown変換
python run.py [PDFファイル名]        # 省略時は assets_com_9ji_kotuanzen.pdf

# 埋め込み画像の抽出
python extract_images.py [PDFファイル名] [DPI]     # DPI省略時は200

# ベクター描画グラフの抽出
python extract_charts.py [PDFファイル名] [MIN_AREA] [DPI]   # MIN_AREA省略時は20000, DPI省略時は200

# 精度検証（目視確認用ページ画像の生成含む）
python verify.py [PDFファイル名]
```

いずれも `source_pdf/` からPDFを読み込み、結果は `pdf-inspector/output/` 以下に保存される。
