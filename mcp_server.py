from fastmcp import FastMCP
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pandas as pd

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

    # Convert to DataFrame
    df = pd.DataFrame(videos)

    return df

if __name__ == "__main__":
    mcp.run(transport="stdio")