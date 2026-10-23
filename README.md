# CodeAlpha_FAQChatbot

An FAQ chatbot built for **Task 2 of the CodeAlpha Artificial Intelligence internship**. It answers questions about the CodeAlpha internship by matching your question to the most similar FAQ.

## Features
- 30 FAQs about the CodeAlpha internship stored in `faqs.json`
- NLTK preprocessing: tokenization, lowercasing, stopword and punctuation removal, lemmatization (NLTK data downloads automatically)
- TF-IDF + cosine similarity (scikit-learn) to find the best match
- Fallback "Sorry, I don't know" reply when no FAQ is similar enough
- Streamlit chat UI (with optional matched-FAQ/score display) and a command-line mode

## Tech Stack
Python 3, NLTK, scikit-learn, Streamlit

## Setup
```bash
git clone https://github.com/x3r01432/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
CLI mode: `python chatbot.py`  ·  Tests: `python test_chatbot.py`

## Project Structure
```
CodeAlpha_FAQChatbot/
├── app.py            # Streamlit chat UI
├── chatbot.py        # Preprocessing, TF-IDF matching, CLI mode
├── faqs.json         # FAQ dataset
├── test_chatbot.py   # Quick sanity test
├── requirements.txt
├── LICENSE
└── README.md
```

## Author
[x3r01432](https://github.com/x3r01432)

## License
MIT
