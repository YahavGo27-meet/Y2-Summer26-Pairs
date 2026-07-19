import { useNavigate } from 'react-router-dom'
import { AGENTS } from '../lib/agents.js'
import '../styles/home.css'

export default function Home() {
  const navigate = useNavigate()

  const openAgent = (agentId) => navigate(`/chat/${agentId}`)

  return (
    <div className="home">
      <header className="home-header">
        <div className="home-badge">
          <span className="dot" />
          MEET Program · Year 1
        </div>
        <h1 className="home-title">MEET Y1 Assistant</h1>
        <p className="home-subtitle">
          Your learning companion for Computer Science and Entrepreneurship.
          Get guidance, hints, and step-by-step explanations — designed to help
          you think independently, not just hand you the answer.
        </p>
      </header>

      <div className="home-cards">
        {Object.values(AGENTS).map((agent) => (
          <button
            key={agent.id}
            className="agent-card"
            style={{
              '--accent': agent.accent,
              '--accent-soft': agent.accentSoft,
              '--accent-line': agent.accentRing,
            }}
            onClick={() => openAgent(agent.id)}
            aria-label={`Open ${agent.name} agent`}
          >
            <div className="agent-icon">{agent.emoji}</div>
            <h2 className="agent-name">{agent.name}</h2>
            <p className="agent-tagline">{agent.description}</p>
            <span className="agent-cta">
              Start chatting
              <span className="arrow">→</span>
            </span>
          </button>
        ))}
      </div>

      <footer className="home-footer">
        <strong>MEET Y1 Assistant</strong> · Guidance over answers. Learn by thinking.
      </footer>
    </div>
  )
}
