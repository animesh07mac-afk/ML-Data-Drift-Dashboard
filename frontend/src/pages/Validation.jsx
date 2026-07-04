import Navbar from "../components/Navbar";

export default function Validation() {
  const data = JSON.parse(localStorage.getItem("driftResult"));

  if (!data || !data.validation) {
    return (
      <>
        <Navbar />
        <div style={{ color: "white" }}>
          <h2>No validation data available.</h2>
        </div>
      </>
    );
  }

  const v = data.validation;

  return (
    <>
      <Navbar />

      <div style={{ padding: "20px", color: "white" }}>
        <h1>Validation Report</h1>
        <div
  style={{
    background: v.schema_valid ? "#052e16" : "#3f0d0d",
    borderLeft: v.schema_valid
      ? "5px solid #22c55e"
      : "5px solid #ef4444",
    padding: "18px",
    borderRadius: "12px",
    margin: "25px 0",
  }}
>
  <h2>
    {v.schema_valid
      ? "✅ Validation Successful"
      : "❌ Validation Failed"}
  </h2>

  <p style={{ marginTop: "8px", color: "#cbd5e1" }}>
    {v.schema_valid
      ? "Reference and Current datasets have compatible schema."
      : "Reference and Current datasets are not compatible."}
  </p>
</div>

        <div
          style={{
            display: "grid",
           gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
            marginTop: "30px",
          }}
        >
          <div className="card">
            <h3>Schema</h3>
            <h2>{v.schema_valid ? "✅ Valid" : "❌ Invalid"}</h2>
          </div>

          <div className="card">
            <h3>Reference Rows</h3>
            <h2>{v.reference_rows}</h2>
          </div>

          <div className="card">
            <h3>Current Rows</h3>
            <h2>{v.current_rows}</h2>
          </div>

          <div className="card">
            <h3>Reference Columns</h3>
            <h2>{v.reference_columns}</h2>
          </div>

          <div className="card">
            <h3>Current Columns</h3>
            <h2>{v.current_columns}</h2>
          </div>

          <div className="card">
            <h3>Reference Duplicates</h3>
            <h2>{v.reference_duplicates}</h2>
          </div>

          <div className="card">
            <h3>Current Duplicates</h3>
            <h2>{v.current_duplicates}</h2>
          </div>
        </div>

        <br />

        <div className="bottom-grid">

  <div className="table-section">

    <h2>Missing Columns</h2>

    {v.missing_columns.length === 0 ? (
      <p style={{ color: "#22c55e" }}>✔ No Missing Columns</p>
    ) : (
      <ul>
        {v.missing_columns.map((col) => (
          <li key={col}>{col}</li>
        ))}
      </ul>
    )}

    <br />

    <h2>Extra Columns</h2>

    {v.extra_columns.length === 0 ? (
      <p style={{ color: "#22c55e" }}>✔ No Extra Columns</p>
    ) : (
      <ul>
        {v.extra_columns.map((col) => (
          <li key={col}>{col}</li>
        ))}
      </ul>
    )}

  </div>

  <div className="table-section">

    <h2>Datatype Mismatches</h2>

    {v.dtype_mismatches.length === 0 ? (
      <p style={{ color: "#22c55e" }}>
        ✔ No Datatype Mismatches
      </p>
    ) : (
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Reference</th>
            <th>Current</th>
          </tr>
        </thead>

        <tbody>
          {v.dtype_mismatches.map((item, index) => (
            <tr key={index}>
              <td>{item.column}</td>
              <td>{item.ref_dtype}</td>
              <td>{item.cur_dtype}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}

  </div>

</div>
        {v.dtype_mismatches.length === 0 ? (
          <p>None</p>
        ) : (
          <table border="1" cellPadding="10">
            <thead>
              <tr>
                <th>Column</th>
                <th>Reference</th>
                <th>Current</th>
              </tr>
            </thead>

            <tbody>
              {v.dtype_mismatches.map((item, index) => (
                <tr key={index}>
                  <td>{item.column}</td>
                  <td>{item.ref_dtype}</td>
                  <td>{item.cur_dtype}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}