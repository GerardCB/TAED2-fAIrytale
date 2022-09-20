import { faArrowDown, faArrowRight } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useState } from 'react'
import { useMobile } from '../context/ThemeContext'

const InputContent = () => {
  const isMobile = useMobile()
  const [inputContent, setInputContent] = useState('')
  const [result, setResult] = useState({ ok: false, img: '', loading: true })

  const getImage = () => {
    if (inputContent !== '') {
      setResult(oldResult => ({ ...oldResult, ok: true, loading: true }))
      fetch('https://random.imagecdn.app/300/150', {
        method: 'GET',
      })
        .then(res => res.url)
        .then(data => {
          setResult(oldResult => ({ ...oldResult, img: data }))
        })
    } else {
      setResult(oldResult => ({ ...oldResult, ok: false }))
    }
  }

  return (
    <div style={container}>
      <div style={isMobile ? mobileInputContainer : inputContainer}>
        <p style={titleStyle}>Enter your fAIrytale here 🧚 ⬇️</p>
        <textarea
          value={inputContent}
          onChange={e => setInputContent(e.target.value)}
          style={inputStyle}
        />
      </div>
      <div
        style={isMobile ? mobileArrowContainer : arrowContainer}
        className='grow-on-hover'
        onClick={getImage}
      >
        <FontAwesomeIcon icon={isMobile ? faArrowDown : faArrowRight} />
      </div>
      <div style={isMobile ? mobileInputContainer : inputContainer}>
        <div style={outputStyle}>
          {result.ok ? (
            <>
              <p style={{ display: result.loading ? 'block' : 'none' }}>
                Loading...
              </p>
              <img
                src={result.img}
                style={{ display: result.loading ? 'none' : 'block' }}
                alt='result'
                onLoad={() =>
                  setResult(oldResult => ({ ...oldResult, loading: false }))
                }
              />
            </>
          ) : (
            <p>Type something and submit</p>
          )}
        </div>
        <p style={titleStyle}>See the result here 🤖⬆️</p>
      </div>
    </div>
  )
}

export default InputContent

const container = {
  display: 'flex',
  maxWidth: '90vw',
  gap: '20px',
  flexWrap: 'wrap',
}

const inputContainer = {
  width: '300px',
  display: 'flex',
  flexDirection: 'column',
  gap: '10px',
}

const mobileInputContainer = {
  width: '90vw',
  display: 'flex',
  flexDirection: 'column',
  gap: '10px',
}

const arrowContainer = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  fontSize: '2em',
}

const mobileArrowContainer = {
  height: '50px',
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  fontSize: '2em',
}

const titleStyle = {
  margin: 0,
  fontSize: '1.2em',
  fontWeight: 600,
}

const inputStyle = {
  border: 0,
  height: 'calc(300px - 20px)',
  width: 'calc(100% - 20px)',
  outline: 'none',
  padding: '10px',
  backgroundColor: 'rgba(0,0,0,0.3)',
  color: 'white',
  borderRadius: '10px',
  resize: 'none',
}

const outputStyle = {
  width: '100%',
  height: '300px',
  backgroundColor: 'rgba(0,0,0,0.3)',
  borderRadius: '10px',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
}
