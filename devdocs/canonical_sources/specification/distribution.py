"""Distribution specification part."""
from shikumi_devdoc.fields.specification import condition, detail, level, related, MUST, MUST_NOT, SHOULD, SHOULD_NOT, MAY, INFORMATIVE
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title

@summary('wheel の文書資産と、sdist のリリースソース構成に関する規則。')
@canonical_source('Distribution', filename='distribution.md', order=90, merge_policy="local", heading="identity")
class SPECIFICATION_PART:
    """wheel に含める文書資産と、sdist に含めるリリースソースに関する規則。"""

    class DIST_001:
        """wheel は `devdocs/` 全体を `shikumi_devdoc/resources/devdocs/` に参照コーパスとして含めなければならない。"""
        title @= 'Installed reference corpus'
        level @= MUST

    class DIST_002:
        """wheel は公開 `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/` を `shikumi_devdoc/resources/published_docs/` に含めなければならない。"""
        title @= 'Installed published documents'
        level @= MUST

    class DIST_003:
        """wheel に含める文書資産を `shikumi_devdoc` の importable public API として扱ってはならない。文書資産は package resource として扱う。"""
        title @= 'Documentation resources are not public modules'
        level @= MUST_NOT

    class DIST_004:
        """MIT License 本文は project metadata の license file として wheel に含め、公開文書資産へ別コピーすることを要求してはならない。"""
        title @= 'License distribution'
        level @= MUST

    class DIST_005:
        """sdist からテスト環境を再構築できるよう、テスト用 optional dependency は `pytest` への依存を project metadata に宣言しなければならない。"""
        title @= 'Test dependency metadata'
        level @= MUST

    class DIST_006:
        """トップレベル `shikumi_devdoc` は Context 系と `fields` / `norms` / `realizers` 名前空間を公開し、文書記述 DSL や標準 field を flat に再公開してはならない。"""
        title @= 'Small top-level public namespace'
        level @= MUST

    class DIST_007:
        """{{TERM_001}} の基盤記述に必要な公開実体は `shikumi_devdoc.norms.<domain>` に分類しなければならない。{{TERM_001}} と共通 policy は `shikumi_devdoc.norms.common`、{{TERM_002}} の {{TERM_007}} writer と検証 system は `shikumi_devdoc.norms.document` に置く。用途別の {{TERM_009}} は任意利用の convenience API として `shikumi_devdoc.fields.<domain>` に置いてよいが、generic document core の必須意味論にしてはならない。"""
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_009
        title @= 'Namespaced norms authoring surface'
        level @= MUST

    class DIST_008:
        """標準 Realizer と公開成果物値は `shikumi_devdoc.realizers.<domain>` に分類し、各 domain 内では `MarkdownRealizer` など文脈上十分な短い名前を利用できなければならない。"""
        title @= 'Namespaced realizer surface'
        level @= MUST
    class DIST_009:
        """sdist は、そのリリースを build・test・文書再生成・distribution verification できるリリースソースを含めなければならない。少なくとも実装、テスト、`devdocs/`、公開 `docs/`、`scripts/`、ルートの公開文書、license、build metadata を含める。"""
        title @= 'Complete release source in sdist'
        level @= MUST

    class DIST_010:
        """sdist は Git hosting や hosted CI などリポジトリ運用にだけ必要な設定をリリースソースとして要求してはならない。`.github/` のような repository-operation-only path は除外してよく、VCS ignore 対象の cache、virtual environment、build artifact、IDE metadata は配布してはならない。"""
        title @= 'Repository-operation files are outside sdist'
        level @= MUST_NOT

