import importlib
import pkgutil
from typing import Any

class PluginManager:
    def __init__(self) -> None:
        self.plugins: dict[str, Any] = {}
        self.discover_plugins()

    def discover_plugins(self) -> None:
        import omega.plugins as plugins_package

        for finder, name, ispkg in pkgutil.iter_modules(plugins_package.__path__):
            module = importlib.import_module(f"omega.plugins.{name}")
            candidate = getattr(module, f"{name.capitalize()}Plugin", None)
            if candidate:
                self.plugins[name] = candidate()

    def get(self, plugin_name: str) -> Any:
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> list[str]:
        return sorted(self.plugins.keys())