# Import things
import json
import csv
from datetime import datetime
import os
from bs4 import BeautifulSoup
import re
import pdb

## Read from local HTML file
def read_html_file(file_path):
    try:
        print(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return None

## Parse out the planner section
def parse_planner_section(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Return the entire soup object since we'll use CSS selectors directly
    return soup


# Extract meal information from the HTML
def get_dates(soup):
    # Find all date cards
    date_cards = soup.select("div.date_cards.d-flex.flex-column")

    dates = []
    for div in date_cards:
        print(div)
        date = div['id']
        dates.append(date)
    
    if not date_cards:
        print("No date_card elements found")
        return None

    return dates

def select_meals(soup, curr_date):
    """
    Extract meals for a specific date.
    
    Args:
        soup: BeautifulSoup object with the HTML content
        curr_date: Date ID to extract meals for
        
    Returns:
        List of meals for the specified date
    """
    # Find the div for the current date
    curr_day = soup.find_all("div", id=curr_date)
    if not curr_day:
        print(f"No div found with id {curr_date}")
        return []
        
    # Get meal times
    curr_times = [x.text.strip() for x in curr_day[0].find_all(
        "div", class_=['date_card_date', 'font-small'])]
        
    # Get meal containers
    meal_css = curr_day[0].find_all("div", class_=['outline-box', 'pb-0', 'px-2', 'pt-2', 'mb-2', 'date_card_cont'])
    
    meal_total = []

    # Process each meal
    for curr_meal, curr_time in zip(meal_css, curr_times):
        # Get meal title
        meal_title_element = curr_meal.find("span")
        meal_title = meal_title_element.text.strip() if meal_title_element else "Unknown Meal"
        
        # Get meal details
        meal_details = [x.text.strip() for x in curr_meal.find_all('a', class_='mealplan')]
        
        # Combine into a single string with time, title, and details
        result = " ".join([curr_time, meal_title] + meal_details)
        meal_total.append(result)

    return meal_total


def extract_meal_info(date_cards):
    meal_plan = {}
    
    for date_card in date_cards:
        # Get the date ID
        date_id = date_card.get('id')
        if not date_id:
            continue
            
        # Find the date text
        date_text_element = date_card.find(class_='date_card_date')
        if not date_text_element or not date_text_element.text.strip():
            continue
            
        date_text = date_text_element.text.strip()
        meal_plan[date_text] = {}
        
        # Find all meal times and their corresponding meals
        time_sections = date_card.find_all(class_='meal_time')
        
        for time_section in time_sections:
            # Get the time text
            time_text_element = time_section.find(class_='meal_time_text')
            if not time_text_element or not time_text_element.text.strip():
                continue
                
            time_text = time_text_element.text.strip()
            meal_plan[date_text][time_text] = []
            
            # Find all meals for this time
            meal_elements = time_section.find_all(class_='mealplan')
            
            for meal_element in meal_elements:
                meal_text = meal_element.text.strip()
                if meal_text:
                    meal_plan[date_text][time_text].append(meal_text)
    
    return meal_plan


## Build a dictionary with [day][time][meal]
def organize_meals(meal_info):
    # This function might not be needed if extract_meal_info already creates the desired structure
    # But it could be used for additional processing or restructuring if needed
    return meal_info

## Save the file
def save_to_json(data, filename=None):
    # Create meal_plans directory if it doesn't exist
    plans_dir = "meal_plans"
    if not os.path.exists(plans_dir):
        os.makedirs(plans_dir)
        print(f"Created directory: {plans_dir}")
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(plans_dir, f"meal_plan_{timestamp}.json")
    else:
        # If filename is provided, make sure it's in the meal_plans directory
        filename = os.path.join(plans_dir, os.path.basename(filename))
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Meal plan saved to {filename}")
    return filename

def save_to_csv(data, filename=None):
    """
    Save meal plan data to a CSV file.
    
    Args:
        data: Dictionary with date->meals mapping
        filename: Optional filename, will generate a timestamped one if not provided
    
    Returns:
        The filename where data was saved
    """
    # Create meal_plans directory if it doesn't exist
    plans_dir = "meal_plans"
    if not os.path.exists(plans_dir):
        os.makedirs(plans_dir)
        print(f"Created directory: {plans_dir}")
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(plans_dir, f"meal_plan_{timestamp}.csv")
    else:
        # If filename is provided, make sure it's in the meal_plans directory
        filename = os.path.join(plans_dir, os.path.basename(filename))
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Meal Details'])
        
        # For each date, write all meals
        for date, meals in data.items():
            # Flatten the meals list
            flat_meals = []
            for meal in meals:
                flat_meals.extend(meal)
            
            # Write one row per date with all meals
            writer.writerow([date, '; '.join(flat_meals)])
    
    print(f"Meal plan saved to {filename}")
    return filename

## Debug functions
def debug_show_elements(soup, selector=None, limit=10, depth=0):
    """
    Display HTML elements with their attributes for debugging.
    
    Args:
        soup: BeautifulSoup object or element
        selector: Optional CSS selector to filter elements
        limit: Maximum number of elements to display
        depth: Current recursion depth for indentation
    """
    pdb.set_trace()
    elements = soup.find_all('div', class_=[selector])
    
    count = 0
    for element in elements[:limit]:
        indent = "  " * depth
        # Print tag name and attributes
        attrs = ' '.join([f'{k}="{v}"' if isinstance(v, str) else f'{k}={v}' for k, v in element.attrs.items()])
        print(f"{indent}<{element.name} {attrs}>")
        
        # Print text content if it exists and isn't just whitespace
        if element.string and element.string.strip():
            print(f"{indent}  TEXT: {element.string.strip()}")
        
        count += 1
        if count >= limit:
            remaining = len(elements) - limit
            if remaining > 0:
                print(f"{indent}... and {remaining} more elements")
            break

def debug_explore_structure(soup, max_depth=3):
    """
    Explore and print the overall structure of the HTML document.
    """
    def _explore(element, depth=0, max_depth=3):
        if depth > max_depth:
            return
        
        indent = "  " * depth
        if element.name:
            # Print element tag and basic info
            class_attr = f" class='{' '.join(element.get('class', []))}'" if element.get('class') else ""
            id_attr = f" id='{element['id']}'" if element.get('id') else ""
            print(f"{indent}<{element.name}{class_attr}{id_attr}>")
            
            # Process children
            for child in element.children:
                if child.name:  # Skip NavigableString objects
                    _explore(child, depth + 1, max_depth)
    
    _explore(soup, 0, max_depth)

def debug_find_by_text(soup, text, limit=10):
    """
    Find elements containing the specified text.
    """
    elements = soup.find_all(string=lambda s: text.lower() in s.lower() if s else False)
    
    print(f"Found {len(elements)} elements containing '{text}':")
    for i, element in enumerate(elements[:limit]):
        parent = element.parent
        print(f"{i+1}. {parent.name} - {element.strip()[:50]}")
    
    if len(elements) > limit:
        print(f"...and {len(elements) - limit} more")

if __name__ == "__main__":
    import sys
    
    # Check if file path is provided as argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the HTML file: ")
    
    # Read HTML from file
    html_content = read_html_file(file_path)
    if not html_content:
        exit(1)
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Debug mode - interactive exploration
    if len(sys.argv) > 2 and sys.argv[2] == '--debug':
        print("\n===== HTML DEBUGGING MODE =====")
        print("Available commands:")
        print("1. List classes: Show all CSS classes in the document")
        print("2. Find text: Search for elements containing specific text")
        print("3. Show elements: Display elements matching a CSS selector")
        print("4. Explore structure: Show document structure up to a certain depth")
        print("5. Exit: Exit debugging mode")
        
        while True:
            choice = input("\nEnter command (1-5): ")
            
            if choice == '1':
                # List all classes
                classes = set()
                for tag in soup.find_all(True):
                    if tag.has_attr('class'):
                        for cls in tag['class']:
                            classes.add(cls)
                print("\nAvailable classes in the HTML:")
                print(sorted(list(classes)))
                
            elif choice == '2':
                # Find text
                search_text = input("Enter text to search for: ")
                debug_find_by_text(soup, search_text)
                
            elif choice == '3':
                # Show elements matching selector
                selector = input("Enter CSS selector (e.g. 'div.className'): ")
                limit = int(input("Maximum elements to display: ") or "10")
                debug_show_elements(soup, selector, limit)
                
            elif choice == '4':
                # Explore structure
                depth = int(input("Maximum depth to explore (1-5): ") or "3")
                debug_explore_structure(soup, min(max(1, depth), 5))
                
            elif choice == '5':
                print("Exiting debug mode...")
                break
                
            else:
                print("Invalid choice, please try again.")
        
        exit(0)
    
    # Regular execution
    # Parse the planner section
    planner_section = parse_planner_section(html_content)

    # Get dates
    dates = get_dates(planner_section)
    if not dates:
        print("No date elements found")
        print("Available classes in the HTML:")
        classes = set()
        for tag in soup.find_all(True):
            if tag.has_attr('class'):
                for cls in tag['class']:
                    classes.add(cls)
        print(sorted(list(classes)))
        exit(1)

    # Process all dates and gather meals
    meal_plan = {}
    for curr_date in dates:
        print(f"Processing date: {curr_date}")
        meals = select_meals(planner_section, curr_date)
        if meals:
            meal_plan[curr_date] = meals
    
    # Save to JSON file
    save_to_json(meal_plan)
