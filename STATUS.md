# shikumi-devdoc Project Status

This document describes the current state of `shikumi-devdoc` and future-facing notices from the current point of view. Historical state transitions are not retained here; user-facing changes that actually occurred belong in the CHANGELOG.

This document is authored with the unified canonical-document model and the standard `shikumi_devdoc.fields.status` field set rather than a dedicated Project Status regulation.

## STATUS_001

title: Development stage

Current development stage: Beta. Current public version: `0.3.5`.

## STATUS_002

title: Supported Python

Current supported Python range: `>=3.11`.

## STATUS_003

title: Shikumi compatibility

`shikumi-devdoc 0.3.5` requires `shikumi>=0.2.0`. The compatibility baseline was established by the breaking 0.3.0 release. Because Shikumi's policy from 0.2.0 onward is to preserve backward compatibility, no upper bound is imposed unless a concrete incompatibility is identified.

## STATUS_004

title: Installed documentation resources

related: [DIST_001](docs/specification/distribution.md#dist_001-installed-reference-corpus), [DIST_002](docs/specification/distribution.md#dist_002-installed-published-documents), [DIST_011](docs/specification/distribution.md#dist_011-pep-561-typed-package-marker)

The wheel includes the complete `devdocs/` reference corpus together with this release's published README, Project Status, CHANGELOG, and `docs/` tree as package resources, and also includes the PEP 561 `py.typed` marker in the package.

## STATUS_005

title: Distribution and CI status

`shikumi-devdoc` is distributed through PyPI, and its source repository is public on [GitHub](https://github.com/minoru-jp/shikumi-devdoc). Repository references in the README use public GitHub URLs so that the documentation links also resolve from the README displayed on PyPI.

GitHub Actions centralizes quality and test validation in the reusable `checks.yml` workflow. The shared gate runs Ruff 0.16.10 format checking and linting, BasedPyright 1.40.1 checks for both the package source and the consumer typing contract, a mypy 2.4.0 check of the documented canonical-source override recipe, canonical-document synchronization, the test suite on Python 3.11 through 3.14, and the test suite against the minimum supported `shikumi==0.2.0`. Normal CI calls these shared checks on pushes and pull requests to `main`, and also builds and verifies the wheel and sdist.

Publishing a GitHub Release first runs the same shared checks. Only after all checks succeed does the release workflow verify that the tag matches the project version, build and verify the wheel and sdist, and publish those verified artifacts to PyPI through Trusted Publishing. A revision that fails Ruff, either the package-source or consumer-contract BasedPyright check, the documented mypy override recipe, canonical-document synchronization, the supported-Python test matrix, or the minimum-Shikumi test therefore cannot proceed to release-artifact build or PyPI publication.

## STATUS_006

title: Static analysis status

For static analysis, `ruff format --check .`, `ruff check .`, and BasedPyright are all clean. Ruff is pinned to 0.16.10, targets Python 3.11, and uses that pinned version's stable default rule set as its lint baseline without implicitly opting into preview diagnostics. BasedPyright 1.40.1 checks `src/shikumi_devdoc` against Python 3.11 and, following the same quality policy as Shikumi itself, disables `reportUnnecessaryIsInstance`, `reportImplicitStringConcatenation`, `reportExplicitAny`, `reportPrivateUsage`, and `reportImplicitOverride`; with that policy it reports 0 errors / 0 warnings.

Code is not rewritten into less direct Python solely to satisfy the type checker. When a local `pyright: ignore` is needed to preserve runtime validation or semantic identity behavior, the concrete reason is written immediately next to that exception. Internal helpers whose runtime contract genuinely accepts broader input are typed to that contract instead of retaining an unnecessary suppression.

Separately, the `tests/typing` BasedPyright standard-mode contract checks a focused authoring sample together with `devdocs/canonical_sources` and `tests/examples` as consumer-side usage code, and this check also reports 0 errors / 0 warnings. The consumer contract does not inherit the package-source diagnostic suppressions and verifies that, with the PEP 561 `py.typed` marker published, real DSL usage including repeated field and merge `@=` operations does not become a type error under the BasedPyright / Pyright type model. This 0/0 status does not mean that every type checker consuming PEP 561 information is guaranteed to produce the same diagnostics.

## STATUS_007

title: Static analysis suppression policy

The five BasedPyright diagnostics disabled by this project are treated as project policy based on the responsibility of each diagnostic, not as broad escape hatches for making type checking pass.

`reportImplicitStringConcatenation` is primarily a notation/style rule rather than a core type-safety rule. `reportImplicitOverride` requires explicit `@override` annotations but does not disable type compatibility checking for overrides themselves. `reportPrivateUsage` is treated as a policy for package-internal API boundaries rather than Python-enforced access control.

`reportUnnecessaryIsInstance` is disabled so that runtime validation can remain in places where a check is unnecessary according to static types but still protects against invalid values supplied by untyped runtime callers. Because this policy also means genuinely unnecessary `isinstance()` checks are no longer detected automatically, checks without a defensive runtime purpose should not be retained during code review.

`reportExplicitAny` is handled with particular care because, among the five disabled diagnostics, it has the greatest potential to weaken type checking. `Any` is limited to boundaries such as metadata and arbitrary Python types where using `object`, generics, Protocols, or another more precise type would be unnatural; normal processing code must not be covered with `Any` merely to avoid warnings. If existing uses of `Any` can later be replaced with more precise types without adding undue complexity, re-enabling `reportExplicitAny` should be considered together with Shikumi itself.

Accordingly, the current 0 errors / 0 warnings status does not mean that every BasedPyright diagnostic is enabled at maximum strictness. It means the code is clean under the policy above, with diagnostics considered type defects enabled. Likewise, local `pyright: ignore` directives are restricted to cases with a concrete reason to preserve runtime semantics.

## STATUS_008

title: Canonical-source authoring style and mypy boundary

Shikumi core does not require authoring with `@=`; the descriptors in `shikumi.standard` are provided as an optional standard authoring style. `shikumi-devdoc` intentionally adopts this style so that fields, merges, and similar declarations can be arranged as `name @= value` and remain easy to read as document source. Canonical sources are executable Python, but normal operation treats them as a documentation-authoring domain using the Python runtime rather than as a general area for arbitrary application logic.

The writers in `shikumi-devdoc` annotate `__imatmul__` with the temporary binding type actually returned at runtime rather than statically preserving the original writer type through `Self`. Because augmented assignment conceptually rebinds `name = name.__imatmul__(value)`, mypy reports this type change as `Result type of @ incompatible in assignment [misc]`. This does not mean the DSL is inherently unrepresentable in mypy; it is an interaction with the project's current choice to keep these return annotations faithful to the runtime binding objects. BasedPyright / Pyright accept the same consumer source without errors.

For users who also check canonical sources with mypy, the recommended practice is to keep canonical sources in a dedicated module or package and disable the `misc` error code for that scope:

```toml
[[tool.mypy.overrides]]
module = ["your_project.devdocs.canonical_sources.*"]
disable_error_code = ["misc"]
```

The `module` pattern only takes effect when it matches the module name that mypy actually resolves. mypy derives module names from the directory layout, so when a directory above the canonical-source package belongs to another package (for example, below a `tests/` directory that contains `__init__.py`), a parent package name such as `tests.` can be prepended, the pattern no longer matches, and `misc` is not suppressed. In that case, match the pattern to the resolved module name, select the package with `mypy -p`, or declare the import root with `explicit_package_bases` and `mypy_path`. This repository's recipe check places its fixture below the `tests` package and uses the last option as test-harness configuration only; it is not part of the recommended recipe above.

`misc` is not specific to augmented assignment; it is a bucket used for multiple mypy diagnostics. The override therefore also suppresses other `misc` diagnostics inside that canonical-source package. Keep the override limited to the semantic canonical-source boundary and avoid mixing general application logic into that package. Per-line ignores and project-wide disabling of type checking are not the standard practice. Diagnostics outside `misc` remain active.

The formal CI consumer-typing contract continues to target BasedPyright, and a zero-error mypy result for all canonical source is not itself a release-gate requirement. Separately, a dedicated mypy recipe check verifies that the documented override accepts repeated `@=` while a clear non-`misc` type error in the same package remains visible.

## NOTICE_001

title: API stability after 0.3.0

kind: General

condition: From the `0.3.0` Beta release until the first major-version release.

From the `0.3.0` Beta release onward, public APIs will be maintained without backward-incompatible changes. The project will continue to be used in real workflows and dogfooded to confirm API stability; if no material problems emerge, it will then move to a major-version release.
## NOTICE_002

title: Deprecation of placeholders

kind: General

condition: From `0.3.2` until migration to `1.0.0`.

`@canonical_source(..., placeholders=...)` is deprecated as of 0.3.2. `placeholders=True` remains backward-compatible with `merge_policy="all"`, while `placeholders=False` remains backward-compatible with `merge_policy="local"`. New code should use `merge_policy`. The `placeholders` parameter is scheduled for removal in 1.0.0.

