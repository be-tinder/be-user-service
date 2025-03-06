import functools


class DependencyContainer:
    """A simple container that stores named singletons or instances."""
    _dependencies = {}

    @classmethod
    def register(cls, name: str, instance):
        cls._dependencies[name] = instance

    @classmethod
    def resolve(cls, name: str):
        if name not in cls._dependencies:
            raise ValueError(f"Dependency '{name}' not found in container")
        return cls._dependencies[name]


def autowired(*dependencies):
    """Decorator to auto-inject named dependencies from DependencyContainer."""

    def wrapper(cls):
        original_init = cls.__init__

        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            for dep_name in dependencies:
                setattr(self, dep_name, DependencyContainer.resolve(dep_name))
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    return wrapper
