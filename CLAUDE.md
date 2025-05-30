# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run script: `python html_scrape.py` or `python calendar_invite.py`
- Install dependencies: `conda env create -f environment.yml`
- Activate environment: `conda activate senpro_scrape`

## Code Style Guidelines
- Imports: Group standard library imports first, followed by third-party packages, then local imports
- Formatting: Use 4 spaces for indentation, max line length 88 characters
- Types: Use type hints for function parameters and return values
- Naming: Use snake_case for variables/functions, CamelCase for classes
- Comments: Use descriptive comments for code blocks as seen in html_scrape.py
- Error Handling: Use try/except blocks with specific exceptions
- Documentation: Add docstrings to functions and modules
- do not create a separate main() function to run, and instead call all the
  functions after the if __name__==__main__ block

## Project Structure
- html_scrape.py: Web scraping script for meal planning
- calendar_invite.py: Creates calendar invites from scraped data
- environment.yml: Conda environment specification
