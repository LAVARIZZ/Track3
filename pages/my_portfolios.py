import streamlit as st  
import pandas as pd
print('p',st.session_state['portfolio'])
st.write("### Your Portfolio")

if st.session_state['portfolio']:
    print('d;')
    portfolio_df = pd.DataFrame(st.session_state['portfolio'], columns=['Ticker'])
    st.write(portfolio_df)
else:
    st.write("Your portfolio is empty.")

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()
# Streamlit app
st.title("Post on FinConnect")

# Function to make the API request
def generate_image():

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')} "
    }
    data = {    
        "model": "dall-e-3",
        "prompt": f"Create a image with white background, On left half of image write all these in bullet points (colored) {st.session_state['portfolio']}. DO NOT include any other text, image,graphic or visualization in the image.",
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Generate image on button click
if st.button("Generate Image"):
    response = generate_image()
    print(response)
    if 'data' in response:
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.error("Failed to generate image. Please check the API response.")

# Run the app
if __name__ == '__main__':
    st.write("Click the button above to generate an image.")
