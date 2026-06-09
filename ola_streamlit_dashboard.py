import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="OLA Ride Analytics",
    page_icon="🚖",
    layout="wide"
)

st.title("🚖 OLA Ride Analytics")


connection_string = "mysql+mysqlconnector://root:Sakthi%40123@localhost/project2_db"
engine = create_engine(connection_string)

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard Overview",
        "Successful Bookings",
        "Average Ride Distance",
        "Customer Cancellations",
        "Top Customers",
        "Driver Cancellations",
        "Prime Sedan Ratings",
        "UPI Payments",
        "Customer Ratings",
        "Ride Details"
    ]
)

if menu == "Dashboard Overview":

    total_rides = pd.read_sql(
        "SELECT COUNT(*) AS total FROM ola_data",
        engine
    )

    revenue = pd.read_sql(
        "SELECT SUM(Booking_Value) AS revenue FROM ola_data WHERE Incomplete_Rides='No'",
        engine
    )

    customers = pd.read_sql(
        "SELECT COUNT(DISTINCT Customer_ID) AS customers FROM ola_data",
        engine
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rides", int(total_rides.iloc[0, 0]))
    col2.metric("Revenue", f"₹{revenue.iloc[0,0]:,.0f}")
    col3.metric("Customers", int(customers.iloc[0, 0]))

elif menu == "Successful Bookings":

    query = """
    SELECT *
    FROM ola_data
    WHERE Booking_Status='Success'
    """

    df = pd.read_sql(query, engine)

    st.subheader("Successful Bookings")
    st.dataframe(df)

elif menu == "Average Ride Distance":

    query = """
    SELECT Vehicle_Type,
           AVG(Ride_Distance) AS Average_Ride_Distance
    FROM ola_data
    GROUP BY Vehicle_Type
    ORDER BY Average_Ride_Distance DESC
    """

    df = pd.read_sql(query, engine)

    fig, ax = plt.subplots()
    ax.bar(df["Vehicle_Type"], df["Average_Ride_Distance"])
    plt.xticks(rotation=45)
    plt.title("Average Ride Distance by Vehicle Type")

    st.pyplot(fig)
    st.dataframe(df)

elif menu == "Customer Cancellations":

    query = """
    SELECT Canceled_Rides_by_Customer,
           COUNT(*) AS Cancelled_by_Customers
    FROM ola_data
    GROUP BY Canceled_Rides_by_Customer
    """

    df = pd.read_sql(query, engine)

    if len(df) > 1:
        df = df.iloc[1:]

    fig, ax = plt.subplots()

    ax.pie(
        df["Cancelled_by_Customers"],
        labels=df["Canceled_Rides_by_Customer"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)
    st.dataframe(df)

elif menu == "Top Customers":

    query = """
    SELECT Customer_ID,
           COUNT(*) AS Total_Rides
    FROM ola_data
    GROUP BY Customer_ID
    ORDER BY Total_Rides DESC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    st.dataframe(df)

elif menu == "Driver Cancellations":

    query = """
    SELECT Canceled_Rides_by_Driver,
           COUNT(*) AS Cancelled_by_Driver
    FROM ola_data
    GROUP BY Canceled_Rides_by_Driver
    ORDER BY Cancelled_by_Driver DESC
    """

    df = pd.read_sql(query, engine)
    df = df.iloc[1:]

    st.bar_chart(df.set_index("Canceled_Rides_by_Driver"))
    st.dataframe(df)

elif menu == "Prime Sedan Ratings":

    query = """
    SELECT Driver_Ratings,
           COUNT(*) AS Rating_Count
    FROM ola_data
    WHERE Vehicle_Type='Prime Sedan'
    GROUP BY Driver_Ratings
    """

    df = pd.read_sql(query, engine)
    df = df.iloc[1:]

    st.bar_chart(df.set_index("Driver_Ratings"))
    st.dataframe(df)

elif menu == "UPI Payments":

    query = """
    SELECT *
    FROM ola_data
    WHERE Payment_Method='UPI'
    """

    df = pd.read_sql(query, engine)

    st.metric("Total UPI Transactions", len(df))
    st.dataframe(df)

elif menu == "Customer Ratings":

    query = """
    SELECT Vehicle_Type,
           AVG(Customer_Rating) AS Average_Customer_Rating
    FROM ola_data
    GROUP BY Vehicle_Type
    ORDER BY Average_Customer_Rating DESC
    """

    df = pd.read_sql(query, engine)

    st.bar_chart(df.set_index("Vehicle_Type"))
    st.dataframe(df)

elif menu == "Ride Details":

    query1 = """
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM ola_data
    WHERE Incomplete_Rides='No'
    """

    query2 = """
    SELECT *
    FROM ola_data
    WHERE Incomplete_Rides!='No'
    """

    df1 = pd.read_sql(query1, engine)
    df2 = pd.read_sql(query2, engine)
    st.subheader("Booking value of Completed Rides")
    st.metric(
        "Revenue from Completed Rides",
        f"₹{df1.iloc[0,0]:,.0f}"
    )
    st.subheader("Incomplete Rides Details") 
    st.dataframe(df2)
