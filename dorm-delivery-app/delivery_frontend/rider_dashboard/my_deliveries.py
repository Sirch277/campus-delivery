import streamlit as st
import time
from datetime import datetime
from utils.api_calls import get_my_deliveries, update_delivery_status

def show_my_deliveries():
    """Show rider's current and past deliveries"""
    st.header("🚚 My Deliveries")
    
    # Delivery status filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        status_filter = st.selectbox(
            "Filter by status",
            ["All Active", "In Progress", "Completed", "Failed/Cancelled"],
            key="rider_delivery_filter"
        )
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest First", "Oldest First", "Payout", "Urgency"]
        )
    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        if auto_refresh:
            time.sleep(15)  # Refresh every 15 seconds
            st.rerun()
    
    # Get rider's deliveries
    deliveries = get_my_deliveries() or []
    # MOCK DATA - REMOVE LATER
    deliveries = [
    {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Textbook", "status": "in_transit", "payout": 5.00, "customer_name": "Alex J."},
    {"id": 2, "pickup_location": "Bookstore", "dropoff_location": "Dorm B", "item_description": "Notebooks", "status": "accepted", "payout": 4.50, "customer_name": "Jordan K."}
]
    
    
    if not deliveries:
        show_no_deliveries_state()
        return
    
    # Filter deliveries based on selection
    filtered_deliveries = filter_rider_deliveries(deliveries, status_filter)
    
    # Sort deliveries
    sorted_deliveries = sort_rider_deliveries(filtered_deliveries, sort_by)
    
    # Display deliveries
    show_delivery_stats(filtered_deliveries)
    
    if not filtered_deliveries:
        show_empty_filter_state(status_filter)
        return
    
    # Show deliveries list
    for delivery in sorted_deliveries:
        display_rider_delivery_detail(delivery)
    
    # Quick actions
    show_quick_actions()

def show_no_deliveries_state():
    """Show state when rider has no deliveries"""
    st.info("📭 You don't have any deliveries yet.")
    st.write("""
    **Get started:**
    - Check 'Available Tasks' to find deliveries near you
    - Accept your first delivery to begin earning
    - Make sure your availability is set to 'Online'
    """)
    
    if st.button("📋 Find Available Tasks", type="primary"):
        st.sidebar.radio("Go to", ["Dashboard", "Available Tasks", "My Deliveries", "Earnings"], 
                       index=1, key="rider_nav")
        st.rerun()

def filter_rider_deliveries(deliveries, status_filter):
    """Filter deliveries based on status selection"""
    status_groups = {
        "All Active": ['accepted', 'picked_up', 'in_transit', 'delivered'],
        "In Progress": ['accepted', 'picked_up', 'in_transit'],
        "Completed": ['completed'],
        "Failed/Cancelled": ['failed', 'cancelled']
    }
    
    target_statuses = status_groups.get(status_filter, [])
    if status_filter == "All Active":
        return [d for d in deliveries if d.get('status') in target_statuses]
    else:
        return [d for d in deliveries if d.get('status') in target_statuses]

def sort_rider_deliveries(deliveries, sort_by):
    """Sort deliveries based on selected criteria"""
    if sort_by == "Newest First":
        return sorted(deliveries, key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == "Oldest First":
        return sorted(deliveries, key=lambda x: x.get('created_at', ''))
    elif sort_by == "Payout":
        return sorted(deliveries, key=lambda x: x.get('payout', 0) or 0, reverse=True)
    elif sort_by == "Urgency":
        # Sort urgent deliveries first
        return sorted(deliveries, key=lambda x: 1 if x.get('urgency') == 'Urgent' else 0, reverse=True)
    return deliveries

def show_delivery_stats(deliveries):
    """Show statistics about current deliveries"""
    if not deliveries:
        return
    
    active_count = len([d for d in deliveries if d.get('status') in ['accepted', 'picked_up', 'in_transit']])
    completed_count = len([d for d in deliveries if d.get('status') == 'completed'])
    total_earnings = sum([d.get('payout', 0) or 0 for d in deliveries if d.get('status') == 'completed'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active", active_count)
    with col2:
        st.metric("Completed", completed_count)
    with col3:
        st.metric("Total", len(deliveries))
    with col4:
        st.metric("Earnings", f"${total_earnings:.2f}")

def show_empty_filter_state(status_filter):
    """Show message when filter returns no results"""
    st.info(f"📭 No {status_filter.lower()} deliveries found.")
    if status_filter != "All Active":
        if st.button("Show All Deliveries"):
            st.rerun()

def display_rider_delivery_detail(delivery):
    """Display detailed delivery information for rider"""
    delivery_id = delivery.get('id', 'N/A')
    status = delivery.get('status', 'unknown')
    payout = delivery.get('payout', 5.00) or 5.00
    
    with st.container():
        st.markdown("---")
        
        # Delivery header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"### 🚚 Delivery #{delivery_id}")
        with col2:
            st.metric("Payout", f"${payout:.2f}")
        with col3:
            status_badge = get_rider_status_badge(status)
            st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
        
        # Delivery details
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**📍 Pickup:** {delivery.get('pickup_location', 'Unknown')}")
            st.write(f"**🎯 Dropoff:** {delivery.get('dropoff_location', 'Unknown')}")
            st.write(f"**📦 Item:** {delivery.get('item_description', 'No description')}")
            
            # Customer information
            if delivery.get('customer_name'):
                st.write(f"**👤 Customer:** {delivery.get('customer_name')}")
            if delivery.get('customer_phone'):
                st.write(f"**📞 Contact:** {delivery.get('customer_phone')}")
        
        with col2:
            # Timing information
            if delivery.get('created_at'):
                created_time = format_delivery_time(delivery.get('created_at'))
                st.write(f"**🕐 Accepted:** {created_time}")
            
            if delivery.get('estimated_arrival'):
                st.write(f"**⏱️ ETA:** {delivery.get('estimated_arrival')}")
            
            # Urgency and special instructions
            if delivery.get('urgency'):
                urgency_icon = "🔥" if delivery.get('urgency') == 'Urgent' else "⏱️"
                st.write(f"**{urgency_icon} Urgency:** {delivery.get('urgency')}")
            
            if delivery.get('item_size'):
                st.write(f"**📏 Size:** {delivery.get('item_size')}")
        
        # Special instructions
        if delivery.get('instructions'):
            with st.expander("📝 Delivery Instructions"):
                st.write(delivery.get('instructions'))
        
        # Action buttons based on delivery status
        show_delivery_actions(delivery)
        
        # Delivery progress tracker
        if status in ['accepted', 'picked_up', 'in_transit', 'delivered']:
            show_delivery_progress(delivery)

def get_rider_status_badge(status):
    """Get colored status badge for rider view"""
    status_config = {
        'accepted': ('🔵 Accepted', 'Pick up the item', '#0074D9'),
        'picked_up': ('🚗 Picked Up', 'Deliver to destination', '#2ECC40'),
        'in_transit': ('🚚 In Transit', 'On the way', '#FF851B'),
        'delivered': ('✅ Delivered', 'Awaiting confirmation', '#7FDBFF'),
        'completed': ('🏁 Completed', 'Delivery finished', '#B10DC9'),
        'failed': ('❌ Failed', 'Delivery failed', '#FF4136'),
        'cancelled': ('🚫 Cancelled', 'Delivery cancelled', '#AAAAAA')
    }
    
    text, description, color = status_config.get(status, ('⚪ Unknown', 'Unknown status', '#AAAAAA'))
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em;" title="{description}">{text}</span>'

def format_delivery_time(timestamp):
    """Format delivery timestamp to readable time"""
    try:
        if 'T' in timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%I:%M %p')
    except:
        pass
    return "Unknown time"

def show_delivery_actions(delivery):
    """Show action buttons based on delivery status"""
    delivery_id = delivery.get('id')
    status = delivery.get('status')
    
    st.markdown("### 🎯 Delivery Actions")
    
    if status == 'accepted':
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚗 Start Pickup", key=f"start_{delivery_id}", type="primary", width='stretch'):
                update_delivery_action(delivery_id, 'start')
        with col2:
            if st.button("📍 Get Directions", key=f"directions_{delivery_id}", width='stretch'):
                show_directions(delivery)
        with col3:
            if st.button("❌ Cannot Complete", key=f"fail_{delivery_id}", width='stretch'):
                show_fail_delivery_modal(delivery_id)
    
    elif status == 'picked_up':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚚 Start Delivery", key=f"deliver_{delivery_id}", type="primary", width='stretch'):
                update_delivery_action(delivery_id, 'start')
        with col2:
            if st.button("📍 Dropoff Directions", key=f"dropoff_{delivery_id}", width='stretch'):
                show_directions(delivery, is_dropoff=True)
    
    elif status == 'in_transit':
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Mark Delivered", key=f"delivered_{delivery_id}", type="primary", width='stretch'):
                update_delivery_action(delivery_id, 'mark-delivered')
        with col2:
            if st.button("📞 Contact Customer", key=f"contact_{delivery_id}", width='stretch'):
                contact_customer(delivery)
        with col3:
            if st.button("⚠️ Report Issue", key=f"issue_{delivery_id}", width='stretch'):
                show_issue_modal(delivery_id)
    
    elif status == 'delivered':
        st.info("📝 Waiting for customer confirmation...")
        if st.button("🔄 Check Status", key=f"check_{delivery_id}"):
            st.rerun()

def show_delivery_progress(delivery):
    """Show delivery progress steps"""
    status = delivery.get('status')
    steps = [
        ('accepted', '🔵', 'Accepted', 'Delivery accepted'),
        ('picked_up', '🚗', 'Picked Up', 'Item collected from customer'),
        ('in_transit', '🚚', 'In Transit', 'On the way to dropoff'),
        ('delivered', '✅', 'Delivered', 'Item delivered to destination'),
        ('completed', '🏁', 'Completed', 'Delivery confirmed and paid')
    ]
    
    current_index = next((i for i, (step_status, _, _, _) in enumerate(steps) if step_status == status), 0)
    
    st.markdown("#### 📊 Delivery Progress")
    progress_cols = st.columns(len(steps))
    
    for i, (step_status, icon, title, description) in enumerate(steps):
        with progress_cols[i]:
            if i < current_index:
                st.success("✓")
                st.caption(f"**{title}**")
            elif i == current_index:
                st.info(icon)
                st.caption(f"**{title}**")
                st.caption(description)
            else:
                st.write("○")
                st.caption(title)

def update_delivery_action(delivery_id, action):
    """Update delivery status with the given action"""
    with st.spinner("Updating delivery status..."):
        success = update_delivery_status(delivery_id, action)
        
        if success:
            st.success(f"✅ Delivery status updated!")
            time.sleep(2)
            st.rerun()
        else:
            st.error("❌ Failed to update delivery status")

def show_directions(delivery, is_dropoff=False):
    """Show directions to pickup/dropoff location"""
    location = delivery.get('dropoff_location') if is_dropoff else delivery.get('pickup_location')
    st.info(f"🗺️ Directions to {location}")
    st.write("**Campus Navigation:**")
    st.write(f"- Head towards {location}")
    st.write("- Use campus maps app for precise directions")
    st.write("- Allow 5-10 minutes for travel time")
    
    # Placeholder for actual map integration
    st.write("🚧 Interactive campus map coming soon!")

def contact_customer(delivery):
    """Show customer contact information"""
    st.info("📞 Customer Contact")
    if delivery.get('customer_phone'):
        st.write(f"**Phone:** {delivery.get('customer_phone')}")
        st.write("💡 Tip: Call or text when you're 5 minutes away")
    else:
        st.write("📧 Customer contact information not available")
        st.write("Use the in-app messaging system to communicate")

def show_fail_delivery_modal(delivery_id):
    """Show modal for reporting failed delivery"""
    with st.form(key=f"fail_form_{delivery_id}"):
        st.warning("🚨 Report Delivery Issue")
        st.write("Please provide details about why this delivery cannot be completed:")
        
        issue_type = st.selectbox(
            "Issue Type",
            ["Customer not available", "Item not ready", "Location inaccessible", "Other issue"]
        )
        
        details = st.text_area("Additional Details", placeholder="Describe what happened...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Report Issue", type="primary")
        with col2:
            cancel = st.form_submit_button("Cancel")
        
        if submit:
            # TODO: Implement fail delivery API call
            st.error("Delivery marked as failed. Support will review the issue.")
            time.sleep(2)
            st.rerun()

def show_issue_modal(delivery_id):
    """Show modal for reporting delivery issues"""
    with st.form(key=f"issue_form_{delivery_id}"):
        st.warning("⚠️ Report Delivery Problem")
        
        problem = st.selectbox(
            "What's the issue?",
            ["Can't find location", "Customer not responding", "Item issues", "Traffic delay", "Other"]
        )
        
        description = st.text_area("Problem Description")
        
        if st.form_submit_button("Submit Report"):
            st.info("Issue reported. Support will contact you if needed.")
            time.sleep(2)
            st.rerun()

def show_quick_actions():
    """Show quick action buttons at the bottom"""
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Find More Tasks", width='stretch'):
            st.sidebar.radio("Go to", ["Dashboard", "Available Tasks", "My Deliveries", "Earnings"], 
                           index=1, key="rider_nav")
            st.rerun()
    with col2:
        if st.button("💰 View Earnings", width='stretch'):
            st.sidebar.radio("Go to", ["Dashboard", "Available Tasks", "My Deliveries", "Earnings"], 
                           index=3, key="rider_nav")
            st.rerun()
    with col3:
        if st.button("🔄 Refresh All", width='stretch'):
            st.rerun()