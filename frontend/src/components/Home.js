import AnimatedLogo from './AnimatedLogo'
import AnimatedTitle from './AnimatedTitle'
import InputContent from './InputContent'

const Home = () => {
  return (
    <div style={container}>
      <AnimatedLogo />
      <AnimatedTitle />
      <InputContent />
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
