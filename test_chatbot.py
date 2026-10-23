from chatbot import FAQChatbot, FALLBACK
bot = FAQChatbot()
cases = ["Is this internship remote?", "how should I name my github repo", "Do I get paid?",
         "how many tasks must I finish", "Will I receive a certificate?", "What's the weather on Mars?"]
for q in cases:
    a, m, s = bot.match(q)
    print(f"Q: {q}\n  -> {m} ({s:.2f})")
assert bot.respond("What's the weather on Mars?") == FALLBACK
print("OK")
# Security review F6: very long input is capped and still handled
a, m, s = bot.match("Is this internship remote? " * 1000)
print("Long input ->", m)
print("OK (security)")
