"""Canonical Japanese README source for shikumi-devdoc."""

from devdocs.canonical_sources.api_reference.norms import (
    API_REFERENCE_PART as NORMS_API,
)
from devdocs.canonical_sources.api_reference.realizers import (
    API_REFERENCE_PART as REALIZERS_API,
)
from devdocs.canonical_sources.specification.api_reference import (
    SPECIFICATION_PART as API_REFERENCE_SPEC,
)
from devdocs.canonical_sources.specification.document import (
    SPECIFICATION_PART as DOCUMENT_SPEC,
)
from devdocs.canonical_sources.specification.specification import (
    SPECIFICATION_PART as SPECIFICATION_SPEC,
)
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge
from shikumi_devdoc.norms.document import test_target_field, title


install_command = test_target_field("install command")
minimal_source = test_target_field("minimal source")
render_command = test_target_field("render command")
rendered_markdown = test_target_field("rendered Markdown")
vocabulary_merge_example = test_target_field("Vocabulary merge example")

@canonical_source('{{project.name}}', filename='README.md', merge_policy="all", unreferenced_fields=IGNORE, heading="title")
class SECTION_001:
    r"""
    `{{project.name}}` は、開発文書を意味構造を持つ Python の {{TERM_001}} として記述し、[Shikumi](https://pypi.org/project/shikumi/) で検証し、Markdown の {{TERM_002}} へ実現するためのライブラリである。

    {{TERM_014}} と共通の {{TERM_002}} model を二つの基盤として提供する。用語や表記は Vocabulary に集約し、README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference などは、nested class・docstring template・作者定義 {{TERM_007}} を組み合わせる同じ document model で構成する。
    """

    merge @= TERMS.TERM_001
    merge @= TERMS.TERM_002
    merge @= TERMS.TERM_007
    merge @= TERMS.TERM_014

    class SECTION_002:
        r"""
        `{{project.name}}` は、継続的に更新される開発文書について、正本を Python 上の検証可能な意味情報として保ち、必要な {{TERM_005}} を反映して再生成可能な {{TERM_002}} を得たい場合に使用する。

        | 目的 | 基盤 |
        | --- | --- |
        | 用語の名称と概念定義を一元管理する | {{TERM_014}} |
        | README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference などを構成する | {{TERM_002}} model |

        Specification や API Reference は built-in の文書種別ではない。用途別の意味は作者側の {{TERM_008}} が担い、`shikumi_devdoc.fields` にある {{TERM_009}} を再利用しても、project-local な field を定義してもよい。
        """
        title @= "何に使えるのか"

        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_008
        merge @= TERMS.TERM_009

        related @= (
            SPECIFICATION_SPEC.SPEC_001,
            API_REFERENCE_SPEC.APIREF_001,
            DOCUMENT_SPEC.DOC_006,
        )

    class SECTION_003:
        r"""
        PyPI からインストールする。

        ```bash
        {{install_command}}
        ```

        最小の {{TERM_001}} は `@canonical_source(...)` を付けた root class と、その下に置く nested class だけで記述できる。

        ```python
        {{minimal_source}}
        ```

        module を CLI に渡すと {{TERM_002}} を生成する。

        ```bash
        {{render_command}}
        ```

        生成される Markdown は次のようになる。

        ```markdown
        {{rendered_markdown}}
        ```

        nested class は追加 decorator なしで下位 {{TERM_006}} となり、その階層が見出し階層へ対応する。context、field、Vocabulary、index などは必要になった時点で同じモデルへ追加できる。
        """
        title @= "最小の使い方"

        install_command @= "pip install shikumi-devdoc"
        minimal_source @= """
        from shikumi_devdoc.norms.common import canonical_source

        @canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
        class EXAMPLE:
            class Introduction:
                '''Hello from shikumi-devdoc.'''
        """
        render_command @= "shikumi-devdoc render document myproject.example -o build/"
        rendered_markdown @= """
        # Example

        ## Introduction

        Hello from shikumi-devdoc.
        """

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_006

        related @= (
            NORMS_API.norms.common.canonical_source,
            REALIZERS_API.realizers.document.MarkdownRealizer,
        )

    class SECTION_004:
        r"""
        `{{project.name}}` では Markdown を直接編集して正本とせず、{{TERM_001}} と {{TERM_005}} から validation と realization を経て {{TERM_002}} を確定する。

        ```text
        {{TERM_001}}
              + {{TERM_005}}
                ↓ Shikumi による解釈・検証
             SemanticView
                ↓ shikumi-devdoc の realizer
        {{TERM_002}}
                ↓ project-specific {{TERM_004}}
          {{TERM_003}}
        ```

        `shikumi-devdoc` が一貫して責任を持つのは {{TERM_002}} までである。翻訳、ローカライズ、文章表現の調整、媒体変換、配布などは、プロジェクト固有の {{TERM_004}} が {{TERM_003}} を作る工程として扱う。

        {{TERM_002}} は共通の {{TERM_006}} / template / {{TERM_007}} / merge モデルで記述する。nested class が文書階層、docstring が本文 template、field が構造化された付加情報になる。背景説明のような prose は docstring に保ち、構造として意味を持つ情報だけを field として分離できる。

        generic document core は Specification や API Reference の意味論を組み込まない。文書用途を増やすときは別 grammar を増やすのではなく、必要な {{TERM_008}} と presentation を同じ基盤へ組み合わせる。
        """
        title @= "コアモデル"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_008

        related @= (
            DOCUMENT_SPEC.DOC_001,
            DOCUMENT_SPEC.DOC_002,
            DOCUMENT_SPEC.DOC_006,
            REALIZERS_API.realizers.document.MarkdownRealizer,
        )

    class SECTION_005:
        r"""
        {{TERM_014}} は、用語の名称と概念定義を {{TERM_001}} として保持する。各 {{TERM_015}} は `TERM_N` 形式の安定した class identity を持つため、利用文書は実際の用語文字列を複製せず term class を参照できる。

        ```python
        {{vocabulary_merge_example}}
        ```

        template では通常 `\{{TERM_001}}` のような短い参照を使える。複数の Vocabulary から同名 identity を取り込んだ場合は、必要な範囲だけ Python identity を修飾して区別できる。具体的な名前解決規則は Specification を参照する。

        文書固有の構造化情報は {{TERM_007}} として宣言する。作者は project-local な {{TERM_008}} を定義でき、頻出する組み合わせには `shikumi_devdoc.fields` の {{TERM_009}} を利用できる。generic core は field のドメイン意味を所有しない。

        docstring、`prose_field`、`title @= ...` は {{TERM_010}} として {{TERM_013}} や external placeholder を扱える。field 系の `@=` 左辺名は同じ node の local reference として自動的に利用でき、`merge` は class target、文字列、明示 alias など追加の参照を登録する。`merge_policy="all"` は local/external の双方、`"local"` は local のみ、`"external"` は external のみを許可し、`"forbidden"` は双方を拒否する。旧 `placeholders` boolean は 0.3.2 で非推奨となり、1.0.0 で削除予定である。通常の `field`、`list_field`、`table_field`、`test_target_field` の値自体は {{TERM_011}} として扱う。`test_target_field` は通常のテストから直接検証したい文字列断片を分離するためのもので、Markdown fence や language は surrounding template 側に記述する。Python object relation を文書間参照として実現したい場合は `reference_field` を使い、標準 `related` はその convenience field として利用できる。未参照 field は `APPEND` で本文へ追加するか、`IGNORE` で source-only の意味情報として保持できる。
        """
        title @= "Vocabulary と構造化情報"

        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_015
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_008
        merge @= TERMS.TERM_009
        vocabulary_merge_example @= "merge @= TERMS.TERM_001"

        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_013

        related @= (
            SPECIFICATION_SPEC.SPEC_007,
            SPECIFICATION_SPEC.SPEC_008,
            DOCUMENT_SPEC.DOC_006,
            NORMS_API.norms.document.field,
        )

    class SECTION_006:
        r"""
        `{{project.name}}` は、人間が意図や判断、レビューを担い、LLM が {{TERM_001}} の継続的な編集を支援する文書運用を主要な利用形態の一つとして想定する。

        そのため、記述量の少なさだけを優先せず、意味の明示、機械的な validation、{{TERM_002}} の安定した再生成を重視する。一方で、LLM の利用は不要な複雑さを許容する理由にはせず、意味の重複や具体的な必要性のない抽象化は避ける。
        """
        title @= "LLM を介した文書運用"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002

    class SECTION_007:
        r"""
        `{{project.name}}` 自身の文書も `{{project.name}}` で構築している。

        - [Authoring Guide](docs/authoring_guide/INDEX.md): canonical source を設計・保守するための実践的な判断指針。
        - [Specification](docs/specification/INDEX.md): 保証する振る舞いと制約。
        - [API Reference](docs/api/INDEX.md): 公開インターフェース。
        - [Project Status](STATUS.md): 現在状態と現在から見た方向・告知。
        - [CHANGELOG](CHANGELOG.md): 過去の変更履歴。
        - [devdocs workspace](devdocs/README.md): このリポジトリの文書生成ワークスペース。
        - [`devdocs/canonical_sources/`](devdocs/canonical_sources/): 実際に使用している {{TERM_001}}。
        - [`devdocs/canonical_documents/`](devdocs/canonical_documents/): 検証済み source と {{TERM_005}} から生成した日本語 {{TERM_002}}。

        `devdocs/` は authoring API の参照例でもある。{{TERM_001}} と対応する {{TERM_002}} を比較すると、記述、context 注入、実現結果の関係を追跡できる。

        リポジトリ直下や `docs/` に配置する英語の {{TERM_003}} は、日本語 {{TERM_002}} を入力とする別の {{TERM_004}} で作成する。この翻訳・公開工程は `shikumi-devdoc` 自体の機能ではない。
        """
        title @= "Documentation"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_004

    class SECTION_008:
        r"""
        現在のバージョンは `{{project.version}}`。Python `{{project.requires-python}}` を対象とする。現在の開発段階や今後の方向は [`STATUS.md`](STATUS.md) を参照する。
        """
        title @= "バージョン"

    class SECTION_009:
        r"""
        `{{project.name}}` は MIT License で提供する。ライセンス本文は [`LICENSE`](LICENSE) を参照すること。
        """
        title @= "ライセンス"
