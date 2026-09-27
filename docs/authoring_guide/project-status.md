# Writing Project Status

Project Status describes the current state and future direction of the project rather than release history.

## When to create one

Create one when users need more detail than the README can reasonably provide about maturity, compatibility policy, migration direction, or states such as Beta, experimental, or maintenance-only. A stable project with no special notices may not need a separate status document.

## Separate current facts from future direction

Do not mix current state, future direction, and conditional notices into one undifferentiated paragraph. `shikumi_devdoc.fields.status` provides `kind`, `condition`, and `related` when those meanings benefit from structure; human-readable node titles use `shikumi_devdoc.norms.document.title`.

## Do not replace the CHANGELOG

Project Status is a current snapshot. The CHANGELOG records historical release facts. Update the status document when the present state changes, while preserving the past change event in the CHANGELOG.
