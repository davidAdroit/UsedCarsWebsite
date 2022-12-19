###
'''
David Burris-Mendoza

Final CS230 Project
'''
import streamlit as st
import pandas as pd
import csv

import plotly.express as px
st.title("David's Used Cars - You buy em")
st.header("Craigslist Used Cars for Sale!")
# Create the tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Car Search", "Listings Map", "About", "Listing Data", "Car Search +"])
#these tabs are to navigate the webapp
cars_file = "used_cars_data.csv"



def car_chart(cars_file):
    df3 = pd.read_csv(cars_file)

    prices = df3['price']

    st.line_chart(prices)
    #this is a function that creates a chart that displays prices
def region_chart(cars_file):
    used_cars = pd.read_csv(cars_file)
    year_data = used_cars['year'][(used_cars['year'] >= 1940) & (used_cars['year'] <= 2022)]

    st.bar_chart(year_data)
    #this is a function that creates a chart that displays the years of the cars for sale from 1940-2022

with tab1:
    st.header("Home")
    st.text('Check out our used cars!')
    st.error("Please refer to craigslist urls for $0 prices")
    st.text("Below is a chart containing all the listings currently up")
    st.text("You can further filter them through our Car Search engine")
    #
    car_image1 = "https://carfax-img.vast.com/carfax/v2/9111543372186929145/1/344x258"
    st.image(car_image1, caption = "Used Car on the lot", use_column_width = True)
    st.subheader("Cars Currently For Sale") #image w/ a caption
    with open('used_cars_data.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        car_list = []
        for row in csv_reader:
            unnamed_id = row[1]
            url = row[2]
            region = row[3]
            region_url = row[4]
            price = row[5]
            year = row[6]
            manufacturer = row[7]
            model = row[8]
            car_data = {'price': price, 'year': year, 'manufacturer': manufacturer, 'model': model}
            car_list.append(car_data)
    df = pd.DataFrame(car_list)
    st.dataframe(df) #dataframe displaying a chart with the price, year, manufacturer, and model of the cars, just a little preview of the website
with tab2:
    st.header("Car Search")
    df = pd.read_csv('used_cars_data.csv')
    st.text("You can search for a type of car here and filter by price! \n links to listings are provided")

    query = st.text_input("Search for a manufacturer or model:") #search bar for user
    df['price'] = pd.to_numeric(df['price']) #makes sure price is a number
    min_price, max_price = st.slider('Price range:', min_value=0, max_value=150000, value=(0, 150000)) #slider range 0-150k for price
    sort_order = st.radio("Sort prices by:", ("Ascending", "Descending")) #sort by cheap to most expensive or vice versa
#i assumed that people buying used cars on craigslist would not filter for prices higher than 150k
    filtered_df = df[(df['manufacturer'].str.contains(query, case=False)) | (df['model'].str.contains(query, case=False))]
    filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]
    if sort_order == "Ascending":
        filtered_df = filtered_df.sort_values(by='price')
    else:
        filtered_df = filtered_df.sort_values(by='price', ascending=False)
    filtered_df = filtered_df[['manufacturer', 'model', 'price', 'url']] #just display these to user



    st.dataframe(filtered_df)


with tab3:
    st.header("Map of the World")
    st.text("View locations where car listings exist")

    df = pd.read_csv(cars_file)
    df["lat"] = pd.to_numeric(df["lat"]).fillna(0) #if cell is empty
    df["longitude"] = pd.to_numeric(df["longitude"]).fillna(0) #incase cell is empty
    st.map(df) #map of data


with tab4:
    st.header("About Us")
    car_image1 = "https://cdn.pixabay.com/photo/2016/04/01/12/16/car-1300629__340.png"
    st.image(car_image1, caption = "Car sold on 12/14/2022\n $75,000", use_column_width = True)

    st.text("Welcome to our website, where you'll find a wide selection \n of high-quality used cars for sale. My name is David, and \n I am the owner of this business.")
    st.text("I have always been passionate about cars and have spent \n years scouring Craigslist and other sources for the best deals \n on used vehicles. But more than just finding \n good deals, I believe in bringing home-grown values to the car-buying \n process. That means treating each and every customer with \n the respect and honesty they deserve. We hope you'll \n give us a chance to show you what sets us apart from the \n competition. Thank you for considering us for your next vehicle purchase.")
    st.success("Other inquiries or questions? Contact David at:  david.adroit@outlook.com")
with tab5:
    st.subheader("Interesting Data")
    st.text("This interactive chart displays the various prices of all our listed vehicles")
    car_chart(cars_file)#calling the function

    st.text('This is another chart that displays the years in which cars are listed')
    region_chart(cars_file)
    st.text("Below is a Plotly chart that displays the distribution of the states where \n listings are up")
    df = pd.read_csv("used_cars_data.csv")
    states = df["state"]
    state_counts = states.value_counts()
    values = state_counts.values
    labels = state_counts.index

    fig = px.pie(values=values, names=labels, title="State Distribution")

    fig.update_traces(textinfo="value+percent")
    st.plotly_chart(fig) #this is a plotly chart which shows state distribution for cars for sale
with tab6:
    st.subheader("Filter by fuel type & condition")
    st.text("Filter by condition and fuel type to see options")
    condition = st.radio("Select condition:", ("New", "Good", "Excellent", "Fair", "Like New"))
    fuel = st.selectbox("Select fuel type:", ("Gas", "Electric"))

    used_carz = pd.read_csv('used_cars_data.csv')
    st.dataframe(used_carz)

    filtered_df = used_carz[(used_carz['condition'] == condition) & (used_carz['fuel'] == fuel)]

