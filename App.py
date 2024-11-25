import streamlit as st
import pandas as pd
import random

# App Configuration
st.set_page_config(page_title="VIP Sprinter and Party Bus Booking", layout="wide")

# Generate Demo Data with Images
def generate_demo_vehicles():
    images = [
        "IMG_3639.jpeg", "IMG_3649.jpeg", "IMG_3892.jpeg",
        "IMG_4336.jpeg", "IMG_4390.jpeg", "IMG_4459.jpeg", "IMG_4460.jpeg"
    ]
    vehicles = [
        {"Name": f"Sprinter {i}", "Type": "Sprinter", "Capacity": random.randint(8, 12),
         "Price/Hour": random.randint(100, 150), "Fuel Cost/Hour": random.randint(20, 30),
         "Maintenance Cost/Hour": random.randint(10, 20), "Image": random.choice(images)}
        for i in range(1, 8)
    ]
    vehicles += [
        {"Name": f"Party Bus {i}", "Type": "Party Bus", "Capacity": random.randint(20, 30),
         "Price/Hour": random.randint(200, 300), "Fuel Cost/Hour": random.randint(40, 60),
         "Maintenance Cost/Hour": random.randint(20, 30), "Image": random.choice(images)}
        for i in range(1, 9)
    ]
    return pd.DataFrame(vehicles)

# Initialize Inventory
inventory = generate_demo_vehicles()

# Helper Functions
def calculate_revenue_and_costs(df):
    df["Daily Revenue (8 hours)"] = df["Price/Hour"] * 8
    df["Daily Fuel Cost (8 hours)"] = df["Fuel Cost/Hour"] * 8
    df["Daily Maintenance Cost (8 hours)"] = df["Maintenance Cost/Hour"] * 8
    df["Daily Profit"] = df["Daily Revenue (8 hours)"] - df["Daily Fuel Cost (8 hours)"] - df["Daily Maintenance Cost (8 hours)"]
    return df

inventory = calculate_revenue_and_costs(inventory)

# Pages
def home_page():
    st.title("VIP Sprinter & Party Bus Booking")
    st.write("""
        Welcome to the VIP Sprinter and Party Bus Booking App! Manage your fleet, analyze profits, 
        view customer bookings, and more. Our app ensures smooth operations and helps you grow your business.
    """)
    st.image("https://via.placeholder.com/800x400", caption="Luxury Vehicles for Every Occasion")

def inventory_page():
    st.title("Vehicle Inventory")
    st.write("Explore your fleet with details and images:")
    for index, row in inventory.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(row["Image"], caption=row["Name"], use_column_width=True)
        with col2:
            st.write(f"**Name**: {row['Name']}")
            st.write(f"**Type**: {row['Type']}")
            st.write(f"**Capacity**: {row['Capacity']} passengers")
            st.write(f"**Price/Hour**: ${row['Price/Hour']}")
            st.write(f"**Daily Profit**: ${row['Daily Profit']:.2f}")
        st.markdown("---")

def rental_prices_page():
    st.title("Rental Pricing Overview")
    st.write("View pricing and profit potential for your fleet:")
    st.dataframe(inventory[["Name", "Type", "Capacity", "Price/Hour", "Daily Revenue (8 hours)", "Daily Profit"]])

def profit_metrics_page():
    st.title("Profit Metrics")
    st.write("Analyze your fleet's performance:")
    total_daily_revenue = inventory["Daily Revenue (8 hours)"].sum()
    total_daily_profit = inventory["Daily Profit"].sum()
    st.metric("Total Daily Revenue", f"${total_daily_revenue:,.2f}")
    st.metric("Total Daily Profit", f"${total_daily_profit:,.2f}")
    st.bar_chart(inventory.set_index("Name")["Daily Profit"])

def booking_page():
    st.title("Customer Bookings")
    st.write("Manage and view all customer bookings:")
    booking_data = pd.DataFrame({
        "Customer Name": [f"Customer {i}" for i in range(1, 11)],
        "Vehicle": random.choices(inventory["Name"], k=10),
        "Hours Booked": random.choices(range(4, 10), k=10),
        "Total Cost": [random.randint(500, 2000) for _ in range(10)]
    })
    st.dataframe(booking_data)

def add_vehicle_page():
    st.title("Add a New Vehicle")
    st.write("Use the form below to add a new vehicle to your fleet:")
    with st.form("Add Vehicle"):
        name = st.text_input("Vehicle Name")
        vehicle_type = st.selectbox("Vehicle Type", ["Sprinter", "Party Bus"])
        capacity = st.number_input("Seating Capacity", min_value=1, step=1)
        price_per_hour = st.number_input("Price per Hour ($)", min_value=50, step=10)
        fuel_cost = st.number_input("Fuel Cost per Hour ($)", min_value=5, step=5)
        maintenance_cost = st.number_input("Maintenance Cost per Hour ($)", min_value=5, step=5)
        image = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])
        submitted = st.form_submit_button("Add Vehicle")
        if submitted:
            new_vehicle = {
                "Name": name,
                "Type": vehicle_type,
                "Capacity": capacity,
                "Price/Hour": price_per_hour,
                "Fuel Cost/Hour": fuel_cost,
                "Maintenance Cost/Hour": maintenance_cost,
                "Image": image.name if image else "https://via.placeholder.com/300x200"
            }
            global inventory
            inventory = pd.concat([inventory, pd.DataFrame([new_vehicle])], ignore_index=True)
            st.success("Vehicle added successfully!")

def customer_feedback_page():
    st.title("Customer Feedback")
    st.write("View customer feedback and reviews:")
    feedback = pd.DataFrame({
        "Customer Name": [f"Customer {i}" for i in range(1, 11)],
        "Vehicle": random.choices(inventory["Name"], k=10),
        "Rating (out of 5)": random.choices(range(3, 6), k=10),
        "Feedback": random.choices([
            "Excellent service!", "Very comfortable ride.", 
            "Driver was punctual.", "Will book again.", "Loved the experience!"
        ], k=10)
    })
    st.dataframe(feedback)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home", "Inventory", "Rental Prices", "Profit Metrics", 
    "Customer Bookings", "Add a New Vehicle", "Customer Feedback"
])

# Render Pages
if page == "Home":
    home_page()
elif page == "Inventory":
    inventory_page()
elif page == "Rental Prices":
    rental_prices_page()
elif page == "Profit Metrics":
    profit_metrics_page()
elif page == "Customer Bookings":
    booking_page()
elif page == "Add a New Vehicle":
    add_vehicle_page()
elif page == "Customer Feedback":
    customer_feedback_page()
