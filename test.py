import requests

query = "AI agents"

url = f"https://www.reddit.com/search.json?q={query}"

headers = {
    "User-Agent": "research-assistant"
}

response = requests.get(url, headers=headers)

data = response.json()

for post in data["data"]["children"]:

    post = post["data"]

    print(post["title"])