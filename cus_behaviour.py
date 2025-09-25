import streamlit as st
import pandas as pd

file_uploaded = st.file_uploader("C:\\Users\\DELL\\Downloads\\Desktop\\Kaggle\\Customer Purchasing Behaviours.xlsx", type=["xlsx"])

if file_uploaded is not None:
    df = pd.read_excel(file_uploaded)

    st.subheader("Preview of Data")
    st.write(df.head())

    st.subheader("Quick Stats")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
st.subheader("KPI")

Total_Revenue = (df["purchase_amount"] * df["purchase_frequency"]).sum()
Total_Number_Sales = df["purchase_frequency"].sum()
Total_Sales = df["purchase_amount"].sum()

st.metric("Total Revenue:",f"${Total_Revenue:.2f}")
st.metric("Quantity Sold:", Total_Number_Sales)
st.metric("Selling Price:", Total_Sales)

st.markdown("Top 10 Customers By Total_Revenue")
df["tot_revenue"] = df["purchase_amount"] * df["purchase_frequency"]
highest_customers = (
    df.groupby("user_id")["tot_revenue"]
    .sum()
    .sort_values(ascending = False)
    .head(10)
)

st.subheader("Top 10 Customers By Total Revenue")
st.line_chart(highest_customers)

st.markdown("Top 10 Loyal Customer By Total Sales")
loyal_customers = (
    df.groupby("loyalty_score")["purchase_amount"]
    .sum()
    .sort_values(ascending = False)
    .head(10)
)
st.subheader("Top 10 Customers By Total Sales")
st.line_chart(loyal_customers)

MAX_Income = df["annual_income"].max()
bins = [0, 20000, 40000, 60000, MAX_Income]
labels = ["Low (<20k)", "Medium (20k-40k)", "High (40k-60k)", "VIP (>60k)"]

df["Income_Band"] = pd.cut(
    df["annual_income"],
    bins=bins,
    labels=labels,
    include_lowest=True
)
band_summary = (
    df.groupby("Income_Band")["purchase_amount"]
    .mean()
    .reset_index()
)

st.subheader("Purchase Behaviour By Annual Income")
st.bar_chart(band_summary.set_index("Income_Band"))

Min_Age = df["age"].min()
Max_Age = df["age"].max()
age_bins = [Min_Age, 30, 40, 50, Max_Age]
age_labels = ["20-30", "30-40", "40-50", "50-60"]

df["Highest_spend"] = pd.cut(
    df["age"],
    bins = age_bins,
    labels = age_labels,
    include_lowest = True
)

Age_Spend = (
    df.groupby("Highest_spend")["purchase_amount"]
    .mean()
    .reset_index()
)

st.subheader("Purchase Behaviour By Age")
st.bar_chart(Age_Spend.set_index("Highest_spend"))

df["Age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, include_lowest=True)
summary = df.groupby(["Age_group", "Income_Band"])["purchase_amount"].mean().reset_index()
pivot_summary = summary.pivot(index="Age_group", columns="Income_Band", values="purchase_amount")

st.subheader("Purchase Behaviour By Income Band & Age Group")
st.bar_chart(pivot_summary)


