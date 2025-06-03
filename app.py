
import streamlit as st
import numpy as np
import joblib
import trimesh

# Load the trained surrogate model
model = joblib.load("surrogate_resistance_model.pkl")

st.set_page_config(page_title="OpsimNav MVP", layout="centered")
st.title("🚢 OpsimNav – Maritime AI Surrogate Platform")
st.markdown("Upload your ship STL and enter operational parameters to estimate fuel consumption and compliance KPIs.")

# Upload STL file
uploaded_file = st.file_uploader("Upload STL File", type=["stl"])
if uploaded_file:
    mesh = trimesh.load(uploaded_file, file_type='stl')
    st.success("STL file loaded successfully.")

    # Estimate basic geometric features
    length = mesh.extents[0]
    beam = mesh.extents[1]
    draft = mesh.extents[2]

    st.write(f"📐 Estimated Dimensions from STL:")
    st.write(f"- Length: {length:.2f} m")
    st.write(f"- Beam: {beam:.2f} m")
    st.write(f"- Draft: {draft:.2f} m")

    st.markdown("---")

    # User inputs for conditions
    speed = st.slider("Ship Speed (knots)", 5.0, 25.0, 14.0)
    wave_height = st.slider("Wave Height (m)", 0.0, 5.0, 1.5)
    wave_angle = st.slider("Wave Direction Angle (°)", 0, 180, 90)
    trim_angle = st.slider("Trim Angle (°)", -2.0, 5.0, 0.0)

    # Predict resistance
    if st.button("Estimate Fuel & Compliance"):
        X_input = np.array([[length, beam, draft, speed, wave_height, wave_angle, trim_angle]])
        resistance = model.predict(X_input)[0]

        # Approximate fuel consumption (fictional formula)
        fuel_consumption = 0.00025 * resistance * speed

        # Approximate CII (fictional scaling)
        cii_score = 120 - fuel_consumption
        rating = "A" if cii_score > 90 else "B" if cii_score > 75 else "C" if cii_score > 60 else "D"

        st.success(f"⚙️ Estimated Resistance: {resistance:.2f} kN")
        st.info(f"⛽ Estimated Fuel Consumption: {fuel_consumption:.2f} tons/day")
        st.warning(f"📊 CII Rating (approx): {rating}")
