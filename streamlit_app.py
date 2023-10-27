import streamlit
import pandas
import requests
import snowflake.connector
import urllib.error import URLError


streamlit.title("My Parents New Healthy Diner")

streamlit.header('  🥗 🐔 Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('  🥣 Hard-Boiled Free-Range Egg')
streamlit.text("  🥑 Avacado Toast")
streamlit.header("  🥣 🥗 🐔 🥑🍞 Make your Own Breakfast")


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits.", list(my_fruit_list.index))

streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_selected = streamlit.multiselect("Pick some fruits.", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
streamlit.text(fruityvice_response)

streamlit.header("Fruityvice Fruit Advice!")

# normalizing the josn file 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# taking the output to display on streamlit
streamlit.dataframe(fruityvice_normalized)
streanlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
