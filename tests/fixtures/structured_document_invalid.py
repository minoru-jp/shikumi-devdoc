from tests.fixtures.document_field_vocabulary import compatibility, level
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Invalid", filename="invalid.md", placeholders=False, heading="identity")
class INVALID:
    class RepeatedField:
        level @= "MUST"
        level @= "SHOULD"
        compatibility @= ("CPython 3.11",)

        class L2:
            class L3:
                class L4:
                    class L5:
                        class L6:
                            pass
