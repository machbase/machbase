import requests
params = {"q":"select * from example", "format":"csv", "heading":"false"} 
response = requests.get("http://127.0.0.1:5654/db/query", params)
print(response.text)
