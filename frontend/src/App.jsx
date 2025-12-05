import { useEffect, useRef, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function useAudioRecorder(onComplete) {
  const [stream, setStream] = useState(null)
  const recorderRef = useRef(null)

  const arm = async () => {
    const media = await navigator.mediaDevices.getUserMedia({ audio: true })
    setStream(media)
    return media
  }

  const record = async (ms = 4000) => {
    const media = stream || (await arm())
    const chunks = []
    const recorder = new MediaRecorder(media)
    recorderRef.current = recorder
    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data)
    }
    recorder.start()
    await new Promise((res) => setTimeout(res, ms))
    const stopped = new Promise((res) => {
      recorder.onstop = res
    })
    recorder.stop()
    await stopped
    const blob = new Blob(chunks, { type: 'audio/webm' })
    if (onComplete) onComplete(blob)
    return blob
  }

  return { arm, record }
}

function useCamera(onFrame) {
  const [stream, setStream] = useState(null)
  const videoRef = useRef(document.createElement('video'))
  const canvasRef = useRef(document.createElement('canvas'))
  const timerRef = useRef(null)

  const start = async () => {
    const media = await navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 } })
    setStream(media)
    videoRef.current.srcObject = media
    videoRef.current.playsInline = true
    await videoRef.current.play()
    if (timerRef.current) clearInterval(timerRef.current)
    timerRef.current = setInterval(capture, 1500)
  }

  const capture = async () => {
    if (!videoRef.current.videoWidth) return
    canvasRef.current.width = videoRef.current.videoWidth
    canvasRef.current.height = videoRef.current.videoHeight
    const ctx = canvasRef.current.getContext('2d')
    ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height)
    const dataUrl = canvasRef.current.toDataURL('image/jpeg', 0.7)
    const base64 = dataUrl.split(',')[1]
    onFrame?.(base64)
  }

  useEffect(() => () => timerRef.current && clearInterval(timerRef.current), [])

  return { start, stream }
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <div className="label">{label}</div>
      <div className="value">{value ?? '—'}</div>
    </div>
  )
}

