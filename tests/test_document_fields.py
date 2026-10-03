from shikumi_devdoc.norms._document import (
    DocumentField,
    FieldPresentation,
    FieldValue,
    document_node_identity,
)
from shikumi_devdoc.norms.document import system, test_target_field
from shikumi_devdoc.realizers.document import MarkdownRealizer
from tests.fixtures import (
    document_field_invalid,
    document_fields,
    document_literal_fields,
    structured_document_invalid,
    structured_document_source,
)
from tests.fixtures.document_field_vocabulary import requirement_status


def test_document_supports_external_author_defined_fields() -> None:
    result = system.validate(structured_document_source, placement=())
    assert result.is_valid, result.diagnostics

    validation = next(
        item
        for item in result.view.entities
        if item.subject is structured_document_source.VALIDATION
    )
    fields = validation.values(DocumentField)
    assert len(fields) == 1
    assert isinstance(fields[0], FieldValue)
    assert fields[0].schema is requirement_status.schema
    assert fields[0].schema.name == "status"
    assert fields[0].binding_name == "requirement_status"
    assert fields[0].value == "draft"


def test_python_binding_name_and_canonical_field_name_are_independent() -> None:
    assert requirement_status.name == "status"

    result = system.validate(structured_document_source, placement=())
    documents = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)
    validation = next(
        document for document in documents if document.filename == "validation.md"
    )
    assert "status: draft" in validation.content
    assert "requirement_status" not in validation.content


def test_nested_classes_are_markdown_heading_nesting_and_fields_are_not_headings() -> (
    None
):
    result = system.validate(structured_document_source, placement=())
    documents = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)
    validation = next(
        document for document in documents if document.filename == "validation.md"
    )

    assert "# Validation" in validation.content
    assert "## SourceValidation" in validation.content
    assert "### RejectInvalidSource" in validation.content
    assert "level: MUST" in validation.content
    assert "## level" not in validation.content
    assert "### level" not in validation.content
    assert "tag: validation, canonical-source" in validation.content


def test_document_node_identity_follows_class_nesting_not_document_root() -> None:
    assert (
        document_node_identity(structured_document_source.VALIDATION.SourceValidation)
        == "SourceValidation"
    )
    assert (
        document_node_identity(
            structured_document_source.VALIDATION.SourceValidation.RejectInvalidSource
        )
        == "SourceValidation.RejectInvalidSource"
    )


def test_field_cardinality_and_table_width_are_validated() -> None:
    result = system.validate(structured_document_invalid, placement=())
    assert not result.is_valid
    codes = {d.code for d in result.diagnostics}
    assert "document.field.cardinality" in codes
    assert "document.field.table.row_length" in codes


def test_structural_fields_render_markdown_shapes() -> None:
    result = system.validate(structured_document_source, placement=())
    assert result.is_valid, result.diagnostics

    documents = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)
    rendering = next(
        document for document in documents if document.filename == "rendering.md"
    )

    assert "steps:\n\n- validate the source\n- render the document" in rendering.content
    assert (
        "compatibility:\n\n"
        "| runtime | status |\n"
        "| --- | --- |\n"
        "| CPython 3.11 | supported |\n"
        "| CPython 3.12 | supported |"
    ) in rendering.content
    assert "```python\nresult = render(source)\nassert result\n```" in rendering.content
    assert "example:" not in rendering.content


def test_markdown_rejects_heading_depth_beyond_commonmark_limit() -> None:
    result = system.validate(structured_document_invalid, placement=())
    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert not check.is_realizable
    assert "markdown.document.heading.depth" in {d.code for d in check.diagnostics}


def test_test_target_field_is_literal_text_without_markdown_presentation() -> None:
    writer = test_target_field("diagram")
    assert writer.value_type is str
    assert writer.presentation is FieldPresentation.TEST_TARGET


