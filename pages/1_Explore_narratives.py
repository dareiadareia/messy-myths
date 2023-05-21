import streamlit as st
import pandas as pd
import os
import json
# from st_aggrid import AgGrid

st.title('Here you can explore and compare narratives')

directory_data = 'data'

list_of_seqs = []
for filename in os.listdir(directory_data):
	f = os.path.join(directory_data, filename)
	if os.path.isfile(f):
		with open(f) as file:
			list_of_seqs.append(json.loads(file.read()))

#if "selected" in st.session_state:
#    del st.session_state.selected

number_of_narratives = st.number_input('Number of narratives to compare', 
	min_value=1,
	max_value=len(list_of_seqs),
	value=1,
	step=1)

if "selected_narratives" not in st.session_state or st.button("Start again"):
	st.session_state.selected_narratives=[]

multiple_choice = [f'{seq["title"]} ({seq["passage reference"]})' for seq in list_of_seqs if f'{seq["title"]} ({seq["passage reference"]})' not in st.session_state.selected_narratives]

# selected_narratives = []
for i in range(number_of_narratives):
	st.session_state.selected_narratives.append(st.selectbox('Choose a story to compare',
	multiple_choice,
	#key = narrative1,
	key = f'narrative{i+1}'
	)
		)

st.session_state.selected_narratives = list(set(st.session_state.selected_narratives))

narratives_to_show = []
for seq in list_of_seqs:
	if f'{seq["title"]} ({seq["passage reference"]})' in st.session_state.selected_narratives:
		narratives_to_show.append(seq)

# narratives_to_show

cols = st.columns(number_of_narratives)

for i, col in enumerate(cols):
	print(i)
	with col:
		st.table(pd.DataFrame.from_records(narratives_to_show[i]["hyleme sequence"]))

#for seq in list_of_seqs:
	# seq_id = seq["sequence id"]
	# seq_ref = seq["title"] + f'({seq["passage reference"]})'
	# seq_as_table = pd.DataFrame.from_records(seq["hyleme sequence"])




