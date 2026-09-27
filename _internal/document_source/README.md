# `_internal/document_source/`

このディレクトリには、README、CHANGELOG、用語に関する Python 記述と、中間文書の生成時に共通して使用する運用情報を配置する。

- `readme/canonical.py`: README の正本。
- `changelog/canonical.py`: CHANGELOG の正本ルートと未公開変更。
- `changelog/released.py`: 公開済み release を保持する物理分割 part。
- `vocabulary/canonical.py`: 用語の正本。
- `vocabulary/terms.py`: 用語から生成した、人間が IDE で参照するためのモジュール。
- `notice.toml`: 中間文書の冒頭へ加える共通の注意事項と、後続作業に必要な指示。

中間文書を生成するときは、`notice.toml` を `--notice` で明示的に指定する。CLI はこのファイルを自動探索しない。

プロジェクト名や版など生成時点で変化し得る値は、このディレクトリへ設定ファイルとして保持しない。必要な値をその時点の JSON オブジェクトへまとめ、`--context` に JSON 文字列として渡す。

```bash
CONTEXT='{"project":{"name":"shikumi-devdoc","version":"0.1.0","requires-python":">=3.11"}}'

shikumi-devdoc render document \
  _internal.document_source.readme.canonical \
  -o _internal/document_build/ja/README.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source

shikumi-devdoc render changelog \
  _internal.document_source.changelog \
  -o _internal/document_build/ja/CHANGELOG.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source
```

`--notice` は運用中に変更の少ない文言、`--context` は実現時点のスナップショットという役割で分けて扱う。翻訳へ渡す中間文書では `--translation-source` を付け、`preserve_spelling` など翻訳向けの意味情報も Markdown に保持する。
