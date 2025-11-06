import React, { useEffect, useRef, useState } from 'react'

export default function App(){
  const [msgs, setMsgs] = useState([])
  const [text, setText] = useState('')
  const [user, setUser] = useState('me')
  const wsRef = useRef(null)

  const load = async () => {
    const r = await fetch('http://localhost:8000/messages')
    setMsgs(await r.json())
  }
  useEffect(()=>{ load(); const ws = new WebSocket('ws://localhost:8000/ws'); wsRef.current=ws;
    ws.onmessage = e => setMsgs(m => [...m, JSON.parse(e.data)])
    return () => ws.close()
  },[])

  const send = e => { e.preventDefault(); wsRef.current?.send(JSON.stringify({user, text})); setText('') }
  return (<div style={{maxWidth:720, margin:"2rem auto", fontFamily:"sans-serif"}}>
    <h1>Chat</h1>
    <div style={{border:"1px solid #ccc", padding:12, minHeight:200}}>
      {msgs.map((m,i)=>(<div key={i}><b>{m.user}:</b> {m.text}</div>))}
    </div>
    <form onSubmit={send} style={{display:"flex", gap:8, marginTop:12}}>
      <input value={user} onChange={e=>setUser(e.target.value)} placeholder="name" style={{width:120}}/>
      <input value={text} onChange={e=>setText(e.target.value)} placeholder="message" style={{flex:1}}/>
      <button>Send</button>
    </form>
  </div>)
}
