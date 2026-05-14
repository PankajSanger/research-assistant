
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)
request = youtube.search().list(
            q="lion",
            part="snippet",
            type="video",
            maxResults=3
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

