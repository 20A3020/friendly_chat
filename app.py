
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

select_prompt = st.sidebar.selectbox('誰に宛てたメッセージですか？', ['友人・知人', '先生', '上司', '論文など'])
answer_volume = st.sidebar.slider('校正結果の出力数を決めてください。', 1, 3, 1)
answer_accuracy = st.sidebar.slider('校正結果の揺らぎを設定してください。(小さいほど内容のブレが無くなります)', 0, 10, 7)

# st.session_stateを使いメッセージのやりとりを保存    
if select_prompt == '友人・知人':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正AIです。"},
        {"role": "user", "content": "友人へ宛てたメッセージを校正してください。尚、『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』という3つの条件を遵守してください。"},
        {"role": "system", "content": "また、校正結果は" + str(answer_volume) + "個出力してください。"},
        ]
elif select_prompt == '先生':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正AIです。"},
        {"role": "user", "content": "先生へ宛てたメッセージを校正してください。尚、『敬語を使う』『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』という4つの条件を遵守してください。"},
        {"role": "system", "content": "また、校正結果は" + str(answer_volume) + "個出力してください。"},
        ]
elif select_prompt == '上司':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正AIです。"},
        {"role": "user", "content": "上司へ宛てたメッセージを校正してください。尚、『礼節を弁えた,簡潔な文章にする』『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』という4つの条件を遵守してください。"},
        {"role": "system", "content": "また、校正結果は" + str(answer_volume) + "個出力してください。"},
        ]
elif select_prompt == '論文など':
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な文章校正AIです。"},
        {"role": "user", "content": "論文を校正してください。尚、『誤字・脱字の訂正』『曖昧な表現の訂正』『要点の強調』『表現・表記方法の統一』『だ・である調の文体にする』『整合性の取れない点を指摘する』『論文として適した文でない点を指摘する』という7つの条件を遵守してください。"},
        {"role": "system", "content": "また、校正結果は" + str(answer_volume) + "個出力してください。"},
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature = answer_accuracy/10
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
