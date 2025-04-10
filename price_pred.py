import streamlit as st
import pickle
import numpy as np
import pandas as pd
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

def encode_value(encoder, value):
    """Safely encode categorical values using label encoder."""
    if encoder is None:
        return -1  # Default encoding if encoder is missing
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        return -1  # Assigning a default encoding for unseen values

def main():
    """Main function to run the Streamlit Car Price Prediction App."""
    # Load Model and Label Encoders
    try:
        with open("model1.pkl", "rb") as model_file:
            model = pickle.load(model_file)
        with open("label_encoders1.pkl", "rb") as encoder_file:
            label_encoders = pickle.load(encoder_file)

        # Convert label encoder keys to lowercase
        label_encoders = {k.lower(): v for k, v in label_encoders.items()}

    except FileNotFoundError:
        st.error("Model files not found! Ensure 'model.pkl' and 'label_encoders.pkl' exist.")
        return

    # Load car dataset
    try:
        df = pd.read_csv("car_details2.csv")
    except FileNotFoundError:
        st.error("Dataset file not found! Ensure 'car_details2.csv' exists.")
        return

    # Ensure column names are lowercase
    df.columns = df.columns.str.lower()

    # Unique dropdown options
    brand_options = sorted(df["brand"].dropna().astype(str).unique().tolist())
    fuel_options = sorted(df["fuel_type"].dropna().astype(str).unique().tolist())
    insurance_options = sorted(df["insurance"].dropna().astype(str).unique().tolist())
    location_options = sorted(df["location"].dropna().astype(str).unique().tolist())
    ownership_options = sorted(df["ownership"].dropna().astype(str).unique().tolist())
    transmission_options = sorted(df["transmission"].dropna().astype(str).unique().tolist())

    # Apply background image
    set_bg("bgimage.jpeg")  # Use relative path

    st.title("🚘 Car Price Prediction")
    st.write("Fill in the details below to predict the estimated price of a used car.")

    # Layout with 2 columns
    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox("Select Brand", brand_options)
        model_options = df[df["brand"] == brand]["model"].dropna().astype(str).unique().tolist()
        model = st.selectbox("Select Model", model_options)
        fuel_type = st.selectbox("Fuel Type", fuel_options)
        insurance = st.selectbox("Insurance", insurance_options)
        location = st.selectbox("Location", location_options)

    with col2:
        ownership = st.selectbox("Ownership Type", ownership_options)
        transmission = st.selectbox("Transmission Type", transmission_options)
        engine_displacement = st.number_input("Engine Displacement (cc)", min_value=500, max_value=7000, step=1)
        kms_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, step=100)
        registration_year = st.number_input("Registration Year", min_value=1990, max_value=2025, step=1)
        seats = st.number_input("Number of Seats", min_value=2, max_value=9, step=1)
    
    # Get the first model name for the selected brand
    model_name = df[df["brand"] == brand]["model"].dropna().unique()
    model_name = model_name[0] if len(model_name) > 0 else "Unknown Model"

    # Convert Selected Values to Encoded Values (Handles missing encoders safely)
    brand_encoded = encode_value(label_encoders.get("brand"), brand)
    fuel_type_encoded = encode_value(label_encoders.get("fuel_type"), fuel_type)
    insurance_encoded = encode_value(label_encoders.get("insurance"), insurance)
    location_encoded = encode_value(label_encoders.get("location"), location)
    model_encoded = encode_value(label_encoders.get("model"), model_name)
    ownership_encoded = encode_value(label_encoders.get("ownership"), ownership)
    transmission_encoded = encode_value(label_encoders.get("transmission"), transmission)

    # Prepare input array
    input_data = np.array([[brand_encoded,engine_displacement, fuel_type_encoded, insurance_encoded, kms_driven, 
                             location_encoded, model_encoded, ownership_encoded, registration_year, seats, transmission_encoded]])

    # Predict button
    if st.button("Predict Price 💰"):
        prediction = model.predict(input_data)[0]
        st.success(f"🚗 Estimated Price for {brand} {model_name}: ₹{round(prediction, 2)}")  

# Run the app
if __name__ == "__main__":
    main()
