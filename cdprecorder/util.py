import inspect

class DynamicRepr:
    def __repr__(self) -> str:
        params = inspect.signature(self.__init__).parameters # type: ignore[misc]
        args = []
        for name in params:
            if not hasattr(self, name):
                continue
            args.append(f"{name}={getattr(self, name)!r}")
        args_line = ", ".join(args)

        classname = self.__class__.__name__
        return f"{classname}({args_line})"
