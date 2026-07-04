import {
  LayoutDashboard,
  Upload,
  CheckCircle2,
  BarChart3,
  FileText,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    title: "Upload Dataset",
    path: "/",
    icon: <Upload size={20} />,
  },
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: <LayoutDashboard size={20} />,
  },
  {
    title: "Validation",
    path: "/validation",
    icon: <CheckCircle2 size={20} />,
  },
  {
    title: "EDA",
    path: "/eda",
    icon: <BarChart3 size={20} />,
  },
  {
    title: "Reports",
    path: "/reports",
    icon: <FileText size={20} />,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: <Settings size={20} />,
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
     <div className="logo">
  <h2>DriftScope</h2>
  <p>ML Data Drift Dashboard</p>
</div>
      <nav>
        {menuItems.map((item) => (
          <NavLink
            key={item.title}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
          >
            {item.icon}
            <span>{item.title}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-footer">
  <p>Version 1.0</p>
  <small>Built with React + Flask</small>
</div>
    </aside>
  );
}