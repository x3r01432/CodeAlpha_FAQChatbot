"""FAQ chatbot: NLTK preprocessing + TF-IDF cosine similarity matching."""
import json, string, sys
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FALLBACK = "Sorry, I don't know the answer to that. Try rephrasing your question."


def ensure_nltk_data():
    for path, pkg in [("tokenizers/punkt", "punkt"), ("tokenizers/punkt_tab", "punkt_tab"),
                      ("corpora/stopwords", "stopwords"), ("corpora/wordnet", "wordnet"),
                      ("corpora/omw-1.4", "omw-1.4")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


class FAQChatbot:
    def __init__(self, faq_path=Path(__file__).with_name("faqs.json"), threshold=0.2):
        ensure_nltk_data()
        self.faqs = json.loads(Path(faq_path).read_text(encoding="utf-8"))
        self.threshold = threshold
        self.stop = set(stopwords.words("english"))
        self.lem = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([self.preprocess(f["question"]) for f in self.faqs])

    def preprocess(self, text):
        tokens = nltk.word_tokenize(text.lower())
        return " ".join(self.lem.lemmatize(t) for t in tokens
                        if t not in string.punctuation and t not in self.stop and t.isalnum())

    def match(self, question):
        """Return (answer, matched_question, score)."""
        clean = self.preprocess(question)
        if not clean:
            return FALLBACK, None, 0.0
        scores = cosine_similarity(self.vectorizer.transform([clean]), self.matrix)[0]
        i = int(scores.argmax())
        if scores[i] < self.threshold:
            return FALLBACK, None, float(scores[i])
        return self.faqs[i]["answer"], self.faqs[i]["question"], float(scores[i])

    def respond(self, question):
        return self.match(question)[0]


def cli():
    bot = FAQChatbot()
    print("CodeAlpha FAQ Chatbot (type 'quit' to exit)")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"quit", "exit", "bye"}:
            break
        if q:
            print("Bot:", bot.respond(q))
    print("Bot: Goodbye!")


if __name__ == "__main__":
    cli()
