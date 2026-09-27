# Writing CLI documentation

CLI documentation should help command-line users reach the operation they want to perform.

## When to create it

Create dedicated CLI documentation when the command-line interface is a major public surface and the README's minimal example cannot adequately explain arguments, modes, input/output behavior, or safety boundaries.

## Organize around operations

Structure the document around user tasks rather than parser implementation order. Typical concerns include basic invocation, input or target selection, modes, preview/output, and exit/error behavior.

If one page becomes large, split it into a collection by meaningful concern. Do not create a page per option merely because the parser has many options.

## Make command examples testable

Put commands in `test_target_field` when ordinary tests should inspect the exact command text. Keep the `bash` fence in the surrounding docstring.

```bash
example --input src --output build
```

When option names or invocation shape are likely to drift, cover the documented form with parser or CLI integration tests.

## Put strict contracts in the Specification

CLI documentation focuses on how to use the interface. Exact default-selection rules, option conflicts, forbidden combinations, and exit contracts should live in a Specification when those are compatibility requirements. Link the guide to the relevant specification page.
