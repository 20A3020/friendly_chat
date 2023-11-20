import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.OpenAIAPI.openai_api_key)

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは文章校正専門のAIです。"},
        {"role": "user", "content": "次に入力される文章に対して、『誤字,脱字の訂正』『適切な改行,読点,句読点の挿入』『主張を要約した1文を追加』の3項目を行ってください。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)

    bot_message = response["messages"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("校正はお任せ！")
st.write("ChatGPT APIを使ってあなたの卒論を校正します。")

user_input = st.text_input("校正したい文章を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👦あなたのテキスト"
        if message["role"]=="assistant":
            speaker="🤖校正されたテキスト"

        st.write(speaker + ": " + message["content"])
