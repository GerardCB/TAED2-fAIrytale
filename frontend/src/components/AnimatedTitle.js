const title = 'This is fAIrytale'

const AnimatedTitle = () => {
  return (
    <div style={container}>
      {title.split('').map((char, i) => (
        <p
          key={i}
          style={{
            ...titleStyle,
            marginLeft: char === ' ' ? '10px' : '0px',
            animation: `appear-up 0.5s ${i * 40 + 300}ms forwards`,
          }}
          className='hidden'
        >
          {char}
        </p>
      ))}
    </div>
  )
}

export default AnimatedTitle

const container = {
  display: 'flex',
}

const titleStyle = {
  marginTop: 0,
  fontSize: '2em',
  fontWeight: '600',
}
