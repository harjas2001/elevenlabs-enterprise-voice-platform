import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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