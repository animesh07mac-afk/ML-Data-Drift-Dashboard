import os
import sys
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS

# Pehle src path add karo
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "src"
    )
)

# Ab modules import karo
from validation import run_validation
from preprocessing import preprocess, get_feature_types
from feature_engineering import run_feature_engineering
from drift import run_drift_detection
from eda import numerical_stats
app=Flask(__name__)
CORS(app)
def load_file(file):
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file)

    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload a CSV or Excel file."
        )

@app.route("/")
def home():
    return jsonify({
        "message": "ML Data Drift Backend Running 🚀",
        "status": "success"
    })
@app.route("/analyze", methods=["POST"])
def analyze():
    try:

        if "reference" not in request.files:
            return jsonify({"error": "Reference dataset missing"}), 400

        if "current" not in request.files:
            return jsonify({"error": "Current dataset missing"}), 400

        reference = request.files["reference"]
        current = request.files["current"]

        
        ref_df = load_file(reference)
        cur_df = load_file(current)
        validation=run_validation(ref_df,cur_df)
        if not validation["schema"]["schema_valid"]:
            return jsonify({
                "error":"Schema Validation Failed",
                "validation":{
                    "schema_valid":False,
                    "missing_columns":validation["schema"]["column_comparison"]["missing_in_current"],
                    "extra_columns":validation["schema"]["column_comparison"]["extra_in_current"],
                    "dtype_mismatches":validation["schema"]["dtype_mismatches"].to_dict(orient="records")
                }}),400

        ref_df=preprocess(ref_df)
        cur_df=preprocess(cur_df)

        ft=get_feature_types(ref_df)
        ref_df=run_feature_engineering(ref_df,ft["datetime"])
        cur_df=run_feature_engineering(cur_df,ft["datetime"])
        ft=get_feature_types(ref_df)

        drift_df=run_drift_detection(ref_df,cur_df,ft["numerical"],ft["categorical"])
        # ----------------------------
        # EDA
        # ----------------------------

        eda_stats = numerical_stats(
            ref_df,
            ft["numerical"]
        )

        eda = eda_stats.to_dict(orient="records")
        summary=[]

        # ----------------------------
        # PSI Scores
        # ----------------------------

        psi_scores = []

        psi_df = drift_df.dropna(subset=["psi"])

        for _, row in psi_df.iterrows():

            psi = round(float(row["psi"]), 4)

            if psi < 0.1:
                status = "No Drift"
            elif psi < 0.2:
                status = "Moderate Drift"
            else:
                status = "Significant Drift"

            psi_scores.append({
                "feature": row["feature"],
                "psi": psi,
                "status": status
            })

        drift_detected=0
        for _,row in drift_df.iterrows():
            if row["feature_type"]=="Numerical":
                if row["psi_status"]=="No Drift":
                    status="Stable"
                elif row["psi_status"]=="Moderate Drift":
                    status="Moderate"; drift_detected+=1
                else:
                    status="Drift"; drift_detected+=1
            else:
                if row["drift_status"]=="Drift Detected":
                    status="Drift"; drift_detected+=1
                else:
                    status="Stable"
            summary.append({"feature":row["feature"],"type":row["feature_type"],"status":status})

        psi_df=drift_df.dropna(subset=["psi"])
        max_psi=round(float(psi_df["psi"].max()),4) if len(psi_df) else 0

        return jsonify({
            "features_tested":int(len(drift_df)),
            "drift_detected":int(drift_detected),
            "stable_features":int(len(drift_df)-drift_detected),
            "max_psi":max_psi,
            "summary":summary,
            "psi_scores": psi_scores,
            "eda": eda,
            "validation":{
                "schema_valid":validation["schema"]["schema_valid"],
                "reference_rows":validation["ref_shape"]["rows"],
                "current_rows": validation["cur_shape"]["rows"],
                "reference_columns":validation["ref_shape"]["columns"],
                "current_columns":validation["cur_shape"]["columns"],
                "reference_duplicates":validation["ref_duplicates"]["duplicate_rows"],
                "current_duplicates":validation["cur_duplicates"]["duplicate_rows"],
                "missing_columns":validation["schema"]["column_comparison"]["missing_in_current"],
                "extra_columns":validation["schema"]["column_comparison"]["extra_in_current"],
                "dtype_mismatches":validation["schema"]["dtype_mismatches"].to_dict(orient="records")
            }})
    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__=="__main__":
    app.run(debug=True,port=5001)