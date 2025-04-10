import streamlit as st
import numpy as np
import pandas as pd
import base64
import os
import xgboost as xgb
import pickle

# Function to set a background image
def set_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                padding-top: 100px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Background image not found!")

# Function to safely encode categorical values
def encode_value(encoder, value):
    if encoder is None:
        return -1
    return encoder.transform([value])[0] if value in encoder.classes_ else -1

def main():
    st.set_page_config(page_title="Car Price Predictor", layout="wide")
    set_bg("bgimage.jpeg")

    st.title("🚘 Car Price Prediction")
    st.markdown("Enter car details below to predict the estimated resale price.")

    # Load model and encoders
    try:
        model = xgb.XGBRegressor()
        model.load_model("model1.pkl")

        with open("label_encoders1.pkl", "rb") as file:
            label_encoders = pickle.load(file)
        label_encoders = {k.lower(): v for k, v in label_encoders.items()}
    except Exception as e:
        st.error(f"Failed to load model or encoders: {e}")
        return

    # Load dataset
    try:
        df = pd.read_csv("car_details2.csv")
        df.columns = df.columns.str.lower()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return

    # Get unique dropdown values
    brand_options = sorted(df["brand"].dropna().astype(str).unique())
    fuel_options = sorted(df["fuel_type"].dropna().astype(str).unique())
    insurance_options = sorted(df["insurance"].dropna().astype(str).unique())
    location_options = sorted(df["location"].dropna().astype(str).unique())
    ownership_options = sorted(df["ownership"].dropna().astype(str).unique())
    transmission_options = sorted(df["transmission"].dropna().astype(str).unique())

    # Input form
    with st.form("car_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            brand = st.selectbox("Brand", brand_options)
            filtered_models = df[df["brand"] == brand]["model"].dropna().astype(str).unique().tolist()
            model_selected = st.selectbox("Model", filtered_models)
            fuel_type = st.selectbox("Fuel Type", fuel_options)
            insurance = st.selectbox("Insurance", insurance_options)
            location = st.selectbox("Location", location_options)

        with col2:
            ownership = st.selectbox("Ownership Type", ownership_options)
            transmission = st.selectbox("Transmission Type", transmission_options)
            engine_displacement = st.number_input("Engine Displacement (cc)", 500, 7000, step=1)
            kms_driven = st.number_input("Kilometers Driven", 0, 500000, step=100)
            registration_year = st.number_input("Registration Year", 1990, 2025, step=1)
            seats = st.number_input("Number of Seats", 2, 9, step=1)

        submitted = st.form_submit_button("Predict Price 💰")

    if submitted:
        try:
            input_array = np.array([[
                encode_value(label_encoders.get("brand"), brand),
                engine_displacement,
                encode_value(label_encoders.get("fuel_type"), fuel_type),
                encode_value(label_encoders.get("insurance"), insurance),
                kms_driven,
                encode_value(label_encoders.get("location"), location),
                encode_value(label_encoders.get("model"), model_selected),
                encode_value(label_encoders.get("ownership"), ownership),
                registration_year,
                seats,
                encode_value(label_encoders.get("transmission"), transmission)
            ]])

            prediction = model.predict(input_array)[0]
            st.success(f"💰 Estimated Price for {brand} {model_selected}: ₹{round(prediction, 2)}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

# Run the app
if __name__ == "__main__":
    main()
