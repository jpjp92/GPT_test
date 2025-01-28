### python -m streamlit run app.py

import streamlit as st
from g4f.client import Client

# GPT-4o-mini 클라이언트 초기화
client = Client()

# 페이지 설정: 제목, 아이콘, 레이아웃 설정
st.set_page_config(
    page_title="Chat with AI",
    page_icon="📝",
    layout="centered"
)

# 세션 상태 초기화: 채팅 기록 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 앱 제목 표시
st.title("Chat with AI 🤖")

# 채팅 메시지 UI 출력
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        # 사용자 또는 GPT의 메시지를 구분해 출력
        st.markdown(message['content'])

# 사용자 입력 창
user_prompt = st.chat_input("AI에게 질문해보세요!")

if user_prompt:
    # 사용자의 입력 메시지를 UI에 표시하고 세션 상태에 저장
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # GPT-4o-mini 모델에게 메시지 전달 및 응답 생성
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},  # 시스템 프롬프트
            *st.session_state.chat_history  # 이전 대화 내용 포함
        ]
    )
    
    # GPT 응답 가져오기
    final_response = response.choices[0].message.content

    # GPT 응답을 UI에 표시하고 세션 상태에 저장
    st.session_state.chat_history.append({"role": "assistant", "content": final_response})
    with st.chat_message("assistant"):
        st.markdown(final_response)
