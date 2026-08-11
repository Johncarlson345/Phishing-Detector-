import { useState } from 'react'
import './App.css'
import Header from './Header.jsx'
import Enter from './Enter.jsx'
import Results from './results.jsx'

function App() {
  const [result, setResult] = useState(null)

  return (
    <div className="app-shell">
      <Header />
      <Enter onResult={setResult} />
      <Results result={result} />
    </div>
  )
}

export default App

