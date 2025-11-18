import streamlit as st
import time
from datetime import datetime
from utils.api_calls import get_my_deliveries, update_delivery_status

def show_track_delivery():
    """Show delivery tracking interface"""
    st.header("🚚 Track Your Deliveries")
    
    # Auto-refresh toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Active Deliveries")
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        if auto_refresh:
            st.rerun()
    
    # Get deliveries and filter active ones
    deliveries = get_my_deliveries() or []
    # MOCK DATA - REMOVE LATER
    deliveries = [
    {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Math Textbook", "status": "in_transit", "rider_name": "John D.", "estimated_arrival": "10 minutes"},
    {"id": 2, "pickup_location": "Bookstore", "dropoff_location": "Dorm C", "item_description": "Notebooks", "status": "picked_up", "rider_name": "Mike T."}
]
    active_deliveries = [d for d in deliveries if d.get('status') not in ['completed', 'cancelled', 'failed']]
    completed_deliveries = [d for d in deliveries if d.get('status') in ['completed']]
    
    if not active_deliveries:
        st.info("📭 No active deliveries to track.")
        if completed_deliveries:
            st.write("Check your Order History for completed deliveries.")
        
        # Quick action to create delivery
        if st.button("📦 Create Your First Delivery"):
            st.switch_page("pages/customer_dashboard/create_delivery.py")
        return
    
    # Display active deliveries with tracking
    for delivery in active_deliveries:
        display_delivery_tracking(delivery)
    
    # Manual refresh button
    if st.button("🔄 Refresh Status"):
        st.rerun()

def display_delivery_tracking(delivery):
    """Display detailed tracking for a single delivery"""
    delivery_id = delivery.get('id')
    status = delivery.get('status', 'pending')
    
    with st.container():
        st.markdown("---")
        
        # Delivery header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"### 📦 Delivery #{delivery_id}")
        with col2:
            status_badge = get_status_badge(status)
            st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
        
        # Delivery details
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**📍 Pickup:** {delivery.get('pickup_location', 'Unknown')}")
            st.write(f"**🎯 Dropoff:** {delivery.get('dropoff_location', 'Unknown')}")
            st.write(f"**📦 Item:** {delivery.get('item_description', 'No description')}")
        with col2:
            if delivery.get('rider_name'):
                st.write(f"**🚴 Rider:** {delivery.get('rider_name')}")
            if delivery.get('rider_phone'):
                st.write(f"**📞 Contact:** {delivery.get('rider_phone')}")
            if delivery.get('estimated_arrival'):
                st.write(f"**⏱️ ETA:** {delivery.get('estimated_arrival')}")
        
        # Progress tracker
        st.markdown("### 📊 Delivery Progress")
        show_progress_tracker(status)
        
        # Real-time updates section
        st.markdown("### 🔄 Live Updates")
        show_live_updates(delivery)
        
        # Actions based on status
        show_delivery_actions(delivery)

def get_status_badge(status):
    """Get colored status badge"""
    status_config = {
        'pending': ('🟡 Pending', '#FFA500'),
        'accepted': ('🔵 Accepted', '#0074D9'),
        'picked_up': ('🚗 Picked Up', '#2ECC40'),
        'in_transit': ('🚚 In Transit', '#FF851B'),
        'delivered': ('✅ Delivered', '#7FDBFF'),
        'completed': ('🏁 Completed', '#B10DC9'),
        'failed': ('❌ Failed', '#FF4136')
    }
    
    text, color = status_config.get(status, ('⚪ Unknown', '#AAAAAA'))
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em;">{text}</span>'

def show_progress_tracker(current_status):
    """Show delivery progress as a timeline"""
    steps = [
        ('pending', '🟡', 'Order Placed', 'Delivery request created'),
        ('accepted', '🔵', 'Rider Assigned', 'Rider accepted your delivery'),
        ('picked_up', '📦', 'Picked Up', 'Rider has collected your item'),
        ('in_transit', '🚗', 'In Transit', 'Rider is on the way'),
        ('delivered', '✅', 'Delivered', 'Item has been delivered'),
        ('completed', '🎉', 'Completed', 'Delivery confirmed and closed')
    ]
    
    current_index = next((i for i, (status, _, _, _) in enumerate(steps) if status == current_status), 0)
    
    for i, (status, icon, title, description) in enumerate(steps):
        col1, col2 = st.columns([1, 10])
        
        with col1:
            if i < current_index:
                st.success("✓")  # Completed step
            elif i == current_index:
                st.info(icon)  # Current step
            else:
                st.write("○")  # Future step
        
        with col2:
            if i <= current_index:
                st.write(f"**{title}**")
                st.caption(description)
            else:
                st.write(f"*{title}*")
                st.caption(description)
        
        if i < len(steps) - 1:
            st.markdown("<div style='margin-left: 12px; border-left: 2px solid #ddd; height: 20px;'></div>", 
                       unsafe_allow_html=True)

def show_live_updates(delivery):
    """Show real-time updates and ETA"""
    delivery_id = delivery.get('id', 'unknown')
    status = delivery.get('status')
    
    # ETA estimation based on status
    if status == 'pending':
        st.info("⏳ Waiting for a rider to accept your delivery...")
        st.write("Riders in your area have been notified.")
        
    elif status == 'accepted':
        st.success("🎉 Rider assigned! Your delivery is now being processed.")
        if delivery.get('rider_name'):
            st.write(f"**{delivery.get('rider_name')}** is getting ready to pick up your item.")
        
    elif status == 'picked_up':
        st.success("📦 Item picked up! Your rider has collected your item.")
        show_eta_countdown("Pickup completed - heading to dropoff", delivery_id)  # ADD delivery_id
        
    elif status == 'in_transit':
        st.warning("🚗 Rider is on the way to your dropoff location!")
        show_eta_countdown("Estimated arrival time", delivery_id)  # ADD delivery_id
        
    elif status == 'delivered':
        st.success("✅ Item delivered! Please confirm receipt.")
        st.balloons()
        
    # Last update time
    if delivery.get('updated_at'):
        last_update = delivery.get('updated_at', '').replace('T', ' ').split('.')[0]
        st.caption(f"Last update: {last_update}")


def show_eta_countdown(message, delivery_id):
    """Show ETA countdown (placeholder for real ETA)"""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{message}:**")
        # Placeholder ETA - in real app, this would come from backend
        st.write("🕐 Approximately 10-15 minutes")
    with col2:
        # Simulate live tracking - USE UNIQUE KEY WITH DELIVERY ID
        if st.button("🔄 Update ETA", key=f"update_eta_{delivery_id}"):
            with st.spinner("Getting latest ETA..."):
                time.sleep(1)
                st.rerun()

def show_delivery_actions(delivery):
    """Show actions user can take based on delivery status"""
    status = delivery.get('status')
    delivery_id = delivery.get('id')
    
    st.markdown("### 🎯 Actions")
    
    if status == 'delivered':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Receipt", type="primary", key=f"confirm_{delivery_id}"):
                if update_delivery_status(delivery_id, 'confirm'):
                    st.success("Delivery confirmed! Thank you for using Dorm Delivery.")
                    st.rerun()
                else:
                    st.error("Failed to confirm delivery. Please try again.")
        with col2:
            if st.button("❌ Report Issue", key=f"issue_{delivery_id}"):
                st.error("Please contact support if there's an issue with your delivery.")
    
    elif status in ['in_transit', 'picked_up']:
        st.write("Need to contact your rider?")
        if st.button("📞 Contact Rider", key=f"contact_{delivery_id}"):
            st.info("Rider contact feature coming soon!")
    
    # Emergency/cancel option
    with st.expander("🚨 Emergency / Cancel Delivery"):
        st.warning("Use this only if there's an emergency or you need to cancel")
        if st.button("Cancel This Delivery", key=f"cancel_{delivery_id}"):
            st.error("Please contact support to cancel a delivery: support@dormdelivery.com")

# Auto-refresh every 30 seconds if enabled
def auto_refresh():
    """Auto-refresh the page for real-time updates"""
    time.sleep(30)
    st.rerun()