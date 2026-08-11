import { useState } from "react"

function Enter({ onResult }) {
    const [url, setUrl] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()
        setLoading(true)

        try {
            const response = await fetch("https://08p8c2b5me.execute-api.us-east-1.amazonaws.com/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url }),
            })

            const result = await response.json()

            onResult(result)
        } catch (err) {
            onResult({ error: "Something went wrong. Try again." })
        }

        setLoading(false)
    }

    return (
        <section className="entry-panel">
            <form className="entry-form" onSubmit={handleSubmit}>
                <label htmlFor="website">Website URL</label>
                <input
                    type="text"
                    id="website"
                    placeholder="https://example.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Checking..." : "Check URL"}
                </button>
            </form>
        </section>
    )
}

export default Enter