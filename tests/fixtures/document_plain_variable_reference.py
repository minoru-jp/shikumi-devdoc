from shikumi_devdoc.norms.common import canonical_source

plain_value = "not a field"


@canonical_source("Plain variable", filename="plain-variable.md", placeholders=False, heading="identity")
class PLAIN_VARIABLE:
    """{{plain_value}}"""

    plain_value = plain_value
