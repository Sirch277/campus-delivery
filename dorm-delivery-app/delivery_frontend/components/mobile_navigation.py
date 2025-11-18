import streamlit as st
import streamlit.components.v1 as components
import os

def mobile_navigation():
    """Simple mobile navigation component"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    component_path = os.path.join(current_dir, '..', 'static', 'mobile_nav_component.html')
    
    try:
        with open(component_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Render the component
        components.html(html_content, height=0)
        
    except FileNotFoundError:
        st.error(f"Mobile navigation component not found at: {component_path}")