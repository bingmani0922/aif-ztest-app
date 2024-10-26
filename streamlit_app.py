import os
import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
import openai

# 환경 변수 설정
# api_key = st.secret["OPENAI_API_KEY"]
# os.environ["OPENAI_API_KEY"] = "sk-Ff5UtnaNduMinWUeVMQIniOiThvc9jnnzmUp1Wsx_JT3BlbkFJqsndc9ZGaNBv7pT9CepAZfdSUhSCTqAhMK1B2nL8cA"
openai.api_key = "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"

# 제목과 설명 추가
st.title('Streamlit 간단한 예시')
st.write('이 예시는 사용자가 입력한 텍스트를 화면에 표시하는 간단한 앱입니다.')

# 사용자 입력
user_input = st.text_input("텍스트를 입력하세요:")

# 입력 값 출력
if user_input:
    st.write(f'입력한 텍스트: {user_input}')
