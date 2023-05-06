__author__ = 'dareia'
#import string
#import datetime as datetime
#import json
#import os
import pandas as pd
import streamlit as st

st.title('Enter hylemes below')

if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1

if 'data' not in st.session_state:
    data = pd.DataFrame({'subject':[],'predicate':[],'object':[]})
    st.session_state.data = data

data = st.session_state.data

#source: https://discuss.streamlit.io/t/button-to-add-new-row-of-inputs/33245/2
def save_data():
    row = pd.DataFrame({'subject':[st.session_state.subject],
            'predicate':[st.session_state.predicate],
            'object':[st.session_state.object]})
    st.session_state.data = pd.concat([st.session_state.data, row])
    st.session_state.n_rows = 0

if st.session_state.n_rows > 0:
    form = st.form(clear_on_submit=True, key='input_form'+str(st.session_state.n_rows))
    with form:
        c1, c2, c3 = st.columns(3)
        for i in range(1, st.session_state.n_rows+1):
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
        submit = st.form_submit_button("Save sequence", on_click=save_data)

st.dataframe(data) 

add_row = st.button(label="add")
if add_row:
    st.session_state.n_rows += 1
    st.experimental_rerun()
