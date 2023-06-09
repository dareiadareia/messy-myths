__author__ = 'dareia'
#import string
#import datetime as datetime
#import json
#import os
import pandas as pd
import streamlit as st
import pickle
import datetime

st.write('## Add a new hyleme sequence')

num_rows = st.slider('Number of Rows', min_value=1,max_value=30,value=1)

if 'data' not in st.session_state:
    data = pd.DataFrame({'subject':[],'predicate':[],'object':[]})
    st.session_state.data = data
if 'metadata' not in st.session_state:
    st.session_state.metadata = {}

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
    metadata = current_metadata
    metadata['sequence id'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    st.session_state.metadata = metadata
    # st.dataframe(st.session_state.data) 


form = st.form(
    clear_on_submit=True, 
    key='input_form_2')

with form:
    #c1, c2, c3 = st.columns(3)
    current_metadata = {}
    current_metadata['title'] = st.text_input(label='title', placeholder='Iliad, proem')
    current_metadata['passage reference'] = st.text_input(label='reference', placeholder='Hom. Il. 1–9')
    st.write('narrative:')
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
                      placeholder='see/s', disabled=False, 
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
    presubmit = st.form_submit_button("Process sequence", on_click=save_data(num_rows))

if presubmit:
    st.write("Your surrent sequence:")
    st.dataframe(st.session_state.data)

sequence_dict = {}
hyl_sequence = st.session_state.data.to_dict('records')

# st.write(hyl_sequence)
# st.write(type(hyl_sequence))
for h in hyl_sequence:
    for k, v in h.items():
        h[k] = v[0]
sequence_dict['hyleme sequence'] = hyl_sequence
sequence_dict['metadata'] = st.session_state.metadata

sequence_dict_export = [sequence_dict]
# st.write(sequence_dict_export)
# st.write('----')
# st.write(hyl_sequence)

def add_new_sequence_to_json(sequence_dict_export):
    from save_to_github import push_to_repo_branch
    return(push_to_repo_branch(file_or_variable='variable',
        gitHubFileName='sequences.json', 
        fileName=sequence_dict_export, 
        repo_slug='dareiadareia/messy-myths', 
        branch='main', 
        user = st.secrets.github.user, 
        token = st.secrets.github.token))
    # st.write('Sequence submitted!')
    # st.write('Submitted!')


submit = st.button("Submit sequence")

status = st.container()

if submit:
    status.write('Submitting the sequence...')
    if add_new_sequence_to_json(sequence_dict_export):
        status.write('Submitted!')


# sequence_dict