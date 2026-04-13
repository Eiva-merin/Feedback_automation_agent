import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_videos(query, max_results=10):
    """Search YouTube videos by keyword."""
    youtube = get_youtube_client()
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="relevance"
    )
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "description": item["snippet"]["description"]
        })
    
    print(f"Found {len(videos)} videos for query: {query}")
    return videos

def get_video_comments(video_id, max_results=50):
    """Get top comments from a YouTube video."""
    youtube = get_youtube_client()
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance"
        )
        response = request.execute()
        
        comments = []
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id": video_id,
                "comment": comment["textDisplay"],
                "likes": comment["likeCount"],
                "published_at": comment["publishedAt"]
            })
        
        return comments
    
    except Exception as e:
        print(f"Comments disabled for video {video_id}: {e}")
        return []

def collect_feedback(search_queries, max_videos=5, max_comments=30):
    """Collect comments from multiple search queries."""
    all_comments = []
    all_videos = []
    
    for query in search_queries:
        print(f"\nSearching for: {query}")
        videos = search_videos(query, max_results=max_videos)
        all_videos.extend(videos)
        
        for video in videos:
            print(f"Fetching comments for: {video['title'][:50]}...")
            comments = get_video_comments(video["video_id"], max_results=max_comments)
            
            # Add video title to each comment for context
            for comment in comments:
                comment["video_title"] = video["title"]
                comment["channel"] = video["channel"]
            
            all_comments.extend(comments)
    
    print(f"\nTotal comments collected: {len(all_comments)}")
    return all_videos, all_comments

if __name__ == "__main__":
    queries = [
        "SensitHaptics sim racing review",
        "sim racing haptics hardware review",
        "direct drive haptics sim racing 2024"
    ]
    videos, comments = collect_feedback(queries, max_videos=3, max_comments=20)
    print(f"\nVideos found: {len(videos)}")
    print(f"Comments collected: {len(comments)}")
    print("\nSample comment:", comments[0]["comment"][:100] if comments else "None")