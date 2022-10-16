import uuid from 'react-uuid'
import React, { useEffect, useState, useContext } from 'react'
import { isMobile } from 'react-device-detect'

const deviceDetectContext = React.createContext()
const userIdContext = React.createContext()

export function useMobile() {
  return useContext(deviceDetectContext)
}

export function useUserId() {
  return useContext(userIdContext)
}

const getUserId = () => {
  const data = localStorage.getItem('fairytaleid')
  return data === null ? uuid() : JSON.parse(data)
}

export default function ThemeProvider({ children }) {
  const [mobile, setMobile] = useState(
    isMobile || window.screen.width < window.screen.height
  )

  const [userId, setUserId] = useState(getUserId())

  const checkMobile = () => {
    setMobile(isMobile || window.screen.width < window.screen.height)
    console.log(
      'Changing dimensions may make the app missbehave, please reload after resizing'
    )
  }

  useEffect(() => {
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  useEffect(() => {
    localStorage.setItem('fairytaleid', JSON.stringify(userId))
  }, [userId])

  return (
    <deviceDetectContext.Provider value={mobile}>
      <userIdContext.Provider value={{ userId, setUserId }}>
        {children}
      </userIdContext.Provider>
    </deviceDetectContext.Provider>
  )
}
