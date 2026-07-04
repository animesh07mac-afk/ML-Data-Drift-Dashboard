export default function PSIPanel() {
  const stats = JSON.parse(localStorage.getItem("driftResult")) || {
    psi_scores: [],
  };

  const getColor = (status) => {
    if (status === "No Drift") return "#22c55e";
    if (status === "Moderate Drift") return "#facc15";
    return "#ef4444";
  };

  const getWidth = (psi) => {
    return `${Math.min(psi * 100 * 3, 100)}%`;
  };

  return (
    <div className="psi-panel">
      <h2>PSI Scores</h2>

      {stats.psi_scores.length === 0 ? (
        <p style={{ color: "#94a3b8" }}>No PSI data available.</p>
      ) : (
        stats.psi_scores.map((item, index) => (
          <div className="psi-item" key={index}>
            <div className="psi-header">
              <span>{item.feature}</span>
              <span>{item.psi}</span>
            </div>

            <div className="psi-bar">
              <div
                className="psi-fill"
                style={{
                  width: getWidth(item.psi),
                  background: getColor(item.status),
                }}
              ></div>
            </div>

            <small
              style={{
                color: getColor(item.status),
              }}
            >
              {item.status}
            </small>
          </div>
        ))
      )}
    </div>
  );
}