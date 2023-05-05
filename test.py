__author__ = 'dareia'
import string
import datetime as datetime
import json
import os
import streamlit as st

st.title('Enter hylemes below')

with st.form(key='columns_in_form'):
  c1, c2, c3 = st.columns(3)
    with c1:
      subj = st.text_input('Who', 
                  value="", 
                  max_chars=None, 
                  key="subject", 
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
                  key="predicate", 
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
                  key="object", 
                  type="default", 
                  help=None, 
                  autocomplete=None, 
                  on_change=None, 
                  placeholder='Leda', disabled=False, 
                  label_visibility="visible")

if st.button('Next hyleme'):
    st.write('Ok!')
else:
    pass
  
if st.button('End of sequence'):
    st.write('Sequence entered.')
else:
    pass
