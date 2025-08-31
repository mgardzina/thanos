import yaml
import logging
import sys

log = logging.getLogger("thanos.config")

def load_cfg(env: str = "testnet") -> dict:
    """Load config file based on environment (testnet/mainnet)."""
    filename = f"config.{env}.yaml"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        log.error("Config file %s not found!", filename)
        sys.exit(1)
    except Exception as e:
        log.error("Failed to load config %s: %s", filename, e)
        sys.exit(1)
