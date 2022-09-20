import React, { useEffect, useState, useContext } from 'react'
import { isMobile } from 'react-device-detect'

const deviceDetectContext = React.createContext()

export function useMobile() {
  return useContext(deviceDetectContext)
}

export default function ThemeProvider({ children }) {
  const [mobile, setMobile] = useState(
    isMobile || window.screen.width < window.screen.height
  )

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

  return (
    <deviceDetectContext.Provider value={mobile}>
      {children}
    </deviceDetectContext.Provider>
  )
}
