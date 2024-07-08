import streamlit as st
import google.generativeai as genai
import time

API_KEY = st.secrets["Keys"]["API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

st.title("genai chat bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting message
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I assist you today?"})

# Sidebar
st.sidebar.title("Options")
if st.sidebar.button("Clear chat"):
    st.session_state.messages = []

# Display chat messages from history on app return
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display typing indicator
    with st.chat_message("assistant"):
        typing_indicator = st.empty()
        # typing_indicator.markdown("█")
        typing_indicator.markdown("Thinking... :thinking_face:")
        


    try:
        # Generate the response
        response = chat.send_message(prompt)
        assistant_response = response.text  # Access the 'text' property directly
    except Exception as e:
        assistant_response = f"Error: {str(e)}"

    # Display Assistant response in chat container with typing effect
    typing_text = ""
    for char in assistant_response:
        typing_text += char
        typing_indicator.markdown(typing_text + "█")
        time.sleep(0.01)  # Adjust the speed of the typing effect
    typing_indicator.markdown(typing_text)

    # Add Assistant response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
