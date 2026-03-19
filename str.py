import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(page_title="Flight Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Deepanshu@1",
        database="flight_db"
    )
    flights  = pd.read_sql("SELECT * FROM flights", conn)
    airports = pd.read_sql("SELECT * FROM airport", conn)
    conn.close()

    flights["departure_time_utc"] = pd.to_datetime(flights["departure_time_utc"])
    flights["date"]          = flights["departure_time_utc"].dt.date
    flights["delay_minutes"] = pd.to_numeric(flights["delay_minutes"], errors="coerce").fillna(0)
    flights["is_delayed"]    = flights["delay_minutes"] > 15

    return flights, airports

flights, airports = load_data()

st.sidebar.title(" Navigation")
page = st.sidebar.radio("Choose a page", [
    " Home",
    " Search Flights",
    " Airport Details",
    " Delay Analysis",
    " Leaderboards"
])

# ── PAGE 1 — HOME ─────────────────────────────────────────────
if page == " Home":
    st.title(" Home")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Airports", len(airports))
    c2.metric("Total Flights",  len(flights))
    c3.metric("Avg Delay",      f"{flights['delay_minutes'].mean():.1f} min")

    st.divider()

    st.subheader("Flights by Status")
    st.bar_chart(flights["status"].value_counts())

# ── PAGE 2 — SEARCH FLIGHTS ───────────────────────────────────
elif page == "🔍 Search Flights":
    st.title("🔍 Search Flights")

    search = st.text_input("Search by flight number or airline name")

    c1, c2, c3 = st.columns(3)

    # NO default selected — user picks what they want
    status_filter = c1.multiselect("Filter by Status", flights["status"].unique())
    origin_filter = c2.multiselect("Filter by Origin", flights["origin"].unique())
    date_from     = c3.date_input("From date", value=flights["date"].min())
    date_to       = c3.date_input("To date",   value=flights["date"].max())

    # Start with all flights
    result = flights.copy()

    # Only filter if user actually selected something
    if status_filter:
        result = result[result["status"].isin(status_filter)]
    if origin_filter:
        result = result[result["origin"].isin(origin_filter)]

    # Always apply date filter
    result = result[(result["date"] >= date_from) & (result["date"] <= date_to)]

    # Apply search if user typed something
    if search:
        result = result[
            result["flight_number"].str.contains(search, case=False, na=False) |
            result["airline_name"].str.contains(search, case=False, na=False)
        ]

    st.write("Showing", len(result), "flights")
    st.dataframe(result[["flight_number", "airline_name", "origin", "destination", "delay_minutes", "status"]])

# ── PAGE 3 — AIRPORT DETAILS ──────────────────────────────────
elif page == " Airport Details":
    st.title(" Airport Details")

    selected = st.selectbox("Select an airport", airports["name"].sort_values())
    row = airports[airports["name"] == selected].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("City",     row["city"])
    c2.metric("Country",  row["country"])
    c3.metric("Timezone", row["timezone"])

    st.divider()

    st.subheader("Flights from this airport")
    linked_flights = flights[flights["origin"] == row["iata_code"]]
    st.write("Total flights:", len(linked_flights))
    st.dataframe(linked_flights[["flight_number", "airline_name", "destination", "delay_minutes", "status"]])

# ── PAGE 4 — DELAY ANALYSIS ───────────────────────────────────
elif page == " Delay Analysis":
    st.title(" Delay Analysis")

    st.subheader("Avg Delay by Airport (Top 15 worst)")
    avg_by_airport = flights.groupby("origin")["delay_minutes"].mean().sort_values(ascending=False).head(15).round(1)
    st.bar_chart(avg_by_airport)

    st.divider()

    st.subheader("Avg Delay by Airline (Top 15 worst)")
    avg_by_airline = flights.groupby("airline_name")["delay_minutes"].mean().sort_values(ascending=False).head(15).round(1)
    st.bar_chart(avg_by_airline)

# ── PAGE 5 — LEADERBOARDS ─────────────────────────────────────
elif page == " Leaderboards":
    st.title(" Leaderboards")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader(" Busiest Routes")
        busiest = flights.groupby(["origin", "destination"]).size().reset_index(name="Total Flights")
        busiest["Route"] = busiest["origin"] + " → " + busiest["destination"]
        busiest = busiest.sort_values("Total Flights", ascending=False).head(15)
        st.dataframe(busiest[["Route", "Total Flights"]].reset_index(drop=True))

    with c2:
        st.subheader(" Most Delayed Airports")
        delayed = flights.groupby("origin")["delay_minutes"].mean().reset_index()
        delayed.columns = ["Airport", "Avg Delay (min)"]
        delayed["Avg Delay (min)"] = delayed["Avg Delay (min)"].round(1)
        delayed = delayed.sort_values("Avg Delay (min)", ascending=False).head(15)
        st.dataframe(delayed.reset_index(drop=True))


