import requests
import json
import streamlit as st
from datetime import datetime, timedelta
from urllib.parse import urlparse
import time

def fetch_posts(subreddit, after=None):
    try:
        if after is None:
            url = f"https://www.reddit.com/r/{subreddit}.json"
        else:
            url = f"https://www.reddit.com/r/{subreddit}.json?after={after}"
        params = {"after": after} if after else None
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params=params)
        if response.status_code == 200:
            data = response.json()
            posts = data["data"]["children"]
            after = data["data"]["after"]
            return posts, after
        else:
            return None, None
    except Exception as e:
        print(e)
        return e, None

def format_time(timestamp):
    current_time = datetime.utcnow()
    post_time = datetime.utcfromtimestamp(timestamp)
    time_diff = current_time - post_time
    if time_diff < timedelta(minutes=1):
        return "just now"
    elif time_diff < timedelta(hours=1):
        return f"{int(time_diff.total_seconds() / 60)} minutes ago"
    elif time_diff < timedelta(days=1):
        return f"{int(time_diff.total_seconds() / 3600)} hours ago"
    else:
        return post_time.strftime("%Y-%m-%d %H:%M:%S")

def main():
    st.set_page_config(page_title="Reddit App", page_icon="✍️", layout="centered")
    # Streamlit app code
    st.title("My Reddit App")
    st.markdown("---")
    with open('./css/styles.css', "r") as f:
        style = f.read()
        st.markdown(f'''
<head>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.15/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Righteous&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Dosis:wght@200&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans&family=Righteous&display=swap" rel="stylesheet">
        <!-- Font Awesome CDN -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=El+Messiri&display=swap" rel="stylesheet">
        <style>
            {style}
        </style>
</head>''',
    unsafe_allow_html=True)

    subreddit_list = [
        "all", "popular", "news", "worldnews", "politics", "science", "technology",
        "gaming", "funny", "AskReddit", "memes", "mildlyinteresting", "aww", "pics",
        "gifs", "youtube", "movies", "books", "music", "food", "lifeprotips",
        "wholesomememes", "unpopularopinion", "showerthoughts", "dataisbeautiful",
        "explainlikeim5", "todayilearned", "nosleep", "creepy", "askscience",
        "programming", "webdev", "design", "art", "photoshopbattles", "Documentaries",
        "History", "AskHistorians", "Space", "Futurology", "CozyPlaces", "EarthPorn",
        "CityPorn", "Architecture", "malefashionadvice", "femalefashionadvice",
        "makeupaddiction", "SkincareAddiction", "MechanicalKeyboards", "PCMasterRace"
    ]

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3670/3670005.png", width=120,)
    subreddit = st.sidebar.selectbox("Select a subreddit", subreddit_list, index=0)
    custom_subreddit = st.sidebar.text_input("Or enter a subreddit name", "")

    if custom_subreddit:
        subreddit = custom_subreddit

    after = None  # Initialize 'after' parameter as None
    posts = None  # Initialize 'posts' as None
    posts, after = fetch_posts(subreddit, after)  # Pass 'after' parameter to fetch new posts

    if posts is not None:
        for post in posts:
            post_data = post["data"]
            post_id = post_data["id"]
            post_title = post_data["title"]
            post_author = post_data["author"]
            post_created_utc = post_data["created_utc"]
            post_url = post_data["url"]
            post_num_comments = post_data["num_comments"]
            post_ups = post_data["ups"]
            post_downs = post_data["downs"]
            post_score = post_data["score"]
            post_subreddit = post_data["subreddit"]
            self_text = post_data.get("selftext")
            post_hint = post_data.get("post_hint")
            url_overridden_by_dest = post_data.get("url_overridden_by_dest")
            post_content = ""

            if post_hint == "image":
                # Display image
                post_content = f'<a href="{url_overridden_by_dest}" target="_blank"><img src="{url_overridden_by_dest}" alt="image"></a>'
            elif post_hint == "rich:video":
                if post_url.startswith("https://www.youtu.be/"):
                    # Display YouTube video
                    post_content = st.video(post_url)
                else:
                    # Display embedded video or link
                    post_content = st.video(post_url)
            elif self_text:
                # Display self text
                post_content = self_text
            elif post_url:
                # Display link
                post_content = f'<a href="{post_url}" target="_blank">{post_url}</a>'

            post_header = st.empty()
            post_header.markdown(f'''
                            <div class="reddit-container rounded-xl p-4 mb-4">
                                <div class="reddit-post-header">
                                    <div class="reddit-post-title">
                                        <i class="fa fa-newspaper-o"></i>{post_title}
                                    </div>
                                </div>
                                <div class="reddit-post-author">
                                    <i class="fas fa-user"></i> Posted by: u/{post_author}
                                </div>
                                <div class="reddit-post-time">
                                    <i class="fas fa-clock"></i> Time: {format_time(post_created_utc)}
                                </div>
                                <div class="reddit-post-text">
                                    {post_content}
                                </div>
                                <div class="reddit-post-score-comments mb-2">
                                    <i class="fa fa-plus-square" aria-hidden="true"></i> Score: {post_score} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-arrow-up" aria-hidden="true"></i> Ups: {post_ups} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-arrow-down" aria-hidden="true"></i> Downs: {post_downs} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-comments" aria-hidden="true"></i> Comments: {post_num_comments}
                                </div>
                                <div class="reddit-post-subreddit">
                                    <i class="fas fa-reddit"></i> Subreddit: {post_subreddit}
                                </div>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )


        if st.sidebar.button("Load More", key="load_more"):
                time.sleep(2)  # Delay for better UI experience
                additional_posts, after = fetch_posts(subreddit, after)
                if additional_posts is not None:
                    posts.extend(additional_posts)
                    for post in additional_posts:
                        post_data = post["data"]
                        post_id = post_data["id"]
                        post_title = post_data["title"]
                        post_author = post_data["author"]
                        post_created_utc = post_data["created_utc"]
                        post_url = post_data["url"]
                        post_num_comments = post_data["num_comments"]
                        post_ups = post_data["ups"]
                        post_downs = post_data["downs"]
                        post_score = post_data["score"]
                        post_subreddit = post_data["subreddit"]
                        self_text = post_data.get("selftext")
                        post_hint = post_data.get("post_hint")
                        url_overridden_by_dest = post_data.get("url_overridden_by_dest")
                        post_content = ""

                        if post_hint == "image":
                            # Display image
                            post_content = f'<a href="{url_overridden_by_dest}" target="_blank"><img src="{url_overridden_by_dest}" alt="image"></a>'
                        elif post_hint == "rich:video":
                            if post_url.startswith("https://www.youtu.be/"):
                                # Display YouTube video
                                post_content = st.video(post_url)
                            else:
                                # Display embedded video or link
                                post_content = st.video(post_url)
                        elif self_text:
                            # Display self text
                            post_content = self_text
                        elif post_url:
                            # Display link
                            post_content = f'<a href="{post_url}" target="_blank">{post_url}</a>'

                        post_header = st.empty()
                        post_header.markdown(f'''
                            <div class="reddit-container rounded-xl p-4 mb-4">
                                <div class="reddit-post-header">
                                    <div class="reddit-post-title">
                                        <i class="fa fa-newspaper-o"></i>{post_title}
                                    </div>
                                </div>
                                <div class="reddit-post-author">
                                    <i class="fas fa-user"></i> Posted by: u/{post_author}
                                </div>
                                <div class="reddit-post-time">
                                    <i class="fas fa-clock"></i> Time: {format_time(post_created_utc)}
                                </div>
                                <div class="reddit-post-text">
                                    {post_content}
                                </div>
                                <div class="reddit-post-score-comments mb-2">
                                    <i class="fa fa-plus-square" aria-hidden="true"></i> Score: {post_score} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-arrow-up" aria-hidden="true"></i> Ups: {post_ups} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-arrow-down" aria-hidden="true"></i> Downs: {post_downs} &nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-comments" aria-hidden="true"></i> Comments: {post_num_comments}
                                </div>
                                <div class="reddit-post-subreddit">
                                    <i class="fas fa-reddit"></i> Subreddit: {post_subreddit}
                                </div>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )

        if after:
                st.sidebar.markdown(f"*After value: {after}*")  # Display 'after' value for debugging purposes
        else:
            st.error("Error: Failed to fetch posts from the subreddit. Please try again later.")
        st.sidebar.markdown("---")
        st.sidebar.markdown("**About**")
        st.sidebar.info(
            "This app allows you to browse posts from different subreddits. "
            "Select a subreddit from the dropdown menu or enter a custom subreddit name. "
            "You can also load more posts by clicking the 'Load More' button at the bottom."
        )
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Note**")
        st.sidebar.info(
            "This app fetches data from the Reddit API. "
            "It may take some time to load posts, especially if a large number of posts are requested."
        )
if __name__ == "__main__":
    main()
