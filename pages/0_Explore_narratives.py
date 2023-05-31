import streamlit as st
import pandas as pd
import os
import json
import datetime
# from st_aggrid import AgGr

directory_data = 'data'

def show_narrative(sequence):
	for k, v in sequence["metadata"].items():
		st.write(f'**{k}**: {v}')
	# st.write(sequence["metadata"])
	clean_hyleme_sequence = pd.DataFrame.from_records(sequence["hyleme sequence"]).applymap(lambda x: x[0])
	st.table(clean_hyleme_sequence)

list_of_seqs = []
for filename in os.listdir(directory_data):
	f = os.path.join(directory_data, filename)
	if os.path.isfile(f):
		with open(f) as file:
			list_of_seqs += json.loads(file.read())

human_references = [f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' for seq in list_of_seqs]

selected_narrative_human = st.selectbox("Select a narrative to display:",
	human_references
	)

selected_narrative = [seq for seq in list_of_seqs if f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' == selected_narrative_human]

show_narrative(selected_narrative[0])

# st.table(pd.DataFrame.from_records(selected_narrative[0]["hyleme sequence"]))