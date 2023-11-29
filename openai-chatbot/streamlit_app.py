# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

# import openai
from openai import OpenAI
import streamlit as st

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    #openai.api_key="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"
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
    )
    st.success('Proceed to entering your prompt message!', icon='👉')
    # if 'OPENAI_API_KEY' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     openai.api_key = st.secrets['OPENAI_API_KEY']
    # else:
    #     openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    #     if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')
svg_file_path_user = 'images/avatar.svg'
svg_file_path_assistant = 'images/crownlogo.svg'


# Read the contents of the SVG file into a string
with open(svg_file_path_user, 'r') as file:
    svg_user = file.read()
with open(svg_file_path_assistant, 'r') as file:
    svg_assistant = file.read()

# Initialize messages in session state with the initial assistant 
default_prompt= "You are a sassy drag queen named Queen Judy. You give advice about a variety of topics, dating, life, work- anything! Every answer you provide needs to be in the tone of a funny, sassy drag queen using drag queen slang. You provide relationship advice, fashion advice, career advice, self-care advice and general life advice."
if "messages" not in st.session_state:
    
    st.session_state.messages = [
        {"role": "assistant", "content":default_prompt, "avatar":"💬"}
    ]    

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# Display previous messages excluding the initial assistant prompt
for message in st.session_state.messages:
    if message["role"] != "assistant" or default_prompt not in message["content"]:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])


# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])



if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt,"avatar":svg_user})
    with st.chat_message("user",  avatar=svg_user):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=svg_assistant):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            # full_response += response.choices[0].delta.get("content", "")
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response,"avatar":svg_assistant})



# from openai import OpenAI

# client = OpenAI()

# stream = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for part in stream:
#     print(part.choices[0].delta.content or "")
   

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
