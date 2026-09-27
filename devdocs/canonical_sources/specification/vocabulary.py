"""Vocabulary specification part."""
from shikumi_devdoc.fields.specification import level, MUST, MUST_NOT
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary('語彙源、参照、公開用語集に関する規則。')
@canonical_source('Vocabulary', filename='vocabulary.md', order=20, placeholders=True, heading="identity")
class SPECIFICATION_PART:
    """語彙源、参照、公開用語集に関する規則。"""

    class VOC_001:
        """{{TERM_014}} source は通常の `@canonical_source(...)` root に `@vocabulary` を付与して宣言しなければならない。{{TERM_014}} は独自の文書 grammar を導入してはならない。"""
        merge @= TERMS.TERM_014
        title @= 'Vocabulary profile'
        level @= MUST

    class VOC_002:
        r"""{{TERM_014}} root の direct child は {{TERM_015}} とし、その docstring は `inspect.cleandoc()` 相当の正規化後に `\{{term name}}` 宣言で始まらなければならない。term declaration は正規化済み docstring の先頭に一つだけ存在し、宣言 marker の後ろには同一行の本文を置いてはならない。この宣言が term name を設定する唯一の方法である。"""
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_015
        title @= 'Term declaration'
        level @= MUST

    class VOC_003:
        """term definition は宣言に続く docstring 本文から導出しなければならず、用語名または definition を別 descriptor へ二重記述してはならない。"""
        title @= 'Definition derivation'
        level @= MUST_NOT

    class VOC_004:
        """{{TERM_015}} の canonical Python class は、human-facing な用語名とは独立した canonical term identity と用語名・definition を保持し、{{TERM_006}} から `merge @= term` の target として直接使用できなければならない。文書側は用語名を別名として再記述せず、term class の Python identity を参照名として利用できなければならない。{{TERM_014}} 全体の接続や別個の reference 宣言を要求してはならない。"""
        merge @= TERMS.TERM_015
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_014
        title @= 'Term references are merge targets'
        level @= MUST

    class VOC_005:
        """{{TERM_014}} の term は既定で {{TERM_016}} の公開対象として扱わなければならない。`glossary` が未指定または `True` の term は公開し、`glossary @= False` を明示した term だけを除外しなければならない。"""
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_016
        title @= 'Public glossary selection'
        level @= MUST

    class VOC_006:
        """deprecated 用語の `replacement` は同一 {{TERM_014}} 内の canonical な用語名を指さなければならない。"""
        merge @= TERMS.TERM_014
        title @= 'Replacement target'
        level @= MUST

    class VOC_007:
        r"""一つの {{TERM_006}} は複数の異なる {{TERM_015}} を merge target として保持できなければならない。複数の {{TERM_014}} で `TERM_001` のような短い identity が衝突する場合でも、その衝突自体を error としてはならず、`VocabularyA.TERM_001`、さらに必要なら module path を含む Python identity suffix まで伸ばして一意に参照できなければならない。各参照は対応する canonical term name へ独立して実現され、`preserve_spelling` など翻訳に必要な意味情報は merge target の term identity から導出できなければならない。"""
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_015
        merge @= TERMS.TERM_014
        title @= 'Multiple term merge targets'
        level @= MUST
