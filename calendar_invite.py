# Imports
import os
import json
import sys
from datetime import datetime, timedelta
import re
from icalendar import Calendar, Event
import pdb

def list_available_meal_plans():
    """
    List all available meal plans in the meal_plans directory.
    
    Returns:
        List of filenames of meal plans
    """
    meal_plans_dir = "meal_plans"
    
    if not os.path.exists(meal_plans_dir):
        print(f"Error: {meal_plans_dir} directory does not exist")
        return []
    
    meal_plans = [f for f in os.listdir(meal_plans_dir) if f.endswith('.json')]
    
    if not meal_plans:
        print("No meal plans found in the meal_plans directory")
        return []
    
    return meal_plans

def select_meal_plan():
    """
    Ask the user to select a meal plan file to process.
    
    Returns:
        Full path to the selected meal plan file
    """
    meal_plans = list_available_meal_plans()
    
    if not meal_plans:
        return None
    
    print("\nAvailable meal plans:")
    for i, plan in enumerate(meal_plans):
        print(f"{i+1}. {plan}")
    
    while True:
        try:
            choice = input("\nEnter the number of the meal plan to process (or 'q' to quit): ")
            if choice.lower() == 'q':
                return None
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(meal_plans):
                return os.path.join("meal_plans", meal_plans[choice_idx])
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def load_meal_plan(file_path):
    """
    Load a meal plan from a JSON file.
    
    Args:
        file_path: Path to the meal plan JSON file
        
    Returns:
        Dictionary containing the meal plan data
    """
    try:
        with open(file_path, 'r') as f:
            meal_plan = json.load(f)
        return meal_plan
    except Exception as e:
        print(f"Error loading meal plan: {e}")
        return None

def parse_date_from_id(date_id):
    """
    Extract date from a date ID string (e.g., 'date_cards29-05-2025').
    
    Args:
        date_id: Date ID string from the meal plan
        
    Returns:
        datetime object representing the date
    """
    # Extract date using regex
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})', date_id)
    if match:
        day, month, year = match.groups()
        return datetime(int(year), int(month), int(day))
    else:
        # If extraction fails, use current date
        print(f"Warning: Could not extract date from '{date_id}', using current date")
        return datetime.now()

def parse_time_from_meal(meal_text):
    """
    Extract time from a meal text.
    
    Args:
        meal_text: Text describing the meal
        
    Returns:
        Time as a string (HH:MM) or None if not found
    """
    # Look for time at the beginning of the meal text
    match = re.match(r'(\d{1,2}):(\d{2})', meal_text)
    if match:
        hour, minute = match.groups()
        return f"{int(hour):02d}:{minute}"
    else:
        return None

def create_calendar_event(date, meal_text):
    """
    Create a calendar event for a meal.
    
    Args:
        date: datetime object for the date of the meal
        meal_text: Text describing the meal
        
    Returns:
        icalendar.Event object
    """
    event = Event()
    
    # Extract time from meal text
    time_str = parse_time_from_meal(meal_text)
    
    if time_str:
        hour, minute = map(int, time_str.split(':'))
        event_time = date.replace(hour=hour, minute=minute)
    else:
        # Default to noon if no time is found
        event_time = date.replace(hour=12, minute=0)
    
    # Set event properties
    event.add('summary', meal_text)
    event.add('dtstart', event_time)
    event.add('dtend', event_time + timedelta(minutes=30))  # Default 30-minute duration
    event.add('dtstamp', datetime.now())
    event['uid'] = f"{event_time.strftime('%Y%m%dT%H%M%S')}@senproscrape.meal"
    event.add('description', meal_text)
    
    return event

def create_calendar(meal_plan):
    """
    Create a calendar with events for all meals in the meal plan.
    
    Args:
        meal_plan: Dictionary containing the meal plan data
        
    Returns:
        icalendar.Calendar object
    """
    cal = Calendar()
    cal.add('prodid', '-//SenPro Meal Scraper//senproscrape.meal//')
    cal.add('version', '2.0')
    
    # Process each date in the meal plan
    for date_id, meals in meal_plan.items():
        date = parse_date_from_id(date_id)
        
        # Process each meal for this date
        for meal_text in meals:
            event = create_calendar_event(date, meal_text)
            cal.add_component(event)
    
    return cal

def save_calendar(cal, base_filename):
    """
    Save the calendar to an .ics file in the cal_invites directory.
    
    Args:
        cal: icalendar.Calendar object
        base_filename: Base filename to use for the calendar file
        
    Returns:
        Path to the saved calendar file
    """
    # Create cal_invites directory if it doesn't exist
    cal_dir = "cal_invites"
    if not os.path.exists(cal_dir):
        os.makedirs(cal_dir)
        print(f"Created directory: {cal_dir}")
    
    # Generate filename based on the input meal plan file
    filename = os.path.join(cal_dir, f"{os.path.splitext(os.path.basename(base_filename))[0]}.ics")
    
    # Write calendar to file
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"Calendar invite saved to {filename}")
    return filename

if __name__ == "__main__":
    # Ask which mealplan to read in
    meal_plan_path = select_meal_plan()
    if not meal_plan_path:
        print("No meal plan selected. Exiting.")
        sys.exit(0)
    
    # Load the meal plan
    meal_plan = load_meal_plan(meal_plan_path)
    if not meal_plan:
        sys.exit(1)
    
    # Parse into an ical calendar invite
    cal = create_calendar(meal_plan)
    
    # Save into the cal invites dir
    save_calendar(cal, meal_plan_path)
