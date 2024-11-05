import os

from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")
LOCATOR_TIMEOUT = int(os.getenv("LOCATOR_TIMEOUT"))