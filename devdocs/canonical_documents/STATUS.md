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

現在の開発段階は Beta。現在の公開バージョンは `0.3.5`。

title: Development stage

## STATUS_002

現在の対象 Python バージョン範囲は `>=3.11`。

title: Supported Python

## STATUS_003

`shikumi-devdoc 0.3.5` は `shikumi>=0.2.0` を要求する。互換性の基準線は破壊的変更を行った 0.3.0 で確立した。Shikumi 0.2.0 以降は後方互換性を維持する方針のため、既知の非互換性がない限り上限は設けない。

title: Shikumi compatibility

## STATUS_004

wheel には `devdocs/` 全体と、この版の公開 README、Project Status、CHANGELOG、`docs/` を package resource として含め、PEP 561 の `py.typed` marker も package に含める。

title: Installed documentation resources

related: [DIST_001](../specification/distribution.md#dist_001), [DIST_002](../specification/distribution.md#dist_002), [DIST_011](../specification/distribution.md#dist_011)

## STATUS_005

`shikumi-devdoc` は PyPI で配布し、ソースリポジトリを [GitHub](https://github.com/minoru-jp/shikumi-devdoc) で公開している。PyPI に表示される README からも文書へ移動できるよう、README の repository 内参照は公開 GitHub URL を使用する。

GitHub Actions の品質・テスト検証は再利用可能な `checks.yml` に集約し、Ruff 0.16.10 の format check / lint、BasedPyright 1.40.1 による package source と consumer typing contract の型検査、mypy 2.4.0 による canonical-source override recipe の検証、canonical document の同期、Python 3.11 から 3.14 の test suite、最低対応版 `shikumi==0.2.0` の test suite を同じ品質ゲートとして実行する。通常 CI は `main` への push と pull request からこの共通 checks を呼び出し、あわせて wheel / sdist の build と release distribution verification を確認する。

GitHub Release を publish すると release workflow も同じ共通 checks を最初に実行し、すべて成功した場合だけ tag と project version の一致を確認して wheel / sdist を build・検証する。その検証済み artifact だけを PyPI Trusted Publishing で公開する。したがって Ruff、package source / consumer contract の双方の BasedPyright、documented mypy override recipe、canonical document、対応 Python の test suite、最低対応 Shikumi の test suite を通らない revision は release artifact の build と PyPI publish へ進まない。

title: Distribution and CI status

## STATUS_006

静的解析では `ruff format --check .`、`ruff check .`、BasedPyright がいずれも clean。Ruff は 0.16.10 を固定し、Python 3.11 を target version として設定する。lint はその固定版の stable default rule set を baseline とし、preview diagnostics へ暗黙に opt in しない。package source の検査は BasedPyright 1.40.1 で `src/shikumi_devdoc` を Python 3.11 基準とし、Shikumi 本体と同じ品質方針として `reportUnnecessaryIsInstance`、`reportImplicitStringConcatenation`、`reportExplicitAny`、`reportPrivateUsage`、`reportImplicitOverride` を無効化した上で 0 errors / 0 warnings である。

型チェッカを通すためだけに Python の意味を遠回りに表現する書き換えは避ける。runtime validation や semantic identity comparison など、意味を保持するために局所的な `pyright: ignore` が必要な場合は、その理由を該当箇所の直前に記述する。型注釈の方を runtime contract に合わせて広げられる内部 helper では ignore を残さない。

これとは別に `tests/typing` の BasedPyright standard-mode contract で、専用 authoring sample、`devdocs/canonical_sources`、`tests/examples` を consumer 側の利用コードとして検査し、こちらも 0 errors / 0 warnings とする。consumer contract は package source 側の診断抑制を継承せず、PEP 561 の `py.typed` を公開した状態で field / merge の反復 `@=` を含む実際の DSL が BasedPyright / Pyright の型モデルで型エラーにならないことを保証する。この 0/0 は PEP 561 を利用するすべての型チェッカに同一の診断結果を保証する意味ではない。

title: Static analysis status

## STATUS_007

BasedPyright で無効化している 5 つの診断は、型検査を通すための包括的な逃げ道として扱わず、それぞれの責務に基づく project policy として扱う。

`reportImplicitStringConcatenation` は主として表記・style の規則であり、型安全性の中核ではない。`reportImplicitOverride` は `@override` の明示を要求する規則で、override 自体の型整合性を無効化するものではない。`reportPrivateUsage` は Python の強制的な access control ではなく、package 内部 API の境界方針に関する規則として扱う。

`reportUnnecessaryIsInstance` は、静的型だけを見れば不要でも、型付けされていない runtime caller から不正値を受ける可能性に備える validation を残すため無効化している。この方針によって本当に不要な `isinstance()` も自動検出されなくなるため、防御目的がない check は code review で残さない。

`reportExplicitAny` は 5 項目の中で最も型検査を弱め得るため、特に慎重に扱う。`Any` は metadata や任意の Python type を表現する境界など、`object`、generic、Protocol その他のより正確な型では不自然になる箇所に限定し、通常の処理を `Any` で覆って warning を回避してはならない。将来、複雑さを増やさずに既存の `Any` をより正確な型へ置き換えられる場合は、Shikumi 本体と合わせて `reportExplicitAny` の再有効化を検討する。

したがって現在の 0 errors / 0 warnings は「すべての BasedPyright 診断を最大厳格度で有効化した状態」ではなく、上記 policy で型欠陥として扱う診断を有効にした状態での clean を意味する。局所的な `pyright: ignore` も同様に、実行時意味を保つ具体的な理由がある箇所だけに限定する。

title: Static analysis suppression policy

## STATUS_008

Shikumi core は `@=` による記述を強制せず、`shikumi.standard` の記述器は選択可能な標準 authoring style として提供される。`shikumi-devdoc` は canonical source を文書ソースとして読みやすく保つため、field や merge などを `name @= value` と並べるこの style を意図的に採用している。canonical source は実行可能な Python だが、通常の運用では一般的なアプリケーション処理を自由に混在させる領域ではなく、Python runtime を利用した文書記述領域として扱う。

`shikumi-devdoc` の writer は `__imatmul__` の戻り値型として、静的に元の writer 型を維持する `Self` ではなく、runtime で実際に返す temporary binding 型を注釈する方針を採用している。Python の augmented assignment は概念上 `name = name.__imatmul__(value)` の再束縛を行うため、mypy はこの型の変化を `Result type of @ incompatible in assignment [misc]` として報告する。これは mypy では表現不能な DSL という意味ではなく、runtime に忠実な戻り値型を優先する現在の型注釈方針との相互作用である。BasedPyright / Pyright は同じ consumer source を error なしで受理する。

mypy で canonical source も検査する利用者には、canonical source を専用 module / package に分離し、その範囲で `misc` error code を `[[tool.mypy.overrides]]` の `disable_error_code` に指定する運用を推奨する。

```toml
[[tool.mypy.overrides]]
module = ["your_project.devdocs.canonical_sources.*"]
disable_error_code = ["misc"]
```

`module` pattern は、mypy が実際に解決する module 名と一致して初めて有効になる。mypy は module 名を directory 構成から決めるため、canonical-source package の上位 directory が別の package に属する配置（たとえば `__init__.py` を持つ `tests/` の下）では、`tests.` のような上位 package 名が前置され、pattern が一致せず `misc` が抑止されないことがある。その場合は、pattern を解決後の module 名に合わせるか、`mypy -p` で package を指定するか、`explicit_package_bases` と `mypy_path` で import root を明示する。この repository の recipe check は fixture を `tests` package の配下に置くため、最後の方法を検査用の設定としてだけ使っており、上記の推奨 recipe 自体には含まれない。

`misc` は augmented assignment 専用ではなく、mypy の複数の雑多な診断をまとめる error code である。この override を設定した canonical-source package 内では `@=` 以外の `misc` 診断も抑制される。そのため override は canonical source の意味上の境界に限定し、一般的なアプリケーションロジックを同じ package に混在させないことを推奨する。行単位の ignore や project 全体の型検査無効化は標準運用としない。`misc` 以外の mypy 診断は引き続き有効である。

現行 CI の正式な consumer typing contract は BasedPyright を対象とし、mypy の canonical source 全体での 0-error 状態そのものは release gate としない。一方、上記の推奨 override が反復 `@=` のサンプルを受理し、同じ package 内の `misc` 以外の明白な型エラーを引き続き検出することは、専用の mypy recipe check で検証する。

title: Canonical-source authoring style and mypy boundary

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
