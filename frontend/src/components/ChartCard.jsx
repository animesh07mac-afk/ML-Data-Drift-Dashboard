import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

export default function ChartCard() {
  const stats = JSON.parse(localStorage.getItem("driftResult")) || {
    features_tested: 0,
    drift_detected: 0,
    stable_features: 0,
  };

  const data = [
    {
      name: "Features Tested",
      value: stats.features_tested,
      color: "#3b82f6",
    },
    {
      name: "Drift",
      value: stats.drift_detected,
      color: "#ef4444",
    },
    {
      name: "Stable",
      value: stats.stable_features,
      color: "#22c55e",
    },
  ];

  return (
    <div className="chart-card">
      <h2>Dataset Drift Overview</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid stroke="#334155" strokeDasharray="3 3" />

          <XAxis dataKey="name" stroke="#94a3b8" />

          <YAxis stroke="#94a3b8" />

          <Tooltip />

          <Bar dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={entry.color}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}