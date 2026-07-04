import Navbar from "../components/Navbar";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
export default function EDA() {
  const data = JSON.parse(localStorage.getItem("driftResult"));

  if (!data || !data.eda) {
    return (
      <>
        <Navbar />
        <div style={{ padding: "20px", color: "white" }}>
          <h2>No EDA data available.</h2>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <div style={{ padding: "20px", color: "white" }}>
        <h1>Exploratory Data Analysis</h1>
        <div className="cards">

  <div className="card">
    <h3>Numerical Features</h3>
    <h2>{data.eda.length}</h2>
  </div>

  <div className="card">
    <h3>Average Mean</h3>
    <h2>
      {(
        data.eda.reduce((sum, item) => sum + item.mean, 0) /
        data.eda.length
      ).toFixed(2)}
    </h2>
  </div>

  <div className="card">
    <h3>Highest Value</h3>
    <h2>
      {Math.max(...data.eda.map(item => item.max))}
    </h2>
  </div>

  <div className="card">
    <h3>Lowest Value</h3>
    <h2>
      {Math.min(...data.eda.map(item => item.min))}
    </h2>
  </div>

</div>
<div className="chart-card">

  <h2>Feature Mean Comparison</h2>

  <ResponsiveContainer width="100%" height={350}>
    <BarChart data={data.eda}>

      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />

      <XAxis
        dataKey="feature"
        stroke="#94a3b8"
      />

      <YAxis stroke="#94a3b8" />

      <Tooltip />

      <Bar
        dataKey="mean"
        fill="#3b82f6"
        radius={[8, 8, 0, 0]}
      />

    </BarChart>
  </ResponsiveContainer>

</div>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "20px"
          }}
        >
          <thead>
            <tr>
              <th>Feature</th>
              <th>Mean</th>
              <th>Median</th>
              <th>Std</th>
              <th>Variance</th>
              <th>Min</th>
              <th>Max</th>
              <th>Count</th>
            </tr>
          </thead>

          <tbody>
            {data.eda.map((item, index) => (
              <tr key={index}>
                <td>{item.feature}</td>
                <td>{item.mean}</td>
                <td>{item.median}</td>
                <td>{item.std}</td>
                <td>{item.variance}</td>
                <td>{item.min}</td>
                <td>{item.max}</td>
                <td>{item.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}