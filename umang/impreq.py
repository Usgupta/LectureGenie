import requests

url = 'https://api.pawan.krd/v1/completions'

headers = {
    'Authorization': 'Bearer pk-KRnpVmvJKalEqmFseSighmlOoMyIohZiIHwFRqjNIXeylZXR',
    'Content-Type': 'application/json'
}

data = {
    "model": "text-davinci-003",
    "prompt": "Human: Hello\nAI:",
    "temperature": 0.7,
    "max_tokens": 256,
    "stop": [
        "Human:",
        "AI:"
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.json())
