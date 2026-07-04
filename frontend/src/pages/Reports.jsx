import Navbar from "../components/Navbar";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
export default function Reports() {
  const data = JSON.parse(localStorage.getItem("driftResult")) || {
    features_tested: 0,
    drift_detected: 0,
    stable_features: 0,
    max_psi: 0,
    summary: [],
  };

  const downloadCSV = () => {
    const rows = [
      ["Feature", "Type", "Status"],
      ...data.summary.map((item) => [
        item.feature,
        item.type,
        item.status,
      ]),
    ];

    const csv = rows.map((row) => row.join(",")).join("\n");

    const blob = new Blob([csv], {
      type: "text/csv;charset=utf-8;",
    });

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "drift_report.csv";
    link.click();
  };
  const downloadPDF = () => {
  const doc = new jsPDF();

  doc.setFontSize(18);
  doc.text("ML Data Drift Report", 14, 20);

  doc.setFontSize(12);

  doc.text(`Features Tested : ${data.features_tested}`, 14, 35);
  doc.text(`Drift Detected : ${data.drift_detected}`, 14, 43);
  doc.text(`Stable Features : ${data.stable_features}`, 14, 51);
  doc.text(`Max PSI : ${data.max_psi}`, 14, 59);

  autoTable(doc, {
    startY: 70,
    head: [["Feature", "Type", "Status"]],
    body: data.summary.map((item) => [
      item.feature,
      item.type,
      item.status,
    ]),
  });

  doc.save("ML_Data_Drift_Report.pdf");
};

  return (
    <>
      <Navbar />

      <h1>Reports</h1>

      <div className="cards">

        <div className="card">
          <h3>Features Tested</h3>
          <h2>{data.features_tested}</h2>
        </div>

        <div className="card">
          <h3>Drift Detected</h3>
          <h2>{data.drift_detected}</h2>
        </div>

        <div className="card">
          <h3>Stable Features</h3>
          <h2>{data.stable_features}</h2>
        </div>

        <div className="card">
          <h3>Max PSI</h3>
          <h2>{data.max_psi}</h2>
        </div>

      </div>
<div
  style={{
    display: "flex",
    gap: "15px",
    marginTop: "25px",
    marginBottom: "25px",
  }}
>
  <button onClick={downloadCSV}>
    Download CSV Report
  </button>

  <button onClick={downloadPDF}>
    Download PDF Report
  </button>
</div>

      <table>
        <thead>
          <tr>
            <th>Feature</th>
            <th>Type</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {data.summary.map((item, index) => (
            <tr key={index}>
              <td>{item.feature}</td>
              <td>{item.type}</td>
              <td>{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}