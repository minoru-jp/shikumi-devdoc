from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Framework Vocabulary", filename="FRAMEWORK_GLOSSARY.md", merge_policy="local", heading="identity")
class FrameworkVocabulary:
    class TERM_001:
        '''{{framework term}}

        外部 Vocabulary から参照されるテスト用の概念。
        '''
