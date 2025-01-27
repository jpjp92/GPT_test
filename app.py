# ### python -m streamlit run app.py

import gradio as gr
from g4f.client import Client

# GPT-4o-mini 클라이언트 초기화
client = Client()

# 채팅 함수 정의
def chat_with_gpt(user_input, chat_history):
    try:
        # GPT-4o-mini 모델에게 메시지 전달 및 응답 생성
        messages = [{"role": "system", "content": "You are a helpful assistant"}]
        for history in chat_history:
            messages.append({"role": "user", "content": history[0]})
            messages.append({"role": "assistant", "content": history[1]})
        messages.append({"role": "user", "content": user_input})

        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        final_response = response.choices[0].message.content

        # 채팅 기록 업데이트
        chat_history.append((user_input, final_response))
        return final_response, chat_history
    except Exception as e:
        return f"Error: {str(e)}", chat_history

# Gradio 인터페이스 정의
with gr.Blocks() as demo:
    gr.Markdown("# GPT-4o-mini Chat 🤖")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="GPT에게 질문하기", placeholder="메시지를 입력하세요...")
    clear = gr.Button("대화 초기화")

    # 이벤트 핸들러
    state = gr.State([])
    msg.submit(chat_with_gpt, [msg, state], [chatbot, state])
    clear.click(lambda: ([], []), None, [chatbot, state])

# 앱 실행
if __name__ == "__main__":
    demo.launch()





# import streamlit as st
# from g4f.client import Client

# # GPT-4o-mini 클라이언트 초기화
# client = Client()

# # 페이지 설정: 제목, 아이콘, 레이아웃 설정
# st.set_page_config(
#     page_title="GPT-4o Chat",
#     page_icon="📝",
#     layout="centered"
# )

# # 세션 상태 초기화: 채팅 기록 저장
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 앱 제목 표시
# st.title("GPT-4o-mini Chat 🤖")

# # 채팅 메시지 UI 출력
# for message in st.session_state.chat_history:
#     with st.chat_message(message['role']):
#         # 사용자 또는 GPT의 메시지를 구분해 출력
#         st.markdown(message['content'])

# # 사용자 입력 창
# user_prompt = st.chat_input("GPT-4o-mini에게 질문해보세요!")

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
