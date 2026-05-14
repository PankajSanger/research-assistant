from fastmcp import FastMCP
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

# Create MCP server
mcp = FastMCP(name="Multiply MCP Server")

@mcp.tool
def multiply(a: float, b: float) -> float:
    """multiply two numbers."""
    return a * b

@mcp.tool
def youtube(query: str, max_results: int):
    """
    Call this tool to extract youtube data for the given query/topic and max result outputs.
    """
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results
                )
    response = request.execute()
    # Store results
    videos = []

    for item in response["items"]:
        video_data = {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"]
        }

        videos.append(video_data)

    return videos

@mcp.tool
def reddit(query:str):
    """Fetch reddit posts for the given query/keyword."""

    url = f"https://www.reddit.com/search.json?q={query}"

    headers = {
        "User-Agent": "research-assistant"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    post_title = []
    for post in data["data"]["children"]:
        post = post["data"]
        post_title.append(post["title"])

    return post_title


@mcp.tool
def semanticscholar(query:str, max_results:int):

    """This research scholar tool searches data for given query/keyword and for given max result output."""

    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,citationCount,url"
    }

    response = requests.get(url, params=params)

    data = response.json()

    scholar_list = []
    for paper in data["data"]:

        scholar_data = {
        "TITLE": paper["title"],
        "YEAR": paper.get("year"),
        "CITATIONS": paper.get("citationCount"),
        "URL": paper.get("url")}

        scholar_list.append(scholar_data)

    return scholar_list

if __name__ == "__main__":
    mcp.run(transport="stdio")