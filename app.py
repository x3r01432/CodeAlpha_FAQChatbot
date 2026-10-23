import streamlit as st
from chatbot import FAQChatbot

st.set_page_config(page_title="CodeAlpha FAQ Chatbot", page_icon="💬")
st.title("💬 CodeAlpha FAQ Chatbot")
st.caption("Ask anything about the CodeAlpha internship.")

@st.cache_resource
def load_bot():
    return FAQChatbot()

bot = load_bot()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me a question about the CodeAlpha internship."}]
with st.sidebar:
    show = st.checkbox("Show matched FAQ and score")
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
    with st.expander("All FAQs"):
        for f in bot.faqs:
            st.markdown(f"- {f['question']}")
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])
if q := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": q})
    st.chat_message("user").write(q)
    ans, matched, score = bot.match(q)
    if show and matched:
        ans += f"\n\n_Matched: \"{matched}\" (score {score:.2f})_"
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
