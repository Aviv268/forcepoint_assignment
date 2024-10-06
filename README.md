# Forcepoint Assignment
This project contains both backend and frontend components.

## Backend: Ride Allocation

The backend simulates processes ride requests from companies(hard coded from the ride_requests.csv), 
aggregates them by destination, simulates approval rides from a transit agency, and distributes the approved rides back to the companies proportionally.

### Features

- Reads the ride requests from a CSV file (`data/ride_requests.csv`)
- Aggregates the ride requests per destination
- Simulates ride approvals from the transit agency
- Distributes approved rides to companies based on their requests
- Writes ride allocations to a CSV file (`data/ride_allocations.csv`).
- Logs activities to `logs/ride_allocation.log`.

### How to Run

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   
2. **Run the Script**
   ```bash
   python -m src.ride_allocation
Or run from the pycharm GUI by right-clicking the ride_allocation.py 

3. **Check the Output**

   The ride allocations will be saved in data/ride_allocations.csv


## Frontend Automation

The frontend automates testing of a web page called "Complicated Page" using Playwright and PyTest.
### Features

- Navigates to the Complicated Page.
- Counts the number of buttons in a specific section.
- Verifies Facebook links in the social media section.
- Fills out and submits a contact form with a math captcha.
- Captures screenshots on test failures.
- Generates test reports using Allure.

### How to Run Tests

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

2. **Install Playwright Browsers**
    
   ```bash
   playwright install
   
3. **Run the Tests**
    
   ```bash
   pytest fe_automation/tests/
Or from the pycharm GUI

4. **Generate Allure Report**
    
   ```bash
   pytest fe_automation/tests/ --alluredir=allure-results
   allure serve reports/allure-results

or by adding --alluredir=allure-results to the "Additional Arguments" in the pytest configuration from the pycharm GUI
## Logs and Reports

- **Logs**: Saved in the `logs/` directory.
- **Screenshots**: Saved in `reports/screenshots/` when tests fail.
