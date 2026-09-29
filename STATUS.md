# shikumi-devdoc Project Status

This document describes the current state of `shikumi-devdoc` and future-facing notices from the current point of view. Historical state transitions are not retained here; user-facing changes that actually occurred belong in the CHANGELOG.

This document is authored with the unified canonical-document model and the standard `shikumi_devdoc.fields.status` field set rather than a dedicated Project Status regulation.

## STATUS_001

title: Development stage

Current development stage: Beta. Current public version: `0.3.3`.

## STATUS_002

title: Supported Python

Current supported Python range: `>=3.11`.

## STATUS_003

title: Shikumi compatibility

`shikumi-devdoc 0.3.3` requires `shikumi>=0.2.0`. The compatibility baseline was established by the breaking 0.3.0 release. Because Shikumi's policy from 0.2.0 onward is to preserve backward compatibility, no upper bound is imposed unless a concrete incompatibility is identified.

## STATUS_004

title: Installed documentation resources

related: [DIST_001](docs/specification/distribution.md#dist_001-installed-reference-corpus), [DIST_002](docs/specification/distribution.md#dist_002-installed-published-documents)

The wheel includes the complete `devdocs/` reference corpus together with this release's published README, Project Status, CHANGELOG, and `docs/` tree as package resources.

## STATUS_005

title: Distribution and CI status

`shikumi-devdoc` is distributed through PyPI, and its source repository is public on [GitHub](https://github.com/minoru-jp/shikumi-devdoc). Repository references in the README use public GitHub URLs so that the documentation links also resolve from the README displayed on PyPI.

GitHub Actions CI runs on pushes and pull requests to `main`. It checks Python 3.11 through 3.14, the minimum supported `shikumi==0.2.0`, canonical-document synchronization, the test suite, and wheel/sdist build and release-distribution verification.

Publishing a GitHub Release runs the release workflow, which verifies that the tag matches the project version, builds and verifies the wheel and sdist, and publishes those verified artifacts to PyPI through Trusted Publishing.

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

