import os
from dotenv import load_dotenv

# load env variables
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Go two levels up
dotenv_path = os.path.join(base_dir, 'resources', '.env')
load_dotenv(dotenv_path=dotenv_path)
openai_api_key = os.getenv('OPENAI_API_KEY')

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


