# Env Variable modules
from dotenv import load_dotenv
import os

# Default LLM
from llama_index.llms.openai import OpenAI

# Load Env variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set LLM
LLM_4o = OpenAI(model="gpt-4o")

# Transcript Handling Variables
BASE_URL_TEMPLATE = "https://app.circleback.ai/api/meeting/view/{meeting_id}/transcript"
TRANSCRIPT_FILE_PATH = "meetings"

