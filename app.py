import os
import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Model setup
model_id = "mistralai/Mistral-7B-Instruct-v0.3"

def load_model(model_id=model_id, max_new_tokens=128, temperature=0.1):
    return HuggingFaceEndpoint(
        repo_id=model_id,
        task="text-generation",
        token=os.getenv("HF_TOKEN"),
        temperature=temperature,
        max_new_tokens=max_new_tokens
    )

# 🧠 Chatbot logic
def generate_response(system_prompt, chat_log, user_input):
    model = load_model(max_new_tokens=st.session_state.max_length)

    history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in chat_log])

    prompt = PromptTemplate.from_template(
        "[INST] {system_prompt}\n\n{history}\nUser: {user_input} [/INST]"
    )

    chain = prompt | model | StrOutputParser()

    response = chain.invoke({
        "system_prompt": system_prompt,
        "user_input": user_input,
        "history": history_text
    })

    chat_log.append({"role": "user", "content": user_input})
    chat_log.append({"role": "assistant", "content": response})
    return response, chat_log

# 🌐 Streamlit setup
st.set_page_config(page_title="AI Chatbot 💬", page_icon="✨")
st.title("🤖 Intelligent Chat Assistant")
st.write("Welcome! Ask me anything and I’ll try to help 🤗")

# Sidebar: customizations
with st.sidebar:
    st.header("Settings ⚙️")

    st.session_state.system_prompt = st.text_area(
        "AI Instructions", value="You're a friendly and helpful assistant."
    )

    st.session_state.max_length = st.slider("Max Response Length", 50, 500, 150)

    reset = st.button("Reset Chat")

# Session state setup
if "chat_log" not in st.session_state or reset:
    st.session_state.chat_log = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

# Chat interface
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.spinner("Thinking..."):
        response, st.session_state.chat_log = generate_response(
            st.session_state.system_prompt,
            st.session_state.chat_log,
            user_input
        )
    st.rerun()

# Display chat history
for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
