import streamlit as st
from utils.api_calls import get_my_deliveries, get_available_tasks, get_user_profile
from . import available_tasks, my_deliveries, earnings, schedule_setup

def show_rider_dashboard():
    """Main rider dashboard with proper button patterns"""
    
    # Initialize session state
    if 'rider_current_page' not in st.session_state:
        st.session_state.rider_current_page = "Dashboard"
    
    # Navigation callback
    def navigate_to(page):
        st.session_state.rider_current_page = page
    
    # Sidebar navigation with callbacks
    st.sidebar.title("🧭 Rider Navigation")
    
    pages = [
        ("🏠 Dashboard", "Dashboard"),
        ("📚 Schedule Setup", "Schedule Setup"),
        ("📋 Available Tasks", "Available Tasks"), 
        ("🚚 My Deliveries", "My Deliveries"),
        ("💰 Earnings", "Earnings")
    ]
    
    for page_name, page_value in pages:
        st.sidebar.button(
            page_name, 
            use_container_width=True,
            key=f"rider_nav_{page_value}",
            on_click=navigate_to, 
            args=(page_value,)
        )
    
    # Route based on session state
    route_to_rider_page(st.session_state.rider_current_page)

def route_to_rider_page(page):
    """Route to the appropriate rider page based on session state"""
    if page == "Dashboard":
        show_rider_home()
    elif page == "Schedule Setup":
        schedule_setup.show_schedule_setup()
    elif page == "Available Tasks":
        available_tasks.show_available_tasks()
    elif page == "My Deliveries":
        my_deliveries.show_my_deliveries()
    elif page == "Earnings":
        earnings.show_earnings()

def show_rider_home():
    """Rider dashboard home page"""
    
    # Navigation callback for quick actions
    def navigate_to(page):
        st.session_state.rider_current_page = page
    
    # Online Toggle Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.header("🚴 Rider Dashboard")
    with col2:
        # Initialize online status if not set
        if 'rider_online' not in st.session_state:
            st.session_state.rider_online = False
            
        online_status = st.toggle(
            "🟢 Go Online", 
            value=st.session_state.rider_online,
            key="online_toggle_main"
        )
    with col3:
        status_color = "🟢" if online_status else "🔴"
        status_text = "Online" if online_status else "Offline"
        st.markdown(f"### {status_color} {status_text}")
    
    # Update online status and show feedback
    if online_status != st.session_state.rider_online:
        st.session_state.rider_online = online_status
        if online_status:
            st.success("🎉 You're now online and can receive delivery requests!")
        else:
            st.info("🔕 You're now offline and won't receive new requests.")
        st.rerun()
    
    # Schedule setup reminder
    if 'rider_schedule' not in st.session_state or not st.session_state.rider_schedule.get('setup_complete'):
        st.warning("⚠️ Please set up your class schedule to start receiving delivery requests!")
        st.button("📚 Set Up Schedule Now", key="setup_schedule_btn", 
                 on_click=navigate_to, args=("Schedule Setup",))
        return  # Stop here if no schedule
    
    # Quick rider stats
    rider_stats = get_rider_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Deliveries", rider_stats['active_deliveries'])
    with col2:
        st.metric("Completed Today", rider_stats['completed_today'])
    with col3:
        st.metric("Earnings Today", f"${rider_stats['earnings_today']:.2f}")
    with col4:
        st.metric("Rating", f"{rider_stats['rating']:.1f}⭐")
    
    # Quick Actions with callbacks
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📋 Find Tasks", use_container_width=True, type="primary",
                 key="btn_find_tasks", on_click=navigate_to, args=("Available Tasks",))
    with col2:
        st.button("🚚 My Deliveries", use_container_width=True,
                 key="btn_my_deliveries", on_click=navigate_to, args=("My Deliveries",))
    with col3:
        st.button("💰 Earnings", use_container_width=True,
                 key="btn_earnings", on_click=navigate_to, args=("Earnings",))
    
    # Current active deliveries
    active_deliveries = rider_stats['active_list']
    if active_deliveries:
        st.subheader("📦 Active Deliveries")
        for delivery in active_deliveries[:3]:
            display_rider_delivery_card(delivery)
        
        if len(active_deliveries) > 3:
            st.info(f"💡 You have {len(active_deliveries) - 3} more active deliveries.")
    else:
        st.info("🌟 No active deliveries. Check available tasks to find new deliveries!")
    
    # Performance metrics
    st.markdown("---")
    st.subheader("📊 Performance Metrics")
    show_performance_metrics(rider_stats)

