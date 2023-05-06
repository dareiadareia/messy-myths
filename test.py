__author__ = 'dareia'
#import string
#import datetime as datetime
#import json
#import os
import pandas as pd
import streamlit as st

st.title('Enter hylemes below')

num_rows = st.slider('Number of Rows', min_value=1,max_value=10,value=1)

if 'data' not in st.session_state:
    data = pd.DataFrame({'subject':[],'predicate':[],'object':[]})
    st.session_state.data = data

#source: https://discuss.streamlit.io/t/button-to-add-new-row-of-inputs/33245/2
def save_data(num_rows):
    for i in range(1, num_rows+1):
        row = pd.DataFrame({'subject':[st.session_state['subject'+str(i)]],
                'predicate':[st.session_state['predicate'+str(i)]],
                'object':[st.session_state['object'+str(i)]]
                })
        st.write(row)
        st.session_state.data = pd.concat([st.session_state.data, row])
        print(st.session_state.data)
    st.dataframe(st.session_state.data) 

form = st.form(
    clear_on_submit=True, 
    key='input_form')

with form:
    c1, c2, c3 = st.columns(3)
    for i in range(1, num_rows+1):
        with c1:
          subj = st.text_input('Who', 
                      value="", 
                      max_chars=None, 
                      key="subject"+str(i), 
                      type="default", 
                      help=None, 
                      autocomplete=None, 
                      on_change=None, 
                      placeholder='Zeus', disabled=False, 
                      label_visibility="visible")
        with c2:
          pred = st.text_input('Does what', 
                      value="", 
                      max_chars=None, 
                      key="predicate"+str(i), 
                      type="default", 
                      help=None, 
                      autocomplete=None, 
                      on_change=None, 
                      placeholder='sees', disabled=False, 
                      label_visibility="visible")
        with c3:
          obj = st.text_input('To whom', 
                      value="", 
                      max_chars=None, 
                      key="object"+str(i), 
                      type="default", 
                      help=None, 
                      autocomplete=None, 
                      on_change=None, 
                      placeholder='Leda', disabled=False, 
                      label_visibility="visible")
    submit = st.form_submit_button("Save sequence", on_click=save_data(num_rows))

