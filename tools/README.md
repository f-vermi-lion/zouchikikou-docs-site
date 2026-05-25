# tools

`zouchikikou-docs-site`の公開workflowで使う共通検査ツールを置くディレクトリです。

## check-language-pairs

日英対応ページの欠落と`:lang:`属性の不一致を検査します。

```bash
tools/check-language-pairs <content-root>...
```

`<content-root>`には、`antora.yml`を持つAntora content rootを指定します。

検査対象は以下です。

- `modules/ROOT/pages/**/*.adoc`
- `modules/ja/pages/**/*.adoc`

issue出力はタブ区切りです。

```text
issue_code<TAB>content_root<TAB>module<TAB>relative_path<TAB>message
```

終了コードは以下です。

- `0`: 問題なし
- `1`: 検査違反あり
- `2`: 引数不正またはcontent root不正

初期範囲では、翻訳内容の差分、更新鮮度、日英リンクの存在は検査しません。

`meta-architecture` componentは日本語運用のため検査対象外です。
