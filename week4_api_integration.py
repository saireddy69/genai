import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("API_URL")

print("Loaded URL:", url)

response = requests.get(url)
print(response.json()[0])
