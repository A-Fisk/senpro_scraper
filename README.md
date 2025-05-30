# SenPro Meal Planner Scraper

A tool to scrape meal plans from a website and organize them into a structured JSON format. Optionally creates calendar invites for meal planning.

## Features

- Scrapes meal planning data from a specified website
- Extracts meal information organized by day and time
- Saves data in a structured JSON format
- Can generate calendar invites from the meal plan data

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

Run the HTML scraper to extract meal plans:

```bash
python html_scrape.py
```

This will:
1. Connect to the meal planning website
2. Extract the meal planning information
3. Save it to a timestamped JSON file (e.g., `meal_plan_20250530_123456.json`)

### Create Calendar Invites (Optional)

Generate calendar invites from the scraped meal plan:

```bash
python calendar_invite.py meal_plan_20250530_123456.json
```

## Customization

To adapt this for different websites, modify the following in `html_scrape.py`:

- Update the URL to point to your target website
- Adjust the CSS selectors to match the structure of the target website
- Modify the data extraction logic if needed

## Requirements

- Python 3.9+
- Beautiful Soup 4
- Requests

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.