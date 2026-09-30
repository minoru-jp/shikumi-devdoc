# DOC-SNIPPET readme-dogfood-specification START
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.specification import MUST, level
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Structured fields",
    filename="specification.md",
    order=50,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    class SPEC_001:
        """canonical root 内の class は {{TERM_006}} として解釈されなければならない。"""

        merge @= TERMS.TERM_006
        title @= "Class-derived document-node identity"
        level @= MUST
# DOC-SNIPPET readme-dogfood-specification END
