
import streamlit as st
import pandas as pd
import random
from fpdf import FPDF

# Mock function to simulate predictions
def predict_kpis(ship_type, wave, wind, engine_load, trim):
    base_speed = {"KCS": 14.0, "Bulk Carrier": 12.5, "Tanker": 11.0}
    speed = base_speed[ship_type] - 0.2 * wave - 0.1 * wind + 0.05 * (engine_load - 75) + 0.02 * trim
    fuel = 50 + (75 - engine_load) * 0.3 + wave * 1.5 + wind * 0.8
    cii = "C" if fuel > 48 else "B" if fuel < 42 else "A"
    return round(speed, 2), round(fuel, 1), cii

# PDF report generator
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
    pdf.output("/mnt/data/opsimnav_report.pdf")

# App title
st.title("OpsimNAV - AI-Driven Maritime KPI Estimation")

st.header("1. Scenario Setup")

ship_type = st.selectbox("Select Ship Type", ["KCS", "Bulk Carrier", "Tanker"])
wave = st.slider("Wave Height (m)", 0.0, 6.0, 3.0, 0.1)
wind = st.slider("Wind Speed (knots)", 0.0, 30.0, 15.0, 1.0)
engine_load = st.slider("Engine Load (%)", 50, 100, 75, 1)
trim = st.slider("Trim Angle (°)", -2.0, 5.0, 0.0, 0.1)

if st.button("Run Prediction"):
    speed, fuel, cii = predict_kpis(ship_type, wave, wind, engine_load, trim)

    st.header("2. Predicted KPIs")
    st.metric("Predicted Vref", f"{speed} knots")
    st.metric("Fuel Consumption", f"{fuel} tons/day")
    st.metric("CII Rating", cii)

    st.header("3. Report Generator")
    generate_pdf_report(ship_type, wave, wind, engine_load, trim, speed, fuel, cii)
    with open("/mnt/data/opsimnav_report.pdf", "rb") as file:
        st.download_button("📄 Download Compliance Report", file, file_name="opsimnav_report.pdf")
