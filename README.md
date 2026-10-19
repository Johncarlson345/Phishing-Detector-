# Phishing URL Detector

A web app that takes a URL and predicts whether it is phishing or legitimate, using a machine learning model that looks only at the URL string itself. No page fetching and no reference databases are needed, so a prediction comes back quickly and safely without ever visiting the link.

**Live demo:** <link>

## How it works

```
React frontend
      |
API Gateway
      |
AWS Lambda (Docker container)
      |-- check Neon Postgres cache for a previous result
      |-- feature_extraction.py: raw URL -> numeric features
      |-- XGBoost pipeline (.pkl): features -> probability
      |
JSON response: label, confidence, tier
```

1. The user submits a URL in the React frontend.
2. The request goes through API Gateway to a Lambda function packaged as a Docker image.
3. The function first checks a Postgres cache (hosted on Neon) for a previous prediction on the same URL.
4. On a cache miss, `feature_extraction.py` computes features directly from the raw URL string, and the saved XGBoost pipeline produces a prediction.
5. The result is stored in the cache and returned to the frontend.

## Model

- **Algorithm:** XGBoost classifier inside a scikit-learn pipeline
- **Input:** features computed from the URL string only, such as URL length, token count, HTTPS flag, TLD popularity, and suspicious file extensions
- **Training data:** phishing URLs from URLHaus and legitimate URLs from Wikipedia and StackOverflow (about 101,000 rows)
- **Accuracy:** about 99.7% on held-out data

I also tested Gaussian and Multinomial Naive Bayes, a linear SVM, and Random Forest on an earlier dataset (PhiUSIIL). Random Forest matched XGBoost on accuracy but trained noticeably slower, and the RBF-kernel SVM was too slow to be practical at this dataset size, so I went with XGBoost.

## Data problems I found and fixed

High accuracy on a dataset does not mean the model learned anything useful, so I checked what the model was relying on. Three problems turned up:

- **Dataset-specific shortcuts.** Every legitimate URL was a bare homepage with no path or query string, so the model was learning "has a path means phishing". I dropped the path length and query parameter features and retrained. Accuracy held, and feature importance spread across real signals.
- **Scheme artifact.** About 1,300 training URLs had no `http` or `https` prefix, and all of them were phishing, because URLHaus lists bare domains while the legitimate links always had a scheme. The model was partly learning "no scheme means phishing", and it flagged `youtube.com` as phishing with 99.8% confidence. I now normalize missing schemes to `https://` before computing any feature, in both training and inference. After retraining, accuracy held at about 99.7% and the false positive disappeared.
- **Training-serving skew.** The original dataset shipped with precomputed features whose formulas were undocumented, and they did not match features computed from raw URLs in production. Predictions were wrong in deployment despite excellent validation scores. I rebuilt the features from raw URLs in a single extractor that is used for both training and inference, so the two can never drift apart.

## Handling uncertainty

The app does not force a verdict when the model is unsure:

| Confidence | What the user sees |
|---|---|
| 80% or higher | Clear label |
| 60% to 79% | Label with a note to verify |
| Below 60% | "Undetermined - use your own judgment" |

## Tech stack

- **Model:** Python, pandas, scikit-learn, XGBoost
- **Backend:** AWS Lambda (Docker image via ECR), API Gateway
- **Database:** PostgreSQL on Neon, used as a prediction cache
- **Frontend:** React

## Project structure

```
<repo-root>/
  frontend/              React app
  backend/
    feature_extraction.py
    handler.py
    Dockerfile
    schema.sql
  notebooks/             training and experiments
  model/                 saved pipeline artifact
```

## Running locally

Set up the database cache:

```
psql "$DATABASE_URL" -f backend/schema.sql
```

Build and run the Lambda image:

```
docker build -t phishing-detector backend/
docker run -p 9000:8080 -e DATABASE_URL="$DATABASE_URL" phishing-detector
```

Send a test request:

```
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"url": "https://example.com"}'
```

Run the frontend:

```
cd frontend
npm install
npm start
```

## Limitations

- The legitimate class comes mostly from Wikipedia and StackOverflow, so the model has seen a narrow slice of what legitimate URLs look like. Unusual but harmless URLs can score as suspicious.
- Features come from the URL string alone. This keeps predictions fast and safe, but it cannot catch a phishing page hosted on a clean-looking URL.
- A few features (token count, TLD popularity, suspicious file extension) approximate the original dataset's formulas, because the exact definitions were not documented.

