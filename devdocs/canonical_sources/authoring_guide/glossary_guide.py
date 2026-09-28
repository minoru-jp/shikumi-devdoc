"""Glossary and Vocabulary authoring pattern."""

from devdocs.canonical_sources.specification.vocabulary import SPECIFICATION_PART as VOCABULARY_SPEC
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


vocabulary_definition_example = test_target_field("Vocabulary definition example")
vocabulary_reference_example = test_target_field("Vocabulary reference example")
external_vocabulary_merge_example = test_target_field("external Vocabulary merge example")


@summary("共有概念を Vocabulary として定義し、必要な term だけを各 document へ merge する方法。")
@canonical_source(
    "Writing a Glossary / Vocabulary",
    filename="glossary.md",
    order=80,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Vocabulary は複数文書で正式名称と概念定義を共有する必要がある場合だけ導入する。"""

    class SECTION_001:
        r"""
        project 固有の用語が複数文書で繰り返され、名称変更や定義を一か所で管理したい場合に Vocabulary を作る。一般語や一度しか使わない語まで Vocabulary 化しない。

        Vocabulary term は既定で Glossary の公開対象になる。内部用 term など公開したくないものだけ `glossary @= False` を明示する。`glossary @= True` は既定値と同じなので通常は書かない。
        """
        title @= "Glossary / Vocabulary を作る場合"

    class SECTION_002:
        r"""
        term class は `TERM_NNN` のような stable identity を持たせ、正規化された docstring の先頭へ `\{{term name}}` declaration を一つだけ書く。docstring は通常の Python indentation に合わせてよい。

        ```python
        {{vocabulary_definition_example}}
        ```
        """
        title @= "Stable term identity を定義する"

        vocabulary_definition_example @= r'''
        from shikumi_devdoc.norms.common import canonical_source
        from shikumi_devdoc.norms.vocabulary import vocabulary


        @vocabulary
        @canonical_source("Project Vocabulary", filename="GLOSSARY.md", merge_policy="local", heading="identity")
        class TERMS:
            class TERM_001:
                """
                {{project term}}

                プロジェクト内で共有する概念の簡潔な定義。
                """
        '''
        related @= (VOCABULARY_SPEC.VOC_001,)

    class SECTION_003:
        r"""
        文書全体へ暗黙に Vocabulary を接続せず、その term を使う document node で canonical term class を直接 `merge` する。

        ```python
        {{vocabulary_reference_example}}
        ```
        """
        title @= "利用する node で直接 merge する"

        vocabulary_reference_example @= r'''
        class Overview:
            """この文書の正本は {{TERM_001}} である。"""

            merge @= TERMS.TERM_001
        '''

    class SECTION_004:
        r"""
        別 package の Vocabulary でも、import した term class を直接 merge target にする。

        ```python
        {{external_vocabulary_merge_example}}
        ```

        同じ短い `TERM_001` が衝突した場合だけ、より長い Python identity や明示 alias で区別する。最初から完全修飾名を多用しない。
        """
        title @= "外部 Vocabulary も同じように参照する"

        external_vocabulary_merge_example @= "merge @= FrameworkVocabulary.TERM_001"
