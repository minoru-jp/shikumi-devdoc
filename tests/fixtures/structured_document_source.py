from tests.fixtures.document_field_vocabulary import (
    compatibility,
    example,
    level,
    related,
    requirement_status,
    steps,
    tag,
)
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Validation", filename="validation.md", order=10, merge_policy="all", heading="identity")
class VALIDATION:
    """Validation rules for {{PROJECT.name}}."""

    requirement_status @= "draft"

    class SourceValidation:
        """Source validation rules."""

        level @= "MUST"
        tag @= "validation"
        tag @= "canonical-source"

        class RejectInvalidSource:
            """Invalid canonical sources must be rejected."""

            level @= "MUST"


@canonical_source("Rendering", filename="rendering.md", order=20, merge_policy="local", heading="identity")
class RENDERING:
    """Rendering rules."""

    class StableOutput:
        """Equivalent input should produce stable output.

        ```python
        {{example}}
        ```
        """

        level @= "SHOULD"
        steps @= "validate the source"
        steps @= "render the document"
        compatibility @= ("CPython 3.11", "supported")
        compatibility @= ("CPython 3.12", "supported")
        example @= """
        result = render(source)
        assert result
        """
