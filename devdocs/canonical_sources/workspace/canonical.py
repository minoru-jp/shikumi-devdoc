"""Canonical Japanese source for devdocs/README.md."""

from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source(
    "devdocs/",
    filename="README.md",
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class SECTION_001:
    r"""
    `devdocs/` は、このリポジトリ自身の文書体系をドッグフーディングするためのオーサリング・ワークスペースである。

    ここでは、Python で記述する {{TERM_001}}、実現時に注入する {{TERM_005}}、そこから生成される {{TERM_002}} を明示的に分離する。{{TERM_002}} から翻訳・ローカライズ・配布などを経て作る {{TERM_003}} は、このライブラリ固有の責務ではなく、このリポジトリの公開運用としてトップレベルの `README.md`、`STATUS.md`、`CHANGELOG.md`、および `docs/` に配置する。
    """

    merge @= TERMS.TERM_001
    merge @= TERMS.TERM_005
    merge @= TERMS.TERM_002
    merge @= TERMS.TERM_003

    class SECTION_002:
        r"""
        ```text
        devdocs/
        ├── README.md
        ├── canonical_sources/
        ├── config/
        │   ├── context.json
        │   └── notice.toml
        └── canonical_documents/
        ```

        - `canonical_sources/` は、{{TERM_002}} を構成する権威ある Python {{TERM_001}} 単位を保持する。
        - Specification / API Reference / STATUS / CHANGELOG の field set は `shikumi_devdoc.fields` の {{TERM_009}} を dogfood する。
        - `config/` は、{{TERM_005}} や生成 notice など、このリポジトリ固有の実現時入力を保持する。
        - `canonical_documents/` は、{{TERM_001}} を検証し、必要な context を注入して realizer で組み立てた {{TERM_002}} を保持する。
        - `README.md` はこのワークスペースの入口であり、このファイル自身も `canonical_sources/workspace/canonical.py` から {{TERM_002}} を生成し、その公開版として配置する。
        """

        title @= "ディレクトリ構成"

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_009
        merge @= TERMS.TERM_005

    class SECTION_003:
        r"""
        `canonical_sources/` の Python 記述体は、{{TERM_002}} を生成するための権威ある {{TERM_001}} である。README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference、Vocabulary、およびこの `devdocs/README.md` の source unit をここに置く。

        README、Authoring Guide、STATUS、CHANGELOG、Specification、API Reference はいずれも共通の `@canonical_source(...)` document model で記述する。Specification と API Reference は専用の root / part 規定体を持たず、各ファイルを独立した {{TERM_002}} とする。collection の `INDEX.md` は {{TERM_001}} を二重記述せず、package を入力とする独立した index realizer から生成し、各文書の `@summary(...)` metadata を概略として利用する。

        {{TERM_001}} では `shikumi_devdoc.norms` の基盤 API と、必要に応じて `shikumi_devdoc.fields` の {{TERM_009}} を import する。{{TERM_001}} と共通 policy は `norms.common`、document {{TERM_007}} writer と検証 system は `norms.document` を利用する。{{TERM_009}} は generic primitives の定義済み組み合わせにすぎず、独自 {{TERM_008}} へ置き換えられる。Norm の実装モジュールは private であり、作例でも公開 import path として使用しない。標準文書実現器は `shikumi_devdoc.realizers.document` から利用する。

        {{TERM_014}} の意味上の正本は `canonical_sources/vocabulary/canonical.py` に保持される。{{TERM_014}} source 自体も通常の `@canonical_source(...)` であり、`@vocabulary` marker が semantic profile を付与する。各 direct child の docstring は共通 indent を正規化した後、先頭の `\{{term name}}` 宣言から用語名を定義し、その後続本文を definition とする。{{TERM_015}} はこの canonical class を直接参照するため、IDE 向け proxy module は生成しない。
        """

        title @= "Canonical source"

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_009
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_008
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_015

    class SECTION_004:
        r"""
        `config/context.json` は、プロジェクト名、現在版、対象 Python 版など、{{TERM_001}} に固定せず realization 時点で外部から注入する値を保持する {{TERM_005}} である。このファイルは `shikumi-devdoc` の一般仕様ではなく、このリポジトリの運用上の入力である。

        Context は歴史的事実の保存先ではない。例えば CHANGELOG の過去バージョンのように後から変化してはならない情報は {{TERM_001}} に直接記述する。一方、README の現在バージョンのように realization 時点の値を反映したい情報は context に置ける。

        `config/notice.toml` は、{{TERM_002}} の先頭へ埋め込む生成上の注意事項と、後続の翻訳・公開工程に渡すこのリポジトリ固有の方針を保持する。

        CLI はこれらのファイルを自動探索しない。`context.json` は JSON 文字列として `--context` へ渡し、`notice.toml` は `--notice` で明示的に指定する。
        """

        title @= "Realization context"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_002

    class SECTION_005:
        r"""
        `canonical_documents/` は `shikumi-devdoc` が一貫して責任を持つ成果物の境界である。{{TERM_001}} を対応する規定体で検証し、{{TERM_005}} を注入し、realizer によって文書として組み立てた結果を {{TERM_002}} とする。

        {{TERM_002}} は生成物だが、単なる一時ファイルではない。この時点で文書としての内容が確定しており、規定体が意図どおり実現されたか、context が正しく反映されたか、翻訳前の日本語が適切かを確認する境界面として Git に保持する。

        {{TERM_002}} は直接編集しない。変更が必要な場合は `canonical_sources/` または {{TERM_005}} へ戻って修正し、再生成する。
        """

        title @= "Canonical document"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_002

    class SECTION_006:
        r"""
        リポジトリルートから、次のように {{TERM_002}} を再生成できる。

        ```bash
        CONTEXT="$(cat devdocs/config/context.json)"

        shikumi-devdoc render glossary \
          devdocs.canonical_sources.vocabulary.canonical \
          -o devdocs/canonical_documents/GLOSSARY.md \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.readme.canonical \
          -o devdocs/canonical_documents \
          --context "$CONTEXT" \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.authoring_guide \
          -o devdocs/canonical_documents/authoring_guide \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render index \
          devdocs.canonical_sources.authoring_guide \
          -o devdocs/canonical_documents/authoring_guide \
          --index-title "shikumi-devdoc Authoring Guide" \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.workspace.canonical \
          -o devdocs/canonical_documents/devdocs \
          --notice devdocs/config/notice.toml

        shikumi-devdoc render document \
          devdocs.canonical_sources.status.canonical \
          -o devdocs/canonical_documents \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.changelog.canonical \
          -o devdocs/canonical_documents/changelog \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.specification \
          -o devdocs/canonical_documents/specification \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render index \
          devdocs.canonical_sources.specification \
          -o devdocs/canonical_documents/specification \
          --index-title "shikumi-devdoc Specification" \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render document \
          devdocs.canonical_sources.api_reference \
          -o devdocs/canonical_documents/api \
          --context "$CONTEXT" \
          --notice devdocs/config/notice.toml \
          --translation-source

        shikumi-devdoc render index \
          devdocs.canonical_sources.api_reference \
          -o devdocs/canonical_documents/api \
          --context "$CONTEXT" \
          --index-title "shikumi-devdoc API Reference" \
          --notice devdocs/config/notice.toml \
          --translation-source
        ```

        `merge_policy` は `merge @= ...` による local merge と external context の許可範囲を `"all"` / `"local"` / `"external"` / `"forbidden"` で宣言する。同じ node に直接定義した field の template 参照は policy の対象外である。このリポジトリでは README は両方の差し込みを使うため `"all"`、Specification は local merge だけを使うため `"local"`、CHANGELOG はどちらも使わないため `"forbidden"` を指定する。これは文書種別そのものではなく、各 canonical source が採用する差し込み経路に合わせた設定である。旧 `placeholders` は 0.3.2 から非推奨である。
        """

        title @= "生成"

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_001

    class SECTION_007:
        r"""
        sdist からテスト・静的解析環境を再構築する場合は、開発用 optional dependency をインストールする。

        ```bash
        python -m pip install '.[test,lint,typecheck]'
        ruff format --check .
        ruff check .
        basedpyright
        basedpyright -p tests/typing
        pytest
        ```

        `test` extra は `pytest>=8.0`、`lint` extra は `ruff==0.16.10`、`typecheck` extra は `basedpyright==1.40.1` と `mypy==2.4.0` を宣言する。Ruff は Python 3.11 を target version とし、固定した Ruff 版の stable default lint rule set を baseline として format check と lint の両方を要求する。BasedPyright は package source と consumer contract を分離し、通常の `basedpyright` では `src/shikumi_devdoc` を Python 3.11 基準・Shikumi 本体と同じ診断方針で 0 errors / 0 warnings にする。`basedpyright -p tests/typing` は standard mode で専用 typing sample、`devdocs/canonical_sources`、`tests/examples` を consumer 利用コードとして検査し、同じく 0 errors / 0 warnings を要求する。mypy は canonical-source 向けに文書化した override recipe が成立し、`misc` 以外の診断を隠さないことだけを専用 script で確認する。いずれも通常利用時の必須依存には含めない。GitHub Actions ではこれらの静的解析、canonical document 同期、対応 Python と最低対応 Shikumi の test suite を reusable `checks.yml` に集約し、通常 CI と release workflow の双方から同じ品質ゲートを使用する。release artifact の build は checks 成功後だけ実行する。

        公開前の distribution verification は hosted CI に依存させず、ローカルで実行する。`build` frontend を利用可能にしたうえで次を実行し、wheel / sdist の内容、installed package、CLI、`pip check`、installed wheel を使った dogfood rendering を確認する。

        ```bash
        python scripts/check_dist.py
        ```

        Shikumi の同時リリース準備中など、必要な dependency version がまだ PyPI にない場合は、その source tree を明示して同じ smoke test を行える。

        ```bash
        python scripts/check_dist.py --shikumi-source /path/to/shikumi
        ```
        """

        title @= "テストと静的解析"

    class SECTION_008:
        r"""
        {{TERM_003}} は {{TERM_002}} から利用者ごとの {{TERM_004}} で作られる派生物であり、`shikumi-devdoc` はその運用方法を規定しない。翻訳、ローカライズ、文章表現の調整、サイト生成、PDF 化、配布先への配置などはプロジェクトごとに異なり得る。

        このリポジトリでは、日本語の {{TERM_002}} を人間または LLM が英語へ翻訳し、トップレベル `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/authoring_guide/`、`docs/specification/`、`docs/api/`、およびこの `devdocs/README.md` へ {{TERM_003}} として配置する。

        `notice.toml` の運用コメントや `shikumi-devdoc:translation-metadata` は {{TERM_003}} の内容ではないため、公開時に除去する。
        """

        title @= "Published document"

        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_004

    class SECTION_009:
        r"""
        `devdocs/` 全体は {{TERM_001}} と {{TERM_002}} を対にして読める参照コーパスとして wheel に含める。インストール後は `shikumi_devdoc/resources/devdocs/` に配置される。

        同じ wheel には、その版でこのリポジトリが用意した published `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/` も `shikumi_devdoc/resources/published_docs/` に含める。これはこのリポジトリの配布方針であり、`shikumi-devdoc` が一般に {{TERM_004}} を規定することを意味しない。これらは importable public API ではなく package resource である。MIT License 本文は `license-files` による通常の wheel license metadata として配布する。
        """

        title @= "wheel での配布"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_004

    class SECTION_010:
        r"""
        sdist はこの版のリリースソースを再構成・検証するための完全な source distribution とする。実装だけでなく、`tests/`、`devdocs/`、公開 `docs/`、`scripts/`、ルートの公開文書、license、build metadata を含める。`scripts/check_dist.py` 自体も sdist に含め、取得した source distribution から同じ distribution verification を再実行できるようにする。

        file selection は個別ファイルを列挙するのではなく、Hatchling が VCS ignore を尊重する既定動作を基礎に、原則としてリリースソース全体を収録する。Git hosting や hosted CI など repository operation にだけ必要な `.github/` は明示的に除外する。cache、virtual environment、`dist/`、IDE metadata など開発機固有または生成済みの一時物は `.gitignore` により配布対象から除外する。
        """

        title @= "sdist での配布"
