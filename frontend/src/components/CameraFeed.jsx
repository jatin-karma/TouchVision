import { useEffect } from "react"

export default function CameraFeed({ videoRef }) {
  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" },
          audio: false,
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.play().catch(() => {})
        }
      } catch (err) {
        console.warn("Camera unavailable:", err.message)
      }
    }

    initCamera()

    return () => {
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(t => t.stop())
      }
    }
  }, [videoRef])

  return (
    <video
      ref={videoRef}
      autoPlay
      playsInline
      muted
    />
  )
}
