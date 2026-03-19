# ✈️ Air Tracker: Flight Analytics Dashboard

A data analytics project that fetches real flight data from the AeroDataBox API, stores it in a MySQL database, and displays it as an interactive dashboard built with Streamlit.

---

## 📌 What This Project Does

- Fetches live flight data from the **AeroDataBox API** (airports, flights, aircraft)
- Stores the data in a structured **MySQL database**
- Displays the data in an interactive **Streamlit web dashboard**
- Lets users filter flights by date, airline, and status
- Shows charts and insights about flight delays, routes, and airlines

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Main programming language |
| MySQL | Database to store flight data |
| Streamlit | Web dashboard |
| AeroDataBox API | Source of flight data |

---

## 📁 Project Structure

```
air-tracker/
│
├── api/
│   └── fetch_data.py        # Fetches data from AeroDataBox API
│
├── database/
│   └── schema.sql           # SQL table definitions
│   └── queries.sql          # All SQL analysis queries
│
├── app/
│   └── flight_dashboard.py  # Streamlit dashboard
│
└── README.md
```

---

## 🗄️ Database Tables

- **flights** — flight number, origin, destination, departure time, delay, status, airline
- **airport** — IATA code, name, city, country, timezone
- **aircraft** — registration, model, manufacturer

---

## 🚀 How to Run This Project

**Step 1 — Clone the repo**
```bash
git clone https://github.com/your-username/air-tracker.git
cd air-tracker
```

**Step 2 — Install required libraries**
```bash
pip install streamlit pandas mysql-connector-python requests
```

**Step 3 — Set up the database**
```bash
mysql -u root -p < database/schema.sql
```

**Step 4 — Fetch data from API**
```bash
python api/fetch_data.py
```

**Step 5 — Run the dashboard**
```bash
streamlit run app/flight_dashboard.py
```

---

## 📊 Dashboard Features

- **Total flights, average delay, delayed flight count** shown as metric cards
- **Flights by Status** — bar chart showing on-time vs delayed vs cancelled
- **Flights by Airline** — which airlines operate the most flights
- **Flights Per Day** — trend line over time
- **Search & Filter** — filter by date, airline, status, or search any keyword

---

## 💡 Key Insights from the Data

- Most flights in the dataset are in **"Expected"** status — meaning scheduled future flights
- Flight volume is spread across **many international airlines** with no single dominant carrier
- Very few **cancellations** observed — suggesting a reliable dataset

---

## 📝 Skills Learned

- Calling REST APIs and parsing JSON data in Python
- Designing and querying a relational SQL database
- Building an interactive web app with Streamlit
- Data filtering and visualization using pandas and charts

---

## 👤 Author

**Deepanshu**  
Built as part of the GUVI Data Analytics capstone project.
