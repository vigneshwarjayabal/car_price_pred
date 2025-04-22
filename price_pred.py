import streamlit as st
import numpy as np
import pandas as pd
import pickle
import base64
import os

def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

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
    model_car=load_model("RandomForestRegressor.pkl")

    encoder_city=load_model("encoder_city.pkl")
    encoder_model=load_model("encoder_model.pkl")
    encoder_insurance=load_model("encoder_insurance.pkl")
    encoder_fuel_type=load_model("encoder_fuel_type.pkl")
    encoder_transmission=load_model("encoder_transmission.pkl")
    encoder_ownership=load_model("encoder_ownership.pkl")

    df=pd.read_csv("Final_UsedCars_Data.csv")
    categorical_features = ["city", "model", "insurance", "fuel_type", "transmission", "ownership"]
    dropdown_options = {feature: df[feature].unique().tolist() for feature in categorical_features}


    col1, col2 = st.columns(2)

    with col1:
        city_select = st.selectbox("Select City", dropdown_options["city"])
        city=encoder_city.transform([[city_select]])[0][0]
        model_select = st.selectbox("Select Car Model", dropdown_options["model"])
        model=encoder_model.transform([[model_select]])[0][0]
        insurance_select = st.selectbox("Insurance Type", dropdown_options["insurance"])
        insurance=encoder_insurance.transform([[insurance_select]])[0][0]
        fuel_type_select = st.selectbox("Fuel Type", dropdown_options["fuel_type"])
        fuel_type=encoder_fuel_type.transform([[fuel_type_select]])[0][0]
        transmission_select = st.selectbox("Transmission Type", dropdown_options["transmission"])
        transmission=encoder_transmission.transform([[transmission_select]])[0][0]
        ownership_select = st.selectbox("Ownership Count", dropdown_options["ownership"])
        ownership=encoder_ownership.transform([[ownership_select]])[0][0]


    with col2:
        seats = st.number_input("Enter Seat Capacity", min_value=2, max_value=10, value=5)
        kms_driven = st.number_input("Enter KM Driven", min_value=1000, value=10000)
        year_of_manufacture = st.number_input("Manufacturing Year", min_value=1900, value=2015)
        engine = st.number_input("Enter Engine CC", min_value=500, value=1200)
        power = st.number_input("Enter Power (HP)", min_value=10.0, value=100.0)
        mileage = st.number_input("Enter Mileage (kmpl)", min_value=5.0, value=15.0)

    
    # Before prediction, print the shape of final_input
    if st.button("💸 Predict Price"):
        input_data = {"city":city, "model":model,"insurance": insurance,"fuel_type" :fuel_type,"seats": seats,"kms_driven" :kms_driven, 
                                "transmission":transmission,"year_of_manufacture": year_of_manufacture, "engine":engine, "power":power,"mileage": mileage,"ownership": ownership}
        input_df=pd.DataFrame([input_data])
        # Call prediction function
        predicted_price = model_car.predict(input_df)

        st.success(f"Predicted price for **{model}** is ₹ {predicted_price[0]:,.2f}")


if __name__ == "__main__":
    main()
