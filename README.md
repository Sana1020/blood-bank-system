🩸 Smart Blood Bank

An intelligent blood donation and management platform that connects patients with suitable donors through compatibility, eligibility, distance, and ranking-based matching.

Smart Blood Bank is a Streamlit-based blood bank management system designed to make the process of managing blood donors, patients, blood requests, inventory, and donor–patient matching more organized and efficient.

The system combines a structured database with a multi-factor matching algorithm to help identify and rank suitable donors for a patient's blood request.

✨ Key Features

 Smart Donor–Patient Matching

Determines donor compatibility with the patient's blood requirements.

Checks donor eligibility before considering a match.

Calculates the geographical distance between donor and patient.

Generates a ranking score to prioritize the most suitable donors.

Displays the best matches in an easy-to-understand interface.

 Patient Management

Add and manage patient records.

Track blood type and patient information.

Create and manage blood requests.

 Donor Management

Register and manage blood donors.

Store donor blood type and relevant information.

Evaluate donor eligibility during the matching process.

 Blood Inventory

Track available blood units.

Organize inventory by blood type.

Support better visibility of available blood resources.

 Dashboard & Statistics

View important blood bank information from a central dashboard.

Monitor donors, patients, requests, and inventory.

Present statistics to support better decision-making.

 Database Management

Uses SQLite for lightweight and reliable local data storage.

Centralized database access through the src/database layer.

CRUD operations are separated from the UI logic.

 Matching Engine

The core of Smart Blood Bank is its donor–patient matching pipeline.

A potential donor is evaluated through several stages:

Patient Blood Request
        │
        ▼
┌───────────────────┐
│ Compatibility     │
│ Check             │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Eligibility       │
│ Check             │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Distance          │
│ Calculation       │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Ranking           │
│ Score             │
└─────────┬─────────┘
          ▼
   Ranked Donors

Matching Factors

Factor

Purpose

Compatibility

Determines whether the donor's blood type can satisfy the request

Eligibility

Filters donors who should not currently be considered

Distance

Estimates how close the donor is to the patient/location

Ranking Score

Combines matching factors to prioritize candidates

The goal is not simply to find a donor, but to identify and rank the most suitable available donors.

 Project Architecture

Smart-Blood-Bank/
│
├── Home.py
│
├── pages/
│   ├── dashboard.py
│   ├── donors.py
│   ├── patients.py
│   ├── blood_requests.py
│   ├── inventory.py
│   ├── matching.py
│   └── statistics.py
│
├── src/
│   ├── algorithms/
│   │   ├── compatibility.py
│   │   ├── distance.py
│   │   ├── eligibility.py
│   │   └── ranking.py
│   │
│   └── database/
│       ├── connection.py
│       ├── crud.py
│       ├── models.py
│       └── init_db.py
│
├── scripts/
│   ├── generate_data.py
│   └── seed_data.py
│
├── data/
│   └── blood_bank.db
│
├── tests/
│
├── .env.example
├── .gitignore
└── docker-compose.yml

Separation of Responsibilities

pages/ → Streamlit user interface and application pages.

src/algorithms/ → Matching and decision logic.

src/database/ → Database connection, models, and CRUD operations.

scripts/ → Data generation and database seeding.

tests/ → Automated testing.

data/ → Local SQLite database.

This structure keeps the application logic separated from the interface and database layer, making the project easier to maintain and extend.

 Tech Stack

Technology

Purpose

Python

Core application logic

Streamlit

Interactive web interface

SQLite

Database

Pandas

Data handling and analysis

Git & GitHub

Version control and collaboration

 Getting Started

1. Clone the repository

git clone https://github.com/Sana1020/Smart-Blood-Bank.git
cd Smart-Blood-Bank

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

3. Install dependencies

If the project contains a requirements.txt file:

pip install -r requirements.txt

4. Initialize / seed the database

Run the project's database initialization or seed script as required:

python scripts/seed_data.py

5. Run the application

streamlit run Home.py

The application will then be available through the local Streamlit server.

 Application Pages

 Home

Provides the main entry point to the Smart Blood Bank application.

📊 Dashboard

Provides an overview of the current blood bank state, including key operational information.

 Donors

Used to manage donor records and donor information.

 Patients

Used to manage patient records.

 Blood Requests

Handles blood requests submitted for patients.

 Inventory

Provides visibility into available blood units and inventory information.

 Matching

The core intelligent feature of the application. It evaluates and ranks donors based on compatibility, eligibility, distance, and ranking score.

 Statistics

Provides analytical insights into the blood bank data.

 Data & Safety Considerations

Smart Blood Bank is an academic/software engineering project intended to demonstrate intelligent matching and blood bank management workflows.

The matching results should be treated as decision-support output, not as a replacement for professional medical judgment, laboratory compatibility testing, blood bank policies, or clinical protocols.

For a production deployment, the system should additionally implement:

Authentication and role-based access control

Encryption of sensitive data

Audit logging

Secure deployment and secrets management

Strong input validation

Production-grade database infrastructure

Clinical validation and regulatory review

 Testing

The project includes a dedicated tests/ directory for testing the application's core functionality.

Recommended areas for testing include:

Blood compatibility rules

Donor eligibility

Distance calculations

Ranking logic

Database CRUD operations

Blood request workflows

Run the test suite with:

pytest

 Future Improvements

Possible future extensions include:

 AI-assisted donor recommendations

 Real-time map and route integration

 Automated donor notifications

 Mobile-friendly interface

 Authentication and role-based permissions

 Cloud database deployment

📊 Advanced analytics and reporting

 Expanded automated test coverage

 Integration with hospital/blood-bank systems

🤝 Team Collaboration

The project is designed with a modular architecture so different team members can work independently on:

Frontend / Streamlit pages

Database layer

Matching algorithms

Data analysis

Testing and quality assurance

Git and GitHub are used for version control and collaborative development.

 Project Status

Status:  Active Development

Smart Blood Bank is being developed as an academic project with a focus on applying software engineering, data management, and intelligent matching techniques to blood donation workflows.


