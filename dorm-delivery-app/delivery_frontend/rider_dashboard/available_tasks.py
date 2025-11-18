import streamlit as st
import time
from datetime import datetime
from utils.api_calls import get_available_tasks, accept_delivery

def show_available_tasks():
    """Show available delivery tasks for riders"""
    st.header("📋 Available Delivery Tasks")
    
    # Auto-refresh and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("Available Near You")
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        if auto_refresh:
            time.sleep(10)  # Refresh every 10 seconds
            st.rerun()
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Get available tasks
    tasks = get_available_tasks() or []
    # MOCK DATA - REMOVE LATER
    tasks = [
    {"id": 1, "pickup_location": "Library", "dropoff_location": "Dorm A", "item_description": "Textbook", "payout": 5.00, "urgency": "Standard", "customer_name": "Alex J."},
    {"id": 2, "pickup_location": "Student Center", "dropoff_location": "Dorm C", "item_description": "Package", "payout": 7.00, "urgency": "Urgent", "customer_name": "Taylor R."}
]
    
    if not tasks:
        show_no_tasks_state()
        return
    
    # Display tasks
    st.success(f"🎯 Found {len(tasks)} available delivery{'s' if len(tasks) != 1 else ''} near you!")
    
    # Sort tasks by urgency and payout
    sorted_tasks = sort_tasks(tasks)
    
    # Display each task
    for task in sorted_tasks:
        display_task_card(task)
    
    # Quick stats
    show_task_stats(tasks)

def show_no_tasks_state():
    """Show state when no tasks are available"""
    st.info("📭 No available delivery tasks at the moment.")
    st.write("""
    **What you can do:**
    - Check back in a few minutes - new deliveries come frequently
    - Make sure your availability is set to 'Online'
    - Expand your delivery range in settings
    """)
    
    # Quick tips for riders
    with st.expander("💡 Tips for getting more deliveries"):
        st.write("""
        - Keep the app open during peak hours (lunch 11AM-1PM, dinner 5PM-7PM)
        - Stay in high-traffic areas like dorms and student centers
        - Maintain a high rating for priority on deliveries
        - Set your availability to receive push notifications
        """)

def sort_tasks(tasks):
    """Sort tasks by priority (urgent first, then by payout)"""
    def task_priority(task):
        priority_score = 0
        if task.get('urgency') == 'Urgent':
            priority_score += 100
        if task.get('item_size') == 'Small':
            priority_score += 10  # Prefer smaller items
        # Add payout to priority (higher payout = higher priority)
        payout = task.get('payout', 0) or 0
        priority_score += payout
        return priority_score
    
    return sorted(tasks, key=task_priority, reverse=True)

def display_task_card(task):
    """Display an available task card"""
    task_id = task.get('id', 'N/A')
    payout = task.get('payout', 5.00)  # Default $5 if not specified
    
    with st.container():
        st.markdown("---")
        
        # Task header with payout
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"### 🚚 Delivery #{task_id}")
        with col2:
            st.metric("Payout", f"${payout:.2f}")
        
        # Task details
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**📍 Pickup:** {task.get('pickup_location', 'Unknown')}")
            st.write(f"**🎯 Dropoff:** {task.get('dropoff_location', 'Unknown')}")
            st.write(f"**📦 Item:** {task.get('item_description', 'No description')}")
            
            # Item size and type
            if task.get('item_size'):
                size_icon = get_size_icon(task.get('item_size'))
                st.write(f"**{size_icon} Size:** {task.get('item_size')}")
        
        with col2:
            # Customer and timing info
            if task.get('customer_name'):
                st.write(f"**👤 Customer:** {task.get('customer_name')}")
            
            if task.get('urgency'):
                urgency_icon = "🔥" if task.get('urgency') == 'Urgent' else "⏱️"
                st.write(f"**{urgency_icon} Urgency:** {task.get('urgency')}")
            
            # Distance and ETA estimates
            st.write(f"**📏 Distance:** ~0.8 miles")  # Placeholder
            st.write(f"**⏱️ Est. Time:** 15-20 min")  # Placeholder
            
            # Posted time
            if task.get('created_at'):
                posted_time = format_posted_time(task.get('created_at'))
                st.caption(f"Posted: {posted_time}")
        
        # Special instructions
        if task.get('instructions'):
            with st.expander("📝 Delivery Instructions"):
                st.write(task.get('instructions'))
        
        # Accept button
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("✅ Accept Delivery", key=f"accept_{task_id}", type="primary", use_container_width=True):
                accept_delivery_task(task_id, task)
        
        with col2:
            if st.button("📍 View Map", key=f"map_{task_id}", use_container_width=True):
                show_task_map(task)
        
        with col3:
            if st.button("ℹ️ Details", key=f"details_{task_id}", use_container_width=True):
                show_task_details(task)

