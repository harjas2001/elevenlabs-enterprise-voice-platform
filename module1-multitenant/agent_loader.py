import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

#Resolve to the brand config in config/brands/
BRANDS_DIR = Path(__file__).parent / "config" / "brands"

# Maps brand_id → env var prefix and yaml filename
BRAND_REGISTRY = {
    "maya": {
        "yaml":       "maya.yaml",
        "env_prefix": "MAYA",
    },
    "aria": {
        "yaml":       "aria.yaml",
        "env_prefix": "ARIA",
    },
    "nova": {
        "yaml":       "nova.yaml",
        "env_prefix": "NOVA",
    },
}


def load_brand_config(brand_id: str) -> dict:
    """
    Load and return config for the given brand_id.
    Env vars take precedence over YAML values for agent_id and voice_id.

    Raises:
        ValueError: if brand_id is not in BRAND_REGISTRY
        FileNotFoundError: if the brand's YAML file is missing
    """
    brand_id = brand_id.lower().strip()

    if brand_id not in BRAND_REGISTRY:
        raise ValueError(
            f"[agent_loader] Unknown brand: '{brand_id}'. "
            f"Valid options: {list(BRAND_REGISTRY.keys())}"
        )

    registry_entry = BRAND_REGISTRY[brand_id]
    yaml_path = BRANDS_DIR / registry_entry["yaml"]

    if not yaml_path.exists():
        raise FileNotFoundError(
            f"[agent_loader] Config file not found: {yaml_path}\n"
            f"  Expected at: {yaml_path.resolve()}"
        )

    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Env vars win over YAML placeholders
    prefix = registry_entry["env_prefix"]
    config["agent_id"] = os.getenv(f"{prefix}_AGENT_ID") or config.get("agent_id")
    config["voice_id"] = os.getenv(f"{prefix}_VOICE_ID") or config.get("voice_id")

    # Always stamp the brand_id onto the config so callers don't have to track it
    config["brand_id"] = brand_id

    return config


def list_brands() -> list[str]:
    """Return all registered brand IDs."""
    return list(BRAND_REGISTRY.keys()) 