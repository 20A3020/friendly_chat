import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

pro = st.sidebar.selectbox('誰に向けて校正しますか？', ['友人', '目上の人', '論文など','選択してください'], index=3)
ans = st.sidebar.slider('校正結果の出力数を決めてください', 1, 3, 1)
num = st.sidebar.slider('出力される校正結果の揺らぎを設定してください。(小さいほど回答が固定されます)', 0.0, 1.0, 0.7)

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    if pro == '友人':
        st.session_state["messages"] = [
          {"role": "system", "content": "あなたは優秀な文章校正アシスタントAIです。"},
          {"role": "user", "content": "友人へ宛てたメッセージを校正してください。尚、『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』という3つの条件を遵守してください。"},
          {"role": "user", "content": "校正結果は" + str(ans) + "個出力してください。"},
          ]
        selectbox(disabled=True)
    elif pro == '目上の人':
        st.session_state["messages"] = [
          {"role": "system", "content": "あなたは優秀な文章校正アシスタントAIです。"},
          {"role": "user", "content": "目上の人間へ宛てたメッセージを校正してください。尚、『礼節を弁えた,簡潔な文章にする』『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』という4つの条件を遵守してください。"},
          {"role": "user", "content": "校正結果は" + str(ans) + "個出力してください。"},
          ]
    elif pro == '論文など':
        st.session_state["messages"] = [
          {"role": "system", "content": "あなたは優秀な文章校正アシスタントAIです。"},
          {"role": "user", "content": "論文を校正してください。尚、『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』『表現・表記方法の統一』『だ・である調の文体にする』『整合性の取れない点を指摘する』『論文として適した文でない点を指摘する』という7つの条件を遵守してください。"},
          {"role": "user", "content": "校正結果は" + str(ans) + "個出力してください。"},
          ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature = num
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("文章校正アシスタント")
st.write("「その文章、誤って誰かを傷つけない？」「隠れたミス、見逃してない？」チェックしてみようよ！")

user_input = st.text_input("", placeholder = "ここに文章を入力してね", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👦あなたのテキスト"
        if message["role"]=="assistant":
            speaker="🤖校正されたテキスト"

        st.write(speaker + ": " + message["content"])
