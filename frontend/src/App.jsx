import Sidebar from "./components/Sidebar";
import { Routes, Route } from "react-router-dom";
import Validation from "./pages/Validation";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import EDA from "./pages/EDA";
import Reports from "./pages/Reports";




export default function App() {
  return (
    <div className="container">
      <Sidebar />

      <main className="content">
        <Routes>
          {/* Upload Page */}
          <Route path="/" element={<Upload />} />

          {/* Dashboard */}
          <Route path="/dashboard" element={<Dashboard />} />

          {/* Future Pages */}
          <Route path="/validation" element={<Validation />} />
          <Route path="/eda" element={<EDA />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </main>
    </div>
  );
}