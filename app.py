# ### python -m streamlit run app.py

import streamlit as st
import time
import uuid
from supabase import create_client
import os
import pandas as pd

# Supabase 클라이언트 초기화
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# GPT-4o-mini 클라이언트 초기화
from g4f.client import Client
client = Client()

# 페이지 설정
st.set_page_config(
    page_title="Chat with AI",
    page_icon="📝",
    layout="wide"  # 레이아웃을 좌우로 확장
)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_nickname" not in st.session_state:
    st.session_state.user_nickname = ""

# Supabase 유저 ID 가져오기/생성
def get_or_create_user(nickname):
    user = supabase.table("users").select("*").eq("nickname", nickname).execute()
    if user.data:
        return user.data[0]["id"]
    else:
        new_user = supabase.table("users").insert({"nickname": nickname}).execute()
        return new_user.data[0]["id"]

# 채팅 기록 저장
def save_chat_history(user_id, session_id, question, answer, time_taken):
    supabase.table("chat_history").insert({
        "user_id": user_id,
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "time_taken": time_taken
    }).execute()

# 세션 ID 생성
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 닉네임 입력 및 설정
with st.sidebar:
    st.title("기본 설정")
    st.session_state.user_nickname = st.text_input(
        "닉네임 설정", placeholder="예: AI Lover", key="nickname_input"
    )
    if st.session_state.user_nickname:
        st.write(f"닉네임: {st.session_state.user_nickname}")

# 유저 ID 가져오기
if st.session_state.user_nickname:
    user_id = get_or_create_user(st.session_state.user_nickname)
else:
    st.warning("닉네임을 먼저 설정하세요.")
    st.stop()

# 페이지 UI
col1, col2 = st.columns([3, 1])

with col1:
    # 앱 제목
    st.title("Chat with AI 🤖")

    # 채팅 메시지 UI 출력
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # 사용자 입력
    user_prompt = st.chat_input("AI에게 질문해보세요!")

    if user_prompt:
        # 사용자 메시지를 UI와 세션에 추가
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # GPT 모델 처리
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                *st.session_state.chat_history
            ]
        )
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        # GPT 응답 가져오기
        final_response = response.choices[0].message.content

        # 응답을 UI와 세션에 추가
        st.session_state.chat_history.append({"role": "assistant", "content": final_response})
        with st.chat_message("assistant"):
            st.markdown(final_response)

        # 채팅 기록 저장
        save_chat_history(user_id, st.session_state.session_id, user_prompt, final_response, time_taken)

        # 응답 시간 표시
        st.info(f"⏱️ 응답 시간: {time_taken}초")

with col2:
    # 대화 기록 다운로드
    st.subheader("대화 기록")
    if st.session_state.chat_history:
        if st.button("기록 다운로드"):
            df = pd.DataFrame(st.session_state.chat_history)
            st.download_button(
                label="Download chat history",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="chat_history.csv",
                mime="text/csv"
            )


# import streamlit as st
# from g4f.client import Client

# # GPT-4o-mini 클라이언트 초기화
# client = Client()

# # 페이지 설정: 제목, 아이콘, 레이아웃 설정
# st.set_page_config(
#     page_title="Chat with AI",
#     page_icon="📝",
#     layout="centered"
# )

# # 세션 상태 초기화: 채팅 기록 저장
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 앱 제목 표시
# st.title("Chat with AI 🤖")

# # 채팅 메시지 UI 출력
# for message in st.session_state.chat_history:
#     with st.chat_message(message['role']):
#         # 사용자 또는 GPT의 메시지를 구분해 출력
#         st.markdown(message['content'])

# # 사용자 입력 창
# user_prompt = st.chat_input("AI에게 질문해보세요!")

# if user_prompt:
#     # 사용자의 입력 메시지를 UI에 표시하고 세션 상태에 저장
#     st.chat_message("user").markdown(user_prompt)
#     st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#     # GPT-4o-mini 모델에게 메시지 전달 및 응답 생성
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant"},  # 시스템 프롬프트
#             *st.session_state.chat_history  # 이전 대화 내용 포함
#         ]
#     )
    
#     # GPT 응답 가져오기
#     final_response = response.choices[0].message.content

#     # GPT 응답을 UI에 표시하고 세션 상태에 저장
#     st.session_state.chat_history.append({"role": "assistant", "content": final_response})
#     with st.chat_message("assistant"):
#         st.markdown(final_response)
