"""Canonical repository-local vocabulary for shikumi-devdoc."""

from shikumi_devdoc.norms.vocabulary import canonical, term, title


@canonical
@title("shikumi-devdoc 内部用語")
class VOCABULARY:
    """shikumi-devdoc 自身の文書を記述するときに意味を固定する最小限の用語。"""

    @term("外部情報")
    class TERM_1:
        """実現時に記述体の外部から与えられ、参照記号を通じて成果物へ取り込まれる情報。"""

    @term("参照記号")
    class TERM_2:
        """外部情報または用語などを参照し、その値を実現結果へ取り込む位置を示す記号。"""

    @term("用語参照体")
    class TERM_3:
        """用語の識別子、名称および説明を、人間がソースコード上から追跡できる形に実現したもの。"""

    @term("表記維持")
    class TERM_4:
        """翻訳などによって文書の言語が変わる場合でも、その用語名の表記を変更せず使用することを示す情報。"""

