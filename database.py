import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_car_recommendations(filters):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    query = "SELECT * FROM car_details WHERE 1=1"
    params = []

    if filters["brand"]:
        query += " AND brand = %s"
        params.append(filters["brand"])
    if filters["location"]:
        query += " AND location = %s"
        params.append(filters["location"])
    if filters["fuel_type"]:
        query += " AND fuel_type = %s"
        params.append(filters["fuel_type"])
    if filters["transmission"]:
        query += " AND transmission = %s"
        params.append(filters["transmission"])
    if filters["ownership"]:
        query += " AND ownership = %s"
        params.append(filters["ownership"])
    if filters["insurance"]:
        query += " AND insurance = %s"
        params.append(filters["insurance"])
    if filters["kms_driven"]:
        query += " AND kms_driven <= %s"
        params.append(filters["kms_driven"])
    if filters["registration_year"]:
        query += " AND registration_year = %s"
        params.append(filters["registration_year"])
    if filters["price"]:
        query += " AND price <= %s"  # Ensure price filtering works correctly
        params.append(filters["price"])
    if filters["seats"]:  # Only filter seats if explicitly mentioned
        query += " AND seats = %s"
        params.append(filters["seats"])

    print("Executing Query:", query)
    print("With Parameters:", params)


    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    cursor.close()
    conn.close()
    return df
