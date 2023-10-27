import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Parents New Healthy Diner")
streamlit.header('  🥗 🐔 Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.header("  🥣 🥗 🐔 🥑🍞 Make your Own Breakfast")
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits.", list(my_fruit_list.index))

fruits_selected = streamlit.multiselect("Pick some fruits.", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
fruit_choice = streamlit.text_input('What fruit would you like to add?')
streamlit.write("The user entered ", fruit_choice)

#create the repeatable block of code called function
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

#new section to display fuityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit or get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()
   
streamlit.header("The fruit load list contains:")



#snowflake-related-functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
   
#allow a end user to add fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")
      return streamlit.text("Thanks for adding " + new_fruit)

streamlit.stop()
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a fruit to the list"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)

         
streamlit.stop()


my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
