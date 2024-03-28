import os
import shutil
import streamlit as st
from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI


API_KEY = os.getenv('OPENAI_API_KEY')

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(directory, uploaded_file):
    remove_existing_files(directory=directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    st.success("File uploaded successfully")

def file_checker():
    file = []
    for filename in os.listdir('data'):
        file_path = os.path.join('data', filename)
        file.append(file_path)

    return file


def social_media(agent):
    content = {}
    prompts = {'LinkedIn': """
                        Craft an engaging LinkedIn post based on this article. 
                        Share a concise yet compelling overview of article's key points to capture the audience's attention. 
                        Remember to include relevant hashtags and a call-to-action to encourage further engagement and drive traffic to your article. Let's create an impactful post that resonates with your LinkedIn network!
            """,

            "Twitter":"""
                        Craft a captivating tweet inspired by the essence of this article. 
                        Condense the key insights into 1-2 punchy lines that grab attention and leave readers intrigued. 
                        Ensure the tweet is concise yet impactful, and don't forget to add relevant hashtags to expand your reach. Let's compose a tweet that sparks curiosity and drives engagement!

            """,


            "Facebook":"""
                        Compose an engaging Facebook post that encapsulates the essence of this article. 
                        Share a brief summary that highlights the most compelling aspects, aiming to captivate your audience's interest. 
                        Consider adding an eye-catching image or video to enhance the post's appeal, and encourage interaction by asking a thought-provoking question or inviting comments. Let's craft a post that resonates with your Facebook followers and sparks meaningful conversations!

            """}

    for platfrom, prompt in prompts.items():
        response = agent.chat(prompt)
        content[platfrom] = response.response

    return content  

def prompts(agent):
    results = {}
    prompt = {'Voice_Ad':'create a article summary for advertisment in 150-200 words',
               'Instagram_post':'create a article summary for instagram post in 10-20 words.' }  

    for platfrom, prompt in prompt.items():        
        response = agent.chat(prompt)
        results[platfrom] = response.response

    return results


def get_response(response:dict):
    for platfrom, response in response.items():
        st.subheader(platfrom)
        st.write(response)
        st.markdown("---")  

def instagram_img(prompt):
    client = OpenAI(api_key=API_KEY)
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    return image_url