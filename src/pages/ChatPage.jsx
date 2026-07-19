import { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase.js'
import { AGENTS } from '../lib/agents.js'
import '../styles/chat.css'

const SUGGESTIONS = {
  cs: [
    'Explain how a for loop works',
    'I have a bug in my function, can you help?',
    'What is the difference between a list and a tuple?',
    'How do I think through a recursion problem?',
  ],
  entrepreneurship: [
    'Help me build a user persona',
    'What is a value proposition?',
    'Sketch a logo idea for my project',
    'How do I validate my business idea?',
  ],
}

const BackIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M19 12H5M12 19l-7-7 7-7" />
  </svg>
)

const TrashIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </svg>
)

const SendIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
  </svg>
)

export default function ChatPage() {
  const { agentId } = useParams()
  const navigate = useNavigate()
  const agent = AGENTS[agentId]

  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [sessionId, setSessionId] = useState(null)

  const messagesRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = useCallback(() => {
    const el = messagesRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [])

  // Load existing session for this agent (most recent)
  useEffect(() => {
    if (!agent) return
    let cancelled = false

    const loadSession = async () => {
      const { data: sessions } = await supabase
        .from('chat_sessions')
        .select('id')
        .eq('agent_mode', agentId)
        .order('updated_at', { ascending: false })
        .limit(1)

      if (cancelled) return

      if (sessions && sessions.length > 0) {
        const sid = sessions[0].id
        setSessionId(sid)
        const { data: msgs } = await supabase
          .from('chat_messages')
          .select('id, role, content, created_at')
          .eq('session_id', sid)
          .order('created_at', { ascending: true })
        if (!cancelled && msgs) setMessages(msgs)
      }
    }

    loadSession()
    return () => { cancelled = true }
  }, [agentId, agent])

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading, scrollToBottom])

  useEffect(() => {
    inputRef.current?.focus()
  }, [agentId])

  if (!agent) {
    return (
      <div style={{ padding: 48, textAlign: 'center' }}>
        <p style={{ color: 'var(--text-soft)', marginBottom: 16 }}>Agent not found.</p>
        <button className="back-btn" onClick={() => navigate('/')}>← Back home</button>
      </div>
    )
  }

  const createSession = async (firstMessage) => {
    const title = firstMessage.length > 60 ? firstMessage.slice(0, 60) + '…' : firstMessage
    const { data, error } = await supabase
      .from('chat_sessions')
      .insert({ agent_mode: agentId, title })
      .select('id')
      .single()
    if (error) throw new Error('Could not start chat session.')
    return data.id
  }

  const persistMessage = async (sid, role, content) => {
    const { data, error } = await supabase
      .from('chat_messages')
      .insert({ session_id: sid, role, content })
      .select('id, role, content, created_at')
      .single()
    if (error) throw new Error('Could not save message.')
    return data
  }

  const touchSession = async (sid) => {
    await supabase.from('chat_sessions').update({ updated_at: new Date().toISOString() }).eq('id', sid)
  }

  const callAgent = async (history) => {
    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY
    const res = await fetch(`${supabaseUrl}/functions/v1/chat-agent`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${anonKey}`,
        apikey: anonKey,
      },
      body: JSON.stringify({ agent: agentId, messages: history }),
    })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error(body.error || `Request failed (${res.status})`)
    }
    const data = await res.json()
    if (!data || typeof data.reply !== 'string') {
      throw new Error('Received an unexpected response from the agent.')
    }
    return data.reply
  }

  const handleSend = async (text) => {
    const content = text.trim()
    if (!content || loading) return

    setError(null)
    const userMsg = { role: 'user', content }
    setMessages((m) => [...m, userMsg])
    setInput('')
    setLoading(true)

    try {
      let sid = sessionId
      if (!sid) {
        sid = await createSession(content)
        setSessionId(sid)
      }

      await persistMessage(sid, 'user', content)

      const history = [...messages, userMsg].map((m) => ({ role: m.role, content: m.content }))
      const reply = await callAgent(history)

      const saved = await persistMessage(sid, 'assistant', reply)
      setMessages((m) => [...m, saved])
      await touchSession(sid)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    if (loading) return
    if (messages.length === 0) return
    const ok = window.confirm('Clear all messages in this chat? This cannot be undone.')
    if (!ok) return

    if (sessionId) {
      await supabase.from('chat_messages').delete().eq('session_id', sessionId)
      await supabase.from('chat_sessions').delete().eq('id', sessionId)
    }
    setMessages([])
    setSessionId(null)
    setError(null)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend(input)
    }
  }

  const handleSuggestion = (s) => handleSend(s)

  return (
    <div
      className="chat"
      style={{
        '--accent': agent.accent,
        '--accent-soft': agent.accentSoft,
        '--accent-ring': agent.accentRing,
      }}
    >
      <header className="chat-header">
        <button className="back-btn" onClick={() => navigate('/')} aria-label="Back to home">
          <BackIcon />
          <span>Home</span>
        </button>
        <div className="chat-header-info">
          <div className="chat-header-icon">{agent.emoji}</div>
          <div className="chat-header-text">
            <div className="chat-header-name">{agent.name}</div>
            <div className="chat-header-sub">
              <span className="live-dot" />
              Rahaf · Y1 Instructor
            </div>
          </div>
        </div>
        <button className="clear-btn" onClick={handleClear} aria-label="Clear chat">
          <TrashIcon />
          <span>Clear</span>
        </button>
      </header>

      <div className="chat-messages" ref={messagesRef}>
        <div className="chat-messages-inner">
          {error && (
            <div className="error-banner">
              <span>⚠</span>
              {error}
            </div>
          )}

          {messages.length === 0 && !loading ? (
            <div className="empty-state">
              <div className="empty-icon">{agent.emoji}</div>
              <h2 className="empty-title">Ask {agent.name === 'Computer Science' ? 'about CS' : 'about Entrepreneurship'}</h2>
              <p className="empty-text">
                {agent.tagline} Rahaf will guide you step by step — without giving you the final answer.
              </p>
              <div className="suggestion-chips">
                {SUGGESTIONS[agentId].map((s) => (
                  <button key={s} className="chip" onClick={() => handleSuggestion(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((m) => (
              <div key={m.id} className={`msg ${m.role}`}>
                <div className="msg-avatar">
                  {m.role === 'user' ? '🧑' : agent.emoji}
                </div>
                <div className="msg-bubble">{m.content}</div>
              </div>
            ))
          )}

          {loading && (
            <div className="typing">
              <div className="typing-avatar">{agent.emoji}</div>
              <div className="typing-bubble">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="chat-input-wrap">
        <div className="chat-input-inner">
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder={`Message ${agent.name}…`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={() => handleSend(input)}
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
        <div className="chat-input-hint">
          Press Enter to send · Shift+Enter for a new line
        </div>
      </div>
    </div>
  )
}
