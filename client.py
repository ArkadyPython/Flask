import requests

response = requests.post("http://127.0.0.1:5000/advertisement",
                         json={
                            "title": "Programming on Django and Flask",
                            "description": "7 years of work experience",
                            "owner": "GameDew"
                         })
print(response.status_code)
print(response.text)

response = requests.delete("http://127.0.0.1:5000/advertisement/7")
print(response.status_code)
print(response.text)

response = requests.get("http://127.0.0.1:5000/advertisement/7")
print(response.status_code)
print(response.text)