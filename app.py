import streamlit as st
import os
import json
from html_scrape import read_html_file, parse_planner_section, get_dates, select_meals, save_to_json
from calendar_invite import list_available_meal_plans, load_meal_plan, create_calendar, save_calendar
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Meal Plan Manager", layout="wide")
st.title("Meal Plan Manager")

# Create tabs for different functionality
tab1, tab2 = st.tabs(["Create Meal Plan", "Generate Calendar Invites"])

# Tab 1: Create Meal Plan
with tab1:
    st.header("Create Meal Plan from HTML")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload HTML file", type="html")
    
    if uploaded_file:
        # Read HTML content from uploaded file
        html_content = uploaded_file.read().decode()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get dates
        dates = get_dates(soup)
        
        if not dates:
            st.error("No date elements found in the HTML file")
            
            # Display available classes for debugging
            classes = set()
            for tag in soup.find_all(True):
                if tag.has_attr('class'):
                    for cls in tag['class']:
                        classes.add(cls)
            
            with st.expander("Available CSS classes"):
                st.write(sorted(list(classes)))
        else:
            # Process all dates and gather meals
            meal_plan = {}
            progress_bar = st.progress(0)
            
            for i, curr_date in enumerate(dates):
                meals = select_meals(soup, curr_date)
                if meals:
                    meal_plan[curr_date] = meals
                progress_bar.progress((i + 1) / len(dates))
            
            # Display meal plan
            st.subheader("Meal Plan")
            
            for date, meals in meal_plan.items():
                with st.expander(f"Date: {date}"):
                    for meal in meals:
                        st.write(meal)
            
            # Save options
            st.subheader("Save Meal Plan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                filename = st.text_input("Filename (without extension)", 
                                         value=f"meal_plan_{datetime.now().strftime('%Y%m%d')}")
            
            with col2:
                if st.button("Save Meal Plan"):
                    if filename:
                        saved_file = save_to_json(meal_plan, f"{filename}.json")
                        st.success(f"Meal plan saved to {saved_file}")
                    else:
                        st.error("Please provide a filename")

# Tab 2: Generate Calendar Invites
with tab2:
    st.header("Generate Calendar Invites")
    
    # List available meal plans
    meal_plans = list_available_meal_plans()
    
    if not meal_plans:
        st.warning("No meal plans found. Please create a meal plan first.")
    else:
        # Select meal plan
        selected_plan = st.selectbox("Select meal plan", meal_plans)
        
        if selected_plan:
            # Load the selected meal plan
            meal_plan_path = os.path.join("meal_plans", selected_plan)
            meal_plan = load_meal_plan(meal_plan_path)
            
            if not meal_plan:
                st.error("Error loading meal plan")
            else:
                # Display meal plan details
                st.subheader("Meal Plan Details")
                
                for date, meals in meal_plan.items():
                    with st.expander(f"Date: {date}"):
                        for meal in meals:
                            st.write(meal)
                
                # Generate calendar invites
                if st.button("Generate Calendar Invites"):
                    with st.spinner("Creating calendar events..."):
                        cal = create_calendar(meal_plan)
                        ics_file = save_calendar(cal, selected_plan)
                        
                        # Provide download link
                        with open(ics_file, "rb") as file:
                            btn = st.download_button(
                                label="Download Calendar Invite (.ics)",
                                data=file,
                                file_name=os.path.basename(ics_file),
                                mime="text/calendar"
                            )
                        
                        st.success("Calendar invites created successfully!")