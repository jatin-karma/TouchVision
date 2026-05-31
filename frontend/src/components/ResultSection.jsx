import { useState } from "react"

export default function ResultSection({ scan, onRemove }) {
  const [speaking, setSpeaking] = useState(false)
  const [copied, setCopied]     = useState(false)
  
  const { loading, annotatedImage, uploadedImage, decodedText, dotCount, cellCount, confidence, filename } = scan

  /* ── TTS via Browser ── */
  const handleSpeak = () => {
    if (!decodedText?.trim()) return
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel()
    
    setSpeaking(true)
    const utt = new SpeechSynthesisUtterance(decodedText)
    
    utt.onend = () => setSpeaking(false)
    utt.onerror = () => setSpeaking(false)
    
    window.speechSynthesis.speak(utt)
  }

  /* ── Copy ── */
  const handleCopy = async () => {
    if (!decodedText) return
    try {
      await navigator.clipboard.writeText(decodedText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy:", err)
    }
  }

  /* ── Download ── */
  const handleDownload = () => {
    if (!decodedText) return
    const blob = new Blob([decodedText], { type: "text/plain" })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement("a")
    a.href     = url
    a.download = `braille_decoded_${Date.now()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const confPct   = Math.round(confidence * 100)
  const wordCount = decodedText ? decodedText.trim().split(/\s+/).length : 0

  if (loading) {
    return (
      <div className="retro-card" style={{ padding: '32px', textAlign: 'center' }}>
        <div style={{ color: 'var(--accent-orange)', fontWeight: 600, fontSize: '1.2rem', marginBottom: '16px' }}>
          ⏳ Analyzing Document...
        </div>
        <div style={{ opacity: 0.7, fontSize: '0.9rem' }}>{filename}</div>
      </div>
    )
  }

  return (
    <div className="results-area" style={{ marginTop: 0, animation: 'fadeIn 0.4s ease-out forwards' }}>
      {/* ── 1. ANNOTATED IMAGE (hero) ── */}
      {annotatedImage ? (
        <div className="retro-card">
          <div className="retro-card-header">
            <h3>Braille Detection <span className="dot-badge">{dotCount} Dots</span></h3>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <span style={{ fontSize: "0.85rem", opacity: 0.7, fontWeight: 500 }}>
                {filename}
              </span>
              <button onClick={onRemove} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--accent-rust)', fontSize: '1.2rem' }}>×</button>
            </div>
          </div>
          <div className="image-preview-container">
            <img src={annotatedImage} alt={`Annotated Braille — ${dotCount} dots`} />
          </div>
        </div>
      ) : uploadedImage ? (
        <div className="retro-card">
          <div className="retro-card-header">
            <h3>Uploaded Image</h3>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <span style={{ fontSize: "0.85rem", opacity: 0.7, fontWeight: 500 }}>
                {filename}
              </span>
              <button onClick={onRemove} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--accent-rust)', fontSize: '1.2rem' }}>×</button>
            </div>
          </div>
          <div className="image-preview-container">
            <img src={uploadedImage} alt="Uploaded Braille" />
          </div>
        </div>
      ) : null}

      {/* ── 2. STATS ── */}
      {annotatedImage && (
        <div className="stats-grid">
          <div className="stat-box">
            <div className="stat-label">Dots</div>
            <div className="stat-value">{dotCount}</div>
          </div>
          <div className="stat-box">
            <div className="stat-label">Cells</div>
            <div className="stat-value">{cellCount}</div>
          </div>
          <div className="stat-box">
            <div className="stat-label">Confidence</div>
            <div className="stat-value">{confPct}%</div>
          </div>
          <div className="stat-box">
            <div className="stat-label">Words</div>
            <div className="stat-value">{wordCount}</div>
          </div>
        </div>
      )}

      {/* ── 3. DECODED TEXT ── */}
      <div className="retro-card">
        <div className="retro-card-header">
          <div className="stat-label" style={{ margin: 0 }}>Detected Text</div>
        </div>

        <div className={`decoded-text-box${!decodedText ? " empty" : ""}`}>
          {decodedText || "No text decoded — try uploading a clearer Braille image"}
        </div>

        {/* Action buttons */}
        <div className="action-strip">
          <button
            className="act-btn"
            onClick={handleCopy}
            disabled={!decodedText}
          >
            {copied ? "Copied!" : "📋 Copy"}
          </button>
          <button
            className="act-btn"
            onClick={handleSpeak}
            disabled={!decodedText || speaking}
          >
            {speaking ? "Speaking…" : "🔊 Speak"}
          </button>
          <button
            className="act-btn"
            onClick={handleDownload}
            disabled={!decodedText}
          >
            💾 Download
          </button>
        </div>
      </div>

    </div>
  )
}
