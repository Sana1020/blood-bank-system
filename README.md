



# Smart Blood Bank

### Intelligent Blood Donor Matching System







Smart Blood Bank is a web-based blood bank management system designed to help healthcare organizations manage donors, patients, blood requests, blood inventory, and donor matching through an integrated platform.

The system goes beyond basic CRUD operations by using **blood compatibility, donor eligibility, geographic distance, request urgency, and a rule-based ranking algorithm** to identify and recommend suitable donors for blood requests.

---

## Project Overview

Finding a suitable blood donor quickly can be challenging, especially during urgent medical situations.

Smart Blood Bank provides an integrated workflow for managing the donor-matching process:

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
Rule-Based Ranking
        |
        v
Donor Recommendations
```

The system also provides:

* Donor management
* Patient management
* Blood request management
* Blood inventory management
* Donor matching
* Statistics and analytics
* System dashboard

---

## Key Features

### Donor Management

* Register new blood donors
* Store donor personal and contact information
* Manage blood type and location
* Track donor availability
* Store the donor's last donation date
* Apply donor eligibility rules

### Patient Management

* Register patients
* Store patient blood type and hospital information
* Manage patient location
* Connect patients with their blood requests

### Blood Request Management

* Create blood requests for patients
* Specify the required blood type
* Define the number of required units
* Set request urgency
* Track request status
* Generate donor recommendations

---

## Intelligent Donor Matching

The core feature of Smart Blood Bank is its donor matching engine.

For each blood request, the system:

1. Checks donor eligibility.
2. Checks blood type compatibility.
3. Calculates geographic distance.
4. Calculates a ranking score.
5. Sorts eligible donors by score.
6. Recommends the highest-ranked donors.
7. Stores generated matches in the database.

The current matching system is **rule-based**, combining multiple factors rather than relying only on blood type.

---

## Donor Eligibility

Before a donor can be considered for matching, the system checks eligibility conditions such as:

* Donor availability
* Donor age
* Time since the last donation

Ineligible donors are excluded before the compatibility and ranking stages.

---

## Blood Compatibility

The system checks whether a donor's blood type is compatible with the blood type required by the request.

Only compatible donors continue to the ranking stage.

---

## Geographic Matching

The system calculates the geographic distance between the donor and the blood request location using latitude and longitude coordinates.

Distance calculation is based on the **Haversine formula**.

This allows the system to consider geographic proximity when ranking potential donors.

---

## Rule-Based Ranking

Eligible and compatible donors are ranked using multiple factors:

| Factor              | Weight |
| ------------------- | -----: |
| Blood Compatibility |    50% |
| Geographic Distance |    30% |
| Request Urgency     |    20% |

The final ranking score combines these factors to prioritize suitable donors.

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

Donors are then sorted in descending order of their final ranking score.

---

## Example Matching Scenario

Example blood request:

```text
Required Blood Type: O+
Urgency: High
```

Possible matching results:

```text
Donor A
Compatible: Yes
Distance: 3.2 km
Ranking Score: 91

Donor B
Compatible: Yes
Distance: 8.7 km
Ranking Score: 76

Donor C
Eligible: No
Status: Excluded
```

The system ranks the eligible and compatible donors and recommends the highest-ranked candidates.

---

## Blood Inventory Management

The inventory module allows the system to:

* Track available blood units
* Monitor inventory by blood type
* Define low-stock thresholds
* Identify low-stock blood types
* Display inventory information through the dashboard

---

## Dashboard and Statistics

The system provides statistics and visual insights into blood bank activity, including:

* Total donors
* Available donors
* Total patients
* Blood requests
* Blood type distribution
* Request status
* Request urgency
* Blood type demand
* Blood inventory
* Matching statistics

---

## Testing

The project includes automated tests for important system components, including:

* Donor eligibility
* Blood compatibility
* Distance calculation
* Ranking logic
* Donor matching functionality

Testing is implemented using **Pytest**.

---

## System Architecture

The project follows a modular architecture separating the user interface, business logic, algorithms, services, and database layer.

```text
Smart-Blood-Bank/
│
├── app.py
│
├── pages/
│   ├── dashboard.py
│   ├── donors.py
│   ├── patients.py
│   ├── inventory.py
│   ├── blood_requests.py
│   ├── matching.py
│   └── statistics.py
│
├── src/
│   │
│   ├── algorithms/
│   │   ├── compatibility.py
│   │   ├── distance.py
│   │   ├── eligibility.py
│   │   └── ranking.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   └── init_db.py
│   │
│   └── services/
│       ├── donor_service.py
│       ├── patient_service.py
│       ├── inventory_service.py
│       ├── request_service.py
│       └── matching_service.py
│
├── scripts/
│   ├── generate_data.py
│   └── seed_data.py
│
├── tests/
│   ├── test_algorithms.py
│   └── test_matching.py
│
├── data/
│   └── blood_bank.db
│
├── requirements.txt
│
└── README.md
```

---

## Database Design

The system uses a relational database managed through **SQLAlchemy ORM**.

### Main Entities

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
   └── Blood Requests
           |
           └── Matches ─────── Donor
                                  |
                                  └── Donations

BloodInventory
   |
   └── Blood Type / Available Units
```

The `Match` entity stores information such as:

* Request ID
* Donor ID
* Compatibility score
* Geographic distance
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

### Algorithms and Data Processing

* Blood compatibility logic
* Donor eligibility logic
* Haversine distance calculation
* Rule-based ranking
* Python data processing

### Testing

* Pytest

### Development Tools

* Git
* GitHub
* VS Code
* Python Virtual Environment

---

## Getting Started

### Prerequisites

Make sure you have Python installed on your system.

### Clone the Repository

```bash
git clone https://github.com/Sana1020/blood-bank-system.git
```

### Navigate to the Project

```bash
cd blood-bank-system
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment on Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

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

Run the automated tests using:

```bash
pytest
```

---




## Project Goals

The main goals of Smart Blood Bank are to:

* Improve donor search efficiency
* Reduce the time required to identify suitable donors
* Prioritize eligible and compatible donors
* Consider geographic proximity
* Support urgent blood requests
* Centralize blood bank management
* Provide useful operational statistics
* Apply algorithmic decision support to donor matching

---

## Future Improvements

Possible future enhancements include:

* Real-time donor notifications
* SMS and email notifications
* Advanced donor availability prediction
* Machine Learning-based donor recommendation
* Hospital-to-blood-bank integration
* Real-time inventory synchronization
* Authentication and role-based access control
* Cloud database deployment
* Interactive geographic maps
* Production web deployment

---

## Project

### Smart Blood Bank — Intelligent Blood Donor Matching System

An academic software project combining:

**Database Management + Algorithms + Software Architecture + Data Processing + Rule-Based Donor Matching**

---

## License

This project was developed for educational and academic purposes.

```
