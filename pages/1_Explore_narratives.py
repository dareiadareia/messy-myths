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

# if "selected_narratives" not in st.session_state or st.button("Start again"):
# 	st.session_state.selected_narratives=[]

selected_narratives=[]

multiple_choice = [f'{seq["title"]} ({seq["passage reference"]})' for seq in list_of_seqs if f'{seq["title"]} ({seq["passage reference"]})' not in selected_narratives]

# selected_narratives = []
for i in range(number_of_narratives):
	selected_narratives.append(st.selectbox('Choose a story to compare',
	multiple_choice,
	#key = narrative1,
	key = f'narrative{i+1}'
	)
		)

selected_narratives = list(set(selected_narratives))

narratives_to_show = []
for seq in list_of_seqs:
	if f'{seq["title"]} ({seq["passage reference"]})' in selected_narratives:
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

def extract_entities(hyleme_sequence):
	# takes a list of dicts as input
	entities = []
	for hyleme in hyleme_sequence:
		print(hyleme)
		if hyleme['subject'] not in entities:
			entities.append(hyleme['subject'])
		if hyleme['object'] not in entities:
			entities.append(hyleme['object'])
	return(list(set(entities)))

def extract_actions(hyleme_sequence):
	# takes a list of dicts as input
	actions = []
	for hyleme in hyleme_sequence:
		if hyleme['predicate'] not in actions:
			actions.append(hyleme['predicate'])
	return(list(set(actions)))

entities = [extract_entities(seq['hyleme sequence']) for seq in narratives_to_show]
actions = [extract_actions(seq['hyleme sequence']) for seq in narratives_to_show]

print(entities)
print(actions)

col1, col2 = st.columns(2)
with col1:
	form1 = st.form(
		key='for_comparison')
	with form1:
		st.write('Choose comparison parametres')
		st.checkbox('subject', key='checkbox_subj')
		st.checkbox('predicate', key='checkbox_pred')
		st.checkbox('object', key='checkbox_obj')
		st.form_submit_button("Save")
with col2:
	form2 = st.form(key='claimed_to_be_same')
	with form2:
		st.write('If you want to treat entities as identical for this comparison, select them')
		currently_same = []
		st.selectbox('', entities,
			key='entity1', label_visibility='collapsed') 
		'=' 
		st.selectbox(
			'', 
			entities,
			key='entity2', label_visibility='collapsed')
		st.selectbox('', 
			actions, 
			key='action1', label_visibility='collapsed') 
		'=' 
		st.selectbox('', 
			actions,
			key='action2', label_visibility='collapsed')
		st.form_submit_button("Save")

st.write('Comparison table')

# comparison_df = ''

# comparison_df_editable = st.experimental_data_editor(comparison_df)

