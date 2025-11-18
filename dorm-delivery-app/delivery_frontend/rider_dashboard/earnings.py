import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.api_calls import get_my_deliveries

def show_earnings():
    """Show rider earnings and financial dashboard"""
    st.header("💰 Earnings Dashboard")
    
    # Time period filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        period = st.selectbox(
            "Time Period",
            ["Today", "This Week", "This Month", "Last Month", "All Time", "Custom Range"],
            key="earnings_period"
        )
    with col2:
        if period == "Custom Range":
            start_date = st.date_input("Start Date")
        else:
            st.write("")  # Spacer
    with col3:
        if period == "Custom Range":
            end_date = st.date_input("End Date")
        else:
            if st.button("🔄 Refresh"):
                st.rerun()
    
    # Get rider's deliveries and calculate earnings
    deliveries = get_my_deliveries() or []
    earnings_data = calculate_earnings_data(deliveries, period)
    
    # Display key metrics
    show_earnings_metrics(earnings_data)
    
    # Earnings charts
    show_earnings_charts(earnings_data)
    
    # Detailed breakdown
    show_earnings_breakdown(earnings_data)
    
    # Payment information
    show_payment_section(earnings_data)

def calculate_earnings_data(deliveries, period):
    """Calculate earnings data based on time period"""
    completed_deliveries = [d for d in deliveries if d.get('status') == 'completed']
    
    # Filter by time period
    now = datetime.now()
    if period == "Today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        filtered_deliveries = [d for d in completed_deliveries 
                             if is_delivery_in_period(d, start_date, now)]
    elif period == "This Week":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        filtered_deliveries = [d for d in completed_deliveries 
                             if is_delivery_in_period(d, start_date, now)]
    elif period == "This Month":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        filtered_deliveries = [d for d in completed_deliveries 
                             if is_delivery_in_period(d, start_date, now)]
    elif period == "Last Month":
        first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = first_day_this_month - timedelta(days=1)
        start_date = start_date.replace(day=1)
        end_date = first_day_this_month - timedelta(seconds=1)
        filtered_deliveries = [d for d in completed_deliveries 
                             if is_delivery_in_period(d, start_date, end_date)]
    else:
        filtered_deliveries = completed_deliveries
    
    # Calculate earnings metrics
    total_earnings = sum([d.get('payout', 5.00) or 5.00 for d in filtered_deliveries])
    delivery_count = len(filtered_deliveries)
    avg_earnings_per_delivery = total_earnings / delivery_count if delivery_count > 0 else 0
    
    # Weekly breakdown for charts
    weekly_data = get_weekly_breakdown(completed_deliveries)
    
    # Delivery type breakdown
    delivery_types = get_delivery_type_breakdown(filtered_deliveries)
    
    return {
        'period': period,
        'total_earnings': total_earnings,
        'delivery_count': delivery_count,
        'avg_earnings_per_delivery': avg_earnings_per_delivery,
        'filtered_deliveries': filtered_deliveries,
        'weekly_data': weekly_data,
        'delivery_types': delivery_types,
        'all_completed': completed_deliveries
    }

def is_delivery_in_period(delivery, start_date, end_date):
    """Check if delivery was completed within the date range"""
    try:
        completed_at = delivery.get('completed_at')
        if not completed_at:
            return False
        
        if 'T' in completed_at:
            delivery_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
            return start_date <= delivery_date <= end_date
    except:
        pass
    return False

def get_weekly_breakdown(deliveries):
    """Get earnings breakdown by week"""
    weekly_earnings = {}
    
    for delivery in deliveries:
        try:
            completed_at = delivery.get('completed_at')
            if completed_at and 'T' in completed_at:
                delivery_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                week_start = delivery_date - timedelta(days=delivery_date.weekday())
                week_key = week_start.strftime('%Y-%m-%d')
                
                payout = delivery.get('payout', 5.00) or 5.00
                if week_key in weekly_earnings:
                    weekly_earnings[week_key] += payout
                else:
                    weekly_earnings[week_key] = payout
        except:
            continue
    
    # Convert to list of tuples and sort
    weekly_list = [(week, earnings) for week, earnings in weekly_earnings.items()]
    weekly_list.sort()
    
    return weekly_list[-8:]  # Last 8 weeks

def get_delivery_type_breakdown(deliveries):
    """Break down earnings by delivery type/characteristics"""
    breakdown = {
        'Standard': 0,
        'Urgent': 0,
        'Large Items': 0
    }
    
    for delivery in deliveries:
        payout = delivery.get('payout', 5.00) or 5.00
        
        if delivery.get('urgency') == 'Urgent':
            breakdown['Urgent'] += payout
        elif delivery.get('item_size') == 'Large':
            breakdown['Large Items'] += payout
        else:
            breakdown['Standard'] += payout
    
    return breakdown

def show_earnings_metrics(earnings_data):
    """Display key earnings metrics"""
    st.subheader("📊 Earnings Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Earnings",
            f"${earnings_data['total_earnings']:.2f}",
            delta=f"{earnings_data['delivery_count']} deliveries"
        )
    
    with col2:
        st.metric(
            "Delivery Count",
            earnings_data['delivery_count'],
            delta="completed"
        )
    
    with col3:
        st.metric(
            "Average per Delivery",
            f"${earnings_data['avg_earnings_per_delivery']:.2f}",
            delta="earnings"
        )
    
    with col4:
        # Calculate projected weekly earnings
        weekly_avg = sum(week[1] for week in earnings_data['weekly_data'][-4:]) / 4 if len(earnings_data['weekly_data']) >= 4 else earnings_data['total_earnings']
        st.metric(
            "Weekly Average",
            f"${weekly_avg:.2f}",
            delta="projected"
        )

