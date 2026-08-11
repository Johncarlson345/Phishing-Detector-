function getTier(confidence) {
    if (confidence >= 0.8) {
        return "high"
    }
    if (confidence >= 0.6) {
        return "moderate"
    }
    return "low"
}

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
    const tier = getTier(result.confidence)

    const verdictText = tier === "low" ? "Undetermined" : result.prediction

    const noteText =
        tier === "moderate"
            ? isLegit
                ? "Leaning legitimate, but not fully certain. Proceed with caution."
                : "Leaning phishing, but not fully certain. Proceed with caution."
            : tier === "low"
                ? "The model can't confidently classify this URL. Use your own judgment before clicking."
                : null

    const cardClass =
        tier === "low" ? "undetermined" : isLegit ? "legitimate" : "phishing"

    return (
        <section className="result-panel">
            <div className={`result-card ${cardClass} ${tier}`}>
                <p className="result-verdict">{verdictText}</p>
                <p className="result-confidence">
                    {(result.confidence * 100).toFixed(1)}% confidence
                </p>
                {noteText && <p className="result-note">{noteText}</p>}
            </div>
        </section>
    )
}

export default Results