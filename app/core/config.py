import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CANDIDATE_SERVICE_URL=os.getenv("CANDIDATE_SERVICE_URL")