def show_earnings_charts(earnings_data):
    """Display earnings charts and visualizations"""
    st.subheader("📈 Earnings Trends")
    
    if len(earnings_data['weekly_data']) > 1:
        # Weekly earnings chart
        weeks = [f"Week {i+1}" for i in range(len(earnings_data['weekly_data']))]
        earnings = [week[1] for week in earnings_data['weekly_data']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weeks,
            y=earnings,
            mode='lines+markers',
            name='Weekly Earnings',
            line=dict(color='#1E90FF', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Weekly Earnings Trend",
            xaxis_title="Week",
            yaxis_title="Earnings ($)",
            template="plotly_white",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 More data needed to show earnings trends")
    
    # Delivery type breakdown pie chart
    if earnings_data['delivery_types']:
        labels = list(earnings_data['delivery_types'].keys())
        values = list(earnings_data['delivery_types'].values())
        
        fig_pie = px.pie(
            values=values,
            names=labels,
            title="Earnings by Delivery Type",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

def show_earnings_breakdown(earnings_data):
    """Show detailed earnings breakdown"""
    st.subheader("📋 Detailed Breakdown")
    
    if not earnings_data['filtered_deliveries']:
        st.info("No delivery data for the selected period")
        return
    
    # Create earnings table
    earnings_list = []
    for delivery in earnings_data['filtered_deliveries']:
        earnings_list.append({
            'Delivery ID': delivery.get('id', 'N/A'),
            'Date': format_delivery_date(delivery.get('completed_at')),
            'Pickup': delivery.get('pickup_location', 'Unknown'),
            'Dropoff': delivery.get('dropoff_location', 'Unknown'),
            'Payout': f"${delivery.get('payout', 5.00) or 5.00:.2f}",
            'Type': get_delivery_type(delivery),
            'Status': 'Completed'
        })
    
    # Display as dataframe
    df = pd.DataFrame(earnings_list)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export as CSV"):
            export_earnings_csv(earnings_list)
    with col2:
        if st.button("💳 Generate Invoice"):
            generate_invoice(earnings_data)

def show_payment_section(earnings_data):
    """Show payment and payout information"""
    st.subheader("💳 Payment Information")
    
    # Available balance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Balance", f"${earnings_data['total_earnings']:.2f}")
    with col2:
        st.metric("Next Payout", "Friday")
    with col3:
        st.metric("Payment Method", "Bank Transfer")
    
    # Payout history
    st.write("#### 🏦 Payout History")
    payout_history = [
        {"Date": "2024-01-05", "Amount": "$45.00", "Status": "Completed"},
        {"Date": "2024-01-12", "Amount": "$52.50", "Status": "Completed"},
        {"Date": "2024-01-19", "Amount": "$38.75", "Status": "Processing"},
    ]
    
    for payout in payout_history:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{payout['Date']}**")
        with col2:
            st.write(payout['Amount'])
        with col3:
            status_color = "green" if payout['Status'] == "Completed" else "orange"
            st.markdown(f"<span style='color: {status_color}'>{payout['Status']}</span>", unsafe_allow_html=True)
    
    # Payment settings
    with st.expander("⚙️ Payment Settings"):
        st.write("**Bank Account Information**")
        st.text_input("Bank Name", value="Campus Credit Union")
        st.text_input("Account Number", type="password")
        st.text_input("Routing Number")
        
        st.write("**Payout Preferences**")
        payout_frequency = st.selectbox(
            "Payout Frequency",
            ["Weekly", "Bi-weekly", "Monthly"]
        )
        
        min_payout = st.number_input(
            "Minimum Payout Amount",
            min_value=10.0,
            value=25.0,
            step=5.0
        )
        
        if st.button("Save Payment Settings", type="primary"):
            st.success("Payment settings updated!")

def format_delivery_date(date_string):
    """Format delivery date for display"""
    try:
        if date_string and 'T' in date_string:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%b %d, %Y')
    except:
        pass
    return "Unknown date"

def get_delivery_type(delivery):
    """Determine delivery type for categorization"""
    if delivery.get('urgency') == 'Urgent':
        return "Urgent"
    elif delivery.get('item_size') == 'Large':
        return "Large Item"
    else:
        return "Standard"

def export_earnings_csv(earnings_list):
    """Export earnings data as CSV"""
    if not earnings_list:
        st.warning("No data to export")
        return
    
    df = pd.DataFrame(earnings_list)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV File",
        data=csv,
        file_name=f"earnings_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def generate_invoice(earnings_data):
    """Generate invoice for earnings"""
    st.info("🧾 Invoice Generation")
    
    invoice_data = {
        "Period": earnings_data['period'],
        "Total Deliveries": earnings_data['delivery_count'],
        "Total Earnings": f"${earnings_data['total_earnings']:.2f}",
        "Average per Delivery": f"${earnings_data['avg_earnings_per_delivery']:.2f}",
        "Generated Date": datetime.now().strftime('%Y-%m-%d')
    }
    
    # Display invoice preview
    st.write("#### Invoice Preview")
    for key, value in invoice_data.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{key}:**")
        with col2:
            st.write(value)
    
    if st.button("📄 Download Invoice PDF"):
        st.success("Invoice generated! PDF download coming soon.")
        # TODO: Implement PDF generation

# Utility function for calculating trends
def calculate_earnings_trend(weekly_data):
    """Calculate earnings trend (up/down)"""
    if len(weekly_data) < 2:
        return 0
    
    recent = weekly_data[-1][1]
    previous = weekly_data[-2][1] if len(weekly_data) >= 2 else recent
    
    if previous == 0:
        return 100 if recent > 0 else 0
    
    return ((recent - previous) / previous) * 100