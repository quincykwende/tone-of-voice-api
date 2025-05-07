import spacy
from textblob import TextBlob
from typing import Dict

nlp = spacy.load("en_core_web_sm")

class ToneAnalyzer:
    @staticmethod
    def analyze_text(text: str) -> Dict:
        """
            Extract measurable NLP features using spaCy + textblob
        """
        doc = nlp(text)
        return {
            "avg_sentence_length": sum(len(sent) for sent in doc.sents) / len(list(doc.sents)),
            "passive_voice_ratio": sum(1 for token in doc if token.dep_ == "nsubjpass") / len(doc),
            "formality_score": ToneAnalyzer._calculate_formality(text),
            "sentiment_polarity": TextBlob(text).sentiment.polarity,
            "sentiment_subjectivity": TextBlob(text).sentiment.subjectivity
        }

    @staticmethod
    def _calculate_formality(text: str) -> float:
        formal_words = {"shall", "thus", "furthermore"}
        informal_words = {"gonna", "wanna", "dude"}
        words = text.lower().split()
        formal = len([w for w in words if w in formal_words])
        informal = len([w for w in words if w in informal_words])
        return formal / (formal + informal + 1e-6)  # Prevent division by zero