import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import base64
from utils.db_manager import DatabaseManager

# Initialize the database manager
db_manager = DatabaseManager()


def image_to_base64(image_path):
    """Convert image to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def create_post_card(
    profile_img, username, post_img, likes, user, comments, post_time, post_id
):
    st.markdown(
        f"""
        <div style="border:1px solid #ddd; padding:16px; margin:16px 0; border-radius:8px; background-color:#fff;">
            <div style="display:flex; align-items:center;">
                <img src="data:image/jpeg;base64,{profile_img}" alt="profile pic" style="width:40px; height:40px; border-radius:50%;">
                <div style="margin-left:8px;">
                    <h3 style="margin:0;">{username}</h3>
                </div>
            </div>
            <img src="data:image/jpeg;base64,{post_img}" alt="post" style="width:100%; margin:16px 0;">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <a href="#" onclick="likePost({post_id}); return false;">
                        <svg aria-label="Like" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                            <path d="M34.6 6.1c5.7 0 10.4 5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path>
                        </svg>
                    </a>
                    <a href="#" onclick="showComments({post_id}); return false;">
                        <svg aria-label="Comment" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                            <path clip-rule="evenodd" d="M47.5 46.1l-2.8-11c1.8-3.3 2.8-7.1 2.8-11.1C47.5 11 37 .5 24 .5S.5 11 .5 24 11 47.5 24 47.5c4 0 7.8-1 11.1-2.8l11 2.8c.8.2 1.6-.6 1.4-1.4zm-3-22.1c0 4-1 7-2.6 10-.2.4-.3.9-.2 1.4l2.1 8.4-8.3-2.1c-.5-.1-1-.1-1.4.2-1.8 1-5.2 2.6-10 2.6-11.4 0-20.6-9.2-20.6-20.5S12.7 3.5 24 3.5 44.5 12.7 44.5 24z" fill-rule="evenodd"></path>
                        </svg>
                    </a>
                    <a href="#" onclick="sharePost({post_id}); return false;">
                        <svg aria-label="Share Post" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                            <path d="M47.8 3.8c-.3-.5-.8-.8-1.3-.8h-45C.9 3.1.3 3.5.1 4S0 5.2.4 5.7l15.9 15.6 5.5 22.6c.1.6.6 1 1.2 1.1h.2c.5 0 1-.3 1.3-.7l23.2-39c.4-.4.4-1 .1-1.5zM5.2 6.1h35.5L18 18.7 5.2 6.1zm18.7 33.6l-4.4-18.4L42.4 8.6 23.9 39.7z"></path>
                        </svg>
                    </a>
                </div>
                <div>
                    <a href="#" onclick="savePost({post_id}); return false;">
                        <svg aria-label="Save" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                            <path d="M43.5 48c-.4 0-.8-.2-1.1-.4L24 29 5.6 47.6c-.4.4-1.1.6-1.6.3-.6-.2-1-.8-1-1.4v-45C3 .7 3.7 0 4.5 0h39c.8 0 1.5.7 1.5 1.5v45c0 .6-.4 1.2-.9 1.4-.2.1-.4.1-.6.1zM24 26c.8 0 1.6.3 2.2.9l15.8 16V3H6v39.9l15.8-16c.6-.6 1.4-.9 2.2-.9z"></path>
                        </svg>
                    </a>
                </div>
            </div>
            <p><b>{user}</b> {comments}</p>
            <p><a href="#" onclick="toggleComments({post_id}); return false;">View all comments</a></p>
            <p><small>{post_time}</small></p>
        </div>
        <script>
            function likePost(postId) {{
                console.log("Like post:", postId);
                // Add your like functionality here
            }}
            function showComments(postId) {{
                console.log("Show comments for post:", postId);
                // Add your show comments functionality here
            }}
            function sharePost(postId) {{
                console.log("Share post:", postId);
                // Add your share functionality here
            }}
            function savePost(postId) {{
                console.log("Save post:", postId);
                // Add your save functionality here
            }}
            function toggleComments(postId) {{
                console.log("Toggle comments for post:", postId);
                // Add your toggle comments functionality here
            }}
        </script>
        """,
        unsafe_allow_html=True,
    )


def test(img):
    st.markdown(
        f"""

    <img src="{img}" alt="profile pic" style="width:40px; height:40px; border-radius:50%;">

    """
    )


def load_data():
    conn = sqlite3.connect("finConnect.db")
    c = conn.cursor()
    c.execute(
        "SELECT posts.id, users.profile_img, users.username, posts.image_data, posts.caption, posts.post_time FROM posts JOIN users ON posts.user_id = users.id"
    )
    posts = c.fetchall()
    c.execute("SELECT * FROM likes")
    likes = c.fetchall()
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()
    return posts, likes, comments


def count_likes(post_id, likes):
    return sum(1 for like in likes if like[1] == post_id)


def get_comments(post_id, comments):
    return [comment for comment in comments if comment[1] == post_id]


def display_posts(posts, likes, comments):
    for post in posts:
        post_id, profile_img, username, post_img, caption, post_time = post
        like_count = count_likes(post_id, likes)
        post_comments = get_comments(post_id, comments)
        comment_texts = " | ".join(
            [f"{comment[3]} ({comment[4]})" for comment in post_comments]
        )
        # Decode base64 images if they are in base64 format
        # if not profile_img.startswith("data:image/jpeg;base64,"):
        #     profile_img = f" data:image/jpeg;charset=utf-8;base64,{profile_img}"
        # if not post_img.startswith("data:image/jpeg;base64,"):
        #     post_img = f"data:image/jpeg;charset=utf-8;base64,,{post_img}"
        # test(profile_img)
        create_post_card(
            profile_img,
            username,
            post_img,
            like_count,
            username,
            comment_texts,
            post_time,
            post_id,
        )


# Streamlit app
st.title("FinConnect")

# Load and display posts
posts, likes, comments = load_data()
display_posts(posts, likes, comments)
