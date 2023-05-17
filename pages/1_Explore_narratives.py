import streamlit as st
import pandas as pd
import os
import json

st.title('Here you can explore and compare narratives')

directory_data = 'data'

list_of_seqs = []
for filename in os.listdir(directory_data):
	f = os.path.join(directory_data, filename)
	if os.path.isfile(f):
		with open(f) as file:
			list_of_seqs.append(json.loads(file.read()))

multiple_choice = [seq["title"] + f'({seq["passage reference"]})' for seq in list_of_seqs]

selected = st.selectbox('Choose a story to compare',
	multiple_choice,
	#key = narrative1,
	)



#for seq in list_of_seqs:
	# seq_id = seq["sequence id"]
	# seq_ref = seq["title"] + f'({seq["passage reference"]})'
	# seq_as_table = pd.DataFrame.from_records(seq["hyleme sequence"])




