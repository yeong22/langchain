# 필요한 라이브러리 임포트
import streamlit as st
from langchain_openai import ChatOpenAI
import streamlit as st

# Streamlit UI 설정
st.set_page_config(page_title="ChatOpenAI Demo", page_icon=":robot:")
st.header("ChatOpenAI Demo")


# 사이드바에 OpenAI API 키 입력 필드 생성
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


#  세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 대화 히스토리 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # API 키가 입력되지 않았을 경우 경고 메시지 표시
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    # OpenAI 클라이언트 초기화
    chat = ChatOpenAI(api_key=openai_api_key)

# 사용자 입력 처리
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in chat.stream(st.session_state.messages):
            full_response += (response.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 스크롤을 최하단으로 이동
st.empty()
