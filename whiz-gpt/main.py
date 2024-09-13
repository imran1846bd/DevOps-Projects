import time
import os
import boto3
import streamlit as st

from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
os.environ["AWS_ACCESS_KEY_ID"] = "AKIA5YXX3EF2MBJHY5WT"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your aws key"
os.environ["AWS_REGION"] = "us-east-1"
st.set_page_config(layout="wide")

hide_streamlit_style = """
<style>
div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}
div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}
div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}
#MainMenu {
    visibility: hidden;
    height: 0%;
}
header {
    visibility: hidden;
    height: 0%;
}
footer {
    visibility: hidden;
    height: 0%;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
.reportview-container {
    margin-top: -2em;
}
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
#stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("WhizGPT")

# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)
@st.cache_resource
def load_llm():
    llm = Bedrock(client=bedrock_runtime, model_id="anthropic.claude-v2")
    llm.model_kwargs = {"temperature": 0.7, "max_tokens_to_sample": 2048}
    model = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
    return model

model = load_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message WhizGPT"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # prompt = prompt_fixer(prompt)
        result = model.predict(input=prompt)

        # Simulate stream of response with milliseconds delay
        for chunk in result.split(' '):  # fix for https://github.com/streamlit/streamlit/issues/868
            full_response += chunk + ' '
            if chunk.endswith('\n'):
                full_response += ' '
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "?")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
