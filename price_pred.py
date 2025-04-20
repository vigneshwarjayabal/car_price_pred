import streamlit as st
import numpy as np
import pandas as pd
import pickle
import base64
import os

def set_bg(image_path):
    """Set background image for the Streamlit app."""
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
        st.warning("Background image not found! Ensure the file path is correct.")


def main():
    # Move this line to the very top of the function
    st.set_page_config(page_title="Car Price Predictor", layout="centered")
    
    # Background image function
    set_bg("bgimage.jpeg")

    st.title("🚗 Used Car Price Predictor")
    st.markdown("Fill the details below to get the **predicted resale price** of your car.")

    # Load model and encoders
    model = pickle.load(open("random_forest_model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))

    # Load raw model mapping data (for dynamic brand → model mapping)
    raw_data = pd.read_csv("car_details2.csv")

    # Get list of brands and build brand → models map
    brand_to_models = raw_data.groupby("brand")["model"].unique().to_dict()

    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox("Brand", sorted(brand_to_models.keys()))
        fuel = st.selectbox("Fuel Type", encoders['fuel_type'].classes_)
        insurance = st.selectbox("Insurance", encoders['insurance'].classes_)
        location = st.selectbox("Location", encoders['location'].classes_)
        ownership = st.selectbox("Ownership", encoders['ownership'].classes_)

    with col2:
        models_for_brand = brand_to_models.get(brand, [])
        model_name = st.selectbox("Model", sorted(models_for_brand))
        transmission = st.selectbox("Transmission", encoders['transmission'].classes_)
        kms_driven = st.number_input("Kilometers Driven", min_value=0)
        engine_disp = st.number_input("Engine Displacement (cc)", min_value=500, max_value=6000)
        seats = st.selectbox("Number of Seats", [2, 4, 5, 6, 7, 8])
        reg_year = st.number_input("Year of Registration", min_value=1990, max_value=2025)
        car_age = 2025 - reg_year

    # Encode inputs
    def encode_inputs(user_inputs):
        encoded = []
        for col, val in user_inputs.items():
            le = encoders.get(col)
            if le:
                try:
                    encoded.append(le.transform([val])[0])
                except:
                    encoded.append(0)  # fallback
            else:
                encoded.append(val)
        return encoded

    # Predict Button
    if st.button("💸 Predict Price"):
        user_input = {
            "brand": brand,
            "fuel_type": fuel,
            "insurance": insurance,
            "location": location,
            "model": model_name,
            "ownership": ownership,
            "transmission": transmission,
            "engine_displacement": engine_disp,
            "kms_driven": kms_driven,
            "seats": seats,
            "car_age": car_age
        }

        final_input = np.array(encode_inputs(user_input)).reshape(1, -1)
        prediction = model.predict(final_input)[0]

        st.success(f"Predicted price for **{brand} {model_name}** is ₹ {int(prediction):,}")

if __name__ == "__main__":
    main()
