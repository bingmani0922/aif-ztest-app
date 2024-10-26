import os
import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# 환경 변수 설정
os.environ["OPENAI_API_KEY"] = "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"

# 메모리 객체 생성
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# CSV 파일 로드
df = pd.read_csv('aif_dummy_data2.csv')
df['enb_cell_id'] = df['eNBId'].map(str) + "_" + df['Cell'].map(str)
df['cell_fdd_id'] = df['NodeId'].map(str) + "_" + df['Cell'].map(str)
df = df[['enb_cell_id', 'ru_name', 'NodeId', 'EUtranCellFDDId', 'earfcndl', 
         'userLabel', 'tac', 'physicalLayerCellId', 'latitude', 'longitude', 
         'administrativeState', 'operationalState']]

# Streamlit UI 설정
st.title("LTE 시설 정보 ChatBot")

# 세션 상태 초기화 및 설정
if "messages" not in st.session_state:
    st.session_state.messages = []
if "enb_cell_id" not in st.session_state:
    st.session_state.enb_cell_id = None

# 초기화 버튼 기능: 세션 초기화 후 기본 상태 설정
def reset_session():
    st.session_state.clear()
    st.session_state.messages = []
    st.session_state.enb_cell_id = None  # enb_cell_id 기본값 설정

# eNBId 입력
def handle_enb_input():
    enb_cell_id = st.session_state.enb_cell_id_input
    st.session_state.enb_cell_id = enb_cell_id
    st.session_state.messages.append({"role": "system", "content": f"eNBId {enb_cell_id}가 설정되었습니다."})

# 질문 처리 함수
def handle_user_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # GPT-4로 응답 처리
        selected_id = st.session_state.enb_cell_id
        filtered_df = df[df['enb_cell_id'] == selected_id]
        if not filtered_df.empty:
            context = filtered_df.fillna("정보 없음").to_dict(orient='records')[0]

            # Prompt 생성
            prompt_template = """
            너는 LTE의 시설 정보에 대해 답변하는 ChatBot이야.
            질문에 대해 선택된 정보 안에서만 대답해 주고, 알 수 없는 정보는 대답하지 마. 

            아래는 선택된 enb_cell_id {selected_id}에 대한 정보야:
            - ru_name, Cell의 called name이야. 일종의 부르기 쉬운 별칭 같은 것: {ru_name}
            - NodeId, BTS 이름, cell이 연동된 DU Name: {NodeId}
            - EUtranCellFDDId, Cell의 시스템 이름이야: {EUtranCellFDDId}
            - EARFCN DL, Cell의 주파수 정보야: {earfcndl}
            - 사용자 라벨, 유저라벨, 운용자가 작성한 라벨: {userLabel}
            - TAC (Tracking Area Code), 택, 테이이씨 : {tac}
            - PCI: {physicalLayerCellId}
            - latitude, cell의 위도, lat : {latitude}
            - longitude, cell의 경도, lon : {longitude}
            - 행정 상태, 운용자가 Lock 해 놓은 상태인지, Unlock이면 정상 서비스 중인 상태: {administrativeState}
            - 운영 상태, Cell이 살아있는지 죽어 있는지, ENABLED이면 살아 있는 거, 즉, 동작 중인 거 : {operationalState}

            대화를 이어가며, 이전 대화 내용을 기억해 주고 이어서 답변할 수 있어.
            질문: {input_text}
            """

            prompt = prompt_template.format(
                selected_id=selected_id,
                ru_name=context.get('ru_name'),
                NodeId=context.get('NodeId'),
                EUtranCellFDDId=context.get('EUtranCellFDDId'),
                earfcndl=context.get('earfcndl'),
                userLabel=context.get('userLabel'),
                tac=context.get('tac'),
                physicalLayerCellId=context.get('physicalLayerCellId'),
                latitude=context.get('latitude'),
                longitude=context.get('longitude'),
                operationalState=context.get('operationalState'),
                administrativeState=context.get('administrativeState'),
                input_text=user_input  # 사용자 입력을 명시적으로 추가
            )

            # LLM 설정
            llm = ChatOpenAI(model='gpt-4', temperature=0)
            chain = LLMChain(
                llm=llm,
                prompt=ChatPromptTemplate.from_template(prompt),
                memory=memory
            )
            response = chain.run({"input_text": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "해당 eNBId에 대한 데이터가 없습니다."})

        # 질문 입력창 비우기
        st.session_state.user_input = ""

# eNBId 입력창 및 초기화 버튼을 같은 줄에 배치
col1, col2 = st.columns([3, 1])
with col1:
    if st.session_state.enb_cell_id is None:
        st.text_input("eNBId 입력:", key="enb_cell_id_input", on_change=handle_enb_input)
    else:
        st.write(f"조회 대상 국소는 ENB_CELL_ID {st.session_state.enb_cell_id}로 설정되었습니다.")
with col2:
    if st.button("초기화"):
        reset_session()  # 페이지 초기화

# eNBId가 설정된 이후에 대화 및 질문 처리
if st.session_state.enb_cell_id:
    # 대화 이력 출력
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div style='color: lime'>{message['content']}</div>", unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"<div style='color: gray'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: black'>{message['content']}</div>", unsafe_allow_html=True)

    # 대화 이력 밑에 두 줄 띄우기
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 질문 입력란 처리
    st.text_input("질문을 입력하세요:", key="user_input", on_change=handle_user_input)