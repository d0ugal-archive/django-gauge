# following PEP 386, versiontools will pick it up
__version__ = (0, 1, 0, "final", 0)

from unipath import FSPath as Path

PROJECT_DIR = Path(__file__).absolute().ancestor(1)
WORKER_BUNDLE = PROJECT_DIR.child("worker_bundle")
