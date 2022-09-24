import './App.css'
import Home from './components/Home'
import ThemeProvider from './context/ThemeContext'

function App() {
  return (
    <ThemeProvider>
      <Home />
    </ThemeProvider>
  )
}

export default App
