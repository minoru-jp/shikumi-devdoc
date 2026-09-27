# shikumi-devdoc Project Status

This document describes the current state of `shikumi-devdoc` and future-facing notices from the current point of view. Historical state transitions are not retained here; user-facing changes that actually occurred belong in the CHANGELOG.

This document is authored with the unified canonical-document model and the standard `shikumi_devdoc.fields.status` field set rather than a dedicated Project Status regulation.

## STATUS_001

title: Development stage

Current development stage: Beta. Current public version: `0.3.1`.

## STATUS_002

title: Supported Python

Current supported Python range: `>=3.11`.

## STATUS_003

title: Shikumi compatibility

`shikumi-devdoc 0.3.1` requires `shikumi>=0.2.0`. The compatibility baseline was established by the breaking 0.3.0 release. Because Shikumi's policy from 0.2.0 onward is to preserve backward compatibility, no upper bound is imposed unless a concrete incompatibility is identified.

## STATUS_004

title: Installed documentation resources

related: [DIST_001](docs/specification/distribution.md#dist_001-installed-reference-corpus), [DIST_002](docs/specification/distribution.md#dist_002-installed-published-documents)

The wheel includes the complete `devdocs/` reference corpus together with this release's published README, Project Status, CHANGELOG, and `docs/` tree as package resources.

## STATUS_005

title: Distribution and CI status

`shikumi-devdoc` is currently published **only through PyPI**. There is not yet a public web page for browsing the source repository.

As a result, some repository-relative links in the README and other published documentation do not resolve when the documentation is viewed on PyPI. This is a known limitation of the current distribution setup.

When the source repository is published on the web, for example on GitHub, the documentation links will be revised against the public repository URL so that they resolve correctly from the published documentation.

There is also no hosted CI at present because there is no public source repository yet. Release verification and PyPI uploads are currently performed locally. CI will be introduced when the repository is published on GitHub and can be configured against that public environment.

## NOTICE_001

title: API stability after 0.3.0

kind: General

condition: From the `0.3.0` Beta release until the first major-version release.

From the `0.3.0` Beta release onward, public APIs will be maintained without backward-incompatible changes. The project will continue to be used in real workflows and dogfooded to confirm API stability; if no material problems emerge, it will then move to a major-version release.
