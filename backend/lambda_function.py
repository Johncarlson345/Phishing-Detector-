import json
import joblib
import pandas as pd
 
from feature_extraction import extract_features
 
pipeline = joblib.load("phishing_pipeline.pkl")
 
 
def lambda_handler(event, context):
    try:
        # Handle CORS preflight request
        method = event.get("requestContext", {}).get("http", {}).get("method")

        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "body": ""
            }

        body = event.get("body")

        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = event

        url = body["url"]

        features = extract_features(url)

        df = pd.DataFrame([features])

        prediction = pipeline.predict(df)[0]
        probabilities = pipeline.predict_proba(df)[0]

        confidence = float(max(probabilities))

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