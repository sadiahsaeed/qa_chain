import streamlit as st
import streamlit_chat
import requests

# Define the API endpoint
API_URL = "https://qa-chain-542808340038.us-central1.run.app/get_query/"

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit app
def main():
    st.title("Simple QA Chatbot")

    # Display conversation history using streamlit_chat
    for msg in st.session_state.messages:
        streamlit_chat.message(msg["content"], is_user=msg["is_user"])

    # Input field for user query
    user_query = st.text_input("Enter your query:", key="user_query", on_change=handle_user_query)

# Handle user query
def handle_user_query():
    user_query = st.session_state.user_query
    if user_query:
        # Display user query in the chat
        st.session_state.messages.append({"content": user_query, "is_user": True})

        # Clear the input box after submission
        st.session_state.user_query = ""

        # Prepare the URL with the query parameter
        url = f"{API_URL}?query={user_query}"

        # Make the POST request to the API
        try:
            response = requests.post(
                url,
                headers={"accept": "application/json"},
                data=""  # Empty body as per the curl request
            )

            if response.status_code == 200:
                # Extract the "result" field from the JSON response
                response_data = response.json()
                if "result" in response_data:
                    bot_reply = response_data["result"]
                else:
                    bot_reply = "The response does not contain a 'result' field."
            else:
                bot_reply = f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            bot_reply = f"An error occurred while making the request: {e}"

        # Display bot reply in the chat
        st.session_state.messages.append({"content": bot_reply, "is_user": False})

if __name__ == "__main__":
    main()
