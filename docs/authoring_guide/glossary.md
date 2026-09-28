# Writing a Glossary / Vocabulary

Introduce a Vocabulary only when multiple documents need to share authoritative concept names and definitions.

## When to create one

Create a Vocabulary when project-specific terms recur across documents and should be renamed or defined centrally. Do not turn ordinary language or one-off terms into Vocabulary entries without a concrete reuse need.

Vocabulary terms are included in the public Glossary by default. Mark only internal or otherwise non-public terms with `glossary @= False`. `glossary @= True` is equivalent to the default and normally need not be written.

## Define stable term identities

Give term classes stable identities such as `TERM_NNN`. The normalized docstring begins with exactly one `{{term name}}` declaration. The source docstring can use normal Python indentation.

```python
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Project Vocabulary", filename="GLOSSARY.md", merge_policy="local", heading="identity")
class TERMS:
    class TERM_001:
        """
        {{project term}}

        A concise definition of a concept shared across the project.
        """
```

## Merge terms directly where they are used

Do not attach a Vocabulary implicitly to an entire document. Merge the canonical term class in the document node that uses it.

```python
class Overview:
    """The source of truth for this document is {{TERM_001}}."""

    merge @= TERMS.TERM_001
```

## External Vocabularies work the same way

Import the term class from another package and use it directly as the merge target.

```python
merge @= FrameworkVocabulary.TERM_001
```

When short identities such as `TERM_001` collide, lengthen the Python identity or use an explicit alias only at the ambiguous boundary. Do not fully qualify every term in advance.
