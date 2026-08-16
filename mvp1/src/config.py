"""Config loading for MVP 1.

Every product threshold (adherence targets, the pharmacist-agreement
graduation gate, KPI thresholds) lives in config.yaml, not hardcoded in
dashboard code — see Sections 4.3 and 7 of the product proposal.
"""

from pathlib import Path

import yaml

MVP1_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = MVP1_DIR / "config.yaml"


def load_config(config_path=None):
    """Load config.yaml. Returns a plain dict."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_data_path(config, key):
    """Resolve a data.* path in config.yaml relative to config.yaml's own
    directory (mvp1/), regardless of which module or cwd is calling."""
    raw = config["data"][key]
    return (MVP1_DIR / raw).resolve()
