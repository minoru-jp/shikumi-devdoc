# DOC-SNIPPET authoring-vocabulary-definition START
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Project Vocabulary", filename="GLOSSARY.md", placeholders=False, heading="identity")
class TERMS:
    class TERM_001:
        '''
        {{project term}}

        プロジェクト内で共有する概念の簡潔な定義。
        '''
# DOC-SNIPPET authoring-vocabulary-definition END
