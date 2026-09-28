"""CLI API reference part."""
from shikumi_devdoc.fields.api_reference import detail, input, kind, name, output, related, NAMESPACE, TYPE, VALUE, OPERATION, OTHER, API_NAMESPACE, API_TYPE, API_VALUE, API_OPERATION, API_OTHER
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from devdocs.canonical_sources.specification.cli import SPECIFICATION_PART as CLI_SPEC

@summary('インストール時に利用できる `shikumi-devdoc` CLI。')
@canonical_source('Command-line interface', filename='cli.md', order=40, merge_policy="all", heading="identity")
class API_REFERENCE_PART:
    """インストール時に公開される `shikumi-devdoc` コマンド。"""


    class render:
        """{{TERM_001}} を検証し、canonical Markdown document を生成する。"""
        merge @= TERMS.TERM_001
        name @= 'shikumi-devdoc render'
        kind @= OPERATION
        related @= (CLI_SPEC.CLI_001, CLI_SPEC.CLI_003)
        input @= 'kind [document | index | glossary]: 実現する成果物種別。'
        input @= 'module [dotted import path]: canonical source module または package。'
        input @= '--output [path]: `document` / `index` では出力ディレクトリ、`glossary` では出力ファイル。'
        output @= 'output [filesystem artifacts]: 検証と実現に成功した Markdown 成果物。'
        detail @= 'Optional controls: `--context`、`--notice`、`--translation-source` を利用できる。`render index` では `--index-title` で索引 H1 を指定できる。'
