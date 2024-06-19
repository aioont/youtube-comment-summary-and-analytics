import streamlit as st
from googleapiclient.discovery import build
from pytube import extract
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys and other constants from Streamlit secrets
api_service_name = st.secrets["API_SERVICE_NAME"]
api_version = st.secrets['API_VERSION']
youtube_api_key = st.secrets['YOUTUBE_API_KEY']

def start_youtube_service():
    """
    Initializes the YouTube service using the API key.

    Returns:
        googleapiclient.discovery.Resource: The YouTube service object.
    """
    return build(api_service_name, api_version, developerKey=youtube_api_key)

def extract_video_id_from_link(url):
    """
    Extracts the video ID from a YouTube URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The extracted video ID.
    """
    return extract.video_id(url)

def get_comments_thread(youtube, video_id, next_page_token=''):
    """
    Retrieves a thread of comments for a specific YouTube video.

    Args:
        youtube (googleapiclient.discovery.Resource): The YouTube service object.
        video_id (str): The ID of the YouTube video.
        next_page_token (str): Token for the next page of results (for pagination).

    Returns:
        dict: The API response containing comments.
    """
    results = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        textFormat='plainText',
        maxResults=100,
        pageToken=next_page_token
    ).execute()
    return results

def load_comments_in_format(comments):
    """
    Formats the retrieved comments into a single string.

    Args:
        comments (dict): The API response containing comments.

    Returns:
        str: All comments concatenated into a single string.
    """
    all_comments_string = ""
    for thread in comments["items"]:
        # Get top-level comment
        comment_content = thread['snippet']['topLevelComment']['snippet']['textOriginal']
        all_comments_string += comment_content + "\n"
        
        # Get replies to the top-level comment, if any
        if 'replies' in thread:
            for reply in thread['replies']['comments']:
                reply_text = reply['snippet']['textOriginal']
                all_comments_string += reply_text + "\n"
    
    return all_comments_string

def fetch_comments(url):
    """
    Fetches comments from a YouTube video URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: All comments from the video concatenated into a single string.
    """
    youtube = start_youtube_service()
    video_id = extract_video_id_from_link(url)
    next_page_token = ''
    all_comments_string = ""
    
    # Retrieve comments from the first page
    data = get_comments_thread(youtube, video_id, next_page_token)
    all_comments_string += load_comments_in_format(data)
    
    # Paginate through remaining comments
    while "nextPageToken" in data:
        next_page_token = data["nextPageToken"]
        data = get_comments_thread(youtube, video_id, next_page_token)
        all_comments_string += load_comments_in_format(data)

    return all_comments_string
