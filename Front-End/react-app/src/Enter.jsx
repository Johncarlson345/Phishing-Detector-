function Enter() {
    return (
        <section className="entry-panel">
            <form className="entry-form">
                <label htmlFor="website">Website URL</label>
                <input type="url" id="website" placeholder="https://example.com" required />
                <button type="submit">Check URL</button>
            </form>
        </section>
    )
}

export default Enter