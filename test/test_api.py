import requests
import json

response = requests.get('http://localhost:8000/api/categories/')
data = response.json()
print("API响应数据:")
print(json.dumps(data, ensure_ascii=False, indent=2))