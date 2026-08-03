import json
import joblib
import pandas as pd

from feature_extraction import feature_extraction

# Load the trained pipeline once when the Lambda container starts
pipeline = joblib.load("phishing_pipeline.pkl")


def lambda_handler(event, context):
    try:
        body = event.get("body")

        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = event

        url = body["url"]

        # Generate features
        features = feature_extraction(url)

        # Convert to DataFrame
        df = pd.DataFrame([features])

        # Make prediction
        prediction = pipeline.predict(df)[0]
        probabilities = pipeline.predict_proba(df)[0]
        confidence = float(max(probabilities))

        # Convert numeric prediction to text
        result = "Legitimate" if prediction == 1 else "Phishing"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "prediction": result,
                "confidence": round(confidence, 4)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }