import streamlit as st
import requests
from .api_calls import API_BASE_URL
    
def login_user(email: str, password: str) -> bool:
    """Attempt to log in a user with email"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get("access_token")
            st.session_state.user = data.get("user")
            st.session_state.user_role = st.session_state.user.get("role") if st.session_state.user else None
            return True
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return False
    
def register_user(name: str, email: str, password: str, role: str) -> bool:
    """Register a new user"""
    try:
        # Debug password length
        original_bytes = password.encode('utf-8')
        st.write(f"🔧 Debug: Original password length: {len(password)} characters")
        st.write(f"🔧 Debug: Original password bytes: {len(original_bytes)} bytes")
        
        # Force truncate to 72 bytes
        if len(original_bytes) > 72:
            st.warning(f"⚠️ Password too long: {len(original_bytes)} bytes, truncating to 72 bytes")
            # Simple truncation - just take first 72 bytes
            truncated_bytes = original_bytes[:72]
            # Try to decode, if it fails, keep removing bytes until it works
            while truncated_bytes:
                try:
                    password = truncated_bytes.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    truncated_bytes = truncated_bytes[:-1]
            
            st.write(f"🔧 Debug: Truncated password length: {len(password)} characters")
            st.write(f"🔧 Debug: Truncated password bytes: {len(password.encode('utf-8'))} bytes")
        
        url = f"{API_BASE_URL}/auth/register"
        
        # Debug the final request
        st.write(f"🔧 Debug: Sending request to {url}")
        st.write(f"🔧 Debug: Username: {name}")
        st.write(f"🔧 Debug: Email: {email}")
        st.write(f"🔧 Debug: Role: {role}")
        st.write(f"🔧 Debug: Final password bytes: {len(password.encode('utf-8'))}")
        
        response = requests.post(
            url,
            json={
                "username": name,  # Send as "username" but use the name value
                "email": email,
                "password": password,
                "role": role
            },
            timeout=10
        )
        
        st.write(f"🔧 Debug: Response status: {response.status_code}")
        st.write(f"🔧 Debug: Response text: {response.text}")
        
        if response.status_code == 200:
            return True
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'Unknown server error')
                st.error(f"❌ Registration failed: {error_detail}")
            except:
                st.error(f"❌ Server error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        st.error(f"💥 Unexpected error: {str(e)}")
        return False

def logout_user():
    """Clear user session and log out"""
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.user_role = None

def get_current_user():
    """Get current user from session state or verify token"""
    if st.session_state.token and st.session_state.user:
        # TODO: Add token verification with backend
        return st.session_state.user
    return None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.token is not None

def get_auth_headers():
    """Get headers with authentication token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}