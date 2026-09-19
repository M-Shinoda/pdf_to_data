# pdf_to_data

PDFをMarkdown等の構造化データに変換する検証プロジェクト。同じPDFに対して異なるアプローチを比較する。

## 構成

- [source_pdf/](source_pdf/) — 変換対象のPDFファイルを置くディレクトリ
- [markitdown/](markitdown/) — [markitdown](https://github.com/microsoft/markitdown) を使ったPDF→Markdown変換。詳細は [markitdown/README.md](markitdown/README.md)
- [pdf-inspector/](pdf-inspector/) — pdf-inspector を使ったPDF→Markdown変換＋画像/グラフ抽出＋精度検証。詳細は [pdf-inspector/README.md](pdf-inspector/README.md)

各ディレクトリは独立したPython仮想環境（`.venv`）を持ち、それぞれの `run.py` を実行して `output/` に結果を出力する。

注意：生成AIを使わず、静的ロジックを使用した方法の検証