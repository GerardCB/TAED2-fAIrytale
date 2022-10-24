import { faClipboard, faXmark } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useState } from 'react'
import { useMobile, useUserId } from '../context/ThemeContext'

const CurrentId = () => {
  const { userId, setUserId } = useUserId()
  const [clickStatus, setClickStatus] = useState(0)
  // 0: nothing, 1: hover, 2: clicked
  const mobile = useMobile()
  const [changeIdOpen, setChangeIdOpen] = useState(false)
  const [inputText, setInputText] = useState('')

  const hoverIn = () => {
    setClickStatus(oldStatus => (oldStatus === 2 ? 2 : 1))
  }

  const hoverOut = () => {
    setClickStatus(oldStatus => (oldStatus === 2 ? 2 : 0))
  }

  const clickCopy = () => {
    navigator.clipboard.writeText(userId)
    setClickStatus(2)
    setTimeout(() => setClickStatus(0), 3000)
  }

  const changeId = async () => {
    const res = await fetch(
      `http://34.171.58.154/user-exists?userId=${inputText}`
    )
      .then(res => res.json())
      .then(data => data)
    console.log(res)

    if (res?.exists) {
      setUserId(inputText)
      setChangeIdOpen(false)
      setInputText('')
    }
  }

  const mouseInfo = {
    backgroundColor: 'rgba(0,0,0,0.5)',
    opacity: clickStatus === 0 ? 0 : 1,
    padding: '8px',
    position: 'absolute',
    transform: 'translateY(-3em)',
    borderRadius: '10px',
    fontSize: '0.8em',
  }

  return (
    <div style={mobile ? containerMobile : containerDesktop}>
      <div style={currentIdContainer}>
        <div>
          <p style={noIdStyle}>Your current ID is</p>
          <p style={idStyle}>{userId}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={mouseInfo}>{clickStatus === 2 ? 'Copied!' : 'Copy'}</div>
          <FontAwesomeIcon
            icon={faClipboard}
            className='copy-icon'
            onMouseEnter={hoverIn}
            onMouseLeave={hoverOut}
            onClick={clickCopy}
          />
        </div>
      </div>
      <div
        style={{ ...currentIdContainer, zIndex: 2 }}
        onClick={() => !changeIdOpen && setChangeIdOpen(true)}
        className={changeIdOpen ? '' : 'grow-less-on-hover'}
      >
        {changeIdOpen ? (
          <div style={changeIdContainer}>
            <FontAwesomeIcon
              icon={faXmark}
              style={closeButon}
              onClick={() => setChangeIdOpen(false)}
              className='grow-on-hover'
            />
            <div>
              <p style={{ margin: '0px 0px 5px 0px' }}>Enter your ID</p>
              <input
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                style={inputId}
              />
            </div>
            <div
              style={setButton}
              onClick={changeId}
              className='grow-less-on-hover'
            >
              SET ID
            </div>
          </div>
        ) : (
          <p style={changeIdText}>CHANGE ID</p>
        )}
      </div>
    </div>
  )
}

export default CurrentId

const containerDesktop = {
  position: 'fixed',
  top: '20px',
  right: '20px',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
  alignItems: 'flex-end',
}

const containerMobile = {
  marginBottom: '30px',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
  alignItems: 'flex-end',
}

const currentIdContainer = {
  padding: '20px',
  borderRadius: '10px',
  backgroundColor: 'rgba(0,0,0,0.15)',
  width: 'fit-content',
  height: 'fit-content',
  display: 'flex',
  gap: '20px',
}

const noIdStyle = {
  margin: 0,
}

const idStyle = {
  fontSize: '1.2em',
  fontWeight: '600',
  margin: 0,
}

const changeIdContainer = {
  display: 'flex',
  alignItems: 'flex-end',
  gap: '20px',
}

const changeIdText = {
  margin: 0,
  fontWeight: '600',
  fontSize: '0.8em',
}

const inputId = {
  backgroundColor: 'rgba(0,0,0,0.2)',
  borderRadius: '10px',
  padding: '10px',
  color: '#EEE',
  border: 0,
  outline: 0,
  fontWeight: '600',
}

const setButton = {
  backgroundColor: 'rgba(0,0,0,0.2)',
  borderRadius: '10px',
  padding: '10px',
  height: 'fit-content',
  fontWeight: '600',
}

const closeButon = {
  position: 'fixed',
  right: '40px',
  marginTop: '-3.2em',
  cursor: 'pointer',
}
