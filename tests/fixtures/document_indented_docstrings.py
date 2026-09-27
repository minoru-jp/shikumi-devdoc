from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Indented", filename="indented.md", heading="identity")
class ROOT:
    """
    Root content.

        Root relative indentation.
    """

    class CHILD:
        r'''
        Child content.

            Child relative indentation.
        '''
