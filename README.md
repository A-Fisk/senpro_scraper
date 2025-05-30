# SenPro Meal Planner Scraper

A tool to scrape meal plans from HTML files and organize them into a structured JSON format. Optionally creates calendar invites for meal planning.

## Features

- Extracts meal planning data from saved HTML files
- Organizes meal information by date and time
- Saves data in a structured JSON format using the date as filename
- Creates calendar invites (.ics files) from the meal plan data

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/senpro_scrape.git
   cd senpro_scrape
   ```

2. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate senpro_scrape
   ```

## Usage

### Scrape Meal Plans

Run the HTML scraper with the path to your saved HTML file:

```bash
python html_scrape.py path/to/saved_page.html
```

This will:
1. Read the HTML file
2. Extract meal planning information
3. Save it to a JSON file named after the first date in the meal plan

You can also run the script in debug mode to explore the HTML structure:

```bash
python html_scrape.py path/to/saved_page.html --debug
```

### Create Calendar Invites

Generate calendar invites from a previously saved meal plan:

```bash
python calendar_invite.py
```

The script will:
1. List all available meal plans in the `meal_plans` directory
2. Let you select which plan to process
3. Create calendar events for each meal
4. Save as an .ics file in the `cal_invites` directory with the same base filename

## Directory Structure

- `html_scrape.py`: Script to extract meal plan data from HTML files
- `calendar_invite.py`: Script to generate calendar invites from meal plans
- `meal_plans/`: Directory where extracted meal plans are stored
- `cal_invites/`: Directory where calendar invites are stored

## Requirements

- Python 3.9+
- Beautiful Soup 4
- icalendar

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.