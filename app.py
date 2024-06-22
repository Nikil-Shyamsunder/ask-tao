import streamlit as st
import app_rag_backend

st.set_page_config(page_title="Ask Tao", page_icon='favicon.png')
st.title("Ask Tao ☯ ")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How does the Tao Te Ching reccommend approaching relationships?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # content = app_rag_backend.get_content([
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ])
        #print(st.session_state.messages[-1]['content'])
        content = app_rag_backend.get_response(st.session_state.messages[-1]['content'])
        
        #content = response.choices[0].get('delta', {}).get('content', '')
        full_response += content
        message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
