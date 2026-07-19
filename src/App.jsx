import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home.jsx'
import ChatPage from './pages/ChatPage.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chat/:agentId" element={<ChatPage />} />
    </Routes>
  )
}
