function Results({ result }) {
    if (!result) {
        return null
    }

    if (result.error) {
        return (
            <section className="result-panel">
                <div className="result-card error">
                    <p className="result-verdict">{result.error}</p>
                </div>
            </section>
        )
    }

    const isLegit = result.prediction === "Legitimate"

    return (
        <section className="result-panel">
            <div className={`result-card ${isLegit ? "legitimate" : "phishing"}`}>
                <p className="result-verdict">{result.prediction}</p>
                <p className="result-confidence">
                    {(result.confidence * 100).toFixed(1)}% confidence
                </p>
            </div>
        </section>
    )
}

export default Results