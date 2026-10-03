"""README authoring pattern."""

from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title

minimal_readme_example = test_target_field("minimal README source")


@summary("repository の入口となる README を prose 中心で簡潔に構成する方法。")
@canonical_source(
    "Writing a README",
    filename="readme.md",
    order=10,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """README は repository の入口として、採用判断と次の行動に必要な情報へ集中させる。"""

    class SECTION_001:
        r"""
        repository を初めて見る読者へ、何をする project か、どう導入するか、最初に何を実行するか、詳細をどこで読むかを示したい場合に README を作る。内部仕様、全設定項目、全 API を README へ詰め込む必要はない。

        README だけで十分な project なら、他の authoring pattern を形式的に追加しない。
        """

        title @= "README を作る場合"

    class SECTION_002:
        r"""
        多くの場合、次の順序で十分である。

        1. project が何をするかを短く説明する。
        2. 重要な利用条件や安全上の境界があれば早い位置に置く。
        3. installation を示す。
        4. 最小の利用例を示す。
        5. CLI、Configuration、API Reference、Specification など、実際に存在する詳細文書へリンクする。

        長い tutorial や完全な reference が必要になったら README を伸ばし続けず、Getting Started や専用 guide へ分ける。
        """

        title @= "推奨構造"

    class SECTION_003:
        r"""
        README は narrative document なので、通常は docstring prose と nested {{TERM_006}} を中心に構成する。見出し構造は nested class と `title @= ...` で表し、表示 title と class identity は分離する。root の `heading="title"` が title を見出しへ実現する。

        コード例を通常のテストから直接検証して実装 drift を防ぎたい場合だけ `test_target_field` に分離する。小さな例示コードは docstring に直接書いてよい。fence は docstring 側に置き、現在 version のように再実現時に変わってよい値だけを realization context に置く。
        """

        title @= "正本は prose 中心でよい"

        merge @= TERMS.TERM_006

    class SECTION_004:
        r"""
        ```python
        {{minimal_readme_example}}
        ```

        README 固有の schema はない。これは generic canonical document の一例であり、必要な節だけを追加する。
        """

        title @= "最小例"

        minimal_readme_example @= r'''
        from shikumi_devdoc.norms.common import canonical_source
        from shikumi_devdoc.norms.document import title


        @canonical_source(
            "Example", filename="README.md", merge_policy="local", heading="title"
        )
        class README:
            """A small tool for processing example inputs."""

            class SECTION_001:
                """Install the package with your normal Python package workflow."""

                title @= "Installation"

            class SECTION_002:
                """Run the smallest useful example, then link to detailed guides."""

                title @= "Quick start"
        '''

    class SECTION_005:
        r"""
        README に全 CLI option、全設定 schema、全 normative rule を重複して書かない。README は概要と導線を担い、詳細の正本はそれぞれの目的文書へ置く。

        README の見出し名を class name に反映し続ける必要もない。タイトル変更で identity が drift する場合は `SECTION_NNN` のような opaque identity を使う。
        """

        title @= "避けること"
