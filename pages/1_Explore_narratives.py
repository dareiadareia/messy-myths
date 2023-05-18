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

number_of_narratives = st.number_input('Number of narratives to compare', 
	min_value=1,
	max_value=None,
	value=1,
	step=1)

selected_narratives = []
for i in range(number_of_narratives):
	selected_narratives.append(st.selectbox('Choose a story to compare',
	multiple_choice,
	#key = narrative1,
	key = f'narrative{i+1}'
	)
		)

multiple_choice = [seq["title"] + f'({seq["passage reference"]})' for seq in list_of_seqs]


for seq in list_of_seqs:
	if seq["title"] + f'({seq["passage reference"]})' in selected_narratives:
		st.table(pd.DataFrame.from_records(seq["hyleme sequence"]))

#for seq in list_of_seqs:
	# seq_id = seq["sequence id"]
	# seq_ref = seq["title"] + f'({seq["passage reference"]})'
	# seq_as_table = pd.DataFrame.from_records(seq["hyleme sequence"])




