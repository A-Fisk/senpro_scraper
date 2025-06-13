import streamlit as st
import os
import json
import shutil
from html_scrape import read_html_file, parse_planner_section, get_dates, select_meals, save_to_json
from calendar_invite import list_available_meal_plans, load_meal_plan, create_calendar, save_calendar
from bs4 import BeautifulSoup
from datetime import datetime

# Function to clear all meal plans and calendar files
def clear_all_data():
    # Clear meal_plans directory
    plans_dir = "meal_plans"
    if os.path.exists(plans_dir):
        shutil.rmtree(plans_dir)
        os.makedirs(plans_dir)
    else:
        os.makedirs(plans_dir)
        
    # Clear cal_invites directory
    cal_dir = "cal_invites"
    if os.path.exists(cal_dir):
        shutil.rmtree(cal_dir)
        os.makedirs(cal_dir)
    else:
        os.makedirs(cal_dir)

# Clear all data at app startup
clear_all_data()

# Initialize session state
if 'current_meal_plan' not in st.session_state:
    st.session_state.current_meal_plan = None

st.set_page_config(page_title="SenPro Calendar Converter", layout="wide")
st.title("SenPro Meal Plan to iCalendar Converter")

# Add a reset button in the sidebar
with st.sidebar:
    st.header("Options")
    if st.button("Reset All Data"):
        clear_all_data()
        st.session_state.current_meal_plan = None
        st.success("All meal plans cleared!")
        st.rerun()

st.markdown("""
This app converts your SenPro meal plans into iCalendar (.ics) files that you can import into any calendar application.

### How to use this app:

1. **Save your SenPro meal plan as HTML**:
   - Go to your SenPro meal planning page
   - Right-click anywhere on the page and select "Save As..." or "Save Page As..."
   - Save the file with a .html extension
   
2. **Upload the HTML file** in the "Create Meal Plan" tab
   
3. **Generate and download the .ics file** in the "Generate Calendar Invites" tab

4. **Import the .ics file** into your calendar application (Google Calendar, Outlook, Apple Calendar, etc.)

### Support & Feature Requests

Having issues or want to suggest improvements? Please open an issue on the
[GitHub repository](https://github.com/A-Fisk/senpro_scrape/issues).
""")

# Create tabs for different functionality
tab1, tab2 = st.tabs(["Step 1: Upload HTML & Create Meal Plan", "Step 2: Generate Calendar File"])

# Tab 1: Create Meal Plan
with tab1:
    st.header("Step 1: Upload SenPro HTML and Create Meal Plan")
    st.write("""
    Upload the HTML file you saved from SenPro. The app will extract all meal information and create a structured meal plan.
    """)
    
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
            
            # Store meal plan in session state
            st.session_state.current_meal_plan = meal_plan
            
            # Display meal plan
            st.subheader("Meal Plan")
            
            for date, meals in meal_plan.items():
                with st.expander(f"Date: {date}"):
                    for meal in meals:
                        if isinstance(meal, dict):
                            meal_text = meal.get("text", "")
                            recipe_links = meal.get("recipe_links", {})
                            
                            st.write(meal_text)
                            
                            if recipe_links:
                                st.markdown("**Recipes:**")
                                for recipe_name, recipe_url in recipe_links.items():
                                    st.markdown(f"- [{recipe_name}]({recipe_url})")
            
            # Save options
            st.subheader("Save Meal Plan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                filename = st.text_input("Filename (without extension)", 
                                         value=f"meal_plan_{datetime.now().strftime('%Y%m%d')}")
            
            with col2:
                if st.button("Save Meal Plan"):
                    if filename:
                        # Clean up meal_plans directory completely
                        plans_dir = "meal_plans"
                        if os.path.exists(plans_dir):
                            # Remove directory and recreate it
                            shutil.rmtree(plans_dir)
                            os.makedirs(plans_dir)
                        else:
                            os.makedirs(plans_dir)
                        
                        # Save the meal plan
                        saved_file = save_to_json(meal_plan, f"{filename}.json")
                        st.success(f"Meal plan saved to {saved_file}")
                    else:
                        st.error("Please provide a filename")

