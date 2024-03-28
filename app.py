import os
from PIL import Image
from utils import utils
import streamlit as st
from dotenv import load_dotenv; load_dotenv()
from lyzr import VoiceBot, ChatBot

# Setup your config
st.set_page_config(
    page_title="Social Media Advisor",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Social Media Advisor by Lyzr")
st.markdown("### Welcome to the Social Media Advisor!")
st.markdown("Social Media Advisor by Lyzr will turns your articles into ready-to-post content for LinkedIn, Instagram, Twitter, and Facebook!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Social Media Advisor Application
data = 'data'
audio_directory = 'audio'
os.makedirs(data, exist_ok=True)
os.makedirs(audio_directory, exist_ok=True)
original_directory = os.getcwd()

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 
def qabot_agent():
    path = utils.get_files_in_directory(data)
    qa_agent = ChatBot.docx_chat(
        input_files=path
    )

    return qa_agent


def voicebot_agent(add_summary):
    vb = VoiceBot(api_key=API_KEY)
    try:
        os.chdir(audio_directory)
        vb.text_to_speech(add_summary)
    finally:
        os.chdir(original_directory)



if __name__ == "__main__":
    style_app() 
    article = st.file_uploader('Upload your article documet',type=["docx"])
    if article:
        utils.save_uploaded_file(directory=data, uploaded_file=article)
        file = utils.file_checker()
        if len(file)>0:
            if st.button('Create'):
                agent = qabot_agent()
                response = utils.social_media(agent=agent)
                results = utils.prompts(agent=agent)
                if response:
                    utils.get_response(response=response)
                    if results:
                        voicebot_agent(add_summary=results['Voice_Ad'])
                        st.subheader('Voice Advertisment')
                        files = utils.get_files_in_directory(audio_directory)
                        audio_file = files[0]
                        st.audio(audio_file)  
                        st.markdown('---')
                        st.subheader('Instagram')
                        insta_image = utils.instagram_img(results['Instagram_post'])
                        st.image(insta_image, caption='Instagram Image', use_column_width=True)

    else:
        utils.remove_existing_files(data)
        st.warning('Please Upload article document file')
    
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Agent's to create the social media advisor, it uses's ChatBot for RAG, and VoiceBot for audio file, and OpenAI dall-e-3 for image generation. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)