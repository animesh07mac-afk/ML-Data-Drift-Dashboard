import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import ChartCard from "../components/ChartCard";
import PSIPanel from "../components/PSIPanel";

export default function Dashboard() {
  const stats = JSON.parse(localStorage.getItem("driftResult")) || {
    features_tested: 0,
    drift_detected: 0,
    stable_features: 0,
    max_psi: 0,
    summary: [],
  };

  return (
    <>
      <Navbar />

      <div className="cards">
        <StatCard
          title="Features Tested"
          value={stats.features_tested}
          color="#3b82f6"
        />

        <StatCard
          title="Drift Detected"
          value={stats.drift_detected}
          color="#ef4444"
        />

        <StatCard
          title="Stable Features"
          value={stats.stable_features}
          color="#22c55e"
        />

        <StatCard
          title="Max PSI"
          value={stats.max_psi}
          color="#f59e0b"
        />
      </div>

      <ChartCard />

      <div className="bottom-grid">
        <div className="table-section">
          <h2>Drift Summary</h2>

          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th>Type</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {stats.summary &&
                stats.summary.map((item, index) => (
                  <tr key={index}>
                    <td>{item.feature}</td>
                    <td>{item.type}</td>
                    <td
                      style={{
                        color:
                          item.status === "Drift"
                            ? "#ef4444"
                            : item.status === "Stable"
                            ? "#22c55e"
                            : "#facc15",
                      }}
                    >
                      {item.status}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>

        <PSIPanel />
      </div>
    </>
  );
}