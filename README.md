# 📊 ML Data Drift Detection Dashboard

An intermediate-level Machine Learning project that automatically detects **data drift** between a **Reference Dataset** and a **Current Dataset** for **any structured tabular CSV dataset**.

---

## 🚀 Features

| Module | Description |
|---|---|
| **Data Validation** | Shape, schema, missing values, duplicate detection |
| **Preprocessing** | Deduplication, missing-value imputation, feature-type detection |
| **Feature Engineering** | Automatic datetime decomposition, age computation from DOB |
| **EDA** | Descriptive stats + histogram, KDE, box plot, bar charts |
| **Drift Detection** | KS Test + PSI (numerical) · Chi-Square Test (categorical) |
| **Report** | Downloadable CSV & Excel drift reports |
| **Dashboard** | Interactive Streamlit app with drag-and-drop CSV upload |

---

## 📁 Project Structure

```
ML-Data-Drift-Dashboard/
│
├── data/
│   ├── reference.csv          # Sample reference dataset
│   └── current.csv            # Sample current dataset (with drift)
│
├── notebooks/
│   ├── 01_Data_Validation.ipynb
│   ├── 02_Preprocessing_Feature_Engineering.ipynb
│   ├── 03_EDA.ipynb
│   └── 04_Data_Drift.ipynb
│
├── src/
│   ├── validation.py          # Module 1 — Data Validation
│   ├── preprocessing.py       # Module 2 — Preprocessing
│   ├── feature_engineering.py # Module 3 — Feature Engineering
│   ├── eda.py                 # Module 4 — EDA
│   ├── drift.py               # Module 5 — Drift Detection
│   └── report.py              # Module 6 — Report Generation
│
├── app.py                     # Module 7 — Streamlit Dashboard
├── requirements.txt
├── README.md
└── reports/                   # Auto-generated drift reports
```

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ML-Data-Drift-Dashboard.git
cd ML-Data-Drift-Dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

Upload your own CSV files via the sidebar, or explore the built-in **sample loan dataset**.

---

## 📓 Notebooks

Run notebooks in order for a step-by-step walkthrough:

```bash
jupyter notebook notebooks/
```

| # | Notebook | Description |
|---|---|---|
| 1 | `01_Data_Validation.ipynb` | Schema & data quality checks |
| 2 | `02_Preprocessing_Feature_Engineering.ipynb` | Cleaning & feature extraction |
| 3 | `03_EDA.ipynb` | Statistics & visualisations |
| 4 | `04_Data_Drift.ipynb` | Drift tests & report export |

---

## 🔬 Drift Detection Methods

### Numerical Features
| Method | Description | Threshold |
|---|---|---|
| **KS Test** | Kolmogorov–Smirnov two-sample test | p-value < 0.05 → Drift |
| **PSI** | Population Stability Index | < 0.1 No Drift · 0.1–0.2 Moderate · > 0.2 Significant |

### Categorical Features
| Method | Description | Threshold |
|---|---|---|
| **Chi-Square Test** | Tests independence of distributions | p-value < 0.05 → Drift |

---

## 🌐 Using Your Own Dataset

The project works with **any structured tabular CSV dataset**.

1. Place your files in `data/reference.csv` and `data/current.csv`, **or**
2. Upload them directly in the Streamlit sidebar.

No column names need to be configured — all feature types are detected automatically.

---

## 📦 Dependencies

```
pandas          Data manipulation
numpy           Numerical computing
matplotlib      Plotting
seaborn         Statistical visualisations
scipy           KS Test, Chi-Square Test
streamlit       Interactive web dashboard
openpyxl        Excel report export
scikit-learn    (optional utilities)
jupyter         Notebook environment
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋 Author

Built as an intermediate ML portfolio project demonstrating modular Python design, statistical testing, and interactive data apps.
