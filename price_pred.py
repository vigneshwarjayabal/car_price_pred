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
    set_bg("bgimage.jpeg")

    st.title("🚗 Used Car Price Predictor")
    st.markdown("Fill the details below to get the **predicted resale price** of your car.")

    # Load model and encoders
    model = pickle.load(open("finalmodel.pkl", "rb"))  # Load your saved model
    encoders = pickle.load(open("encoding_artifacts.pkl", "rb"))  # Load your encoding artifacts

    # Load raw model mapping data (for dynamic brand → model mapping)
    raw_data = pd.read_csv("car.csv")  # Assuming this is your cleaned car dataset

    # Get list of brands and build brand → models map
    brand_to_models = raw_data.groupby("Brand")["Model"].unique().to_dict()

    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox("Brand", sorted(brand_to_models.keys()))
        fuel = st.selectbox("Fuel Type", encoders['Fuel_Type'].classes_)
        insurance = st.selectbox("Insurance", encoders['Insurance'].classes_)
        location = st.selectbox("Location", encoders['Location'].classes_)
        ownership = st.selectbox("Ownership", encoders['Ownership'].classes_)

    with col2:
        models_for_brand = brand_to_models.get(brand, [])
        model_name = st.selectbox("Model", sorted(models_for_brand))
        transmission = st.selectbox("Transmission", encoders['Transmission'].classes_)
        kms_driven = st.number_input("Kilometers Driven", min_value=0)
        engine_disp = st.number_input("Engine Displacement (cc)", min_value=500, max_value=6000)
        seats = st.selectbox("Number of Seats", [2, 4, 5, 6, 7, 8])
        reg_year = st.number_input("Year of Registration", min_value=1990, max_value=2025)
        

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
    
    if st.button("💸 Predict Price"):
        user_input = {
            "Brand": brand,
            "Fuel_Type": fuel,
            "Insurance": insurance,
            "Location": location,
            "Model": model_name,
            "Ownership": ownership,
            "Transmission": transmission,
            "Engine_Displacement": engine_disp,
            "Kms_Driven": kms_driven,
            "Registration_Year": reg_year,
            "Seats": seats,
           
        }
    
        final_input = np.array(encode_inputs(user_input)).reshape(1, -1)
        
        # Debugging: Print the shape of the final_input to check if it matches the expected number of features
        st.write(f"Input features shape: {final_input.shape}")
    
        from babel.numbers import format_currency

        prediction = model.predict(final_input)[0]
        formatted_price = (format_currency(prediction, 'INR', locale='en_IN')/4)
        st.success(f"Predicted price for **{brand} {model_name}** is {formatted_price}")



if __name__ == "__main__":
    main()
