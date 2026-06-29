from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
TOOLGATE_MASTER_KEY = os.getenv("TOOLGATE_MASTER_KEY", "")
