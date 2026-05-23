# zouchikikou-docs-site

造智機巧のアーキテクチャ文書をAntoraで集約して確認するためのサイト用リポジトリです。

## 公開URL

https://f-vermi-lion.github.io/zouchikikou-docs-site/meta-architecture/architecture-documentation-publishing-platform/index.html

## 初期段階の範囲

- publicな文書だけをcontent sourceとして扱う。
- `repository_dispatch`、token / secret、`tools/check-language-pairs`はまだ使わない。

## 初期build

```bash
npm install
npm run build
```

生成物は`build/site/`に出力されます。

## 初回公開

GitHubで以下を行うと、GitHub Pagesで初回公開できます。

1. `zouchikikou-docs-site`の`main`へこのリポジトリの変更をpushする。
2. GitHubの`Settings` -> `Pages`で、Build and deploymentのSourceを`GitHub Actions`にする。
3. GitHubの`Actions` -> `Publish to GitHub Pages` -> `Run workflow`を実行する。
4. workflow完了後、表示されたGitHub Pages URLを確認する。

公開workflowは`.github/workflows/publish.yml`です。

この初回公開workflowは、`repository_dispatch`、token / secret、private repositoryのcontent source、`tools/check-language-pairs`をまだ使いません。