def test_body_template_can_merge_fields_and_prose_fields_can_compose_fields() -> None:
    result = system.validate(document_fields, placement=())
    assert result.is_valid, result.diagnostics

    document = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)[0]
    assert "Status: stable {{PROJECT.name}}." in document.content
    assert "Literal marker: {{changes}}." in document.content
    assert "External value: Demo." in document.content
    # A field merged through another template is not appended again.
    assert "status: stable" not in document.content


def test_unreferenced_append_fields_keep_literal_placeholder_text() -> None:
    result = system.validate(document_fields, placement=())
    document = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)[0]

    assert "- Added {{PROJECT.name}} support." in document.content
    assert "- Kept literal {{status}} syntax." in document.content
    assert 'print("{{PROJECT.name}}")' in document.content
    assert "| {{PROJECT.name}} runtime | supported |" in document.content


def test_ignore_policy_omits_unreferenced_fields() -> None:
    result = system.validate(document_fields, placement=())
    document = MarkdownRealizer({"PROJECT": {"name": "Demo"}}).realize(result.view)[1]
    assert "Visible prose." in document.content
    assert "source-only metadata" not in document.content
    assert "hidden:" not in document.content


def test_literal_fields_never_interpret_placeholder_syntax() -> None:
    result = system.validate(document_literal_fields, placement=())
    assert result.is_valid, result.diagnostics
    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    content = realizer.realize(result.view)[0].content
    assert "scalar: {{PROJECT.version}}" in content
    assert "- {{scalar}}" in content
    assert "```jinja\nHello {{ user.name }}\n```" in content
    assert "| {{PROJECT.version}} | literal |" in content


def test_unknown_field_merge_cycle_and_shape_errors_are_validation_errors() -> None:
    result = system.validate(document_field_invalid, placement=())
    assert not result.is_valid
    codes = {d.code for d in result.diagnostics}
    assert "document.merge.target.unsupported" in codes
    assert "document.reference.cycle" in codes
    assert "document.field.cardinality" in codes
    assert "document.field.table.row_length" in codes


def test_field_binding_is_a_local_template_reference_without_merge() -> None:
    from tests.fixtures import document_field_references

    result = system.validate(document_field_references, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "First:\n- A" in content
    assert "Second:\n- B" in content
    assert "shared:" not in content


def test_field_and_merge_name_collision_is_reported_only_when_referenced() -> None:
    from tests.fixtures import document_field_reference_collision

    result = system.validate(document_field_reference_collision, placement=())
    assert not result.is_valid
    diagnostics = [
        diagnostic
        for diagnostic in result.diagnostics
        if diagnostic.code == "document.reference.ambiguous"
    ]
    assert len(diagnostics) == 1
    assert "TERM_001" in diagnostics[0].message


def test_field_and_merge_collision_can_be_disambiguated() -> None:
    from tests.fixtures import document_field_reference_qualified

    result = system.validate(document_field_reference_qualified, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "Local term and Alpha." in content


def test_plain_class_variable_does_not_enter_local_template_namespace() -> None:
    from tests.fixtures import document_plain_variable_reference

    result = system.validate(document_plain_variable_reference, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer().check(result.view)
    assert not check.is_realizable
    assert "markdown.document.placeholder.forbidden" in {
        diagnostic.code for diagnostic in check.diagnostics
    }


def test_lifecycle_fields_are_generic_document_fields() -> None:
    from tests.fixtures import document_lifecycle_fields

    result = system.validate(document_lifecycle_fields, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "introduced: 0.1.0" in content
    assert "deprecated: 0.3.0" in content
    assert "removed: 0.5.0" in content
    assert "replacement: new_api" in content
    assert "migration:\n\nUse `new_api` when migrating existing callers." in content


def test_reference_field_uses_semantic_reference_presentation() -> None:
    from shikumi_devdoc.norms._document import FieldPresentation
    from shikumi_devdoc.norms.document import reference_field

    writer = reference_field("depends on", (type, tuple), many=True)
    assert writer.presentation is FieldPresentation.REFERENCE
    assert writer.cardinality.value == "many"