def get_rider_stats():
    """Get rider statistics and current deliveries"""
    deliveries = get_my_deliveries() or []
    
    # Filter deliveries for stats
    active_deliveries = [d for d in deliveries if d.get('status') in ['accepted', 'picked_up', 'in_transit']]
    completed_today = [d for d in deliveries if d.get('status') == 'completed']
    
    # Calculate earnings
    earnings_today = len(completed_today) * 5.00
    
    return {
        'active_deliveries': len(active_deliveries),
        'completed_today': len(completed_today),
        'earnings_today': earnings_today,
        'rating': 4.8,
        'active_list': active_deliveries,
        'total_completed': len([d for d in deliveries if d.get('status') == 'completed'])
    }

def display_rider_delivery_card(delivery):
    """Display a delivery card from rider's perspective"""
    status = delivery.get('status', 'unknown')
    delivery_id = delivery.get('id', 'N/A')
    
    # Navigation callback
    def navigate_to_my_deliveries():
        st.session_state.rider_current_page = "My Deliveries"
    
    # Status update callbacks
    def update_status(action):
        # TODO: Implement actual API call
        st.success(f"Status updated for delivery #{delivery_id}!")
        st.rerun()
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write(f"**Delivery #{delivery_id}**")
            st.write(f"📍 **Pickup:** {delivery.get('pickup_location', 'Unknown')}")
            st.write(f"🎯 **Dropoff:** {delivery.get('dropoff_location', 'Unknown')}")
            st.write(f"📦 **Item:** {delivery.get('item_description', 'No description')}")
        
        with col2:
            status_badge = get_rider_status_badge(status)
            st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
            
            if delivery.get('customer_name'):
                st.write(f"**👤 Customer:** {delivery.get('customer_name')}")
            
            if delivery.get('urgency'):
                urgency_icon = "🔥" if delivery.get('urgency') == 'Urgent' else "⏱️"
                st.write(f"**{urgency_icon} {delivery.get('urgency')}**")
        
        with col3:
            # Action buttons based on status with callbacks
            if status == 'accepted':
                st.button("Start", key=f"start_{delivery_id}", on_click=update_status, args=('start',))
            elif status == 'picked_up':
                st.button("Deliver", key=f"deliver_{delivery_id}", on_click=update_status, args=('mark-delivered',))
            elif status == 'in_transit':
                st.button("Arrived", key=f"arrived_{delivery_id}", on_click=update_status, args=('mark-delivered',))
            
            st.button("View", key=f"view_{delivery_id}", on_click=navigate_to_my_deliveries)
        
        st.markdown("---")

def get_rider_status_badge(status):
    """Get colored status badge for rider view"""
    status_config = {
        'accepted': ('🔵 Accepted', '#0074D9'),
        'picked_up': ('🚗 Picked Up', '#2ECC40'),
        'in_transit': ('🚚 In Transit', '#FF851B'),
        'delivered': ('✅ Delivered', '#7FDBFF'),
    }
    
    text, color = status_config.get(status, ('⚪ Unknown', '#AAAAAA'))
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em;">{text}</span>'

def show_performance_metrics(stats):
    """Show rider performance metrics"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Completed", stats['total_completed'])
    with col2:
        st.metric("Success Rate", "98%")
    with col3:
        st.metric("Avg. Delivery Time", "18 min")
    
    st.write("**Weekly Performance**")
    st.info("📈 Performance charts coming soon!")