import requests
import streamlit as st

# Backend API base URL - adjust as needed
API_BASE_URL = "http://127.0.0.1:8000/api"

def make_authenticated_request(method, endpoint, **kwargs):
    """Make authenticated API request with error handling"""
    headers = kwargs.pop('headers', {})
    
    # Check if token exists in session state (handle dev mode)
    if 'token' in st.session_state and st.session_state.token:
        headers['Authorization'] = f"Bearer {st.session_state.token}"
    # If no token (dev mode), proceed without authentication
    
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            headers=headers,
            **kwargs
        )
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {e}")
        return None

# User-related API calls
def get_user_profile():
    """Get current user profile"""
    # In dev mode, return mock user data
    if 'token' not in st.session_state or not st.session_state.token:
        return {"name": "Test User", "email": "test@example.com", "role": "customer"}
    
    response = make_authenticated_request('GET', '/users/me')
    if response and response.status_code == 200:
        return response.json()
    return None

# Delivery-related API calls
def create_delivery(pickup_location, dropoff_location, item_description, instructions=""):
    """Create a new delivery"""
    # In dev mode, return mock success
    if 'token' not in st.session_state or not st.session_state.token:
        return {"id": 999, "status": "pending", "message": "Mock delivery created"}
    
    data = {
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "item_description": item_description,
        "instructions": instructions
    }
    response = make_authenticated_request('POST', '/delivery/', json=data)
    if response and response.status_code == 200:
        return response.json()
    return None

def get_my_deliveries():
    """Get current user's deliveries"""
    # In dev mode, return mock deliveries
    if 'token' not in st.session_state or not st.session_state.token:
        return [
            {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Math Textbook", "status": "in_transit", "rider_name": "John D."},
            {"id": 2, "pickup_location": "Cafeteria", "dropoff_location": "Dorm B", "item_description": "Lunch", "status": "completed", "rider_name": "Sarah M."}
        ]
    
    response = make_authenticated_request('GET', '/delivery/')
    if response and response.status_code == 200:
        return response.json()
    return []

def get_available_tasks():
    """Get available delivery tasks for riders"""
    # In dev mode, return mock tasks
    if 'token' not in st.session_state or not st.session_state.token:
        return [
            {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Textbook", "payout": 5.00, "urgency": "Standard"},
            {"id": 2, "pickup_location": "Student Center", "dropoff_location": "Dorm C", "item_description": "Package", "payout": 7.00, "urgency": "Urgent"}
        ]
    
    response = make_authenticated_request('GET', '/delivery/available-tasks')
    if response and response.status_code == 200:
        return response.json()
    return []

def accept_delivery(delivery_id):
    """Accept a delivery task"""
    # In dev mode, return mock success
    if 'token' not in st.session_state or not st.session_state.token:
        return True
    
    response = make_authenticated_request('POST', f'/delivery/{delivery_id}/accept')
    return response and response.status_code == 200

def update_delivery_status(delivery_id, action):
    """Update delivery status (start, mark-delivered, etc.)"""
    # In dev mode, return mock success
    if 'token' not in st.session_state or not st.session_state.token:
        return True
    
    response = make_authenticated_request('POST', f'/delivery/{delivery_id}/{action}')
    return response and response.status_code == 200