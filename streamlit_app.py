import streamlit as st

# 제목과 설명 추가
st.title('Streamlit 간단한 예시')
st.write('이 예시는 사용자가 입력한 텍스트를 화면에 표시하는 간단한 앱입니다.')

# 사용자 입력
user_input = st.text_input("텍스트를 입력하세요:")

# 입력 값 출력
if user_input:
    st.write(f'입력한 텍스트: {user_input}')
