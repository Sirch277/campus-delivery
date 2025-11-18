import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Button Test",
    page_icon="🧪",
    layout="wide"
)

def main():
    st.title("🧪 Button Behavior Test")
    st.write("Testing the new button patterns from Streamlit documentation")
    
    # Initialize session state
    if 'test_state' not in st.session_state:
        st.session_state.test_state = {
            'current_page': 'home',
            'counter': 0,
            'form_data': None,
            'auto_refresh': False
        }
    
    # Test 1: Navigation with Callbacks
    st.header("1. Navigation with Callbacks")
    st.write("**Testing:** Buttons with `on_click` callbacks for navigation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    def navigate_to(page):
        st.session_state.test_state['current_page'] = page
    
    with col1:
        st.button("🏠 Home", key="nav_home", on_click=navigate_to, args=("home",))
    with col2:
        st.button("📊 Stats", key="nav_stats", on_click=navigate_to, args=("stats",))
    with col3:
        st.button("⚙️ Settings", key="nav_settings", on_click=navigate_to, args=("settings",))
    with col4:
        st.button("📝 Form", key="nav_form", on_click=navigate_to, args=("form",))
    
    # Display current page (should persist!)
    st.info(f"**Current Page:** {st.session_state.test_state['current_page']}")
    
    # Test 2: Counter with Callback
    st.header("2. Counter with Callback")
    st.write("**Testing:** Button that increments counter without nesting")
    
    def increment_counter():
        st.session_state.test_state['counter'] += 1
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("➕ Increment Counter", key="inc_btn", on_click=increment_counter)
    with col2:
        st.metric("Counter Value", st.session_state.test_state['counter'])
    
    # Test 3: Form with Proper Structure
    st.header("3. Form with Proper Structure")
    st.write("**Testing:** Using `st.form()` instead of nested widgets")
    
    with st.form("test_form"):
        name = st.text_input("Your Name")
        color = st.selectbox("Favorite Color", ["Red", "Blue", "Green", "Yellow"])
        agree = st.checkbox("I agree to terms")
        
        submitted = st.form_submit_button("Submit Form", type="primary")
        
        if submitted:
            st.session_state.test_state['form_data'] = {
                'name': name,
                'color': color,
                'agree': agree
            }
            st.success("Form submitted successfully!")
    
    # Show form data (should persist!)
    if st.session_state.test_state['form_data']:
        st.write("**Last Form Submission:**")
        st.json(st.session_state.test_state['form_data'])
    
    # Test 4: Toggle with Callback
    st.header("4. Toggle with Callback")
    st.write("**Testing:** Toggle button that controls UI state")
    
    def toggle_refresh():
        st.session_state.test_state['auto_refresh'] = not st.session_state.test_state['auto_refresh']
    
    col1, col2 = st.columns(2)
    with col1:
        status = "🟢 ON" if st.session_state.test_state['auto_refresh'] else "🔴 OFF"
        st.button(f"Auto-refresh: {status}", key="toggle_btn", on_click=toggle_refresh)
    with col2:
        if st.session_state.test_state['auto_refresh']:
            st.success("Auto-refresh is ENABLED")
            # Simulate auto-refresh
            if st.button("🔄 Simulate Refresh"):
                st.rerun()
        else:
            st.info("Auto-refresh is DISABLED")
    
    # Test 5: Anti-pattern Examples (What NOT to do)
    st.header("5. Anti-pattern Examples")
    st.write("**Testing:** Common mistakes that cause issues")
    
    with st.expander("❌ Anti-pattern: Nested Widgets in Button"):
        st.write("This will cause widgets to disappear:")
        st.code('''
if st.button("Show Form"):
    # ❌ These widgets disappear on next action!
    name = st.text_input("Name")  
    st.selectbox("Option", ["A", "B"])
''')
    
    with st.expander("❌ Anti-pattern: Modify Widget After Render"):
        st.write("This will cause errors:")
        st.code('''
st.text_input("Name", key="name_input")

if st.button("Clear Name"):
    # ❌ Error! Widget already rendered
    st.session_state.name_input = ""  
''')
    
    with st.expander("✅ Correct Pattern: Use Callback"):
        st.write("This works correctly:")
        st.code('''
def clear_name():
    st.session_state.name_input = ""

st.text_input("Name", key="name_input")
st.button("Clear Name", on_click=clear_name)  # ✅ Works!
''')
    
    # Test 6: Dynamic Content with Unique Keys
    st.header("6. Dynamic Content with Unique Keys")
    st.write("**Testing:** Adding dynamic widgets without duplicate keys")
    
    if 'dynamic_items' not in st.session_state:
        st.session_state.dynamic_items = []
    
    def add_item():
        st.session_state.dynamic_items.append(f"Item {len(st.session_state.dynamic_items) + 1}")
    
    def remove_item(index):
        st.session_state.dynamic_items.pop(index)
        st.rerun()
    
    st.button("➕ Add Item", key="add_item_btn", on_click=add_item)
    
    for i, item in enumerate(st.session_state.dynamic_items):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input(f"Item {i+1}", value=item, key=f"dynamic_input_{i}")
        with col2:
            st.button("🗑️", key=f"remove_{i}", on_click=remove_item, args=(i,))
    
    # Session State Debug
    st.header("🔧 Session State Debug")
    st.write("Current session state:")
    st.json(st.session_state.test_state)

if __name__ == "__main__":
    main()