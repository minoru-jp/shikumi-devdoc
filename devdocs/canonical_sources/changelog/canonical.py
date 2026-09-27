"""Canonical Japanese changelog source for shikumi-devdoc."""

from shikumi_devdoc.fields.changelog import (
    added,
    changed,
    deprecated,
    fixed,
    released_on,
    removed,
    security,
    version,
)
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("shikumi-devdoc 変更履歴", filename="CHANGELOG.md", placeholders=False, heading="identity")
class CHANGELOG:
    """`shikumi-devdoc` の versioned change history を記録する。公開されなかった開発 milestone はその旨を明記する。"""

    class V0_3_1:
        """配布物の役割を整理し、sdist をリリース再構成・検証に十分な完全なソース配布物へ変更した。"""

        version @= "0.3.1"

        changed @= '`pyproject.toml` の sdist file selection を個別 `include` 列挙から、VCS ignore を尊重しつつリポジトリ運用物だけを明示的に除外する方式へ変更した。これにより `src/`、`tests/`、`devdocs/`、`docs/`、`scripts/` とルートのリリース文書・build metadata を一つのリリースソースとして配布する。'
        changed @= '`scripts/check_dist.py` を sdist の必須内容として扱い、sdist 自身から build・archive 内容・install・CLI・`pip check`・dogfood rendering を再検証できる配布契約へ更新した。'
        changed @= 'wheel は従来どおり実装、`devdocs/` 参照コーパス、公開 README / Project Status / CHANGELOG / `docs/` を package resource として含める役割を維持する。'

    class V0_3_0:
        """開発文書の専用文書型を汎用 canonical document model と作者定義 field vocabulary へ統合した破壊的変更。"""

        version @= "0.3.0"

        added @= '`shikumi_devdoc.norms.document` に `field`、`list_field`、`table_field`、`test_target_field`、`prose_field`、`reference_field` と共通 `system` を追加した。field factory は明示した literal/template/reference と文書構造上の扱いだけを規定し、field 名や値から追加のドメイン意味や presentation を推論しない。'
        added @= '`reference_field` と標準 `related` の Markdown realization に logical reference link を追加した。canonical source provenance の親 path と canonical filename から canonical document logical path を導出し、参照元・参照先の logical path 間の相対 path と、参照先で実際に出力する Markdown heading から決定論的に導出した fragment を組み合わせる。明示 HTML anchor は追加せず、参照元と参照先を別実行で render しても同じ canonical metadata と heading から同じ logical reference を決定できる。'
        added @= '`shikumi_devdoc.norms.common` に `APPEND` / `IGNORE` を追加し、body template から参照されなかった field を自動実現するか source-only 情報として保持するかを canonical document ごとに選択できるようにした。'
        added @= r'`merge @= ("name", target)` を generic local merge declaration として追加した。docstring と `prose_field` の `{{name}}` は同じ node の merge binding を優先し、文字列、field、Vocabulary term を共通構文で差し込める。`\{{...}}` による literal escape も共通で利用できる。'
        added @= '`code_field` を廃止し、通常のテストから直接検証したい literal text を分離する `test_target_field` を追加した。Markdown fence や language info string は field ではなく surrounding template 側で記述する。'
        added @= '`shikumi_devdoc.fields.lifecycle` に `introduced`、`deprecated`、`removed`、`replacement`、`migration` を追加し、API や仕様項目など文書対象自身の lifecycle 情報を release 単位の CHANGELOG とは独立して記述できるようにした。'
        added @= '`shikumi_devdoc.realizers.index.IndexMarkdownRealizer` と `render index` を追加し、canonical source package を明示入力として document title / filename / `@summary` metadata の collection index を独立生成できるようにした。'
        added @= '`@summary(...)` を canonical source/document の短い概略 metadata として追加し、index realizer は正本ソース path ではなく document link と summary を出力するようにした。'
        added @= '`shikumi_devdoc.fields` を公開し、Specification、API Reference、CHANGELOG、Project Status で頻出する field と関連定数を generic field primitives の定義済み標準セットとして提供した。これらは専用 validator / realizer を持たない任意利用の convenience API である。'
        added @= 'Authoring Guide を canonical document collection として追加し、README、Getting Started、Configuration Guide、CLI documentation、Specification、API Reference、CHANGELOG、Glossary / Vocabulary、Project Status、document collection という目的文書別の authoring pattern を主導線にした。横断的な判断は Advanced authoring、LLM 固有の作業境界は LLM workflow に集約した。'
        added @= '文書中の検証対象コード・設定・command 等を `test_target_field` として純粋な literal text に分離し、`eval` / `exec` せず通常の Python module と pytest で値そのものを検証するドッグフーディングを追加した。'

        changed @= '`@canonical` を `@canonical_source` へ改名し、canonical source という概念名と公開 decorator 名を一致させた。文書 root では title、filename、任意 order、external-placeholder policy、未参照 field policy を共通 metadata として保持する。'
        changed @= '`@canonical_source(...)` に `heading="title" | "identity"` を必須 metadata として追加し、nested node の見出しを human-readable title で実現するか stable class identity で実現するかを作者が明示するようにした。realizer は文書種別から heading 方針を推論しない。'
        changed @= '`shikumi-devdoc 0.3.0` の runtime dependency を `shikumi>=0.2.0` とし、破壊的変更後の Shikumi 0.2.0 を互換性の基準線として明示した。Shikumi 側の 0.2.0 以降の互換性方針に合わせ、既知の非互換性がない将来版を不要に拒否する上限は設けない。'
        changed @= 'nested document node の human-readable title を `title @= "..."` に統一した。title は同じ node の local merge と realization context を解決でき、`heading="title"` では見出し、`heading="identity"` では human-readable metadata として実現する。'
        changed @= '`reference_field` が nested canonical document node を target にする場合、その target root に `heading="identity"` を要求するようにした。title/Vocabulary/context の変更で fragment が変化する `heading="title"` の nested node は stable semantic reference target にできない。document root への参照は filename だけで成立するため例外とする。'
        removed @= 'generic document node の `@title(...)` decorator 記法を削除し、`shikumi_devdoc.norms.document.title` を assignment-only な `title @= ...` writer に変更した。`fields.common` / `fields.specification` / `fields.status` から重複する title export も削除した。'
        changed @= 'Narrative / Itemized の grammar 区分を廃止した。`@canonical_source(...)` 配下の nested class はすべて document node、各 docstring は本文 template として扱い、同じ document realizer で README、STATUS、CHANGELOG、Specification、API Reference を実現する。'
        changed @= 'canonical root と document node の docstring は `inspect.cleandoc()` 相当で正規化してから意味内容として取り込み、Python source 上の共通 indent を除去しつつ本文内部の相対 indent を保持する契約を明文化した。raw/non-raw や引用符の種類はこの意味規則に含めない。'
        changed @= 'Authoring Guide の総則で、`shikumi-devdoc` は特定の文書セットを repository に要求せず必要な文書だけを作るための手段であることを明記した。目的別 authoring pattern は必須 document type ではなく generic canonical-document model の推奨構成として扱う。'
        changed @= 'Narrative document の node identity には表示 title と同期しない `SECTION_NNN` のような opaque stable identity を推奨する authoring convention を追加した。番号は順序・見出しレベル・公開節番号を表さず、この命名は validator では強制しない。Specification の `related` は対称な see-also ではなく依存方向として利用し、循環 import が現れた場合は文書構造を先に見直す方針を Authoring Guide に記載した。'
        changed @= '通常の `field`、`list_field`、`table_field`、`test_target_field` の値は literal content として扱い、内部の placeholder-like text を解釈しない。`prose_field` だけは docstring と同じ template-bearing content として external placeholder と generic local merge を利用できる。'
        changed @= '`@canonical_source(..., placeholders=False)` の意味を template-bearing content における external placeholder の禁止として整理した。canonical-local merge と literal field 内の placeholder-like text は snapshot 文書でも利用できる。'
        changed @= 'Specification、API Reference、Project Status、CHANGELOG のドッグフーディングを共通 document model と `shikumi_devdoc.fields` の標準 field set へ移行した。'
        changed @= 'CLI の文書実現経路を `render document` に統一し、各 `@canonical_source(..., filename=...)` root を `MarkdownDocument` として出力する形にした。'
        changed @= 'Specification / API Reference の `INDEX.md` を表す `root.py` を廃止した。個別文書は `render document`、索引は package を入力とする `render index` で並行して生成する。'
        changed @= '`related` を専用 semantic descriptor と通常 document field の二系統から、`shikumi_devdoc.fields.common.related` の単一 generic reference field へ統合した。表示位置は通常 field と同じ merge / `APPEND` / `IGNORE` policy に従い、表示する場合は canonical metadata から logical Markdown link を生成する。最終 publication layout の探索・推論・link rewrite は realizer の責務に含めない。'
        changed @= 'Vocabulary を通常の `@canonical_source(...)` に `@vocabulary` semantic profile marker を重ねる構成へ一般化した。旧 Vocabulary authoring の `@title` / `@term` と `VOCABULARY` / `TERM_N` の命名制約を廃止し、各 direct child の docstring を `inspect.cleandoc()` 相当で正規化し、その先頭の `{{term name}}` 宣言を用語名の唯一の正本として definition を導出する。'
        changed @= '文書側の Vocabulary 接続 decorator と `vocabulary_refs` を廃止した。Vocabulary の canonical term class を generic `merge` target として直接束縛し、用語名の realization と IDE navigation、`preserve_spelling` の translation metadata を同じ canonical term identity から導出する。'
        changed @= 'Vocabulary term の `glossary` 選択は未指定を公開 (`True`) として扱い、Glossary から除外する term だけ `glossary @= False` を明示する既定値へ変更した。SemanticView には未指定を暗黙の `True` として注入せず、Glossary realizer が effective value として解釈する。'
        changed @= '`merge` の class target に `merge @= target` 省略形を追加した。template では target の Python identity から、その node で一意な最短 suffix を参照名として使用できる。同じ `TERM_001` が複数 Vocabulary から入る場合は Vocabulary class 名、必要なら module path まで修飾して解決し、衝突自体ではなく曖昧な参照の使用だけを error とする。明示別名の `merge @= ("name", target)` は文字列・field target と任意 alias のために維持する。'
        changed @= 'field 系 writer の `@=` 左辺 binding を同じ node の local template namespace へ自動登録し、field と `merge` の名前解決を統合した。同名候補の存在だけでは error にせず、template-bearing content が曖昧な参照を実際に使用した場合だけ拒否する。同じ FieldWriter を複数 binding で使った場合も binding identity ごとに値を分離する。'
        fixed @= 'Vocabulary の一般化後も専用 Glossary realizer を dogfood できるよう、term の既定公開選択と `render glossary` 生成手順を整え、`GLOSSARY.md` を canonical document として再生成するようにした。'

        removed @= 'Specification、API Reference、Project Status、CHANGELOG の専用規定体、専用 Markdown realizer、専用 CLI render kind を削除した。'
        removed @= '`@narrative`、`@itemized`、`@item`、`item_document` など文書 grammar / item 専用の root・node decorator を公開 API から削除した。'
        removed @= 'Vocabulary term を複製する `PythonReferenceModuleRealizer`、`shikumi-devdoc terms`、生成 proxy の private target 属性と互換解決処理を削除した。canonical term class 自体を IDE と `merge` の参照先として使用する。'

    class V0_2_0:
        """PyPI には公開しなかった開発 milestone。Changelog の分割実現と Specification / API Reference / Project Status の追加を中心に、文書体系の表現力と運用性を拡張した。これらの変更は後続の 0.3.0 開発へ引き継がれた。"""

        version @= '0.2.0'

        added @= 'Vocabulary に複数の `alias`、`deprecated`、`replacement` を追加し、公開用語の別名と廃止・置換関係を意味情報として検証・実現できるようにした。'
        added @= 'Changelog に `unreleased` と `breaking` を追加した。Unreleased は一つだけ先頭に置き日付を持たず、breaking な変更項目は元の変更区分を維持したまま Markdown 上で明示される。'
        added @= 'Changelog の canonical source を複数モジュールへ物理分割し、`@changelog_part(order=..., filename=...)` で論理順序と canonical document の filename を宣言しつつ、一つの変更履歴として統合・検証できるようにした。'
        added @= 'Changelog の root と part に `filename` を追加し、標準実現と CLI の既定動作を、指定した出力ディレクトリへ canonical Markdown document を分割生成する形へ変更した。`--single-file` で従来の一枚への統合も明示的に選択できる。'
        added @= 'Specification 規定体と Markdown 実現器を追加した。仕様項目を ID、規範レベル、本文、汎用 `detail` として構造化し、part の `filename` による分割出力と任意の `order`、順序が定義された場合の `--single-file` 統合に対応する。'
        added @= '言語非依存の API Reference 規定体と Markdown 実現器を追加した。API entry を汎用 kind、input、output、`detail` で記述でき、Specification と同じ part filename・任意 order・単一ファイル化モデルを利用できる。'
        added @= '`shikumi-devdoc` 自身の現行仕様と公開 API Reference を新しい規定体で記述するドッグフーディングを追加し、日本語 canonical document から `docs/specification/` と `docs/api/` の published document へ展開する構成にした。'
        added @= 'Specification に `@condition` を追加し、適用条件を規則本文から独立して記述できるようにした。さらに Specification item と API Reference の entry/input/output に `related @= (...)` を追加し、文字列 ID ではなく `@spec` / `@api` の Python 実体を使って項目間関係を記録・検証・実現できるようにした。'
        added @= '一般文書の各見出しでも共有 `related @= (...)` を使用できるようにした。参照先は `@spec` / `@api` の Python 実体として検証・保持し、標準の一般文書 Markdown realizer は関係情報を本文へ自動表示しない。'
        added @= 'Specification と API Reference の標準 Markdown realizer が root 文書へ全項目の索引を自動生成するようにした。全 part に `order` がある場合はその順序を索引へ反映し、未指定 part があれば安定した構造順へフォールバックする。part 文書には索引を重複生成しない。'
        added @= '非履歴の Project Status 規定体と `ProjectStatusMarkdownRealizer` を追加した。現在の事実を Snapshot、将来の意図を Direction、利用者への将来告知を Notice として構造化し、realizer が固定名 `STATUS.md` を生成する。'
        added @= 'wheel に `devdocs/` 全体を参照コーパスとして、公開 README、Project Status、CHANGELOG、Specification、API Reference を公開文書資産として含める配布構成を追加した。MIT License は package data へ複製せず、project metadata の license file として配布する。'

        changed @= 'Changelog を Vocabulary と placeholder 解決から切り離し、タイトル、release label、notes、change 本文を含む自由記述文字列をそのまま canonical Markdown document へ実現するようにした。`\\{{...}}` も Changelog では特別な構文として解釈しない。'
        changed @= '自身の文書オーサリング領域を `_internal/` から `devdocs/` へ再構成し、文書ソース、実現入力、生成文書を分離した。後続の概念整理により、現在は `canonical_sources/`、`config/`、`canonical_documents/` として運用する。'
        changed @= 'Specification / API Reference の root から出力 `filename` を廃止し、標準 Markdown realizer が文書集合全体から `INDEX.md` を自動生成する形へ変更した。part の `filename` は引き続き明示し、`INDEX.md` との衝突は実現時に診断する。'
        changed @= '`@condition` を Specification 専用実装から共有記述器へ整理し、Project Status item でも適用条件を独立した意味情報として記述できるようにした。'
        changed @= 'テスト用 optional dependency として `pytest>=8.0` を project metadata に宣言し、sdist から `.[test]` を使ってテスト環境を再構築できるようにした。'
        changed @= 'Specification / API Reference の各文書ソース単位を `@canonical` で明示する構成へ変更し、root は文書集合の宣言だけを持ち、実内容を Core などの part へ分離した。Specification item は `@spec` の文字列 ID ではなく Python クラス名を identity とし、API entry は通常クラス名から identity component を導出し、入れ子の API entry を階層 path として表現できるようにした。Python 識別子にできない API 名は `@api(name=...)` で明示できる。'
        changed @= '公開 Python API を整理し、トップレベル `shikumi_devdoc` は Context 系と `norms` / `realizers` 名前空間だけを入口として公開する形へ変更した。Norm の実装モジュールは private 化し、文書記述 API と標準実現 API の詳細はそれぞれ `norms` / `realizers` 以下へ集約した。'
        changed @= '公開 API を意味領域ごとの中分類 namespace へ再編した。Norm は `shikumi_devdoc.norms.<domain>`、Realizer は `shikumi_devdoc.realizers.<domain>` から利用し、Specification の規範値は `specification.level.MUST`、API kind は `api_reference.kind.OPERATION`、CHANGELOG kind は `changelog.kind.ADDED`、Project Status notice kind は `status.notice_kind.BREAKING_CHANGE` のように専用 namespace へ束ねる。これにより `title` などの本来の名前を規定体ごとに保持できるようにした。'
        changed @= '一般文書の文字列 `anchor` と `\\{{#...}}` section reference を廃止し、Python 実体とは別の並行 identity を持たない設計へ整理した。Project Status の Snapshot、Direction、Notice も文字列 ID 引数を廃止し、Python クラス名を semantic identity として使用するよう変更した。Vocabulary については、一つの本文で複数の異なる `TERM_N` placeholder を同時に解決できることを回帰テストで固定した。'
        changed @= 'Changelog の分割 part も独立した正本単位として `@canonical` を必須にし、分割 Markdown の生成時には各 part 自身の canonical source を先頭コメントへ反映するよう統一した。'
        changed @= '`related` の契約を、評価時点ですでに解決済みの Python class 実体を直接保持する機構として明確化した。文字列・forward・遅延参照の解決は提供せず、参照元・参照先の文書種別、方向、自己参照、循環性も意味規則として制限しない。既知の Specification/API identity を持たない class は完全修飾 Python 名で Markdown に表示する。'
        changed @= '文書体系の正本境界を再定義した。`@canonical` が示す Python 記述体を canonical source、検証済み source と realization context を realizer が組み立てた結果を canonical document とし、翻訳・ローカライズ・配布などで作る published document はライブラリの責務外とした。ドッグフーディング構成も `devdocs/canonical_sources/` と `devdocs/canonical_documents/` へ改め、中間文書という概念を廃止した。'
        changed @= '`@canonical` が記録する canonical source の出自を current working directory 相対の filesystem path ではなく Python module 構造から導出するよう変更し、同一 source の canonical document が実行ディレクトリによって変化しないようにした。'

    class V0_1_0:
        """最初の公開版。開発文書を Shikumi の意味情報から記述・検証・実現するための基本機能をまとめた。"""

        version @= '0.1.0'
        released_on @= '2026-09-13'

        added @= '一般文書、用語集、変更履歴を記述する規定体と、それぞれを Markdown へ変換する標準実現器を追加した。'
        added @= 'プロジェクト名や版などを外部情報として実現器へ渡し、文書中の参照記号から参照する仕組みを追加した。'
        added @= 'Vocabulary から用語参照体を生成する CLI を追加し、`TERM_N` から IDE で用語名と定義を追跡できるようにした。'
        added @= '用語参照を使用した実体の近くへ置き、本文中の `TERM_N` と `vocabulary_refs` が実体単位で一致することを Validator で検証する仕組みを追加した。'
        added @= '正本を `@canonical` で明示し、Markdown 実現器へ運用側から任意の先頭コメントを渡せる仕組みを追加した。'
        added @= '正本の Python 記述体から日本語の中間文書を生成し、その英訳をリポジトリ直下の公開文書として配置するドッグフーディング運用を追加した。'
        added @= '翻訳用中間 Markdown に `preserve_spelling` 対象を機械可読なメタデータとして保持する `TranslationSourceRealizer` と `render --translation-source` を追加した。'
        added @= '文書見出しへ `anchor @= "..."` で安定した identity を付与し、本文中の `\\{{#anchor}}` から意味的に節を参照する仕組みを追加した。参照は `SectionReference` として意味像へ自動抽出され、未知参照、anchor の重複、不正な anchor 名を検証する。'

        changed @= '用語の翻訳方針を表す情報名を `untranslatable` から `preserve_spelling` へ変更し、「翻訳不能」ではなく表記維持を意味することを明確にした。'
        changed @= '生成時の注意書きと LLM による公開文書作成方針を運用側の `notice.toml` の単一の `notice.content` にまとめた。`render --notice` で明示的に指定した場合だけ中間文書へ埋め込み、設定ファイルの自動探索は行わない。あわせてリポジトリ固有の `build_docs.py` を廃止し、用語参照体生成と中間文書生成を CLI から直接実行する形へ整理した。'
        changed @= '`render --context` を外部情報ファイルの指定ではなく、実現時点のスナップショットを表す単一の JSON 文字列として受け取る形へ整理した。`notice.toml` は固定的な運用文、`--context` は可変な値という役割を分離し、`_internal/document_source/README.md` にこのリポジトリでの生成手順を記載した。'
        changed @= 'Placeholder の字句処理を共通化し、`\\\\{{...}}` による literal escape と `${{...}}` の保持を追加した。用語参照検証も同じ字句規則を使用するため、escape された marker を意味参照として誤認しない。'
        changed @= 'CLI diagnostics に severity、diagnostic code、Python source location、semantic subject を表示するよう改善し、本文中の raw Markdown heading と Markdown の6階層制限を実現前に検査するようにした。'
