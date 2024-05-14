import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)
openai_client.organization = "org-mTUrTQANr2hY7R44zvFAPKfE"
#openai_response = openai_client.chat.completions.create(model= "gpt-4o",messages=[{"role": "user", "content": "hello"}])
print(openai_client.models.list())