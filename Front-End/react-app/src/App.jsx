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
      <p>please keep in mind that if your input does not have https:// in it the model will likely predict it as a phish</p>
    </div>
  )
}

export default App

