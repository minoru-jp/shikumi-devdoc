from shikumi_devdoc.norms.document import canonical, title


@canonical
@title("Structure")
class TITLE_1:
    r"""A fenced example is allowed:

    ```markdown
    ## Example only
    ```

    ## Hidden semantic heading
    """

    @title("Level 2")
    class TITLE_2:
        """"""

        @title("Level 3")
        class TITLE_3:
            """"""

            @title("Level 4")
            class TITLE_4:
                """"""

                @title("Level 5")
                class TITLE_5:
                    """"""

                    @title("Level 6")
                    class TITLE_6:
                        """"""

                        @title("Level 7")
                        class TITLE_7:
                            """"""
