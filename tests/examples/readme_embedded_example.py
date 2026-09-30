# DOC-SNIPPET readme-embedded-example START
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
class EXAMPLE:
    class Introduction:
        "Hello from shikumi-devdoc."
# DOC-SNIPPET readme-embedded-example END
