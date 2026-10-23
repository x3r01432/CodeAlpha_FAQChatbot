import logging
import streamlit as st
from chatbot import FAQChatbot, MAX_QUESTION_CHARS

log = logging.getLogger(__name__)
MAX_HISTORY = 50  # security review F6: cap chat history kept in the session

st.set_page_config(page_title="CodeAlpha FAQ Chatbot", page_icon="💬")
st.title("💬 CodeAlpha FAQ Chatbot")
st.caption("Ask anything about the CodeAlpha internship.")

@st.cache_resource
def load_bot():
    return FAQChatbot()

try:
    bot = load_bot()
except Exception:
    log.exception("Failed to load the chatbot")  # F1: details go to the server log only
    st.error("The chatbot couldn't start. Check the server log for details.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me a question about the CodeAlpha internship."}]
with st.sidebar:
    show = st.checkbox("Show matched FAQ and score")
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
    with st.expander("All FAQs"):
        for f in bot.faqs:
            st.text(f"- {f['question']}")
# F3: messages are rendered as plain text, so user input is never interpreted as Markdown
for m in st.session_state.messages:
    st.chat_message(m["role"]).text(m["content"])
if q := st.chat_input("Type your question...", max_chars=MAX_QUESTION_CHARS):
    q = q[:MAX_QUESTION_CHARS]
    st.session_state.messages.append({"role": "user", "content": q})
    st.chat_message("user").text(q)
    ans, matched, score = bot.match(q)
    if show and matched:
        ans += f"\n\nMatched: \"{matched}\" (score {score:.2f})"
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.session_state.messages = st.session_state.messages[:1] + st.session_state.messages[1:][-MAX_HISTORY:]
    st.chat_message("assistant").text(ans)
