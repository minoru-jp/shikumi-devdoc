# Vocabulary

Rules for vocabulary sources, references, and public glossaries.

## VOC_001 Vocabulary profile

**MUST**

A Vocabulary source must be declared by applying `@vocabulary` to an ordinary `@canonical_source(...)` root. Vocabulary must not introduce a separate document grammar.

## VOC_002 Term declaration

**MUST**

Each direct child of the Vocabulary root is a term entry. After `inspect.cleandoc()`-equivalent normalization, its docstring must begin with a `{{term name}}` declaration. Exactly one term declaration is allowed at the normalized start, and body text must not follow the declaration marker on the same line. This declaration is the only way to set the term name.

## VOC_003 Definition derivation

**MUST NOT**

The term definition is derived from the docstring content following the declaration. The term name or definition must not be duplicated in a separate descriptor.

## VOC_004 Term references are merge targets

**MUST**

A Vocabulary term's canonical Python class must preserve a canonical term identity, name, and definition independently from its human-facing term name, and must be usable directly from a document node as `merge @= term`. Documents must not have to repeat the term name as a local alias, connect an entire Vocabulary, or declare a separate term-reference list.

## VOC_005 Public glossary selection

**MUST**

Vocabulary terms are public glossary entries by default. A term with no `glossary` metadata, or with `glossary @= True`, must be included in the public Glossary. Only a term explicitly marked with `glossary @= False` must be excluded.

## VOC_006 Replacement target

**MUST**

The `replacement` of a deprecated term must refer to a canonical term name in the same Vocabulary.

## VOC_007 Multiple term merge targets

**MUST**

A single document node must be able to register multiple distinct Vocabulary terms as merge targets. If short identities such as `TERM_001` collide across Vocabularies, the collision itself must remain valid; authors must be able to qualify the reference as `VocabularyA.TERM_001` and, if necessary, extend it through the module path until it is unique. Each reference must realize independently to the corresponding canonical term name, and translation semantics such as `preserve_spelling` must be derivable from the merge target's term identity.
