# markitdown

Microsoft製の [markitdown](https://github.com/microsoft/markitdown) を使い、`source_pdf/` 内のPDFをMarkdownに変換する。

## 技術スタック

- Python 3.13
- [markitdown](https://pypi.org/project/markitdown/) 0.1.7 — PDF→Markdown変換本体（内部で pdfminer.six / pdfplumber 等を利用）
- 仮想環境: venv（`.venv/`）

## 実行方法

```bash
cd markitdown
source .venv/bin/activate
python run.py [PDFファイル名]   # 省略時は assets_com_9ji_kotuanzen.pdf
```

`source_pdf/` にあるPDFを読み込み、変換結果を `output/<PDFファイル名>.md` に保存する。標準出力にタイトルと本文の文字数も表示される。
