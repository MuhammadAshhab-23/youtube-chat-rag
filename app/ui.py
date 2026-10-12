
import streamlit as st
from dotenv import load_dotenv

from app.transcript import fetch_transcript
from app.rag_pipeline import create_rag_chain

load_dotenv()

st.set_page_config(
    page_title="YouTube Chat RAG",
    page_icon="🎥"
)

st.title("🎥 YouTube Chat RAG")
st.write("Paste a YouTube URL and ask questions about its content.")

url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Load Video"):
    if not url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript and building RAG pipeline..."):
            try:
                transcript = fetch_transcript(url)
                st.session_state.rag_chain = create_rag_chain(transcript)
                st.session_state.messages = []
                st.session_state.video_loaded = True
                st.success("Video loaded! You can now ask questions.")
            except Exception as error:
                st.error(f"Could not load video: {error}")

if st.session_state.get("video_loaded", False):

    if st.button("🛑 End Chat"):
        st.session_state.video_loaded = False
        st.session_state.messages = []
        st.session_state.rag_chain = None
        st.rerun()

    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask a question about the video...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = st.session_state.rag_chain.invoke(question)
                    st.write(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as error:
                    st.error(f"Error generating answer: {error}")