def get_size_icon(size):
    """Get icon for item size"""
    size_icons = {
        'Small': '🎒',
        'Medium': '👜', 
        'Large': '📦'
    }
    return size_icons.get(size, '📦')

def format_posted_time(created_at):
    """Format how long ago the task was posted"""
    try:
        if 'T' in created_at:
            task_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now()
            diff = now - task_time
            
            minutes = diff.total_seconds() / 60
            if minutes < 1:
                return "Just now"
            elif minutes < 60:
                return f"{int(minutes)} min ago"
            else:
                hours = minutes / 60
                return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
    except:
        pass
    return "Recently"

def accept_delivery_task(task_id, task):
    """Handle delivery acceptance"""
    with st.spinner("Accepting delivery..."):
        success = accept_delivery(task_id)
        
        if success:
            st.success("🎉 Delivery accepted! Head to 'My Deliveries' to manage it.")
            st.balloons()
            
            # Show next steps
            st.info("""
            **Next Steps:**
            1. Go to the pickup location
            2. Confirm pickup with the customer
            3. Deliver to the dropoff location  
            4. Mark as delivered in the app
            5. Get paid!
            """)
            
            # Auto-redirect after a delay
            time.sleep(3)
            st.sidebar.radio("Go to", ["Dashboard", "Available Tasks", "My Deliveries", "Earnings"], 
                           index=2, key="rider_nav")
            st.rerun()
        else:
            st.error("❌ Failed to accept delivery. It may have been taken by another rider.")

def show_task_map(task):
    """Show map view for task (placeholder)"""
    st.info("🗺️ Map view coming soon!")
    st.write(f"**Route:** {task.get('pickup_location')} → {task.get('dropoff_location')}")
    st.write("Interactive campus map will be available in the next update.")

def show_task_details(task):
    """Show detailed task information"""
    with st.expander("📋 Full Task Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Delivery Information**")
            st.write(f"**ID:** #{task.get('id')}")
            st.write(f"**Status:** {task.get('status', 'pending')}")
            st.write(f"**Payout:** ${task.get('payout', 5.00):.2f}")
            st.write(f"**Item Size:** {task.get('item_size', 'Medium')}")
            
        with col2:
            st.write("**Customer Information**")
            st.write(f"**Name:** {task.get('customer_name', 'Not specified')}")
            if task.get('customer_rating'):
                st.write(f"**Rating:** {task.get('customer_rating')}⭐")
        
        st.write("**Full Description**")
        st.write(task.get('item_description', 'No description provided'))
        
        if task.get('instructions'):
            st.write("**Special Instructions**")
            st.write(task.get('instructions'))

def show_task_stats(tasks):
    """Show statistics about available tasks"""
    st.markdown("---")
    st.subheader("📊 Task Statistics")
    
    urgent_tasks = len([t for t in tasks if t.get('urgency') == 'Urgent'])
    small_items = len([t for t in tasks if t.get('item_size') == 'Small'])
    total_payout = sum([t.get('payout', 5.00) or 5.00 for t in tasks])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Urgent Tasks", urgent_tasks)
    with col2:
        st.metric("Small Items", small_items)
    with col3:
        st.metric("Total Payout", f"${total_payout:.2f}")
    
    # Task distribution by location
    st.write("**📍 Task Distribution**")
    locations = {}
    for task in tasks:
        loc = task.get('pickup_location', 'Unknown')
        locations[loc] = locations.get(loc, 0) + 1
    
    for location, count in list(locations.items())[:3]:  # Show top 3
        st.write(f"- {location}: {count} task{'s' if count != 1 else ''}")

# Auto-refresh background process
def start_auto_refresh():
    """Start auto-refresh in background"""
    if st.session_state.get('auto_refresh', False):
        time.sleep(30)  # Refresh every 30 seconds
        st.rerun()