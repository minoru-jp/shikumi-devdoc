# Command-line interface

The installed `shikumi-devdoc` command.

## render

Validate canonical source and generate canonical Markdown artifacts.

name: shikumi-devdoc render

kind: Operation

related: [CLI_001](../specification/cli.md#cli_001), [CLI_003](../specification/cli.md#cli_003)

input: kind [document | index | glossary]: artifact kind to realize.

input: module [dotted import path]: canonical source module or package.

input: --output [path]: output directory for `document` / `index`, or output file for `glossary`.

output: output [filesystem artifacts]: Markdown artifacts produced after successful validation and realization.

detail: Optional controls: `--context`, `--notice`, and `--translation-source`. `render index` also accepts `--index-title` for the index H1.
