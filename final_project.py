import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px

# Reading my ecommerce dataset.
filepath = "ecommerce.csv"
df = pd.read_csv(filepath)
# Droping some columns.
col_drop = ["Unnamed: 0", "c_id"]
df = df.drop(columns = col_drop)

st.title("E-Commerce Dashboard")
# Bringing in the dataframe to the app.
st.dataframe(df.head())
# Creating a new column
df["year"] = pd.to_datetime(df["order_approved_at"]).dt.year
# Displaying the metrics function.
def yearly_record(year, df):
    # get records for delivered goods
    df = df[df["order_status"] =="delivered"]
    yearly_sales = df.groupby("year")["payment_value"].mean()
    yearly_purchase = df.groupby("year")["payment_value"].count()
    sum_yearly_sales = round(yearly_sales.loc[year].sum(), 2)
    sum_yearly_purchase = yearly_purchase.loc[year].sum()
    col1, col2= st.columns(2)
    col1.metric("Total Revenue", value=sum_yearly_sales)
    col2.metric("Total Purchase", value= sum_yearly_purchase)

# Building a Univariant analysis function.
def univariant_analysis(column, year, top_n=8, dataframe= df):
    """
    This function will plot the distribution of the object column datatype in sorted order.

    -------------
    Parameters:
        column: The column of interest
        top_n: How many bar is displayed.

    ------------
    Return:
        figure
    """
    if len(year) != 0:
        # filter the dataset by year.
        dataframe = dataframe[dataframe["year"].isin(year)]
        dataframe = dataframe[dataframe["order_status"] == "delivered"]
        # Get the total unique count of all the entry in the column
        column_count = dataframe[column].value_counts(normalize=True)
        # Get the top_n values
        column_top_n = column_count.head(top_n)
        # Condition for the horizontal bar.
        xlabel_name = column.upper().replace("_", " ")
        fig = px.bar(data_frame= column_top_n, 
                     x=column_top_n.index, 
                     y= column_top_n.values, 
                     color=column_top_n, 
                    title=f"{xlabel_name} DISTRIBUTION").update_layout(xaxis_title=xlabel_name.lower(), yaxis_title="Frequency")
        st.write(fig)
    else:
        pass

def column_payment(column, top_n, year, dataframe=df):
    # filter by year.
    if len(year) != 0:
        dataframe = dataframe[dataframe["year"].isin(year)]
        dataframe = dataframe[dataframe["order_status"] == "delivered"]
        # Get the total unique count of all the entry in the column
        column_count = dataframe.groupby([column])["payment_value"].mean().sort_values(ascending=False)
        # Get the top_n values
        column_top_n = column_count.head(top_n)
        # Condition for the horizontal bar.
        xlabel_name = column.upper().replace("_", " ")
        fig = px.bar(data_frame= column_top_n, 
                     x=column_top_n.index, 
                     y= column_top_n.values, 
                     color=column_top_n, 
                    title=f"MEAN PAYMENT VALUE BY {xlabel_name}").update_layout(xaxis_title=xlabel_name.lower(), yaxis_title="Mean Payment")
        st.write(fig)
    else:
        pass

with st.sidebar:
    year = st.multiselect("Year", [2016, 2017, 2018], default=[2016, 2017, 2018])
    column = st.selectbox("Column", ['customer_state', "seller_state", 'product_category_name_english', 'customer_city', 'seller_city', 'payment_type'])
    top_n = st.number_input("Top N:", 4, len(df[column].unique()))
yearly_record(year, df)
univariant_analysis(column, year, top_n= top_n, dataframe= df)
column_payment(column, top_n, year, dataframe=df)