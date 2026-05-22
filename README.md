# zouchikikou-docs-site

造智機巧のアーキテクチャ文書をAntoraで集約して確認するためのサイト用リポジトリです。

## 初期段階の範囲

- publicな文書だけをcontent sourceとして扱う。
- GitHub Pages deployはまだ行わない。
- `repository_dispatch`、token / secret、`tools/check-language-pairs`はまだ使わない。

## 初期build

```bash
npm install
npm run build
```

生成物は`build/site/`に出力されます。
