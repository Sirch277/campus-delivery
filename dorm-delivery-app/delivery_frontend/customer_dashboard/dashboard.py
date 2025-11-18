import streamlit as st
from utils.api_calls import get_my_deliveries
from . import create_delivery, track_delivery, order_history

def show_customer_dashboard():
    """Main customer dashboard with proper button patterns"""
    
    # Initialize session state
    if 'customer_current_page' not in st.session_state:
        st.session_state.customer_current_page = "Dashboard"
    
    # Navigation callback
    def navigate_to(page):
        st.session_state.customer_current_page = page
    
    # Sidebar navigation with callbacks
    st.sidebar.title("🧭 Navigation")
    
    pages = [
        ("🏠 Dashboard", "Dashboard"),
        ("📦 Create Delivery", "Create Delivery"), 
        ("🚚 Track Delivery", "Track Delivery"),
        ("📋 Order History", "Order History")
    ]
    
    for page_name, page_value in pages:
        st.sidebar.button(
            page_name, 
            use_container_width=True,
            key=f"nav_{page_value}",
            on_click=navigate_to, 
            args=(page_value,)
        )
    
    # Route based on session state
    route_to_page(st.session_state.customer_current_page)

def route_to_page(page):
    """Route to the appropriate page based on session state"""
    if page == "Dashboard":
        show_dashboard_home()
    elif page == "Create Delivery":
        from . import create_delivery
        create_delivery.show_create_delivery()
    elif page == "Track Delivery":
        from . import track_delivery
        track_delivery.show_track_delivery()
    elif page == "Order History":
        from . import order_history
        order_history.show_order_history()

def show_dashboard_home():
    """Customer dashboard home page"""
    st.header("📊 Dashboard Overview")
    
    # Navigation callback for quick actions
    def navigate_to(page):
        st.session_state.customer_current_page = page
    
    # Mock data
    deliveries = get_my_deliveries()
    active_deliveries = [d for d in deliveries if d.get('status') != 'completed']
    completed_deliveries = [d for d in deliveries if d.get('status') == 'completed']
    
    # Quick Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Deliveries", len(active_deliveries))
    with col2:
        st.metric("Completed", len(completed_deliveries))
    with col3:
        st.metric("Total Orders", len(deliveries))
    
    # Quick Actions with callbacks
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📦 Create New Delivery", use_container_width=True, type="primary",
                 key="btn_create", on_click=navigate_to, args=("Create Delivery",))
    with col2:
        st.button("🚚 Track Active", use_container_width=True,
                 key="btn_track", on_click=navigate_to, args=("Track Delivery",))
    with col3:
        st.button("📋 View History", use_container_width=True,
                 key="btn_history", on_click=navigate_to, args=("Order History",))
    
    # Active Deliveries
    if active_deliveries:
        st.subheader("📦 Active Deliveries")
        for delivery in active_deliveries[:3]:
            display_delivery_card(delivery)
    else:
        st.info("🌟 No active deliveries. Create your first delivery to get started!")

def display_delivery_card(delivery):
    """Display a delivery card"""
    status = delivery.get('status', 'unknown')
    
    # Navigation callback for track button
    def navigate_to_track():
        st.session_state.customer_current_page = "Track Delivery"
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Delivery #{delivery.get('id', 'N/A')}**")
            st.write(f"📍 **From:** {delivery.get('pickup_location', 'Unknown')}")
            st.write(f"🎯 **To:** {delivery.get('dropoff_location', 'Unknown')}")
            st.write(f"📦 **Item:** {delivery.get('item_description', 'No description')}")
        
        with col2:
            status_icons = {'pending': '⏳', 'accepted': '👍', 'completed': '✅'}
            status_icon = status_icons.get(status, '⚪')
            st.write(f"**Status:** {status_icon} {status.replace('_', ' ').title()}")
            st.button("Track", key=f"track_{delivery.get('id')}",
                     on_click=navigate_to_track)
        
        st.markdown("---")

