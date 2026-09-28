"""API-reference authoring pattern."""

from devdocs.canonical_sources.api_reference.fields import API_REFERENCE_PART as FIELDS_API
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


api_example = test_target_field("API reference example")


@summary("公開 API を name/kind/input/output/detail と lifecycle field で記述する方法。")
@canonical_source(
    "Writing an API Reference",
    filename="api-reference.md",
    order=60,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """API Reference は公開 surface を subject-centered に検索・確認できる形で記録する。"""

    class SECTION_001:
        r"""
        Python API、HTTP API、command object など、利用者が個々の公開対象について名前、種別、入力、出力、詳細を調べる必要がある場合に作る。使用手順を教える tutorial ではなく、現在の公開 surface を確認する reference とする。
        """
        title @= "API Reference を作る場合"

    class SECTION_002:
        r"""
        API entry ごとに node を作り、表示名は `name` field へ置く。cross-reference される API node を持つ document では `@canonical_source(..., heading="identity")` を使用し、class identity に API 名の表記を同期させる必要がない場合は `API_NNN` のような opaque stable identity を使える。package や機能領域が大きい場合は document collection へ分ける。
        """
        title @= "API subject を node にする"

    class SECTION_003:
        r"""
        `shikumi_devdoc.fields.api_reference` は `name`、`kind`、`input`、`output`、`detail`、`related` と、`NAMESPACE` / `TYPE` / `VALUE` / `OPERATION` / `OTHER` を提供する。

        ```python
        {{api_example}}
        ```

        入出力を文章だけに埋め込むより、一覧や差分で扱う価値がある場合に field として分離する。説明上の背景や例は prose に残してよい。
        """
        title @= "標準 field set を使う"

        api_example @= r'''
        from shikumi_devdoc.fields.api_reference import OPERATION, input, kind, name, output

        class API_001:
            """Process one request and return its result."""

            name @= "run"
            kind @= OPERATION
            input @= "request: Request"
            output @= "RunResult"
        '''
        related @= (FIELDS_API.fields.api_reference,)

    class SECTION_004:
        r"""
        API の導入、非推奨、削除、置換、移行を現在の対象から追える必要がある場合は `shikumi_devdoc.fields.lifecycle` の `introduced`、`deprecated`、`removed`、`replacement`、`migration` を同じ node に付ける。

        CHANGELOG は release-centered、lifecycle field は subject-centered であり、同じ変更事実が両方に現れても役割は異なる。
        """
        title @= "Lifecycle を対象のそばに置く"
