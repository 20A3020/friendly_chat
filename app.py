
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["massages"]
    
    user_message = {"role": "assistant", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは文章生成,校正専門のAIです。"},
            {"role": "user", "content": "入力された下書き文章から『伝えたい内容』を読み取って、その続きを書いてください。"}
        ]
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("あなたの書きたい事、正しく書けてますか？")
st.write("ChatGPTが煩雑な文章構築を助けてくれますよ！")

user_input = st.text_input("文章を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👦あなたのテキスト"
        if message["role"]=="assistant":
            speaker="🤖AIが出力したテキスト"

        st.write(speaker + ": " + message["content"])
