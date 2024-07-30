import streamlit as st
from utils.plant_indentifier import identify_plant
from utils.llm_handler_identification import get_response_from_llm
import os
from PIL import Image
from dotenv import load_dotenv
import time
import io
from PIL import Image
from utils.utils_functions import reset_chat, search_youtube_videos, get_common_name, search_videos_plant

load_dotenv()



st.set_page_config(page_title="Plant Identification", layout="wide", page_icon="🌿")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "plant" not in st.session_state:
    st.session_state.plant = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "new_upload" not in st.session_state:
    st.session_state.new_upload = False
if "video_url" not in st.session_state:
    st.session_state.video_url = None

st.title("Plant Identification and Information")

uploaded_file = st.file_uploader(
    "Choose an image of a plant", type=["jpg", "jpeg", "png"]
)

col3, col1, col2 = st.columns([2, 3, 2], gap="large")

if uploaded_file is not None:
    with col2:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Compress the image
        compressed_image = io.BytesIO()
        image.save(
            compressed_image, format="JPEG", quality=85, optimize=True
        )  # You can adjust the quality as needed
        compressed_image_bytes = compressed_image.getvalue()

        if uploaded_file != st.session_state.last_uploaded_file:
            st.session_state.new_upload = True
            reset_chat()
            st.session_state.last_uploaded_file = uploaded_file

            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("Identifying plant...")
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            api_key = os.getenv("PLANTNET_API_KEY")
            plant = identify_plant(compressed_image_bytes, api_key)
            st.session_state.plant = plant["best_match"]

            if plant:
                st.success(
                    f"Identified Plant: {plant['best_match']} with {plant['score']} confidence"
                )
            else:
                st.markdown("Unable to identify the plant. Please try another image.")

            progress_bar.empty()
            status_text.empty()

    with col1:
        st.subheader("Chat")

        for role, message in st.session_state.conversation:
            if role == "Human":
                st.chat_message("human").write(message)
            else:
                st.chat_message("assistant").write(message)

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        user_input = st.text_input(
            f"Ask a follow-up question about {st.session_state.plant}r and click submit:",
            key="user_input",
            value=st.session_state.user_input,
        )
        if st.button("Submit"):
            if user_input:
                print("user_input", user_input)
                prompt = f"Regarding the plant {st.session_state.plant}: {user_input}"
                response = get_response_from_llm(prompt)
                st.session_state.conversation.append(("Human", user_input))
                st.session_state.conversation.append(("AI", response))
                st.rerun()
    with col3:
        st.subheader("Quick Actions")

        if st.session_state.plant:
            if st.button(f"General Info About {st.session_state.plant}"):
                prompt = f"Give me general information about this plant: {st.session_state.plant}"
                response = get_response_from_llm(prompt)
                search_videos_plant(st.session_state.plant, "general info")

                with st.expander("General Information"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None

            if st.button(f"How to Propagate {st.session_state.plant}"):
                prompt = f"How can I propagate this plant: {st.session_state.plant}"
                response = get_response_from_llm(prompt)

                search_videos_plant(st.session_state.plant, "propagation")

                with st.expander("Propagation Instructions"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None

            

            if st.button(f"Growing Tips for {st.session_state.plant} in a Pot"):
                prompt = f"What are some tips for growing this plant in a pot: {st.session_state.plant}"
                response = get_response_from_llm(prompt)
                search_videos_plant(st.session_state.plant, "growing tips in pot")

                with st.expander("Growing Tips in a Pot"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None

            if st.button(f"Common Pests for {st.session_state.plant}"):
                prompt = f"What are common pests that affect {st.session_state.plant} and how to deal with them?"
                response = get_response_from_llm(prompt)
                search_videos_plant(st.session_state.plant, "common pests")

                with st.expander("Common Pests"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None

            if st.button(f"Watering Schedule for {st.session_state.plant}"):
                prompt = (
                    f"What's the ideal watering schedule for {st.session_state.plant}?"
                )
                response = get_response_from_llm(prompt)
                search_videos_plant(st.session_state.plant, "watering schedule")

                with st.expander("Watering Schedule"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None

            if st.button(f"Soil Requirements for {st.session_state.plant}"):
                prompt = f"What type of soil is best for {st.session_state.plant}?"
                response = get_response_from_llm(prompt)
                search_videos_plant(st.session_state.plant, "soil requirements")

                with st.expander("Soil Requirements"):
                    st.write(response)
                    if st.session_state.video_url:
                        st.video(st.session_state.video_url)
                    st.session_state.video_url = None
