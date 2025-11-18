import streamlit as st
from utils.api_calls import create_delivery

def show_create_delivery():
    """Show the delivery creation form"""
    st.header("📦 Create New Delivery")
    
    # Fixed campus locations - customize these for your school
    campus_locations = [
        "Main Library",
        "Student Center", 
        "Cafeteria",
        "Sports Complex",
        "North Dorm A",
        "North Dorm B",
        "South Dorm A", 
        "South Dorm B",
        "East Dorm A",
        "West Dorm A",
        "Academic Building A",
        "Academic Building B"
    ]
    
    with st.form("create_delivery_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            pickup_location = st.selectbox(
                "📍 Pickup Location",
                options=campus_locations,
                help="Where should the rider pick up your item?"
            )
        
        with col2:
            dropoff_location = st.selectbox(
                "🎯 Dropoff Location", 
                options=campus_locations,
                help="Where should the rider deliver your item?"
            )
        
        # Item details
        item_description = st.text_area(
            "📦 Item Description",
            placeholder="Describe what needs to be delivered...\nExamples: Textbook, Food order, Package, Documents",
            help="Be specific about what the rider is picking up"
        )
        
        # Special instructions
        instructions = st.text_area(
            "📝 Special Instructions (Optional)",
            placeholder="Any special instructions for the rider...\nExamples: 'Call when arriving', 'Leave at front desk', 'Fragile handle with care'",
            help="Additional details to help the rider complete your delivery"
        )
        
        # Urgency level
        urgency = st.select_slider(
            "⏱️ Delivery Urgency",
            options=["Flexible", "Standard", "Urgent"],
            value="Standard",
            help="How quickly do you need this delivered?"
        )
        
        # Estimated size
        item_size = st.radio(
            "📏 Item Size",
            options=["Small (fits in backpack)", "Medium (needs both hands)", "Large (may need cart)"],
            index=0
        )
        
        # Form submission
        submitted = st.form_submit_button("🚀 Create Delivery", type="primary")
        
        if submitted:
            # Validation
            if not item_description.strip():
                st.error("Please provide an item description")
                return
                
            if pickup_location == dropoff_location:
                st.error("Pickup and dropoff locations cannot be the same")
                return
            
                    # TEMPORARY: Mock successful delivery creation
            st.success("🎉 Delivery created successfully! (Development Mode)")
            st.balloons()
        
        # Show mock delivery details
        st.info(f"""
        **Mock Delivery Created:**
        - Pickup_location: {pickup_location}
        - Dropoff_location: {dropoff_location}
        - Item: {item_description}
        - Status: Pending rider assignment
        """)
        
        return 
            
     

def show_delivery_preview(pickup, dropoff, item, instructions):
    """Show a preview of the delivery before submission"""
    st.subheader("📋 Delivery Preview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Pickup:**", pickup)
        st.write("**Item:**", item)
    with col2:
        st.write("**Dropoff:**", dropoff)
        if instructions:
            st.write("**Instructions:**", instructions)