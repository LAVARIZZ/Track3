import streamlit as st

# Function to create a post card
def create_post(profile_img, username, location, post_img, likes, user, comments, post_time):
    st.write(f"""
    <div style="border:1px solid #ddd; padding:16px; margin:16px 0; border-radius:8px; background-color:#fff;">
        <div style="display:flex; align-items:center;">
            <img src="{profile_img}" alt="profile pic" style="width:40px; height:40px; border-radius:50%;">
            <div style="margin-left:8px;">
                <h3 style="margin:0;">{username}</h3>
                <span>{location}</span>
            </div>
            <div style="margin-left:auto;">
                <i class="fas fa-ellipsis-h"></i>
            </div>
        </div>
        <img src="{post_img}" alt="post" style="width:100%; margin:16px 0;">
        <div style="display:flex; justify-content:space-between;">
            <div>
                <!-- Upvote and Downvote Buttons -->
                <button style="background:none; border:none; cursor:pointer;">
                    <svg aria-label="Thumbs up" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                        <path d="M24 8.3l-8.6 8.6c-.3.3-.5.7-.5 1.1v14.6c0 .4.2.8.5 1.1l8.6 8.6c.3.3.7.5 1.1.5s.8-.2 1.1-.5l8.6-8.6c.3-.3.5-.7.5-1.1V18c0-.4-.2-.8-.5-1.1L25.1 8.3c-.3-.3-.7-.5-1.1-.5s-.8.2-1.1.5z"></path>
                    </svg>
                </button>
                <button style="background:none; border:none; cursor:pointer;">
                    <svg aria-label="Thumbs down" color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                        <path d="M24 39.7l8.6-8.6c.3-.3.5-.7.5-1.1V15.4c0-.4-.2-.8-.5-1.1L24 5.7c-.3-.3-.7-.5-1.1-.5s-.8.2-1.1.5L13.2 15c-.3.3-.5.7-.5 1.1v14.6c0 .4.2.8.5 1.1l8.6 8.6c.3.3.7.5 1.1.5s.8-.2 1.1-.5z"></path>
                    </svg>
                </button>
            </div>
            <div>
                <svg aria-label="Save" class="_8-yf5 " color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                    <path d="M43.5 48c-.4 0-.8-.2-1.1-.4L24 29 5.6 47.6c-.4.4-1.1.6-1.6.3-.6-.2-1-.8-1-1.4v-45C3 .7 3.7 0 4.5 0h39c.8 0 1.5.7 1.5 1.5v45c0 .6-.4 1.2-.9 1.4-.2.1-.4.1-.6.1zM24 26c.8 0 1.6.3 2.2.9l15.8 16V3H6v39.9l15.8-16c.6-.6 1.4-.9 2.2-.9z"></path>
                </svg>
            </div>
        </div>
        <p><b>{user}</b> {comments}</p>
        <p><a href="#">View discussions</a></p>
        <p><small>{post_time}</small></p>
    </div>
    """, unsafe_allow_html=True)

# Main function to render the Instagram clone
def main():
    # Inject CSS for custom background color
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f5;  /* Light background color */
        }
        .sidebar .sidebar-content {
            background-color: #efe0e0;  /* Secondary light background color for sidebar */
        }
        h3, span, p, small {
            color: #262730;  /* Text color */
        }
        .css-18e3th9 {
            color: #262730;
            background-color: #b52f2f;
        }
        .css-1d391kg {
            color: #262730;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Portfolio Recommendations")

    # Create sample posts
    create_post(
        profile_img="https://media.geeksforgeeks.org/wp-content/uploads/20220609093229/g-200x200.png",
        username="Ayush Agarwal",
        location="Mumbai, India",
        post_img="https://media.geeksforgeeks.org/wp-content/uploads/20220609090112/gfg1-298x300.jpeg",
        likes=203,
        user="Raju Modi",
        comments="Great post!",
        post_time="2 hours ago"
    )

    create_post(
        profile_img="https://media.geeksforgeeks.org/wp-content/uploads/20220609093229/g-200x200.png",
        username="Keshav Agarwal",
        location="Kolkata, India",
        post_img="https://media.geeksforgeeks.org/wp-content/uploads/20220609090130/gfg3-299x300.jpeg",
        likes=184,
        user="Mayank",
        comments="Nature #love #2021",
        post_time="9 hours ago"
    )

    st.sidebar.title("Suggestions For You")

    suggestions = [
        {"profile_img": "https://media.geeksforgeeks.org/wp-content/uploads/20220609093221/g2-200x200.jpg", "username": "Aditya Verma", "status": "Low Risks Profile"},
        {"profile_img": "https://media.geeksforgeeks.org/wp-content/uploads/20220609093229/g-200x200.png", "username": "Sundar Pichai", "status": "High Returns"},
        {"profile_img": "https://media.geeksforgeeks.org/wp-content/uploads/20220609093221/g2-200x200.jpg", "username": "Elon Musk", "status": "Beginner Friendly"}
    ]

    for suggestion in suggestions:
        st.sidebar.write(f"""
        <div style="display:flex; align-items:center; margin-bottom:16px;">
            <img src="{suggestion['profile_img']}" alt="profile pic" style="width:40px; height:40px; border-radius:50%; margin-right:8px;">
            <div>
                <h4 style="margin:0;">{suggestion['username']}</h4>
                <span>{suggestion['status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
