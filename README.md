# SenPro Meal Planner Scraper

A tool to scrape meal plans from HTML files and organize them into a structured JSON format. Optionally creates calendar invites for meal planning.

## Features

- Extracts meal planning data from saved HTML files
- Organizes meal information by date and time
- Saves data in a structured JSON format using the date as filename
- Creates calendar invites (.ics files) from the meal plan data

## Installation (For Beginners)

### Step 1: Install Miniforge (Conda)

Miniforge is a minimal installer for Conda, which is a package manager that will help install all the required dependencies.

#### For Windows:
1. Download the Miniforge3 installer for Windows from [here](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe)
2. Run the downloaded .exe file
3. Follow the installation prompts, keeping all default options
4. Check the box that says "Add Miniforge3 to my PATH environment variable"

#### For macOS:
1. Download the Miniforge3 installer for macOS from [here](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh) (for Intel Macs) or [here](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh) (for Apple Silicon Macs)
2. Open Terminal (you can find it in Applications > Utilities > Terminal)
3. Navigate to your Downloads folder by typing:
   ```
   cd ~/Downloads
   ```
4. Make the installer executable by typing:
   ```
   chmod +x Miniforge3-MacOSX-*.sh
   ```
5. Run the installer:
   ```
   ./Miniforge3-MacOSX-*.sh
   ```
6. Follow the prompts, accepting the license and default installation location
7. When asked if you want to initialize Miniforge3, type "yes"
8. Close and reopen your Terminal window

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

### Step 3: Create and Activate the Conda Environment

1. In your Terminal or Command Prompt, make sure you're in the project directory (senpro_scrape)
2. Create the conda environment with all required packages:
   ```
   conda env create -f environment.yml
   ```
   This may take a few minutes as it downloads and installs all required packages.
3. Activate the environment:
   - Windows: `conda activate senpro_scrape`
   - macOS: `conda activate senpro_scrape`

## Usage (For Beginners)

### How to Save an HTML File from a Website

1. Visit your meal planning website in your web browser
2. Right-click on the page and select "Save As..." or "Save Page As..."
3. Choose where to save the HTML file (remember this location)
4. Save the file with a .html extension (e.g., `meal_plan.html`)

### Scrape Meal Plans

1. Make sure your conda environment is activated:
   ```
   conda activate senpro_scrape
   ```

2. Run the HTML scraper, replacing the path with the location of your saved HTML file:

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

### Create Calendar Invites

1. Make sure your conda environment is activated:
   ```
   conda activate senpro_scrape
   ```

2. Run the calendar invite generator:
   ```
   python calendar_invite.py
   ```

3. The script will show you a list of available meal plans. Enter the number of the plan you want to use.

4. The script will create a calendar file (.ics) in the `cal_invites` directory.

### How to Use the Calendar File

1. Locate the .ics file in the `cal_invites` directory
2. Double-click the file to open it with your default calendar application (e.g., Outlook, Google Calendar, Apple Calendar)
3. Your calendar application will prompt you to add these events to your calendar

## Directory Structure

- `html_scrape.py`: Script to extract meal plan data from HTML files
- `calendar_invite.py`: Script to generate calendar invites from meal plans
- `meal_plans/`: Directory where extracted meal plans are stored
- `cal_invites/`: Directory where calendar invites are stored

## Troubleshooting

- **"Command not found: conda"**: Try reopening your terminal or command prompt. If that doesn't work, you may need to add conda to your PATH manually.
- **"No module named..."**: Make sure you've activated the conda environment with `conda activate senpro_scrape`.
- **HTML parsing errors**: The script is designed for a specific website structure. If the meal plan website changes its layout, the script may need to be updated.

## Requirements

- Python 3.9+
- Beautiful Soup 4
- icalendar

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.