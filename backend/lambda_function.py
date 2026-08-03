import json
import joblib
import pandas as pd

from feature_extraction import feature_extraction

# Load the trained pipeline once when the Lambda container starts
pipeline = joblib.load("phishing_pipeline.pkl")


def lambda_handler(event, context):
    try:
        # Handle both API Gateway requests and local testing
        body = event.get("body")

        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = event

        # Get URL from request
        url = body["url"]

        # Extract features
        features = feature_extraction(url)

        # Convert to DataFrame
        df = pd.DataFrame([features])

        # Predict
        prediction = pipeline.predict(df)[0]
        probabilities = pipeline.predict_proba(df)[0]

        confidence = float(max(probabilities))

        # Convert numeric prediction to readable text
        # Change this if your labels are reversed
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