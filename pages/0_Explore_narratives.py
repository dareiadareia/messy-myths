import streamlit as st
import pandas as pd
import os
import json
import datetime
# from st_aggrid import AgGr

path_to_data = 'sequence.json'

with open(path_to_data) as file:
	list_of_seqs = json.loads(file.read())

human_references = [f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' for seq in list_of_seqs]

selected_narrative_human = st.selectbox("Select a narrative to display:",
	human_references
	)

selected_narrative = [seq for seq in list_of_seqs if f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' == selected_narrative_human]

st.table(pd.DataFrame.from_records(selected_narrative[0]["hyleme sequence"]))