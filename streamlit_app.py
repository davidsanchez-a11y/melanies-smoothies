# --------------------- importar paquetes/librerías/funciones -----------------------------------
# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# --------------------- TÍTULO Y TEXTOS ESCRITOS DIRECTAMENTE EN LA APP --------------------------
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """)


# ----------------------- DECLARAR ENTRADAS DE INFORMACIÓN ---------------------------------------
# ADD A NAME BOX ON UI FOR PEOPLE TO TYPE IN THEIR NAME 
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

# option = st.selectbox(
#     'What is your favorite fruit?', ('Banana', 'Strawberries', 'Peaches')
# )
# st.write('Your favorite fruit is: ', option)
cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# Para evitar que se muestren los brackets "if ingredients_list is not null: then do everything below this line that is indented."
if ingredients_list:  
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string= ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

# ----------------------------INSERTAR LAS ENTRADAS EN LA BASE DE DATOS ------------------------
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

# New section to display smoothiefroot nutrition information
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
