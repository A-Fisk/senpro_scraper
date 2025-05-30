# SenPro Meal Planner Scraper

**Web App Available Here: https://senproscraper.streamlit.app/**

A tool to scrape meal plans from HTML files and organize them into a structured JSON format. Optionally creates calendar invites for meal planning.

## Features

- Extracts meal planning data from saved HTML files
- Organizes meal information by date and time
- Saves data in a structured JSON format using the date as filename
- Creates calendar invites (.ics files) from the meal plan data
- Web interface for easy use without command line knowledge

## Installation (For Beginners)

### Step 1: Install Python

If you don't already have Python installed:

#### For Windows:
1. Download the Python installer from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
3. Check "Add Python to PATH" during installation
4. Click "Install Now"

#### For macOS:
1. macOS comes with Python, but it's recommended to install the latest version
2. Download the macOS installer from [python.org](https://www.python.org/downloads/macos/)
3. Run the installer package and follow the instructions

### Step 2: Download This Project

#### Using Git (recommended):
1. Install Git if you don't have it already:
   - Windows: Download from [here](https://git-scm.com/download/win)
   - macOS: It may already be installed. If not, you'll be prompted to install it when you try to use it
2. Open Terminal (macOS) or Command Prompt (Windows)
3. Navigate to where you want to save the project:
   ```
   cd ~/Documents
   ```
4. Clone the repository:
   ```
   git clone https://github.com/yourusername/senpro_scrape.git
   ```
5. Navigate into the project folder:
   ```
   cd senpro_scrape
   ```

#### Without Git:
1. Download this repository as a ZIP file
2. Extract the ZIP file to a location of your choice
3. Open Terminal (macOS) or Command Prompt (Windows)
4. Navigate to the extracted folder:
   - Windows example: `cd C:\Users\YourName\Downloads\senpro_scrape`
   - macOS example: `cd ~/Downloads/senpro_scrape`

### Step 3: Install Required Packages

1. In your Terminal or Command Prompt, make sure you're in the project directory (senpro_scrape)
2. Install all required packages:
   ```
   pip install -r requirements.txt
   ```
   This will install all necessary dependencies for the project.

## Usage

### Web App (Recommended)

The easiest way to use this tool is through the web app:

1. Visit **https://senproscraper.streamlit.app/**
2. Upload your HTML file in the "Create Meal Plan" tab
3. View and save the extracted meal plan
4. Switch to the "Generate Calendar Invites" tab to create and download calendar invites

### Command Line Usage

If you prefer using the command line or need more control:

#### How to Save an HTML File from a Website

1. Visit your meal planning website in your web browser
2. Right-click on the page and select "Save As..." or "Save Page As..."
3. Choose where to save the HTML file (remember this location)
4. Save the file with a .html extension (e.g., `meal_plan.html`)

#### Scrape Meal Plans

1. Run the HTML scraper, replacing the path with the location of your saved HTML file:

   Windows example:
   ```
   python html_scrape.py C:\Users\YourName\Downloads\meal_plan.html
   ```

   macOS example:
   ```
   python html_scrape.py ~/Downloads/meal_plan.html
   ```

   If the file is in the same directory as the script, you can simply use:
   ```
   python html_scrape.py meal_plan.html
   ```

This will:
1. Read the HTML file
2. Extract meal planning information
3. Save it to a JSON file in the `meal_plans` folder

#### Create Calendar Invites

1. Run the calendar invite generator:
   ```
   python calendar_invite.py
   ```

3. The script will show you a list of available meal plans. Enter the number of the plan you want to use.

4. The script will create a calendar file (.ics) in the `cal_invites` directory.

#### How to Use the Calendar File

1. Locate the .ics file in the `cal_invites` directory
2. Double-click the file to open it with your default calendar application (e.g., Outlook, Google Calendar, Apple Calendar)
3. Your calendar application will prompt you to add these events to your calendar

### Running the Web App Locally

If you want to run the web app on your local machine:

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Your browser will open with the local version of the web app

## Directory Structure

- `html_scrape.py`: Script to extract meal plan data from HTML files
- `calendar_invite.py`: Script to generate calendar invites from meal plans
- `app.py`: Streamlit web application
- `meal_plans/`: Directory where extracted meal plans are stored
- `cal_invites/`: Directory where calendar invites are stored

## Troubleshooting

- **"Command not found: python"**: Make sure Python is installed and added to your PATH.
- **"No module named..."**: Make sure you've installed all requirements with `pip install -r requirements.txt`.
- **HTML parsing errors**: The script is designed for a specific website structure. If the meal plan website changes its layout, the script may need to be updated.

## Requirements

- Python 3.9+
- Beautiful Soup 4
- icalendar

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.