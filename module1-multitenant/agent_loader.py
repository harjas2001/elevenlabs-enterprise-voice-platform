import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#Resolve to the brand config in config/brands/
BRANDS_DIR = Path(__file__).parent / "config" / "brands"