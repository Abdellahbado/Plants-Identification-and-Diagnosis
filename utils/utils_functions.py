from googleapiclient.discovery import build
import streamlit as st
from utils.llm_handler_identification import get_response_from_llm


def get_common_name(scientific_name):

    prompt = f"What is the common name of the plant with the scientific name (give me only the common name): {scientific_name}?"
    response = get_response_from_llm(prompt)
    common_name = response.split("is")[-1].strip()
    print("response", common_name)

    return common_name


# this function gets the common name of a plant, create a query based on an action and searches youtube
def search_videos_plant(plant_name, action):
    common_name = get_common_name(plant_name)
    common_name = common_name.replace("the ", "")
    search_query = action + " " + common_name
    print("search query", search_query)
    video_urls = search_youtube_videos(search_query)
    if video_urls:
        st.session_state.video_url = video_urls[0]




def search_youtube_videos(query, max_results=1):
    youtube = build(
        "youtube", "v3", developerKey="AIzaSyD2D1IyTpBJvXgUGGB7632mzBc9oE-fU5Q"
    )
    search_response = (
        youtube.search()
        .list(q=query, type="video", part="id,snippet", maxResults=max_results)
        .execute()
    )

    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            )

    return videos


def reset_chat():
    st.session_state.conversation = []
    st.session_state.plant = None
    if "llm_chain" in st.session_state:
        del st.session_state.llm_chain
