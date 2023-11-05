# pip install youtube-transcript-api

import streamlit as st
import langchain_yt_loader as lch
import textwrap

st.title("Ask question to Youtube video")
st.write("Copy the URL of a YouTube video and paste it to the box at left. Then ask a question against the transcript.")
# st.write("https://www.youtube.com/watch?v=-QH8fRhqFHM")
with st.sidebar:
    with st.form(key="yt_form"):
        youtube_url = st.sidebar.text_area("Enter YouTube video URL", max_chars=50, 
                                           key="youtube_url", value="https://www.youtube.com/watch?v=-QH8fRhqFHM")
        query = st.sidebar.text_area("Enter question", max_chars=50, key="query", 
                                     value="Tell me about the video.", help="Ask a question against the transcript.")
        submitted = st.form_submit_button("Submit your question")

if query and youtube_url:
    db = lch.create_vector_db_from_youtube_url(youtube_url)
    docs = lch.get_response_from_query(db, query)

    st.subheader("Answer")
    st.text("#### indicates new line.")
    st.text(textwrap.fill(docs, width=80))

# video_url = "https://www.youtube.com/watch?v=-QH8fRhqFHM"
