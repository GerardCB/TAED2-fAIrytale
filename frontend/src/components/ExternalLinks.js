const ExternalLinks = () => {
  return (
    <div style={container}>
      <div>
        You can also use our public documented API{' '}
        <a href='http://34.171.58.154/docs' target='blank' style={linkStyle}>
          http://34.171.58.154/docs
        </a>
      </div>
      <div>
        Visit our repo on{' '}
        <a
          href='https://github.com/GerardCB/TAED2-fAIrytale'
          target='blank'
          style={linkStyle}
        >
          GitHub
        </a>
      </div>
    </div>
  )
}

export default ExternalLinks

const container = {
  marginTop: '50px',
  padding: '20px',
  borderRadius: '10px',
  backgroundColor: 'rgba(0,0,0,0.15)',
  width: 'fit-content',
  height: 'fit-content',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
}

const linkStyle = {
  color: '#eee',
  textDecoration: 'none',
  fontWeight: '600',
}
