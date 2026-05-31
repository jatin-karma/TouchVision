import { useState } from "react"

export default function SpeakButton({ text }) {
  const [speaking, setSpeaking] = useState(false)

  const handleSpeak = async () => {
    if (!text.trim()) {
      alert("No text to speak")
      return
    }

    setSpeaking(true)

    try {
      const response = await fetch("http://localhost:8000/speak", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      })

      if (!response.ok) {
        const error = await response.json()
        alert(`Error: ${error.error}`)
      }
    } catch (err) {
      alert(`Failed to speak: ${err.message}`)
    } finally {
      setSpeaking(false)
    }
  }

  return (
    <button
      onClick={handleSpeak}
      disabled={speaking}
      className="speak-button"
      style={{
        backgroundColor: speaking ? "#9ca3af" : "#10b981",
        color: "white",
        padding: "10px 20px",
        border: "none",
        borderRadius: "6px",
        cursor: speaking ? "not-allowed" : "pointer",
        fontSize: "1rem",
        fontWeight: "bold",
        transition: "all 0.3s",
        marginTop: "10px",
      }}
    >
      {speaking ? "🔊 Speaking..." : "🔊 Speak Text"}
    </button>
  )
}
