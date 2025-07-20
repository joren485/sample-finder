import importlib
import pkgutil
from pathlib import Path

for _finder, name, _ispkg in pkgutil.walk_packages([str(Path(__file__).parent)], "sample_finder.sources."):
    importlib.import_module(name)
