
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "assistant", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは文章校正専門のAIです。"},
            {"role": "user", "content": "条件に沿って知人との会話で送るメッセージを校正してください。1.相手を不快にさせないこと。2.長ったらしい,堅苦しい文章にしないこと。3.メッセージの本来の意味(伝えたいこと)を損なわないこと。4.誤字脱字は補完すること。"}
        ]
    )

    bot_message = response["choices"][0]["message"]
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
