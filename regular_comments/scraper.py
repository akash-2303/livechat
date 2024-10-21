import json
from googleapiclient.discovery import build

# Replace with your own YouTube Data API key
api_key = "AIzaSyCe5Qb0rBKXW7JUA_VpgiH0QZgWx5N5roA"

# Replace with the YouTube video ID (The part after 'v=' in the video URL)
video_id = "CxL99SsrofM"

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

def get_comments(video_id):
    comments = []
    # Call the API to get the comments
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,  # You can adjust the number of results here
        textFormat="plainText"
    )
    
    while request:
        response = request.execute()

        # Parse the response and extract comments
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comment_info = {
                "author": snippet['authorDisplayName'],
                "authorProfileImageUrl": snippet.get('authorProfileImageUrl', ''),
                "authorChannelUrl": snippet.get('authorChannelUrl', ''),
                "text": snippet['textDisplay'],
                "likeCount": snippet['likeCount'],
                "publishedAt": snippet['publishedAt'],
                "updatedAt": snippet.get('updatedAt', ''),
                "canRate": snippet.get('canRate', True),
                "viewerRating": snippet.get('viewerRating', 'none'),
                "isPublic": snippet.get('isPublic', True)
            }
            comments.append(comment_info)
        
        # Check if there's a next page of comments
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
        else:
            break
    
    return comments
# Fetch the comments for the given video ID
comments = get_comments(video_id)

# Save the comments in a structured JSON format
with open('associatedPress_comments.json', 'w') as f:
    json.dump(comments, f, indent=4)

print("Comments saved to associatedPress_comments.json")
