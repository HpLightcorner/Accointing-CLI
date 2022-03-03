import cattrs


class Unset:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return ""


UNSET: Unset = Unset()
cattrs.register_unstructure_hook(Unset, lambda _: "")
