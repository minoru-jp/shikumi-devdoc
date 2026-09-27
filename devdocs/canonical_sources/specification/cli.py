"""CLI specification part."""

from shikumi_devdoc.fields.specification import MUST, level, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.specification.specification import SPECIFICATION_PART as SPECIFICATION_SPEC


@summary('`shikumi-devdoc` CLI の入出力規則。')
@canonical_source("Command-line interface", filename="cli.md", order=80, placeholders=True, heading="identity")
class SPECIFICATION_PART:
    """`shikumi-devdoc` CLI の入出力規則。"""

    class CLI_001:
        """CLI は成果物の出力先を `-o/--output` で利用者から明示的に受け取らなければならない。"""

        title @= "Explicit output path"
        level @= MUST

    class CLI_002:
        """`render document` の `-o` は、`@canonical_source(..., filename=...)` で決まる {{TERM_002}} を配置する出力ディレクトリとして扱われなければならない。"""

        merge @= TERMS.TERM_002

        title @= "Document output directory"
        level @= MUST
        related @= (SPECIFICATION_SPEC.SPEC_003,)

    class CLI_003:
        """運用 notice を埋め込む場合は `--notice` で TOML ファイルを明示し、CLI が暗黙に探索してはならない。"""

        title @= "Notice is explicit"
        level @= MUST
    class CLI_004:
        """`render index` は {{TERM_001}} package を入力として受け取り、その package に含まれる {{TERM_002}} の索引を `INDEX.md` として指定出力ディレクトリへ生成しなければならない。module 単体は `render index` の入力として受理してはならない。"""

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002

        title @= "Explicit package index rendering"
        level @= MUST
        related @= (SPECIFICATION_SPEC.SPEC_009,)

