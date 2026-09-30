<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/status/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# shikumi-devdoc Project Status

`shikumi-devdoc` の現在状態と、現在から見た将来の告知を記述する。
過去の状態変化は保持せず、実際に起きた利用者向け変更は CHANGELOG が担当する。

この文書は Project Status 専用規定体ではなく、共通 canonical document model と `shikumi_devdoc.fields.status` の standard field set を組み合わせて記述する。

## STATUS_001

現在の開発段階は Beta。現在の公開バージョンは `0.3.4`。

title: Development stage

## STATUS_002

現在の対象 Python バージョン範囲は `>=3.11`。

title: Supported Python

## STATUS_003

`shikumi-devdoc 0.3.4` は `shikumi>=0.2.0` を要求する。互換性の基準線は破壊的変更を行った 0.3.0 で確立した。Shikumi 0.2.0 以降は後方互換性を維持する方針のため、既知の非互換性がない限り上限は設けない。

title: Shikumi compatibility

## STATUS_004

wheel には `devdocs/` 全体と、この版の公開 README、Project Status、CHANGELOG、`docs/` を package resource として含める。

title: Installed documentation resources

related: [DIST_001](../specification/distribution.md#dist_001), [DIST_002](../specification/distribution.md#dist_002)

## STATUS_005

`shikumi-devdoc` は PyPI で配布し、ソースリポジトリを [GitHub](https://github.com/minoru-jp/shikumi-devdoc) で公開している。PyPI に表示される README からも文書へ移動できるよう、README の repository 内参照は公開 GitHub URL を使用する。

GitHub Actions の CI は `main` への push と pull request で実行し、Python 3.11 から 3.14、最低対応版 `shikumi==0.2.0`、canonical document の同期、test suite、wheel / sdist の build と release distribution verification を確認する。

GitHub Release を publish すると release workflow が tag と project version の一致を確認し、wheel / sdist を build・検証した後、その検証済み artifact を PyPI Trusted Publishing で公開する。

title: Distribution and CI status

## NOTICE_001

`0.3.0` の Beta 公開以降、公開 API には破壊的変更を加えず、後方互換性を維持して運用する。実運用とドッグフーディングで API の安定性を確認し、重大な問題がなければメジャーバージョンへ移行する。

title: API stability after 0.3.0

kind: General

condition: `0.3.0` の Beta 公開から最初のメジャーバージョンへ移行するまで。

## NOTICE_002

`@canonical_source(..., placeholders=...)` は 0.3.2 で非推奨となった。`placeholders=True` は `merge_policy="all"`、`placeholders=False` は `merge_policy="local"` と同じ意味で後方互換に解釈される。新規コードは `merge_policy` を使用する。`placeholders` は 1.0.0 で削除予定である。

title: Deprecation of placeholders

kind: General

condition: `0.3.2` から `1.0.0` へ移行するまで。
