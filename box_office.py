# packages
import streamlit as st
import pandas as pd
import plotly.express as px


def load_data():
    df = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\money_2024\mls_finances.csv")
    return df

# page function: revenue generated? player salaries?
def app():
    st.title("Welcome to the Box Office!")

    # Function to load data

    # Load data
    df = load_data()

    color_map = df.set_index('club')['color'].to_dict()

    # Display raw data
    st.write("### Raw Data")
    st.dataframe(df)

    # Value Plot - Treemap (good for proportions)
    fig_value = px.treemap(df, path=["club"], values="value", title="Club Values", color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_value)

    # Revenue Plot - Scatter Plot (to see trends)
    fig_revenue = px.bar(df.sort_values("revenue", ascending=True),
                         x="revenue", y="club", title="Revenue by Club",
                         orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_revenue)

    # Attendance - Bubble Chart
    fig_attendance = px.scatter(df.sort_values("attendance", ascending=True),
                                x="attendance", y="club", title="Attendance by Club",
                                color="club", size="attendance", color_discrete_map=color_map,
                                size_max=10)
    st.plotly_chart(fig_attendance)

    # Payroll - Colored Bar Chart
    fig_payroll = px.bar(df.sort_values("payroll", ascending=True),
                         x="payroll", y="club", title="Payroll by Club",
                         orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_payroll)