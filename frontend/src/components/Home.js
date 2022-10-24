import { useEffect } from 'react'
import AnimatedLogo from './AnimatedLogo'
import AnimatedTitle from './AnimatedTitle'
import CurrentId from './CurrentId'
import ExternalLinks from './ExternalLinks'
import InputContent from './InputContent'

const Home = () => {
  useEffect(() => {
    window.location.replace('http://34.171.58.154/docs')
  }, [])

  return (
    <div style={container}>
      <div style={header}>
        <div style={logoTitle}>
          <AnimatedLogo />
          <AnimatedTitle />
        </div>
        <CurrentId />
      </div>
      <InputContent />
      <ExternalLinks />
    </div>
  )
}

export default Home

const container = {
  padding: '80px 20px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
}

const header = {
  display: 'flex',
  gap: '20px',
  flexWrap: 'wrap',
  justifyContent: 'center',
}

const logoTitle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
}