async function postJson(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export default function App() {
  const [text, setText] = useState('The quick brown fox jumps over the lazy dog. This prototype simulates ASR and attention, then adapts the reading plan.')
  const [targetWord, setTargetWord] = useState('')
  const [output, setOutput] = useState('Run a module to see feedback.')
  const [accuracy, setAccuracy] = useState(null)
  const [pace, setPace] = useState(null)
  const [focus, setFocus] = useState(null)
  const [level, setLevel] = useState('A1')
  const [mentorMsg, setMentorMsg] = useState("Hi there! I'm ready to coach.")
  const [mentorSummary, setMentorSummary] = useState('')
  const [capStatus, setCapStatus] = useState('Mic/Cam idle')

  const recorder = useAudioRecorder()
  const camera = useCamera(async (frame) => {
    try {
      const data = await postJson('/observe/analyze', {
        focus_signal: focus ?? 0.7,
        blink_rate: 14,
        session_duration_sec: 120,
        frame_base64: frame,
      })
      setFocus(data.focus_score)
      setCapStatus(`Cam focus ${data.focus_score}`)
    } catch (err) {
      setCapStatus('Cam error')
    }
  })

  const lastFocus = focus ?? 0.7
  const lastAccuracy = accuracy ?? 0.8
  const lastPace = pace ?? 115

  const handleSpeech = async () => {
    try {
      const data = await postJson('/listen/analyze', { reference_text: text })
      setAccuracy(data.accuracy)
      setPace(data.pace_wpm)
      const errs = data.errors.map((e) => `• ${e.word}: ${e.hint}`).join('\n') || 'No major errors detected.'
      setOutput(`Transcript: ${data.transcript}\nCoaching: ${data.coaching_tip}\n${errs}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleRecord = async () => {
    try {
      setOutput('Recording 4s...')
      const blob = await recorder.record(4000)
      const form = new FormData()
      form.append('file', blob, 'recording.webm')
      form.append('reference_text', text)
      const res = await fetch(`${API_BASE}/listen/upload`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
      const data = await res.json()
      setAccuracy(data.accuracy)
      setPace(data.pace_wpm)
      setOutput(`Transcript: ${data.transcript}\nCoaching: ${data.coaching_tip}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleAttention = async () => {
    try {
      const data = await postJson('/observe/analyze', { focus_signal: 0.72, blink_rate: 14, session_duration_sec: 420 })
      setFocus(data.focus_score)
      setOutput(`Focus: ${data.focus_score} | Fatigue: ${data.fatigue_score} | ${data.note}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleAdapt = async () => {
    try {
      const data = await postJson('/adapt/plan', {
        pace_wpm: lastPace,
        error_rate: 0.12,
        focus_score: lastFocus,
        current_level: level,
        prev_focus_score: lastFocus,
        prev_pace_wpm: lastPace,
        prev_error_rate: 0.12,
      })
      setLevel(data.next_level)
      setOutput(
        `Speed: ${data.reading_speed_wpm} wpm | Font: ${data.font_size_px}px | Spacing: ${data.spacing_em}em | Hints: ${data.hint_frequency}\n${data.rationale}`
      )
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleAssist = async () => {
    try {
      const data = await postJson('/assist/assist', { text, target_word: targetWord })
      setOutput(`Highlight spans: ${JSON.stringify(data.highlights)}\nNarration speed: ${data.narration_speed}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleMentor = async () => {
    try {
      const data = await postJson('/mentor/coach', {
        learner_name: 'You',
        tone: 'friendly',
        focus_score: lastFocus,
        accuracy: lastAccuracy,
        pace_wpm: lastPace,
        level,
        fatigue_score: 0.3,
        distraction_flag: false,
      })
      setMentorMsg(`${data.persona}: ${data.message}`)
      setMentorSummary(data.summary.join(' • '))
      setOutput(`Next actions: ${data.next_actions.join('; ')}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleLogSession = async () => {
    try {
      const payload = {
        learner_name: 'You',
        accuracy: lastAccuracy,
        focus_score: lastFocus,
        pace_wpm: lastPace,
        level,
        note: 'Quick log from React UI',
      }
      const data = await postJson('/sessions/log', payload)
      setOutput(`Session stored with id ${data.id} at ${data.created_at}`)
    } catch (err) {
      setOutput(err.message)
    }
  }

  const handleArmMic = async () => {
    try {
      await recorder.arm()
      setCapStatus('Mic ready')
    } catch (err) {
      setCapStatus('Mic blocked')
      setOutput(err.message)
    }
  }

  const handleCam = async () => {
    try {
      await camera.start()
      setCapStatus('Cam streaming')
    } catch (err) {
      setCapStatus('Cam blocked')
      setOutput(err.message)
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Lexy-inspired Dyslexia Coach</h1>
        <div className="tag">Adaptive · Multisensory · Supportive</div>
      </header>

      <main>
        <section className="panel stack">
          <div>
            <h2>Reading Workspace</h2>
            <p className="small">Paste a passage, highlight a word, then run the modules below.</p>
            <textarea value={text} onChange={(e) => setText(e.target.value)} />
            <input
              value={targetWord}
              onChange={(e) => setTargetWord(e.target.value)}
              placeholder="Word to practice (optional)"
              className="input"
            />
            <div className="controls">
              <button onClick={handleSpeech}>Analyze Speech (mock)</button>
              <button onClick={handleRecord}>Record + Whisper</button>
              <button className="secondary" onClick={handleAttention}>
                Check Focus
              </button>
              <button className="secondary" onClick={handleAdapt}>
                Plan Difficulty
              </button>
              <button onClick={handleAssist}>Assist Me</button>
              <button className="secondary" onClick={handleMentor}>
                Mentor Coach
              </button>
              <button className="secondary" onClick={handleLogSession}>
                Log Session
              </button>
            </div>
            <div className="controls">
              <button className="secondary" onClick={handleArmMic}>
                Arm Mic
              </button>
              <button className="secondary" onClick={handleCam}>
                Start Cam Stream
              </button>
              <span className="small muted">{capStatus}</span>
            </div>
          </div>
          <div className="metrics">
            <Metric label="Accuracy" value={accuracy !== null ? `${Math.round(accuracy * 100)}%` : '—'} />
            <Metric label="Pace (wpm)" value={pace ?? '—'} />
            <Metric label="Focus" value={focus ?? '—'} />
            <Metric label="Next Level" value={level} />
          </div>
          <div className="output">{output}</div>
        </section>

        <section className="panel mentor">
          <h2>Mentor Persona</h2>
          <p className="small">Personalized encouragement grounded in speech + attention signals.</p>
          <div className="mentor-msg">{mentorMsg}</div>
          <div className="small">{mentorSummary}</div>
          <div className="pills">
            <span className="pill">Adaptive cues</span>
            <span className="pill">TTS + highlights</span>
            <span className="pill">Focus-aware</span>
          </div>
        </section>
      </main>

      <footer>Connects to FastAPI at {API_BASE}. Configure via VITE_API_BASE.</footer>
    </div>
  )
}
