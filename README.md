# ENPM611 Project Application - GitHub Issues Analysis (Poetry Project)

This project analyzes GitHub issues from the [python-poetry/poetry](https://github.com/python-poetry/poetry/issues) repository to generate insights about contributor activity, issue trends, and issue resolution behavior.  

It was implemented using the provided ENPM611 Project Application Template and extended with three fully functional analyses.

---
## Project Overview
This application loads issue data from a local JSON file and performs multiple analyses using Python, Pandas, and Matplotlib.

The project implements and extends the following core modules:
- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration parameters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With these utilities, the three implemented analyses generate meaningful, data-driven insights.

---
## Setup Instructions
### Clone and prepare your environment
Fork this repository and clone the fork to your local machine.  
In the root directory of the application, create a virtual environment, and activate that environment:
```bash
python -m venv .env
source .env/bin/activate       # (Mac/Linux)
.env\Scripts\activate          # (Windows)
```

### Install dependencies
Install required packages from requirements.txt:
```
pip install -r requirements.txt
```

### Download and configure the data file
The dataset (poetry_issues.json and poetry_issues_all.json) required for this project is already included in the repository under the data/ directory.
No additional download or configuration is needed.
If you move or replace the dataset, make sure the file path in config.json matches the new location.
By default, it should look like this:
{
  "data_path": "data/poetry_issues.json",
  "output_dir": "output/charts"
}
This configuration ensures that all analyses automatically load issue data from the included JSON file and save charts to the output/charts directory.

Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis
Run the project from the command line using:
python run.py --feature <number>

where <number> corresponds to one of the implemented analyses below.

---
###Feature 1: Contributor Activity Analysis
File: contributor_activity_analysis.py
This feature analyzes contributor participation based on the "creator" field from the dataset.

Outputs:
-Counts the number of issues created by each contributor.
-Optionally filters by year.
-Displays and saves a bar chart of the top 10 contributors.
-Prints total contributors, average issues per contributor, and most active contributor.

Run Command:
python run.py --feature 1

Sample Output:
Loaded 661 issues from data/poetry_issues.json.
Detected years in dataset: 2018, 2019, 2020, 2021, 2022, 2023, 2024

Enter a year to filter by (or press Enter to analyze all years): 2018

Showing contributor activity for year 2018


Would you like to save this chart? (Y/N): y

✅ Chart saved to: output/charts/contributor_activity_2018_20251102-112808.png


Contributor Activity Summary
----------------------------------------
Total contributors analyzed: 4
Total issues created: 4
Average issues per contributor: 1.00
Most active contributor: daisylb (1 issues)
Issue data range: 2018-06-12 → 2018-12-06
----------------------------------------

---
###Feature 2: Reopened vs Closed Issue Ratio Analysis
File: reopened_closed_ratio_analysis.py
This analysis focuses on understanding how effectively issues are resolved and how often they need to be reopened.
By examining the ratio of reopened to closed issues, we can monitor the overall stability and maintainability of the project.

Outputs:
-Filters issues within a specified date range.
-Counts and compares the number of closed, reopened, and open issues.
-Calculates the reopened-to-closed ratio to highlight trends in resolution quality.
-Generates a pie chart showing the distribution of issue statuses.
-Gives the option to save the visualization as a PNG file.

Run Command:
python run.py --feature 2

Sample Output:

Enter start date (YYYY-MM-DD) or press Enter to skip: 2024-01-01
Enter end date (YYYY-MM-DD) or press Enter to skip: 2025-01-01

Issue Status Summary
----------------------------------------
Closed: 296 issues (74.56%)
Open: 95 issues (23.93%)
Reopened: 6 issues (1.51%)

Issue data range: 2024-01-01 → 2024-10-20
----------------------------------------

Do you want to save this chart as a PNG file? (y/n): y
Chart saved as 'issue_status_chart.png'.


---
###Feature 3: Issue Creation Trend Analysis
File: issue_creation_trend_analysis.py
This feature analyzes how issue creation volume changes over time.

Outputs:
-Displays monthly trends for a given year or yearly trends overall.
-Calculates total and average number of issues.
-Shows the most active month/year.
-Generates and displays a line or bar chart of issue creation activity.

Run Command:
python run.py --feature 3

Sample Output:

---
##VSCode Configuration
To simplify development and debugging:
.vscode/launch.json – Provides preconfigured run/debug options for each analysis.
.vscode/settings.json – Adjusts formatting and interface preferences for better navigation.

You can run and debug individual features directly from VSCode’s Run and Debug panel.