import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
import time
import tempfile

st.set_page_config(page_title="OpsimNAV", page_icon="🌊", layout="centered")

# --- Style ---
st.markdown("""
    <style>
        .main { background-color: #f4f9f9; }
        h1, h2, h3 { color: #033e8c; }
        .stButton>button { background-color: #033e8c; color: white; border-radius: 8px; }
        .stDownloadButton>button { background-color: #088395; color: white; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# --- Mock prediction logic ---
def predict_kpis(ship_type, wave, wind, engine_load, trim):
    base_speed = {"KCS": 14.0, "Bulk Carrier": 12.5, "Tanker": 11.0}
    speed = base_speed[ship_type] - 0.2 * wave - 0.1 * wind + 0.05 * (engine_load - 75) + 0.02 * trim
    fuel = 50 + (75 - engine_load) * 0.3 + wave * 1.5 + wind * 0.8
    cii = "C" if fuel > 48 else "B" if fuel < 42 else "A"
    return round(speed, 2), round(fuel, 1), cii

# --- PDF report generator ---
def generate_pdf_report(ship_type, wave, wind, engine_load, trim, speed, fuel, cii):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="OpsimNAV Compliance Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Ship Type: {ship_type}", ln=True)
    pdf.cell(200, 10, txt=f"Wave Height: {wave} m", ln=True)
    pdf.cell(200, 10, txt=f"Wind Speed: {wind} knots", ln=True)
    pdf.cell(200, 10, txt=f"Engine Load: {engine_load} %", ln=True)
    pdf.cell(200, 10, txt=f"Trim Angle: {trim} deg", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Predicted Vref: {speed} knots", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Fuel Consumption: {fuel} tons/day", ln=True)
    pdf.cell(200, 10, txt=f"CII Rating: {cii}", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- UI ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Ship_silhouette.svg/1920px-Ship_silhouette.svg.png", width=300)
st.title("OpsimNAV")
st.subheader("AI-Powered Maritime KPI Estimation & Compliance Reporting")

with st.form("input_form"):
    st.markdown("### 1. Scenario Setup")
    col1, col2 = st.columns(2)
    with col1:
        ship_type = st.selectbox("Ship Type", ["KCS", "Bulk Carrier", "Tanker"])
        engine_load = st.slider("Engine Load (%)", 50, 100, 75, 1)
        trim = st.slider("Trim Angle (°)", -2.0, 5.0, 0.0, 0.1)
    with col2:
        wave = st.slider("Wave Height (m)", 0.0, 6.0, 3.0, 0.1)
        wind = st.slider("Wind Speed (knots)", 0.0, 30.0, 15.0, 1.0)

    submitted = st.form_submit_button("🔍 Run Prediction")

if submitted:
    with st.spinner("Running AI-based prediction..."):
        time.sleep(1.5)
        speed, fuel, cii = predict_kpis(ship_type, wave, wind, engine_load, trim)

    st.markdown("### 2. Predicted Operational KPIs")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚓ Vref", f"{speed} knots")
    col2.metric("⛽ Fuel Use", f"{fuel} tons/day")
    col3.metric("🌍 CII Rating", cii)

    st.markdown("### 3. Flow Field Visualization")
    st.image("https://i.imgur.com/Vjoxbl5.jpeg", caption="Simulated Pressure Field around Ship", use_column_width=True)

    st.markdown("### 4. Performance Suggestions")
    if cii == "C":
        st.warning("Consider reducing trim by 1.5° to improve fuel efficiency.")
    if wave > 4:
        st.info("High waves detected. Reduce engine load for safety.")
    if fuel > 50:
        st.info("High fuel use. Consider streamlined hull variant.")

    st.markdown("### 5. Hull Variant Comparison")
    cols = st.columns(3)
    cols[0].image("https://i.imgur.com/yGq4LOA.jpeg", caption="Hull A – Baseline\nCII: C", use_column_width=True)
    cols[1].image("https://i.imgur.com/Dmb3Ghv.jpeg", caption="Hull B – Streamlined\nCII: B", use_column_width=True)
    cols[2].image("https://i.imgur.com/0oLwRKm.jpeg", caption="Hull C – Bulbous Bow\nCII: A", use_column_width=True)

    st.markdown("---")
    st.markdown("### 6. Compliance Report")
    pdf_path = generate_pdf_report(ship_type, wave, wind, engine_load, trim, speed, fuel, cii)
    with open(pdf_path, "rb") as file:
        st.download_button("📄 Download PDF Report", file, file_name="opsimnav_report.pdf")
