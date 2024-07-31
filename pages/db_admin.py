# app.py
import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import requests
from utils.db_manager import DatabaseManager

db_manager = DatabaseManager()

st.title("FINI Data Entry")


def image_url_to_base64(image_url):
    """Convert image URL to base64 string."""
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# Add a user
st.header("Add User")
username = st.text_input("Username")
profile_img_url = st.text_input("Profile Image URL")
if st.button("Add User"):
    if profile_img_url:
        profile_image_base64 = image_url_to_base64(profile_img_url)
        db_manager.add_user(username, profile_image_base64)
        st.success(f"User {username} added!")
    else:
        st.error("Please provide a profile image URL.")

# Add a post
st.header("Add Post")
users = db_manager.conn.execute("SELECT id, username FROM users").fetchall()
user_options = {username: user_id for user_id, username in users}
selected_user = st.selectbox("Select User", options=list(user_options.keys()))
post_image_url = st.text_input("Post Image URL", key="post_image_url")
caption = st.text_area("Caption")
if st.button("Add Post"):
    if post_image_url:
        post_image_base64 = image_url_to_base64(post_image_url)
        user_id = user_options[selected_user]
        db_manager.add_post(user_id, post_image_base64, caption)
        st.success("Post added!")
    else:
        st.error("Please provide a post image URL.")

# Add a like
st.header("Add Like")
posts = db_manager.conn.execute("SELECT id FROM posts").fetchall()
post_options = [post_id for post_id, in posts]
selected_post = st.selectbox("Select Post ID", options=post_options)
users = db_manager.conn.execute("SELECT id, username FROM users").fetchall()
user_options = {username: user_id for user_id, username in users}
selected_user = st.selectbox(
    "Select User", options=list(user_options.keys()), key="like_user"
)
if st.button("Add Like"):
    user_id = user_options[selected_user]
    db_manager.add_like(selected_post, user_id)
    st.success("Like added!")

# Add a comment
st.header("Add Comment")
posts = db_manager.conn.execute("SELECT id FROM posts").fetchall()
post_options = [post_id for post_id, in posts]
selected_post = st.selectbox("Select Post ID", options=post_options, key="comment_post")
users = db_manager.conn.execute("SELECT id, username FROM users").fetchall()
user_options = {username: user_id for user_id, username in users}
selected_user = st.selectbox(
    "Select User", options=list(user_options.keys()), key="comment_user"
)
comment = st.text_area("Comment")
if st.button("Add Comment"):
    user_id = user_options[selected_user]
    db_manager.add_comment(selected_post, user_id, comment)
    st.success("Comment added!")

db_manager.close()
