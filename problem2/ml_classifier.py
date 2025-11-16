"""Binary sentiment classifier for airline customer feedback."""
from __future__ import annotations

from typing import List, Sequence, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TrainingDatum = Tuple[str, str]


def _validate_training_data(training_data: Sequence[TrainingDatum]) -> List[TrainingDatum]:
    """Clean and validate input rows."""

    cleaned: List[TrainingDatum] = []
    for text, label in training_data:
        normalized_text = (text or "").strip()
        normalized_label = (label or "").strip().lower()
        if not normalized_text:
            continue  # skip empty entries
        if normalized_label not in {"positive", "negative"}:
            raise ValueError(f"Invalid label: {label!r}")
        cleaned.append((normalized_text, normalized_label))
    if not cleaned:
        raise ValueError("Training data is empty after cleaning.")
    return cleaned


def train_sentiment_model(training_data: Sequence[TrainingDatum]) -> Pipeline:
    """Train a Logistic Regression sentiment model."""

    cleaned = _validate_training_data(training_data)
    texts, labels = zip(*cleaned)

    pipeline: Pipeline = Pipeline(
        steps=[
            (
                "vectorizer",
                TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1),
            ),
            (
                "classifier",
                LogisticRegression(max_iter=1000, solver="lbfgs"),
            ),
        ]
    )
    pipeline.fit(texts, labels)
    return pipeline


def predict_sentiment(model: Pipeline, new_text: str) -> str:
    """Predict whether `new_text` is positive or negative."""

    if not isinstance(model, Pipeline):
        raise TypeError("model must be a sklearn Pipeline returned by train_sentiment_model")
    normalized_text = (new_text or "").strip()
    if not normalized_text:
        raise ValueError("new_text must be a non-empty string")
    prediction = model.predict([normalized_text])[0]
    return str(prediction)


if __name__ == "__main__":
    demo_training = [
        ("The flight was on time, and the staff was friendly.", "positive"),
        ("I had to wait 3 hours due to a delay. Terrible!", "negative"),
        ("Great legroom and comfortable seats.", "positive"),
        ("Lost my luggage, extremely upset about this.", "negative"),
        ("Check-in was smooth, no issues at all.", "positive"),
    ]

    model = train_sentiment_model(demo_training)
    samples = [
        "The seats were comfortable and service was great!",
        "They lost my baggage and were very unhelpful!",
        "Nothing special, just an average flight.",
    ]
    for text in samples:
        print(text, "->", predict_sentiment(model, text))
