import spacy
from database import get_car_recommendations
import subprocess

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

# Define brand names (including multi-word brands)
car_brands = [
    "maruti", "land rover", "honda", "skoda", "hyundai", "mg", "bmw",
    "kia", "jeep", "mercedes benz", "toyota", "ford", "mahindra",
    "audi", "volkswagen", "tata", "renault", "nissan", "jaguar",
    "porsche", "mini cooper", "volvo", "mitsubishi", "chevrolet",
    "datsun", "fiat", "lexus", "bentley", "force", "maserati", "isuzu",
    "citroen"
]

# Convert to lowercase for case-insensitive matching
car_brands = [brand.lower() for brand in car_brands]

# Function to format price with Indian numeral system
def format_indian_price(price):
    price_str = f"{price:,}"
    parts = price_str.split(",")
    if len(parts) > 2:
        parts[0] = parts[0] + parts[1]
        del parts[1]
    return ",".join(parts)

# Function to extract car preferences
def extract_car_preferences(user_input):
    doc = nlp(user_input.lower())
    filters = {
        "brand": None, "engine_displacement": None, "fuel_type": None, "insurance": None,
        "kms_driven": None, "location": None, "model": None, "ownership": None,
        "price": None, "registration_year": None, "seats": None, "transmission": None
    }

    words = user_input.lower().split()

    # Detect multi-word brands
    for brand in car_brands:
        if brand in user_input.lower():
            filters["brand"] = brand.title()  # Title case for better formatting
            break

    for token in doc:
        text = token.text
        if text in ['mumbai', 'chennai', 'gurgaon', 'coimbatore', 'tiruchirappalli',
                    'new delhi', 'noida', 'bangalore', 'hyderabad', 'chandigarh',
                    'mohali', 'kochi', 'madurai', 'jaipur', 'thiruvananthapuram']:
            filters["location"] = text.title()
        elif text in ["manual", "automatic"]:
            filters["transmission"] = text.capitalize()
        elif text in ["petrol", "diesel", "electric", "cng", "lpg"]:
            filters["fuel_type"] = text.capitalize()
        elif text in ["first", "second", "third", "fourth"]:
            filters["ownership"] = text.capitalize() + " Owner"
        elif text in ["expired", "comprehensive", "third party", "zero dep"]:
            filters["insurance"] = text.title()
        elif text.isdigit():
            num = int(text)
            if num > 1900 and num < 2025:
                filters["registration_year"] = num
            elif num > 5000:
                filters["kms_driven"] = num
            elif num < 20:
                if "seater" in words or "seats" in words:
                    filters["seats"] = num
            else:
                filters["price"] = num * 100000  

    if "lakh" in words:
        for i, word in enumerate(words):
            if word.isdigit() and i < len(words) - 1 and words[i + 1] == "lakh":
                filters["price"] = int(word) * 100000

    return filters

# Function to refine filters based on user queries
def refine_filters(user_input, previous_filters):
    default_filters = {
        "brand": None, "engine_displacement": None, "fuel_type": None, "insurance": None,
        "kms_driven": None, "location": None, "model": None, "ownership": None,
        "price": None, "registration_year": None, "seats": None, "transmission": None
    }

    refined_filters = {**default_filters, **previous_filters}
    new_filters = extract_car_preferences(user_input)
    for key, value in new_filters.items():
        if value is not None:
            refined_filters[key] = value

    return refined_filters

# Chatbot response function with proper HTML formatting
def chatbot_response(user_input, filters):
    updated_filters = refine_filters(user_input, filters)
    recommendations = get_car_recommendations(updated_filters)

    if recommendations.empty:
        return "❌ No cars found matching your criteria. Try adjusting your preferences!", updated_filters

    response = """
    <div style='background-color: #F1F8E9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>
    <b>🚗 Here are some recommended cars for you:</b><br><br>
    """

    for _, row in recommendations.iterrows():
        price_formatted = format_indian_price(row['price'])
        response += f"""
        <div style='border: 2px solid #ddd; padding: 15px; border-radius: 8px; background-color: #ffffff; margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
            <h3 style='color: #1E88E5;'>🚘 {row['brand']} {row['model']}</h3>
            <p>📍 <b>Location:</b> {row['location']}</p>
            <p>💰 <b>Price:</b> ₹{price_formatted}</p>
            <p>⛽ <b>Fuel Type:</b> {row['fuel_type']} | ⚙️ <b>Transmission:</b> {row['transmission']}</p>
            <p>🛣️ <b>Kilometers Driven:</b> {row['kms_driven']} km | 🚗 <b>Seats:</b> {row['seats']}</p>
            <p>📆 <b>Registration Year:</b> {row['registration_year']} | 🏷️ <b>Ownership:</b> {row['ownership']}</p>
        </div>
        """

    response += "</div>"
    
    return response, updated_filters
