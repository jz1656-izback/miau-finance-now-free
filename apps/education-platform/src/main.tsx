import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
// Education tracker
try{const sid=localStorage.getItem('_miau_sid')||'s_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);localStorage.setItem('_miau_sid',sid);navigator.sendBeacon('/api/v1/marketing/track',JSON.stringify({event:'page_view',path:window.location.pathname,host:'localhost:5174',session_id:sid}))}catch(e){}
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
