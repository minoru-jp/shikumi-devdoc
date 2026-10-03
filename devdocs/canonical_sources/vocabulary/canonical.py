"""Canonical repository-local vocabulary for shikumi-devdoc."""

from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source(
    "shikumi-devdoc 内部用語",
    filename="GLOSSARY.md",
    merge_policy="local",
    heading="identity",
)
class TERMS:
    """shikumi-devdoc の文書体系で共有する主要概念の用語。"""

    class TERM_001:
        """
        {{canonical source}}

        canonical document の内容と構造の正本となる Python 記述体。
        """

    class TERM_002:
        """
        {{canonical document}}

        canonical source から実現され、公開工程へ渡す時点で内容が確定した基準文書。
        """

    class TERM_003:
        """
        {{published document}}

        canonical document から公開工程を通じて派生し、利用者へ提供される文書。
        """

    class TERM_004:
        """
        {{publication workflow}}

        canonical document を published document へ変換し、公開形態へ整えるプロジェクト固有の工程。
        """

    class TERM_005:
        """
        {{realization context}}

        canonical source の外部に置かれ、文書の実現時に与えられる入力値の集合。
        """

    class TERM_006:
        """
        {{document node}}

        canonical document の階層と内容を構成する一つの意味的な文書単位。
        """

    class TERM_007:
        """
        {{field}}

        document node に付随する、名前を持つ構造化情報の単位。
        """

    class TERM_008:
        """
        {{field vocabulary}}

        特定の文書領域で用いる field と値に意味を与える、作者側の語彙集合。
        """

    class TERM_009:
        """
        {{standard field set}}

        汎用的な field を組み合わせて shikumi-devdoc が再利用用に提供する定義済みの field 集合。
        """

    class TERM_010:
        """
        {{template-bearing content}}

        placeholder や local reference を解釈して実現されるテンプレート性を持つ文書内容。
        """

    class TERM_011:
        """
        {{literal content}}

        placeholder などのテンプレート解釈を行わず、そのままの値として扱う文書内容。
        """

    class TERM_012:
        """
        {{external placeholder}}

        realization context にある外部値を文書内容へ取り込むための参照位置。
        """

    class TERM_013:
        """
        {{local reference}}

        document node 内の template 参照名と、その node で利用できる field、値、概念を結び付ける局所的な参照。
        """

    class TERM_014:
        """
        {{Vocabulary}}

        文書内で共有する用語名と概念定義を canonical source として保持する語彙集合。
        """

    class TERM_015:
        """
        {{Vocabulary term}}

        Vocabulary に属し、固有の名称と概念定義を持つ一つの用語。
        """

    class TERM_016:
        """
        {{Glossary}}

        Vocabulary から公開対象の用語と定義を取り出して構成する、人間向けの用語集。
        """

    class TERM_017:
        """
        {{表記維持}}

        翻訳などで文書の言語が変わっても、用語名の表記を変更せず扱うという意味情報。
        """
