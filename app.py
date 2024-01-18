
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

select_prompt = st.sidebar.selectbox('どのプロンプトを利用しますか？', ['友人向けメッセージ', 'ビジネスメール', '論文'])

# st.session_stateを使いメッセージのやりとりを保存    
if select_prompt == '友人向けメッセージ':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正アシスタントAIです。"},
        {"role": "user", "content": "友人に向けたメッセージを書きます。『誤字・脱字を訂正する』『親しく,砕けた口調にする』『要点は繰り返して強調する』という3つの条件に従って校正してください。"},
        ]
elif select_prompt == 'ビジネスメール':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正アシスタントAIです。"},
        {"role": "user", "content": "職場の上司に向けたメールを書きます。『正しく丁寧な文体にする』『誤字・脱字を訂正する』『要件を明確に,簡潔に伝える内容にする』という3つの条件に従って校正してください。結果は3通り出力してください。"},
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
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
