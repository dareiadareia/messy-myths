__author__ = 'dareia'
import string
import datetime as datetime
import json
import os
import streamlit as st

st.title('Enter hylemes below')

st.text_input('Who', 
              value="", 
              max_chars=None, 
              key="subject", 
              type="default", 
              help=None, 
              autocomplete=None, 
              on_change=None, 
              placeholder='Zeus', disabled=False, 
              label_visibility="visible")

st.text_input('Does what', 
              value="", 
              max_chars=None, 
              key="predicate", 
              type="default", 
              help=None, 
              autocomplete=None, 
              on_change=None, 
              placeholder='sees', disabled=False, 
              label_visibility="visible")


st.text_input('To whom', 
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
