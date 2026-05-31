import logo from "../assets/logo.png"

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <img src={logo} alt="TouchVision Logo" style={{ width: '52px', height: '52px', objectFit: 'contain', filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.25))' }} />
          <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.2 }}>
            <h2 style={{ margin: 0, fontFamily: 'Playfair Display', fontSize: '1.7rem', letterSpacing: '0.5px', color: '#fff' }}>
              Touch<span style={{ color: 'var(--accent-orange)' }}>Vision</span>
            </h2>
            <span style={{ fontSize: '0.68rem', letterSpacing: '2.5px', opacity: 0.75, textTransform: 'uppercase', fontWeight: 600, color: '#fff' }}>
              ⠗ Read Beyond Sight ⠗
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

