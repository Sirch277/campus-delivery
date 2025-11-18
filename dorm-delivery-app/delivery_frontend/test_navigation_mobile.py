import streamlit as st
import streamlit.components.v1 as components

# Configure the page
st.set_page_config(
    page_title="Dorm Delivery Mobile Test",
    page_icon="🚚", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject mobile enhancement CSS
mobile_css = """
<style>
/* Mobile Bottom Navigation */
@media (max-width: 768px) {
    /* Hide the default sidebar navigation on mobile */
    section[data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Create bottom navigation bar */
    .mobile-bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        display: flex;
        justify-content: space-around;
        padding: 8px 4px;
        border-top: 1px solid #e0e0e0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    
    .mobile-nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 8px 12px;
        border: none;
        background: none;
        border-radius: 8px;
        min-height: 44px;
        min-width: 60px;
        font-size: 12px;
        color: #666;
        cursor: pointer;
    }
    
    .mobile-nav-item.active {
        color: #1E90FF;
        background: #F0F8FF;
    }
    
    .nav-icon {
        font-size: 18px;
        margin-bottom: 2px;
    }
    
    /* Add padding to main content for bottom nav */
    .main .block-container {
        padding-bottom: 80px !important;
    }
    
    /* Hide sidebar completely on mobile */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
}

/* Desktop - hide mobile nav */
@media (min-width: 769px) {
    .mobile-bottom-nav {
        display: none !important;
    }
}
</style>
"""

st.markdown(mobile_css, unsafe_allow_html=True)

# Define test pages
def dashboard():
    st.header("📊 Dashboard")
    st.write("This is the dashboard page")
    
def create_delivery():
    st.header("📦 Create Delivery")
    st.write("Create delivery form here")
    
def track_delivery():
    st.header("🚚 Track Delivery") 
    st.write("Tracking interface here")
    
def order_history():
    st.header("📋 Order History")
    st.write("Order history here")

# Create pages for navigation
pages = [
    st.Page(dashboard, title="Dashboard", icon="🏠"),
    st.Page(create_delivery, title="Create Delivery", icon="📦"),
    st.Page(track_delivery, title="Track Delivery", icon="🚚"),
    st.Page(order_history, title="Order History", icon="📋"),
]

# Get current page from st.navigation
current_page = st.navigation(pages, position="sidebar")

# Create mobile bottom navigation
mobile_nav_html = """
<div class="mobile-bottom-nav">
    <button class="mobile-nav-item" onclick="navigateTo(0)">
        <span class="nav-icon">🏠</span>
        <span>Home</span>
    </button>
    <button class="mobile-nav-item" onclick="navigateTo(1)">
        <span class="nav-icon">📦</span>
        <span>Create</span>
    </button>
    <button class="mobile-nav-item" onclick="navigateTo(2)">
        <span class="nav-icon">🚚</span>
        <span>Track</span>
    </button>
    <button class="mobile-nav-item" onclick="navigateTo(3)">
        <span class="nav-icon">📋</span>
        <span>History</span>
    </button>
</div>

<script>
function navigateTo(pageIndex) {
    // This would need to integrate with st.navigation
    // For now, just show an alert
    alert("Would navigate to page: " + pageIndex);
}
</script>
"""

components.html(mobile_nav_html, height=0)

# Run the current page
current_page.run()

# Debug info
st.sidebar.write("Debug Info:")
st.sidebar.write("Current page:", current_page)
st.sidebar.write("Screen width test - resize to see mobile/desktop")