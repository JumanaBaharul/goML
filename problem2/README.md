# Problem 2 – Binary Sentiment Classification

This folder contains a lightweight machine learning pipeline that trains a
binary classifier on airline customer feedback and predicts whether a new text
is positive or negative.

## Files

- `ml_classifier.py` – exposes `train_sentiment_model` and `predict_sentiment`.
- `api_keys.env` – placeholder (no external APIs used).
- `requirements.txt` – dependencies for the ML pipeline.

## Setup

```bash
cd problem2
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Training & Prediction

```python
from ml_classifier import train_sentiment_model, predict_sentiment

training_rows = [
    ("The flight was on time, and the staff was friendly.", "positive"),
    ("I had to wait 3 hours due to a delay. Terrible!", "negative"),
]
model = train_sentiment_model(training_rows)
print(predict_sentiment(model, "Great legroom and comfortable seats."))
print(predict_sentiment(model, "Lost my luggage, extremely upset about this."))
```

## Using the Provided Dataset

Place the `2026 dataset.csv` file in the repository root (already included).
You can load it with pandas:

```python
import pandas as pd
from ml_classifier import train_sentiment_model

df = pd.read_csv('../2026 dataset.csv')
training_data = list(df[['Text', 'Label']].itertuples(index=False, name=None))
model = train_sentiment_model(training_data)
```
