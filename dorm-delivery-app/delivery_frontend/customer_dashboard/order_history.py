import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api_calls import get_my_deliveries

def show_order_history():
    """Show order history and past deliveries"""
    st.header("📋 Order History")
    
    # Filters and search
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search deliveries", placeholder="Search by item, location, rider...")
    with col2:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "Completed", "Failed", "Cancelled", "Pending", "In Progress"]
        )
    with col3:
        sort_order = st.selectbox(
            "Sort by",
            ["Newest First", "Oldest First", "Status"]
        )
    
    # Get deliveries
    deliveries = get_my_deliveries() or []
    # MOCK DATA - REMOVE LATER
    deliveries = [
    {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Math Textbook", "status": "completed", "rider_name": "John D.", "created_at": "2024-01-15T10:00:00", "completed_at": "2024-01-15T10:25:00"},
    {"id": 2, "pickup_location": "Cafeteria", "dropoff_location": "Dorm B", "item_description": "Lunch", "status": "completed", "rider_name": "Sarah M.", "created_at": "2024-01-14T12:30:00", "completed_at": "2024-01-14T12:45:00"}
]
    
    if not deliveries:
        show_empty_state()
        return
    
    # Apply filters
    filtered_deliveries = filter_deliveries(deliveries, search_term, status_filter)
    
    # Apply sorting
    sorted_deliveries = sort_deliveries(filtered_deliveries, sort_order)
    
    # Display results
    show_delivery_stats(filtered_deliveries)
    show_deliveries_list(sorted_deliveries)
    
    # Export option
    show_export_options(filtered_deliveries)

def show_empty_state():
    """Show empty state when no deliveries exist"""
    st.info("📭 No delivery history found.")
    st.write("Your completed and past deliveries will appear here.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 Create Your First Delivery", type="primary"):
            st.switch_page("pages/customer_dashboard/create_delivery.py")
    with col2:
        if st.button("🚚 Track Active Deliveries"):
            st.switch_page("pages/customer_dashboard/track_delivery.py")

def filter_deliveries(deliveries, search_term, status_filter):
    """Filter deliveries based on search and status"""
    filtered = deliveries
    
    # Search filter
    if search_term:
        search_term = search_term.lower()
        filtered = [
            d for d in filtered
            if (search_term in d.get('item_description', '').lower() or
                search_term in d.get('pickup_location', '').lower() or
                search_term in d.get('dropoff_location', '').lower() or
                search_term in d.get('rider_name', '').lower())
        ]
    
    # Status filter
    if status_filter != "All":
        status_map = {
            "Completed": ["completed"],
            "Failed": ["failed"],
            "Cancelled": ["cancelled"],
            "Pending": ["pending"],
            "In Progress": ["accepted", "picked_up", "in_transit", "delivered"]
        }
        target_statuses = status_map.get(status_filter, [])
        filtered = [d for d in filtered if d.get('status') in target_statuses]
    
    return filtered

def sort_deliveries(deliveries, sort_order):
    """Sort deliveries based on selected order"""
    if sort_order == "Newest First":
        return sorted(deliveries, key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_order == "Oldest First":
        return sorted(deliveries, key=lambda x: x.get('created_at', ''))
    elif sort_order == "Status":
        status_order = ['pending', 'accepted', 'picked_up', 'in_transit', 'delivered', 'completed', 'failed', 'cancelled']
        return sorted(deliveries, key=lambda x: status_order.index(x.get('status', 'pending')))
    return deliveries

def show_delivery_stats(deliveries):
    """Show delivery statistics"""
    if not deliveries:
        return
    
    total = len(deliveries)
    completed = len([d for d in deliveries if d.get('status') == 'completed'])
    failed = len([d for d in deliveries if d.get('status') == 'failed'])
    success_rate = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Deliveries", total)
    with col2:
        st.metric("Completed", completed)
    with col3:
        st.metric("Failed", failed)
    with col4:
        st.metric("Success Rate", f"{success_rate:.1f}%")

def show_deliveries_list(deliveries):
    """Display the list of deliveries"""
    st.subheader(f"📄 Delivery History ({len(deliveries)} orders)")
    
    for delivery in deliveries:
        show_delivery_card(delivery)

def show_delivery_card(delivery):
    """Display a delivery card in history view"""
    status = delivery.get('status', 'unknown')
    delivery_id = delivery.get('id', 'N/A')
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            # Basic delivery info
            st.write(f"**Delivery #{delivery_id}**")
            st.write(f"📍 **From:** {delivery.get('pickup_location', 'Unknown')}")
            st.write(f"🎯 **To:** {delivery.get('dropoff_location', 'Unknown')}")
            st.write(f"📦 **Item:** {delivery.get('item_description', 'No description')}")
            
            # Date information
            created_date = format_date(delivery.get('created_at'))
            completed_date = format_date(delivery.get('completed_at'))
            
            st.caption(f"Ordered: {created_date}")
            if completed_date:
                st.caption(f"Completed: {completed_date}")
        
        with col2:
            # Status and rider info
            status_badge = get_status_badge(status)
            st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
            
            if delivery.get('rider_name'):
                st.write(f"**🚴 Rider:** {delivery.get('rider_name')}")
            
            # Delivery time (if completed)
            if delivery.get('completed_at') and delivery.get('created_at'):
                delivery_time = calculate_delivery_time(
                    delivery.get('created_at'),
                    delivery.get('completed_at')
                )
                if delivery_time:
                    st.write(f"**⏱️ Time:** {delivery_time}")
        
        with col3:
            # Actions
            if status == 'completed':
                st.success("✅ Completed")
                if st.button("📊 Rate", key=f"rate_{delivery_id}"):
                    show_rating_modal(delivery)
            elif status == 'failed':
                st.error("❌ Failed")
            elif status in ['pending', 'accepted', 'picked_up', 'in_transit', 'delivered']:
                if st.button("🚚 Track", key=f"track_{delivery_id}"):
                    st.switch_page("pages/customer_dashboard/track_delivery.py")
            else:
                st.info("📝 " + status.title())
        
        st.markdown("---")

def get_status_badge(status):
    """Get colored status badge"""
    status_config = {
        'pending': ('🟡 Pending', '#FFA500'),
        'accepted': ('🔵 Accepted', '#0074D9'),
        'picked_up': ('🚗 Picked Up', '#2ECC40'),
        'in_transit': ('🚚 In Transit', '#FF851B'),
        'delivered': ('✅ Delivered', '#7FDBFF'),
        'completed': ('🏁 Completed', '#B10DC9'),
        'failed': ('❌ Failed', '#FF4136'),
        'cancelled': ('🚫 Cancelled', '#AAAAAA')
    }
    
    text, color = status_config.get(status, ('⚪ Unknown', '#AAAAAA'))
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em;">{text}</span>'

def format_date(date_string):
    """Format date string to readable format"""
    if not date_string:
        return None
    
    try:
        # Handle ISO format date string
        if 'T' in date_string:
            date_part = date_string.split('T')[0]
            return datetime.strptime(date_part, '%Y-%m-%d').strftime('%b %d, %Y')
        else:
            return datetime.strptime(date_string, '%Y-%m-%d').strftime('%b %d, %Y')
    except:
        return date_string

def calculate_delivery_time(start_date, end_date):
    """Calculate delivery duration"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        duration = end - start
        
        hours = duration.total_seconds() / 3600
        if hours < 1:
            minutes = duration.total_seconds() / 60
            return f"{int(minutes)} min"
        else:
            return f"{hours:.1f} hours"
    except:
        return None

def show_rating_modal(delivery):
    """Show rating modal for completed deliveries"""
    with st.form(key=f"rate_form_{delivery.get('id')}"):
        st.subheader("⭐ Rate Your Delivery")
        
        st.write(f"Delivery #{delivery.get('id')}")
        st.write(f"Rider: {delivery.get('rider_name', 'Unknown')}")
        
        rating = st.slider("Overall Rating", 1, 5, 5)
        feedback = st.text_area("Feedback (Optional)", placeholder="How was your delivery experience?")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Submit Rating", type="primary")
        with col2:
            cancel = st.form_submit_button("Cancel")
        
        if submit:
            # TODO: Implement rating submission to backend
            st.success("🎉 Thank you for your feedback!")
            st.rerun()

def show_export_options(deliveries):
    """Show options to export delivery history"""
    with st.expander("💾 Export Delivery History"):
        st.write("Download your delivery history for your records.")
        
        if st.button("📄 Export as CSV"):
            export_csv(deliveries)
        
        if st.button("📊 Export as Excel"):
            export_excel(deliveries)

def export_csv(deliveries):
    """Export deliveries as CSV"""
    if not deliveries:
        st.warning("No data to export")
        return
    
    # Prepare data for CSV
    data = []
    for delivery in deliveries:
        data.append({
            'Delivery ID': delivery.get('id'),
            'Pickup Location': delivery.get('pickup_location'),
            'Dropoff Location': delivery.get('dropoff_location'),
            'Item Description': delivery.get('item_description'),
            'Status': delivery.get('status'),
            'Rider': delivery.get('rider_name', ''),
            'Created Date': format_date(delivery.get('created_at')),
            'Completed Date': format_date(delivery.get('completed_at')),
            'Instructions': delivery.get('instructions', '')
        })
    
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"dorm_delivery_history_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def export_excel(deliveries):
    """Export deliveries as Excel"""
    st.info("Excel export coming soon!")
    # Similar implementation to CSV but with Excel format