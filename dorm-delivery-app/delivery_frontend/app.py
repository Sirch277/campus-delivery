import streamlit as st
import streamlit.components.v1 as components
from customer_dashboard.dashboard import show_customer_dashboard
from rider_dashboard.dashboard import show_rider_dashboard
import os

# Page configuration
st.set_page_config(
    page_title="Dorm Delivery",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_mobile_navigation():
    """Inject mobile navigation JavaScript"""
    # Mobile menu JavaScript
    mobile_js = """
    <script>
    // Mobile menu functionality
    function setupMobileMenu() {
        // Create mobile menu button
        const menuBtn = document.createElement('button');
        menuBtn.className = 'mobile-menu-btn';
        menuBtn.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        menuBtn.onclick = toggleMobileMenu;
        
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.onclick = closeMobileMenu;
        
        document.body.appendChild(menuBtn);
        document.body.appendChild(overlay);
    }

    function toggleMobileMenu() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (sidebar) {
            sidebar.classList.toggle('mobile-open');
        }
        if (overlay) {
            overlay.classList.toggle('active');
        }
    }

    function closeMobileMenu() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (sidebar) {
            sidebar.classList.remove('mobile-open');
        }
        if (overlay) {
            overlay.classList.remove('active');
        }
    }

    // Initialize when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupMobileMenu);
    } else {
        setupMobileMenu();
    }

    // Close menu when clicking sidebar buttons (they cause page reload)
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-testid="stSidebar"] .stButton')) {
            setTimeout(closeMobileMenu, 100);
        }
    });
    </script>
    """
    
    # Inject the JavaScript
    components.html(mobile_js, height=0)

def main():
    # Apply your existing CSS
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, 'static', 'style.css')
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"❌ CSS file not found at: {css_path}")
    
    st.title("🚚 Dorm Delivery - Development Mode")
    
    # Let user choose role without login
    role = st.radio(
        "Choose your role:",
        ["Customer", "Delivery Rider"],
        horizontal=True
    )
    
    # Mock user data
    st.session_state.user = {
        "name": "Test User", 
        "email": "test@example.com",
        "role": "customer" if role == "Customer" else "rider"
    }
    st.session_state.user_role = st.session_state.user["role"]
    st.session_state.token = "dev_token"
    
    # Initialize session state
    if 'customer_current_page' not in st.session_state:
        st.session_state.customer_current_page = "Dashboard"
    if 'rider_current_page' not in st.session_state:
        st.session_state.rider_current_page = "Dashboard"
    
    st.success("🔓 Development Mode - No authentication required")
    
    # Inject mobile navigation JavaScript
    inject_mobile_navigation()
    
    # Show the appropriate dashboard
    if role == "Customer":
        show_customer_dashboard()
    else:
        show_rider_dashboard()

if __name__ == "__main__":
    main()