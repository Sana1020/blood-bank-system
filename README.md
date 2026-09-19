# Smart Blood Bank

### Intelligent Blood Donor Matching System

Smart Blood Bank is a web-based blood bank management system designed to help healthcare organizations manage donors, patients, blood requests, blood inventory, and donor matching in an efficient and intelligent way.

The system goes beyond traditional CRUD operations by using **blood compatibility, donor eligibility, geographic distance, request urgency, and ranking algorithms** to identify and recommend the most suitable donors for each blood request.

---

## Project Overview

Finding the right blood donor quickly can be challenging, especially during urgent medical situations.

Smart Blood Bank provides an integrated platform that manages the complete donor-matching process:

```text
Donor Registration
        |
        v
Donor Eligibility
        |
        v
Blood Compatibility
        |
        v
Geographic Distance
        |
        v
Ranking & Scoring
        |
        v
Best Donor Recommendations
```

The system also provides blood inventory management, patient management, blood request tracking, statistics, and a dashboard for monitoring the overall system.

---

## Key Features

### Donor Management

* Register new blood donors.
* Store donor personal and contact information.
* Manage blood type and location.
* Track donor availability.
* Store the donor's last donation date.
* Apply donor eligibility rules.

### Patient Management

* Register patients.
* Store patient blood type and hospital information.
* Manage patient location.
* Connect patients with their blood requests.

### Blood Request Management

* Create blood requests for patients.
* Specify required blood type.
* Define the number of required units.
* Set request urgency.
* Track request status.
* Connect requests with recommended donors.

### Intelligent Donor Matching

The core feature of the system is the donor matching engine.

For every blood request, the system:

1. Checks donor eligibility.
2. Checks blood type compatibility.
3. Calculates geographic distance.
4. Calculates a ranking score.
5. Sorts donors from best to worst.
6. Recommends the most suitable donors.
7. Stores generated matches in the database.

### Geographic Matching

The system calculates the distance between the donor and the blood request location using geographic coordinates.

This helps prioritize donors who are geographically closer to the patient.

### Ranking System

Donors are ranked using multiple factors:

| Factor              | Weight |
| ------------------- | -----: |
| Blood Compatibility |    50% |
| Geographic Distance |    30% |
| Request Urgency     |    20% |

The ranking system allows the application to prioritize donors based on more than blood type alone.

### Blood Inventory Management

* Track available blood units.
* Monitor inventory by blood type.
* Define low-stock thresholds.
* Update blood inventory.
* Support inventory monitoring through the dashboard.

### Dashboard and Statistics

The system provides visual insights into the blood bank, including:

* Total donors
* Patient statistics
* Blood inventory
* Blood requests
* Request urgency
* Blood type distribution
* Matching statistics

### Testing

The project includes automated tests for important parts of the system, including donor matching and algorithmic functionality.

---

## System Architecture

The project follows a modular architecture separating the user interface, business logic, algorithms, and database layer.

```text
Smart-Blood-Bank/
|
|-- app.py
|
|-- pages/
|   |-- dashboard.py
|   |-- donors.py
|   |-- patients.py
|   |-- inventory.py
|   |-- blood_requests.py
|   |-- matching.py
|   `-- statistics.py
|
|-- src/
|   |
|   |-- algorithms/
|   |   |-- compatibility.py
|   |   |-- distance.py
|   |   |-- eligibility.py
|   |   `-- ranking.py
|   |
|   |-- database/
|   |   |-- connection.py
|   |   |-- crud.py
|   |   |-- models.py
|   |   `-- init_db.py
|   |
|   `-- services/
|       |-- donor_service.py
|       |-- patient_service.py
|       |-- inventory_service.py
|       |-- request_service.py
|       `-- matching_service.py
|
|-- scripts/
|   |-- generate_data.py
|   `-- seed_data.py
|
|-- tests/
|   |-- test_algorithms.py
|   `-- test_matching.py
|
|-- data/
|   `-- blood_bank.db
|
|-- requirements.txt
`-- README.md
```

---

## Matching Algorithm

The donor matching process combines several algorithms.

### 1. Donor Eligibility

A donor must satisfy the required eligibility conditions before being considered.

The system checks factors such as:

* Donor availability
* Donor age
* Time since the last donation

Ineligible donors are removed before the matching process continues.

### 2. Blood Compatibility

The system checks whether the donor's blood type is compatible with the patient's requested blood type.

Only compatible donors continue to the next stage.

### 3. Distance Calculation

The system calculates the distance between donor and patient/request locations using latitude and longitude coordinates.

The calculation is based on the Haversine formula.

### 4. Ranking

Each eligible and compatible donor receives a ranking score based on:

```text
Compatibility Score
        +
Distance Score
        +
Urgency Score
        |
        v
Final Ranking Score
```

Donors are then sorted in descending order of their ranking score.

---

## Database Design

The system uses a relational database managed through SQLAlchemy ORM.

Main entities include:

* `Donor`
* `Patient`
* `BloodRequest`
* `Donation`
* `BloodInventory`
* `Match`

### Main Relationships

```text
Patient
   |
   `-- Blood Requests
           |
           `-- Matches -------- Donor
                                  |
                                  `-- Donations

BloodInventory
   |
   `-- Blood Type / Available Units
```

The `Match` entity stores important matching information such as:

* Request ID
* Donor ID
* Compatibility score
* Distance
* Ranking score
* Match status
* Creation timestamp

---

## Technologies Used

### Programming Language

* Python

### Frontend and UI

* Streamlit

### Database

* SQLite
* SQLAlchemy ORM

### Data and Algorithms

* Python
* SQLAlchemy
* Geographic distance calculation
* Blood compatibility logic
* Donor eligibility logic
* Ranking algorithm

### Testing

* Pytest

### Development Tools

* Git
* GitHub
* VS Code
* Jupyter / Python environment

---

## Getting Started

### Prerequisites

Make sure you have Python installed.

Clone the repository:

```bash
git clone https://github.com/Sana1020/blood-bank-system.git
```

Navigate to the project directory:

```bash
cd blood-bank-system
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Run Tests

To run the automated tests:

```bash
pytest
```

---

## Application Screenshots

Add screenshots of the main application pages here.

Recommended screenshots:

* Dashboard
* Donor Management
* Patient Management
* Blood Requests
* Blood Inventory
* Donor Matching
* Statistics

Example:

```markdown
![Dashboard](screenshots/dashboard.png)
![Donor Matching](screenshots/matching.png)
![Blood Inventory](screenshots/inventory.png)
```

---

## Project Goals

The main goals of Smart Blood Bank are to:

* Improve donor search efficiency.
* Reduce the time required to identify suitable donors.
* Prioritize compatible and eligible donors.
* Consider geographic proximity.
* Support urgent blood requests.
* Provide centralized blood bank management.
* Offer useful statistics for decision-making.

---

## Future Improvements

Possible future enhancements include:

* Real-time notifications for donors.
* SMS/email notifications.
* Advanced donor availability prediction.
* Machine Learning-based donor recommendation.
* Hospital-to-blood-bank integration.
* Real-time inventory synchronization.
* Authentication and role-based access control.
* Cloud database deployment.
* Interactive geographic maps for donor locations.
* Deployment as a production web application.

---

## Project

**Smart Blood Bank — Intelligent Blood Donor Matching System**

Developed as an academic software project combining:

**Database Management + Algorithms + Software Architecture + Data Processing + Intelligent Donor Matching**

---

## License

This project is developed for educational and academic purposes.

