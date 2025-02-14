import streamlit as st
from streamlit_option_menu import option_menu
import base64


# Set page configuration
st.set_page_config(page_title="CarWise - Your Ultimate Car Companion", layout="wide")

# Load background image
def set_bg(image_path):
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.3);
            z-index: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background image
set_bg("https://raw.githubusercontent.com/vigneshwarjayabal/car_price_pred/main/bgimage.jpeg")

# Custom CSS for improved UI
st.markdown(
    """
    <style>
        /* Floating Card */
        .card {
            position: relative;
            margin: auto;
            margin-top: 50px;
            width: 55%;
            padding: 25px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            color: #d1e8ff; /* Light Blue for better readability */
            font-family: 'Poppins', sans-serif;
        }
        
        /* Headings */
        .card h1, .card h3 {
            color: #ff7043; /* Bright Orange for emphasis */
        }

        /* Navigation Menu */
        .css-1avcm0n {
            background: #222;
            padding: 8px;
            border-radius: 8px;
        }
        .css-1avcm0n div {
            font-size: 16px !important;
            font-weight: 600;
            color: #f8f9fa !important;
        }
        
        /* Smooth Hover Effect for Buttons */
        .stButton>button {
            width: 180px;
            height: 45px;
            font-size: 16px;
            border-radius: 8px;
            transition: 0.3s;
            background-color: #ff5722;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #ff7043 !important;
            color: white !important;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction", "Chatbot"],
    icons=["house", "car-front", "robot"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#ff7043", "font-size": "18px"},
        "nav-link": {"color": "#f8f9fa", "font-size": "16px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#ff7043"},
    }
)

if selected in ["Home", "Price Prediction"]:
    set_bg("C:/study material/guvi/project/car_pred/bgimage.jpeg")


# Home Page Content
if selected == "Home":
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="card">
            <h1>🚗 Welcome to <span style="color:#ff7043;">CarWise</span> – Your Ultimate Car Companion!</h1>
            <p>Revolutionize the way you buy used cars with AI-powered price predictions and a smart chatbot.</p>
            <h3>🔍 Smart Price Predictions</h3>
            <p>Get market-based car price estimates—no more guesswork, just data-driven insights!</p>
            <h3>🤖 Your Personal Car Advisor</h3>
            <p>Tell our AI chatbot what you need, and get tailored car recommendations instantly!</p>
            <h3>🌟 Why Choose CarWise?</h3>
            <p>✅ <b>No hidden fees</b> – Enjoy unlimited access.<br>
               ✅ <b>Seamless experience</b> – Works on any device.<br>
               ✅ <b>Expert insights</b> – Stay ahead in the car market.</p>
            <p><b>Join CarWise today and drive smarter! 🚀</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Price Prediction": 
    import price_pred
    price_pred.main()

elif selected == "Chatbot":
    st.markdown("<style>.stApp { background-image: none !important; }</style>", unsafe_allow_html=True)
    import chatbot
    chatbot.main()
