import streamlit as st

# Set page configuration
st.set_page_config(page_title="YouTube Comments Summarizer", layout="wide")

# Sidebar navigation
navigation = st.sidebar.radio(
    "Navigation",
    ["Home", "Video Stats"]  # Add more pages as needed
)

# Home page
if navigation == "Home":
    st.markdown("## Home Page")
    import streamlit as st
    from comments import fetch_comments
    from utils import get_summary

    # Set page configuration
    #st.set_page_config(page_title="YouTube Comments Summarizer", layout="wide")

    # Custom CSS styles
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #0E1117;
            color: #FAFAFA;
        }

        .container {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .content {
            max-width: 800px;
            width: 100%;
            padding: 20px;
            background-color: #262730;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .form-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }

        .input-field {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #FAFAFA;
            border-radius: 5px;
            font-size: 16px;
            background-color: #0E1117;
            color: #FAFAFA;
        }

        .submit-button {
            background-color: #FF4B4B;
            color: #FAFAFA;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }

        .submit-button:hover {
            background-color: #FF6B6B;
        }

        .summary-container {
            background-color: #262730;
            color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Page content
    st.title("YouTube Comments Summarizer")
    st.write(
        "Looking to quickly understand what viewers are saying about your video? This tool is for you!"
    )
    st.markdown(
        """
        This tool summarizes comments from any YouTube video using Google's Gemini API.
        To get your own API key, visit [Google Gemini API](https://ai.google.dev/gemini-api).
        """
    )

    # Form container
    with st.container():
        form = st.form("template_form", clear_on_submit=True)
        url_input = form.text_input(
            "Enter YouTube video URL",
            placeholder="https://www.youtube.com/watch?v=example_video_id",
            key="url_input",
        )
        user_gemini_api_key = form.text_input(
            "Enter your Gemini API key (leave blank to use the default key)",
            placeholder="Your Gemini API key",
            type="password",
            key="gemini_api_key",
        )
        submit = form.form_submit_button("Get Summary")

        # Use the provided Gemini API key, or default to the key from the environment
        gemini_api_key = user_gemini_api_key if user_gemini_api_key else st.secrets['GEMINI_API_KEY']

        if submit and url_input:
            with st.spinner("Fetching Summary..."):
                # Get Comments from YouTube API - INPUT
                text = fetch_comments(url_input)
                # Tokenization and Summarization - MAIN CODE
                final_summary = get_summary(text, gemini_api_key)
                # Display the output on Streamlit - OUTPUT
                with st.container():
                    st.markdown(f"<div class='summary-container'>{final_summary}</div>", unsafe_allow_html=True)

# Video Stats page
elif navigation == "Video Stats":
    st.markdown("## Video Statistics")
    import streamlit as st
    from googleapiclient.discovery import build
    from PIL import Image

    # Custom CSS styles
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #0E1117;
            color: #FAFAFA;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        img {
            max-width: 80px;
            max-height: 80px;
            border-radius: 50%;
            margin-right: 20px;
        }

        .channel-title {
            font-size: 32px;
            font-weight: 700;
        }

        .stat-container {
            display: flex;
            justify-content: space-around;
            width: 100%;
            max-width: 800px;
            margin-bottom: 20px;
        }

        .stat-card {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .stat-value {
            font-size: 24px;
            font-weight: 700;
        }

        .stat-label {
            font-size: 16px;
        }

        .submit-button {
            background-color: #FF4B4B;
            color: #FAFAFA;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
            margin-top: 20px;
        }

        .submit-button:hover {
            background-color: #FF6B6B;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # YouTube API key (replace with your API key)
    api_key = st.secrets["YOUTUBE_API_KEY"]

    # Function to fetch channel details
    def fetch_channel_details(channel_id):
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        return response["items"][0]

    # Function to format subscriber count
    def format_subscriber_count(count):
        if count >= 1000000:
            return f"{int(count / 1000000):.1f}M"
        elif count >= 1000:
            return f"{int(count / 1000):.1f}K"
        else:
            return str(count)

    # Streamlit app
    st.title("YouTube Channel Analytics")

    # Get channel ID from user input
    channel_id = st.text_input("Enter your channel ID")

    # Button to fetch channel statistics
    if st.button("Get Analytics", key="get_analytics_button"):
        if channel_id:
            channel_details = fetch_channel_details(channel_id)
            channel_stats = channel_details["statistics"]

            with st.container():
                st.header("Channel Overview")
                col1, col2, col3 = st.columns(3)

                with col1:
                    channel_logo_url = channel_details["snippet"]["thumbnails"]["default"]["url"]
                    st.image(channel_logo_url, use_column_width=True, caption="Channel Logo")

                with col2:
                    st.subheader("Channel Title")
                    st.write(channel_details["snippet"]["title"])

                with col3:
                    st.subheader("Channel Description")
                    st.write(channel_details["snippet"]["description"])

            with st.container():
                st.header("Channel Statistics")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Subscribers")
                    subscriber_count = format_subscriber_count(int(channel_stats["subscriberCount"]))
                    st.markdown(f"<p class='stat-value'>{subscriber_count}</p>", unsafe_allow_html=True)
                    st.markdown("<p class='stat-label'>Total Subscribers</p>", unsafe_allow_html=True)

                with col2:
                    st.subheader("Video Views")
                    view_count = format_subscriber_count(int(channel_stats["viewCount"]))
                    st.markdown(f"<p class='stat-value'>{view_count}</p>", unsafe_allow_html=True)
                    st.markdown("<p class='stat-label'>Total Video Views</p>", unsafe_allow_html=True)

                with col3:
                    st.subheader("Video Count")
                    video_count = channel_stats["videoCount"]
                    st.markdown(f"<p class='stat-value'>{video_count}</p>", unsafe_allow_html=True)
                    st.markdown("<p class='stat-label'>Total Uploaded Videos</p>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a YouTube channel ID.")

