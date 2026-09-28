from shikumi_devdoc.norms.common import canonical_source, merge
from tests.examples.framework_vocabulary import FrameworkVocabulary


@canonical_source("External Vocabulary Example", filename="external-vocabulary.md", merge_policy="local", heading="identity")
class DOCUMENT:
    class Overview:
        '''The shared name is {{TERM_001}}.'''

        # DOC-SNIPPET authoring-external-vocabulary START
        merge @= FrameworkVocabulary.TERM_001
        # DOC-SNIPPET authoring-external-vocabulary END
