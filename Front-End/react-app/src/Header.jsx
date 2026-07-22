function Header() {
    return (
        <header className="page-header">
            <div className="brand-group">
                <h1>Is it a Phish?</h1>
                <p className="subtitle">Paste a URL below and get a quick visual check for phishing risk.</p>
            </div>
            <nav className="page-nav">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Fish</a></li>
                </ul>
            </nav>
        </header>
    )
}
export default Header