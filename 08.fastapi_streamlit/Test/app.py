import streamlit as st
import requests


st.write("Hello World")
st.write("This is my first Streamlit app!")

st.markdown("## This is a markdown header")
st.markdown("You can use **markdown** to format your text.")    

st.write("You can also use Streamlit's built-in functions to create interactive elements.")
st.markdown("<h1>This is a header</h1>", unsafe_allow_html=True) # Use unsafe_allow_html to render HTML tags

#page configuration
st.set_page_config(
    page_title="Our streamlit app",
    page_icon=":heart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

#style
st.markdown("""
            <style>
            button {
                color:green;
                background:red;
                border: 1px solid black;
                border-radius: 5px;
                padding: 10px;
                width: 100px;
            }
            </style>
            <button id> click</button>
            
            """, unsafe_allow_html=True
            )


#name input
name = st.text_input("Enter your name")
#number input with min, max, default value and step
st.number_input("Enter your age", min_value=0, max_value=100, value=25, step=1) 


#horizontal line
st.markdown("---")

#submit button
if st.button("Submit"):
    st.write('sucessfully submitted')
    
if st.button("Click me"):
    st.success("Button clicked!")
    
#fetch items from api 
r = requests.get("http://localhost:8000/items")

r.status_code
#horizontal line
st.markdown("---")
st.write(r.json())
#horizontal line
st.markdown("---")
#display items in a list
for item in r.json():
    st.write(item['name'])