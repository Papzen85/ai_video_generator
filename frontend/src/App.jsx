import React, {useState} from 'react'

export default function App(){
  const [script, setScript] = useState('A cinematic sunrise over a misty valley.\n\nA lone traveler walks toward the light.');
  const [status, setStatus] = useState('idle');
  const submit = async () => {
    setStatus('queuing...');
    const res = await fetch('/api/generate_realistic_clip', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({script, mode: 'realistic'})
    });
    const data = await res.json();
    setStatus(JSON.stringify(data));
  };
  return (<div style={{fontFamily:'Arial', padding:20}}>
    <h1>VidCraft - Realistic Mode (Preview)</h1>
    <textarea value={script} onChange={e=>setScript(e.target.value)} rows={8} style={{width:'100%'}}/>
    <br/>
    <button onClick={submit} style={{marginTop:10}}>Generate Realistic Clip (queue)</button>
    <p>Status: {status}</p>
    <p>Note: This is a scaffold. Replace backend stubs with real model integrations.</p>
  </div>);
}
