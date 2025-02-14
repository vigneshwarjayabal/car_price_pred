import streamlit as st
import streamlit.components.v1 as components  # Import Streamlit's HTML rendering component
from nlp import chatbot_response

def main():
    st.title("🚗 CarWise Recommendation Chatbot")
    st.markdown("<p style='font-size:16px; color: #555;'>Welcome! Ask me anything about finding the perfect used car.</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "filters" not in st.session_state:
        st.session_state.filters = {}

    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        response, updated_filters = chatbot_response(user_input, st.session_state.filters)
        st.session_state.filters = updated_filters  
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"🧑‍💻 **You:** {msg['content']}", unsafe_allow_html=True)
        else:
            # Use components.html to render full HTML properly
            components.html(msg["content"], height=400, scrolling=True)  # ✅ Fix: Ensures proper HTML rendering

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.filters = {}
        st.rerun()

if __name__ == "__main__":
    main()
