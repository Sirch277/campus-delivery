import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Dorm Delivery Test",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define test pages that mimic your actual structure
def customer_dashboard():
    st.header("📊 Customer Dashboard")
    st.write("Active Deliveries: 3")
    st.write("Completed Orders: 12")
    st.button("📦 Create New Delivery")
    
def create_delivery():
    st.header("📦 Create Delivery")
    st.text_input("Pickup Location")
    st.text_input("Dropoff Location")
    st.text_area("Item Description")
    st.button("Submit Delivery Request")
    
def track_delivery():
    st.header("🚚 Track Delivery")
    st.selectbox("Select Delivery", ["Delivery #123", "Delivery #124", "Delivery #125"])
    st.write("**Status:** In Transit 🚗")
    
def order_history():
    st.header("📋 Order History")
    st.dataframe({
        "Order ID": [123, 124, 125],
        "Status": ["Delivered", "In Transit", "Pending"],
        "Date": ["2024-01-15", "2024-01-14", "2024-01-13"]
    })

def rider_dashboard():
    st.header("🚴 Rider Dashboard")
    st.write("Available Tasks: 5")
    st.write("Earnings Today: $45.50")
    st.button("🔄 Refresh Tasks")

def available_tasks():
    st.header("📦 Available Tasks")
    st.write("• Delivery #201 - Dorm A to Dorm B")
    st.write("• Delivery #202 - Library to Dorm C")
    st.button("Accept Delivery #201")

# Test different navigation configurations
st.title("🚚 Dorm Delivery - Navigation Test")

# Test 1: Simple list navigation (no sections)
st.subheader("Test 1: Simple List Navigation")
pages_simple = [
    st.Page(customer_dashboard, title="Dashboard", icon="🏠"),
    st.Page(create_delivery, title="Create Delivery", icon="📦"),
    st.Page(track_delivery, title="Track Delivery", icon="🚚"),
    st.Page(order_history, title="Order History", icon="📋"),
]

position1 = st.radio("Navigation Position:", ["sidebar", "top", "hidden"], key="pos1", horizontal=True)
current_page1 = st.navigation(pages_simple, position=position1)
current_page1.run()

st.markdown("---")

# Test 2: Section-based navigation (like your customer/rider structure)
st.subheader("Test 2: Section-based Navigation")

pages_sections = {
    "Customer": [
        st.Page(customer_dashboard, title="Dashboard", icon="🏠"),
        st.Page(create_delivery, title="Create Delivery", icon="📦"),
        st.Page(track_delivery, title="Track Delivery", icon="🚚"),
        st.Page(order_history, title="Order History", icon="📋"),
    ],
    "Rider": [
        st.Page(rider_dashboard, title="Rider Dashboard", icon="🚴"),
        st.Page(available_tasks, title="Available Tasks", icon="📦"),
    ]
}

position2 = st.radio("Navigation Position:", ["sidebar", "top", "hidden"], key="pos2", horizontal=True)
current_page2 = st.navigation(pages_sections, position=position2)
current_page2.run()

# Mobile testing instructions
st.markdown("---")
st.subheader("📱 Mobile Testing Instructions")
st.write("1. Resize your browser to mobile width (or use browser dev tools)")
st.write("2. Test both 'sidebar' and 'top' positions")
st.write("3. Check if navigation is touch-friendly")
st.write("4. See how it behaves on small screens")