export default function StatCard({ title, value, color }) {
  return (
    <div className="card">

      <h4>{title}</h4>

      <h1 style={{ color }}>{value}</h1>

    </div>
  );
}