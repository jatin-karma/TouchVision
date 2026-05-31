export default function ControlPanel({ onCapture, onFileSelect, fileInputRef, loading }) {
  return (
    <div className="control-panel">
      <button
        onClick={onCapture}
        disabled={loading}
        className="capture-button"
        style={{
          backgroundColor: loading ? "#9ca3af" : "#2563eb",
          color: "white",
          padding: "15px 30px",
          fontSize: "1.1rem",
          fontWeight: "bold",
          border: "none",
          borderRadius: "8px",
          cursor: loading ? "not-allowed" : "pointer",
          transition: "all 0.3s",
          width: "100%",
        }}
      >
        {loading ? "📸 Reading Braille..." : "📸 Read from Camera"}
      </button>

      <div className="divider" style={{ margin: "15px 0", textAlign: "center", color: "#999", fontSize: "0.9rem" }}>
        — OR —
      </div>

      <div className="file-upload-section">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={onFileSelect}
          style={{ display: "none" }}
        />
        <button
          onClick={() => fileInputRef?.current?.click()}
          disabled={loading}
          style={{
            backgroundColor: loading ? "#9ca3af" : "#10b981",
            color: "white",
            padding: "15px 30px",
            fontSize: "1.1rem",
            fontWeight: "bold",
            border: "none",
            borderRadius: "8px",
            cursor: loading ? "not-allowed" : "pointer",
            transition: "all 0.3s",
            width: "100%",
          }}
        >
          {loading ? "📄 Processing..." : "📄 Upload Image"}
        </button>
      </div>

      <div className="instructions">
        <h3>📋 Instructions</h3>
        <ol>
          <li>Position your device camera over the Braille document</li>
          <li>Ensure good lighting and minimal shadows</li>
          <li>Click "Read Braille" to process the image</li>
          <li>The decoded text will appear below</li>
          <li>Click "Speak Text" to hear it read aloud</li>
        </ol>
      </div>

      <div className="tips">
        <h3>💡 Tips for Best Results</h3>
        <ul>
          <li>Use natural or bright lighting</li>
          <li>Keep the document flat and in focus</li>
          <li>Avoid shadows and reflections</li>
          <li>Position the camera perpendicular to the paper</li>
          <li>Ensure the entire Braille section is visible</li>
        </ul>
      </div>
    </div>
  )
}

const styles = `
.control-panel {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-panel h3 {
  font-size: 1rem;
  color: #1e40af;
  margin-bottom: 10px;
}

.control-panel ol,
.control-panel ul {
  margin-left: 20px;
  color: #374151;
  line-height: 1.6;
}

.control-panel li {
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.instructions,
.tips {
  background-color: #f0f9ff;
  border-left: 4px solid #2563eb;
  padding: 15px;
  border-radius: 6px;
}

.tips {
  border-left-color: #10b981;
  background-color: #f0fdf4;
}
`

if (typeof document !== 'undefined') {
  const styleSheet = document.createElement("style")
  styleSheet.textContent = styles
  document.head.appendChild(styleSheet)
}
