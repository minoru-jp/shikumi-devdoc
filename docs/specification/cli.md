# Command-line interface

Input/output rules for the `shikumi-devdoc` CLI.

## CLI_001

The CLI must require callers to provide artifact output paths explicitly through `-o/--output`.

title: Explicit output path

level: MUST

## CLI_002

For `render document`, `-o` must be treated as the output directory containing canonical documents whose filenames are declared by `@canonical_source(..., filename=...)`.

title: Document output directory

level: MUST

related: [SPEC_003](specification.md#spec_003)

## CLI_003

When an operational notice is embedded, the TOML file must be provided explicitly through `--notice`; the CLI must not discover it implicitly.

title: Notice is explicit

level: MUST

## CLI_004

`render index` must accept a canonical-source package and generate an index of the canonical documents in that package as `INDEX.md` in the selected output directory. A standalone module must not be accepted as input to `render index`.

title: Explicit package index rendering

level: MUST

related: [SPEC_009](specification.md#spec_009)
