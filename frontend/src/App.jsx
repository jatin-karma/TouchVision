import { useState, useRef, useCallback } from "react"
import CameraFeed from "./components/CameraFeed"
import ResultSection from "./components/ResultSection"
import Sidebar from "./components/Sidebar"
import brandImg from "./assets/brand.jpg"

export default function App() {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [dragOver, setDragOver] = useState(false)

  const [showCameraModal, setShowCameraModal] = useState(false)

  const videoRef = useRef(null)
  const fileInputRef = useRef(null)

  const sendToBackend = async (file, previewUrl) => {
    // ... no changes here
    setLoading(true)
    setError("")

    // Create a temporary scan object while loading
    const tempId = Date.now().toString()
    const newScan = {
      id: tempId,
      filename: file.name,
      uploadedImage: previewUrl,
      annotatedImage: "",
      decodedText: "",
      dotCount: 0,
      cellCount: 0,
      confidence: 0,
      loading: true,
    }
    
    // Add to top of list
    setScans(prev => [newScan, ...prev])

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        setError(errData.error || `Server error: ${res.status}`)
        // Remove failed scan
        setScans(prev => prev.filter(s => s.id !== tempId))
      } else {
        const data = await res.json()
        setScans(prev => prev.map(s => s.id === tempId ? {
          ...s,
          loading: false,
          decodedText: data.text || "",
          confidence: data.confidence || 0,
          dotCount: data.dots_detected || 0,
          cellCount: data.cells_found || 0,
          annotatedImage: data.annotated_image || ""
        } : s))
      }
    } catch (err) {
      setError(`Cannot reach backend. (${err.message})`)
      setScans(prev => prev.filter(s => s.id !== tempId))
    } finally {
      setLoading(false)
    }
  }

  const handleFileSelect = async (files) => {
    if (!files || files.length === 0) return
    
    // Process all files in parallel
    Array.from(files).forEach(file => {
      if (!file.type.startsWith("image/")) return
      
      const reader = new FileReader()
      reader.onload = (e) => {
        sendToBackend(file, e.target.result)
      }
      reader.readAsDataURL(file)
    })
  }

  const handleInputChange = (e) => handleFileSelect(e.target.files)

  const onDragOver  = useCallback((e) => { e.preventDefault(); setDragOver(true)  }, [])
  const onDragLeave = useCallback(()  => setDragOver(false), [])
  const onDrop      = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    handleFileSelect(e.dataTransfer.files)
  }, [])

  const captureAndPredict = async () => {
    if (!videoRef.current) { setError("Camera not ready"); return }

    const canvas = document.createElement("canvas")
    canvas.width  = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    canvas.getContext("2d").drawImage(videoRef.current, 0, 0)

    canvas.toBlob(async (blob) => {
      if (!blob) { setError("Failed to capture frame"); return }
      const previewUrl = URL.createObjectURL(blob)
      const file = new File([blob], "camera_frame.jpg", { type: "image/jpeg" })
      setShowCameraModal(false) // Close modal
      await sendToBackend(file, previewUrl)
    }, "image/jpeg")
  }

  const removeScan = (id) => {
    setScans(prev => prev.filter(s => s.id !== id))
  }

  return (
    <div className="app-container">
      <Sidebar />

      <main className="main-content">
        <header className="welcome-header">
          {/* Left: Text + Buttons */}
          <div className="welcome-text">
            <p className="welcome-eyebrow">⠃⠗⠁⠊⠇⠇⠑ — Braille AI Reader</p>
            <h1>Welcome Back!</h1>
            <p className="welcome-sub">Instantly decode Braille documents using AI.<br/>Scan or upload an image to get started.</p>
            
            <div style={{ display: 'flex', gap: '16px', marginTop: '28px', flexWrap: 'wrap' }}>
              <button className="theme-action-btn primary" onClick={() => setShowCameraModal(true)}>
                <span>📷</span> Scan Document
              </button>
              <button className="theme-action-btn secondary" onClick={() => fileInputRef.current?.click()}>
                <span>📤</span> Upload Image
              </button>
            </div>
          </div>

          {/* Right: Brand image */}
          <div className="welcome-brand">
            <img src={brandImg} alt="TouchVision — Read Beyond Sight" />
          </div>
        </header>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          style={{ display: "none" }}
          onChange={handleInputChange}
        />

        {/* ── Camera Popup Modal ── */}
        {showCameraModal && (
          <div style={{
            position: 'fixed', inset: 0, zIndex: 100,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            backgroundColor: 'rgba(0,0,0,0.8)'
          }}>
            <div style={{
              backgroundColor: 'var(--bg-card)', padding: '24px',
              borderRadius: '24px', maxWidth: '600px', width: '90%',
              display: 'flex', flexDirection: 'column', gap: '20px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ margin: 0, fontFamily: 'Playfair Display', fontSize: '1.4rem' }}>Scan Braille</h3>
                <button 
                  onClick={() => setShowCameraModal(false)}
                  style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: 'var(--text-dark)' }}
                >
                  ×
                </button>
              </div>
              
              <div style={{ width: '100%', borderRadius: '16px', overflow: 'hidden', backgroundColor: '#000' }}>
                <CameraFeed videoRef={videoRef} />
              </div>
              
              <button 
                className="theme-action-btn primary" 
                style={{ width: '100%', justifyContent: 'center', padding: '16px' }}
                onClick={captureAndPredict}
              >
                📸 Capture Image
              </button>
            </div>
          </div>
        )}

        {error && (
          <div style={{ backgroundColor: "#F8D7DA", color: "#721C24", padding: "16px", borderRadius: "12px", marginTop: "24px" }}>
            ⚠️ {error}
          </div>
        )}

        {/* ── Recent Scans Grid ── */}
        {scans.length > 0 && (
          <div className="scans-container" style={{ marginTop: '48px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <h2 style={{ fontFamily: 'Playfair Display', fontSize: '1.8rem' }}>Recent Scans</h2>
              <button 
                onClick={() => setScans([])}
                style={{ background: 'transparent', border: 'none', color: 'var(--accent-rust)', cursor: 'pointer', fontWeight: 600 }}
              >
                Clear All
              </button>
            </div>
            
            <div className="scans-list" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
              {scans.map(scan => (
                <ResultSection
                  key={scan.id}
                  scan={scan}
                  onRemove={() => removeScan(scan.id)}
                />
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
