"""Executable coverage for the Authoring Guide test-target-field example."""

# DOC-SNIPPET authoring-test-target-field START
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import test_target_field, title


example = test_target_field("example")


@canonical_source("Guide", filename="guide.md", placeholders=False, heading="title")
class GUIDE:
    class SECTION_001:
        """
        ```python
        {{example}}
        ```
        """
        title @= "Example"
        example @= """
        print("hello")
        """
# DOC-SNIPPET authoring-test-target-field END