# Tab 2: Generate Calendar Invites
with tab2:
    st.header("Step 2: Generate iCalendar File")
    st.write("""
    Generate an iCalendar (.ics) file from your meal plan that you can import into 
    Google Calendar, Apple Calendar, Outlook, or any other calendar application.
    """)
    
    # Check for current meal plan in session state
    if st.session_state.current_meal_plan:
        meal_plan = st.session_state.current_meal_plan
        
        # Display meal plan details
        st.subheader("Meal Plan Details")
        
        for date, meals in meal_plan.items():
            with st.expander(f"Date: {date}"):
                for meal in meals:
                    st.write(meal)
        
        # Generate calendar invites
        if st.button("Generate Calendar Invites"):
            with st.spinner("Creating calendar events..."):
                # Create a temporary filename for the calendar
                filename = f"meal_plan_{datetime.now().strftime('%Y%m%d')}"
                
                # Generate calendar
                cal = create_calendar(meal_plan)
                ics_file = save_calendar(cal, filename)
                
                # Provide download link
                with open(ics_file, "rb") as file:
                    btn = st.download_button(
                        label="Download Calendar File (.ics)",
                        data=file,
                        file_name=os.path.basename(ics_file),
                        mime="text/calendar"
                    )
                
                st.success("Calendar file created successfully!")
                
                # Add import instructions
                with st.expander("How to import this calendar file"):
                    st.markdown("""
                    ### Importing your calendar file:
                    
                    #### Google Calendar:
                    1. Go to [Google Calendar](https://calendar.google.com/)
                    2. Click the "+" next to "Other calendars"
                    3. Select "Import"
                    4. Upload the .ics file you downloaded
                    5. Choose the calendar to add the events to
                    6. Click "Import"
                    
                    #### Apple Calendar:
                    1. Open the Calendar app
                    2. Go to File > Import
                    3. Select the .ics file you downloaded
                    4. Click "Import"
                    
                    #### Outlook:
                    1. Open Outlook
                    2. Go to File > Open & Export > Import/Export
                    3. Select "Import an iCalendar (.ics) or vCalendar file"
                    4. Browse to the .ics file you downloaded
                    5. Click "Open"
                    """)
    else:
        # List available meal plans - as a fallback
        meal_plans = list_available_meal_plans()
        
        if not meal_plans:
            st.warning("No meal plan found. Please upload an HTML file and create a meal plan in Step 1.")
        else:
            # If only one meal plan exists, select it automatically
            if len(meal_plans) == 1:
                selected_plan = meal_plans[0]
                st.info(f"Using meal plan: {selected_plan}")
                
                # Load the selected meal plan
                meal_plan_path = os.path.join("meal_plans", selected_plan)
                meal_plan = load_meal_plan(meal_plan_path)
                
                # Store in session state
                st.session_state.current_meal_plan = meal_plan
                
                # Display meal plan details
                if meal_plan:
                    st.subheader("Meal Plan Details")
                    
                    for date, meals in meal_plan.items():
                        with st.expander(f"Date: {date}"):
                            for meal in meals:
                                if isinstance(meal, dict):
                            meal_text = meal.get("text", "")
                            recipe_links = meal.get("recipe_links", {})
                            
                            st.write(meal_text)
                            
                            if recipe_links:
                                st.markdown("**Recipes:**")
                                for recipe_name, recipe_url in recipe_links.items():
                                    st.markdown(f"- [{recipe_name}]({recipe_url})")
                    
                    # Generate calendar invites
                    if st.button("Generate Calendar Invites"):
                        with st.spinner("Creating calendar events..."):
                            cal = create_calendar(meal_plan)
                            ics_file = save_calendar(cal, selected_plan)
                            
                            # Provide download link
                            with open(ics_file, "rb") as file:
                                btn = st.download_button(
                                    label="Download Calendar File (.ics)",
                                    data=file,
                                    file_name=os.path.basename(ics_file),
                                    mime="text/calendar"
                                )
                            
                            st.success("Calendar file created successfully!")
                            
                            # Add import instructions
                            with st.expander("How to import this calendar file"):
                                st.markdown("""
                                ### Importing your calendar file:
                                
                                #### Google Calendar:
                                1. Go to [Google Calendar](https://calendar.google.com/)
                                2. Click the "+" next to "Other calendars"
                                3. Select "Import"
                                4. Upload the .ics file you downloaded
                                5. Choose the calendar to add the events to
                                6. Click "Import"
                                
                                #### Apple Calendar:
                                1. Open the Calendar app
                                2. Go to File > Import
                                3. Select the .ics file you downloaded
                                4. Click "Import"
                                
                                #### Outlook:
                                1. Open Outlook
                                2. Go to File > Open & Export > Import/Export
                                3. Select "Import an iCalendar (.ics) or vCalendar file"
                                4. Browse to the .ics file you downloaded
                                5. Click "Open"
                                """)
                else:
                    st.error("Error loading meal plan")
