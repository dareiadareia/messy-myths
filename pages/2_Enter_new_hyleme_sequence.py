__author__ = 'dareia'
#import string
#import datetime as datetime
#import json
#import os
import pandas as pd
import streamlit as st
import pickle

st.title('Enter hylemes below')

num_rows = st.slider('Number of Rows', min_value=1,max_value=30,value=1)

if 'data' not in st.session_state:
    data = pd.DataFrame({'subject':[],'predicate':[],'object':[]})
    st.session_state.data = data

#source: https://discuss.streamlit.io/t/button-to-add-new-row-of-inputs/33245/2
def save_data(num_rows):
    data = pd.DataFrame({'subject':[],'predicate':[],'object':[]})
    st.session_state.data = data
    for i in range(num_rows):
        row = pd.Series({'subject':[st.session_state['subject'+str(i)]],
                'predicate':[st.session_state['predicate'+str(i)]],
                'object':[st.session_state['object'+str(i)]]
                })
        #st.write(row)
        st.session_state.data.loc[len(st.session_state.data)] = row
    st.dataframe(st.session_state.data) 

form = st.form(
    clear_on_submit=True, 
    key='input_form_2')

with form:
    #c1, c2, c3 = st.columns(3)
    for i in range(num_rows):
        c1, c2, c3 = st.columns(3)
        #with st.container():
        with c1:
            subj = st.text_input(label='subject', 
                value="", 
                max_chars=None, 
                key="subject"+str(i), 
                type="default", 
                help=None, 
                autocomplete=None, 
                on_change=None, 
                placeholder='Zeus', disabled=False, 
                label_visibility="collapsed")
        with c2:
            pred = st.text_input(label='predicate', 
                      value="", 
                      max_chars=None, 
                      key="predicate"+str(i), 
                      type="default", 
                      help=None, 
                      autocomplete=None, 
                      on_change=None, 
                      placeholder='sees', disabled=False, 
                      label_visibility="collapsed")
        with c3:
            obj = st.text_input(label='object', 
                      value="", 
                      max_chars=None, 
                      key="object"+str(i), 
                      type="default", 
                      help=None, 
                      autocomplete=None, 
                      on_change=None, 
                      placeholder='Leda', disabled=False, 
                      label_visibility="collapsed")
    submit = st.form_submit_button("Process sequence", on_click=save_data(num_rows))

sequence_dict = st.session_state.data.to_dict('records')


if st.button("Check sequence"):
    st.write("Your surrent sequence:", sequence_dict)

def add_new_sequence_to_json(sequence_dict):
    from save_to_github import push_to_repo_branch
    push_to_repo_branch(file_or_variable='variable',
        gitHubFileName='sequence.json', 
        fileName=sequence_dict, 
        repo_slug='dareiadareia/messy-myths', 
        branch='main', 
        user = st.secrets.github.user, 
        token = st.secrets.github.token)
    

st.button("Submit sequence", on_click=add_new_sequence_to_json(sequence_dict))
