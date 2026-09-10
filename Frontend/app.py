import streamlit as st
from api_client import query_rag_backend

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI & Computer Science Learning Assistant")
st.caption("Ask questions about your uploaded documents and get grounded answers with source citations.")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources & Citations"):
                for src in message["sources"]:
                    st.write(f"- {src}")

# Accept user input
if prompt := st.chat_input("Ask a question (e.g., What is machine learning?)..."):
    # Render user prompt immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render assistant response with loading indicator
    with st.chat_message("assistant"):
        with st.spinner("Searching vector store and generating response..."):
            try:
                # Query backend API
                data = query_rag_backend(prompt)
                answer = data.get("answer", "No answer received.")
                sources = data.get("sources", [])

                # Render content
                st.markdown(answer)
                if sources:
                    with st.expander("📚 Sources & Citations"):
                        for src in sources:
                            st.write(f"- {src}")

                # Save assistant response to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                error_msg = f"⚠️ Failed to reach the assistant API. Ensure backend is running. Error: {str(e)}"
                st.error(error_msg)