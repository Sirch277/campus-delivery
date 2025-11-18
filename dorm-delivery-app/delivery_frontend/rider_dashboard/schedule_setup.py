import streamlit as st
import datetime
from datetime import timedelta

def show_schedule_setup():
    """Show class schedule setup form for riders"""
    
    st.title("📚 Set Up Your Class Schedule")
    st.write("Configure your availability based on your semester timetable")
    
    # Semester Selection
    st.header("1. Select Your Semester")
    
    col1, col2 = st.columns(2)
    
    with col1:
        semester = st.radio(
            "Current Semester",
            ["Autumn Semester (September - January)", 
             "Spring Semester (March - June)",
             "Custom Dates"],
            key="semester_select"
        )
    
    with col2:
        # Auto-fill dates based on selection
        today = datetime.date.today()
        year = today.year
        
        if semester == "Autumn Semester (September - January)":
            start_date = datetime.date(year, 9, 1)
            end_date = datetime.date(year + 1, 1, 15)
            
        elif semester == "Spring Semester (March - June)":
            start_date = datetime.date(year, 3, 1)
            end_date = datetime.date(year, 6, 15)
            
        else:  # Custom dates
            start_date = st.date_input("Start Date", datetime.date(year, 9, 1))
            end_date = st.date_input("End Date", datetime.date(year, 12, 15))
    
    # Display semester info
    st.info(f"**Semester Period:** {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    
    # Class Schedule Setup
    st.header("2. Add Your Weekly Classes")
    st.write("Enter your recurring weekly classes. We'll automatically calculate your delivery availability.")
    
    # Initialize class list in session state
    if 'classes' not in st.session_state:
        st.session_state.classes = []
    
    # Class input form
    with st.form("class_form"):
        col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
        
        with col1:
            day = st.selectbox("Day", 
                             ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        with col2:
            start_time = st.time_input("Start Time", datetime.time(9, 0))
        
        with col3:
            end_time = st.time_input("End Time", datetime.time(10, 0))
            # Validate end time
            if end_time <= start_time:
                st.error("End time must be after start time")
        
        with col4:
            course_name = st.text_input("Course", placeholder="e.g., Mathematics")
        
        location = st.selectbox("Location", 
                              ["Building 7", "Building 6", "Building 5", "Library", "Gym", "Online"])
        
        submitted = st.form_submit_button("➕ Add Class")
        
        if submitted:
            if end_time > start_time:
                new_class = {
                    "day": day,
                    "start_time": start_time,
                    "end_time": end_time,
                    "course": course_name,
                    "location": location
                }
                st.session_state.classes.append(new_class)
                st.success(f"Added {course_name} on {day}")
            else:
                st.error("Please fix the time range")
    
    # Display current classes
    if st.session_state.classes:
        st.subheader("Your Classes")
        
        # Group by day for better display
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        classes_by_day = {day: [] for day in days_order}
        
        for class_item in st.session_state.classes:
            classes_by_day[class_item["day"]].append(class_item)
        
        for day in days_order:
            day_classes = classes_by_day[day]
            if day_classes:
                with st.expander(f"📅 {day}"):
                    for i, class_item in enumerate(day_classes):
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"**{class_item['course']}**")
                        with col2:
                            st.write(f"{class_item['start_time'].strftime('%H:%M')} - {class_item['end_time'].strftime('%H:%M')}")
                        with col3:
                            if st.button("🗑️", key=f"delete_{day}_{i}"):
                                st.session_state.classes.remove(class_item)
                                st.rerun()
    
    # Availability Preview
    if st.session_state.classes:
        st.header("3. Your Delivery Availability")
        show_availability_preview(st.session_state.classes)
    
    # Save and Continue
    if st.button("💾 Save Schedule & Continue", type="primary", width='stretch'):
     save_schedule(start_date, end_date, st.session_state.classes)
     st.session_state.schedule_saved = True  # Set flag
     st.rerun()
    # Show success message only after save
    if st.session_state.get('schedule_saved'):
     st.balloons()
     st.success("✅ Schedule saved! Use the sidebar to go back to Dashboard.")
    # Clear the flag so it doesn't show again
     st.session_state.schedule_saved = False
    
    

def show_availability_preview(classes):
    """Show calculated delivery availability based on classes"""
    
    # Simple availability calculation
    st.write("Based on your classes, you'll be available for deliveries during these times:")
    
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days_order:
        day_classes = [c for c in classes if c["day"] == day]
        if day_classes:
            # Sort classes by start time
            day_classes.sort(key=lambda x: x["start_time"])
            
            # Calculate gaps between classes
            available_slots = []
            current_time = datetime.time(8, 0)  # Start at 8 AM
            
            
            for class_item in day_classes:
                class_start = class_item["start_time"]
                class_end = class_item["end_time"]
                
                # If there's a gap before this class
                if current_time < class_start:
                    gap_hours = (datetime.datetime.combine(datetime.date.today(), class_start) - 
                                datetime.datetime.combine(datetime.date.today(), current_time)).seconds / 3600
                    if gap_hours >= 1:  # Only show slots of 1+ hours
                        available_slots.append(f"{current_time.strftime('%H:%M')} - {class_start.strftime('%H:%M')}")
                
                current_time = max(current_time, class_end)
            
            # Add time after last class
            if current_time < datetime.time(22, 0):  # Until 10 PM
              available_slots.append(f"{current_time.strftime('%H:%M')} - 22:00")
            
            if available_slots:
                with st.expander(f"✅ {day} - Available Slots", expanded=True):
                    for slot in available_slots:
                        st.write(f"🕐 {slot}")
            else:
                st.write(f"❌ {day} - No available slots")
        else:
            st.write(f"🌟 {day} - Full day availability!")

def save_schedule(start_date, end_date, classes):
    """Save schedule to session state (will be backend later)"""
    st.session_state.rider_schedule = {
        "semester_start": start_date,
        "semester_end": end_date,
        "classes": classes,
        "setup_complete": True
    }
    
    # Calculate and store availability
    st.session_state.rider_availability = calculate_availability(classes)

def calculate_availability(classes):
    """Calculate delivery availability from classes"""
    # This will be expanded with more sophisticated logic
    availability = {}
    
    for class_item in classes:
        day = class_item["day"]
        if day not in availability:
            availability[day] = []
        # For now, just store the inverse of class times
        # This will be refined with actual gap calculation
    
    return availability

if __name__ == "__main__":
    show_schedule_setup()