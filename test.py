__author__ = 'dareia'
import string
import datetime as datetime
import json
import os
import streamlit as st

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
              placeholder='Zeus', disabled=False, 
              label_visibility="visible")


st.text_input('To whom', 
              value="", 
              max_chars=None, 
              key="object", 
              type="default", 
              help=None, 
              autocomplete=None, 
              on_change=None, 
              placeholder='Zeus', disabled=False, 
              label_visibility="visible")

