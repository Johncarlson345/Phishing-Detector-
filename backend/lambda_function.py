import os
import json
import joblib
import pandas as pd
import psycopg2
 
from feature_extraction import extract_features_batch, normalize_url
 
pipeline = joblib.load("phishing_pipeline.pkl")
 
 
def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=5432,
        sslmode="require"
    )
 
 
def get_tier(confidence):
    if confidence >= 0.8:
        return "high"
    if confidence >= 0.6:
        return "moderate"
    return "low"
 
 
def lambda_handler(event, context):
    body = json.loads(event["body"])
    url = normalize_url(body["url"].strip())
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT prediction, confidence, tier FROM predictions WHERE url = %s",
        (url,)
    )
    cached = cur.fetchone()
 
    if cached:
        prediction, confidence, tier = cached
        confidence = float(confidence)
    else:
        features = extract_features_batch([url])
        df = pd.DataFrame(features)
 
        pred = pipeline.predict(df)[0]
        prob = pipeline.predict_proba(df)[0]
 
        prediction = "Legitimate" if pred == 1 else "Phishing"
        confidence = float(max(prob))
        tier = get_tier(confidence)
 
        cur.execute(
            """
            INSERT INTO predictions (url, prediction, confidence, tier)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE
            SET prediction = EXCLUDED.prediction,
                confidence = EXCLUDED.confidence,
                tier = EXCLUDED.tier,
                created_at = now()
            """,
            (url, prediction, confidence, tier)
        )
        conn.commit()
 
    cur.close()
    conn.close()
 
    result = {
        "prediction": "Undetermined" if tier == "low" else prediction,
        "confidence": confidence,
        "tier": tier
    }
 
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }