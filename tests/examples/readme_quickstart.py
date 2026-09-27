# DOC-SNIPPET readme-minimal-source START
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Example", filename="example.md", placeholders=False, heading="identity")
class EXAMPLE:
    class Introduction:
        '''Hello from shikumi-devdoc.'''
# DOC-SNIPPET readme-minimal-source END
