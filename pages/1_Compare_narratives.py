import streamlit as st
import pandas as pd
import os
import json
import datetime
import numpy as np 

from Home import test_function

# from st_aggrid import AgGrid

# st.title('Here you can explore and compare narratives')

directory_data = 'data'
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')

list_of_seqs = []
for filename in os.listdir(directory_data):
	f = os.path.join(directory_data, filename)
	if os.path.isfile(f):
		with open(f) as file:
			list_of_seqs += json.loads(file.read())

with open('sequences.json') as file:
	list_of_seqs += json.loads(file.read())
# st.write(list_of_seqs)

# number_of_narratives = st.number_input('Number of narratives to compare', 
# 	min_value=1,
# 	max_value=len(list_of_seqs),
# 	value=1,
# 	step=1)

number_of_narratives = 2

# if "selected_narratives" not in st.session_state or st.button("Start again"):
# 	st.session_state.selected_narratives=[]

selected_narratives=[]

multiple_choice = [f'{seq["metadata"]["title"]} ({seq["metadata"]["passage reference"]})' for seq in list_of_seqs if f'{seq["metadata"]["title"]} ({seq["metadata"]["passage reference"]})' not in selected_narratives]

st.write(f'## Select narratives')

# selected_narratives = []
for i in range(number_of_narratives):
	selected_narratives.append(st.selectbox(f'Choose a story to compare ({i+1})',
	multiple_choice,
	#key = narrative1,
	key = f'narrative{i+1}'
	)
		)

# --uncomment to remove repetition
# selected_narratives = list(set(selected_narratives)) 

narratives_to_show = []
for seq in list_of_seqs:
	if f'{seq["metadata"]["title"]} ({seq["metadata"]["passage reference"]})' in selected_narratives:
		narratives_to_show.append(seq)

# narratives_to_show is a list of sequences with metadata

cols = st.columns(number_of_narratives)

# def style_similar(v, props):
# 	return props if v 

for i, col in enumerate(cols):
	# print(i)
	with col:
		st.write(f'**Narrative {i+1}**')
		try:
			st.table(pd.DataFrame.from_records(narratives_to_show[i]["hyleme sequence"])
			)
		except IndexError:
			pass

#for seq in list_of_seqs:
	# seq_id = seq["sequence id"]
	# seq_ref = seq["title"] + f'({seq["passage reference"]})'
	# seq_as_table = pd.DataFrame.from_records(seq["hyleme sequence"])

def extract_entities(hyleme_sequence):
	# takes a list of dicts as input
	entities = []
	for hyleme in hyleme_sequence:
		# print(hyleme)
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

entities = [[] for i in range(len(narratives_to_show))]
actions = [[] for i in range(len(narratives_to_show))]
for i in range(len(narratives_to_show)):
	entities[i] = extract_entities(narratives_to_show[i]['hyleme sequence'])
	entities[i].sort()
	actions[i] = extract_actions(narratives_to_show[i]['hyleme sequence'])
	actions[i].sort()

print('Entities are:')
print(entities)
print(actions)


if "same_entities" not in st.session_state:
	st.session_state.same_entities = []

if "same_actions" not in st.session_state:
	st.session_state.same_actions = []

st.write(f'## Comparison settings')

with st.container():
	col1, col2 = st.columns(2)
	with col1:
		form1 = st.form(
			key='for_comparison')
		with form1:
			st.write('Choose and save comparison parametres')
			compare_subj = st.checkbox('subject', key='checkbox_subj')
			compare_pred = st.checkbox('predicate', key='checkbox_pred')
			compare_obj = st.checkbox('object', key='checkbox_obj')
			submitted1 = st.form_submit_button("Save")
	with col2: 
		if 'comparison_criteria' not in st.session_state:
			st.session_state.comparison_criteria = []
		comparison_boolean = [compare_subj, compare_pred, compare_obj]
		st.session_state.comparison_criteria = [["subject", "predicate", "object"][x] for x in range(3) if comparison_boolean[x]]
		comparison_str = ', '.join(st.session_state.comparison_criteria)
		# st.write('')
		if len(st.session_state.comparison_criteria) > 0:
			st.success(
			f'Comparing by **{comparison_str}**.'
			)
		else:
			st.warning('**No settings yet**! Please enter and save settings in the form on the left.')
st.divider()
# st.session_state.comparison_criteria = list(set(st.session_state.comparison_criteria))
with st.container():
	st.info('If you want to treat entities/actions as identical for this comparison, select them here.')
	col1, col2 = st.columns(2)
	with col1:
		if len(narratives_to_show) > 1:
			form2 = st.form(key='entities_to_be_same')
			with form2:
				'Entities to be treated as equal:'
				subcol1, subcol2, subcol3 =  st.columns([3,1,3])
				with subcol1:
					entity_1 = st.selectbox('Entities to be treated as equal', 
						entities[0],
						key='entity1', 
						label_visibility='collapsed'
					) 
				with subcol2:
					'=' 
				with subcol3:
					entity_2 = st.selectbox('Entities to be treated as equal', 
					entities[1],
					key='entity2', 
					label_visibility='collapsed')
				submitted2 = st.form_submit_button("Add")
				if submitted2 and (entity_1, entity_2) not in st.session_state.same_entities:
					st.session_state.same_entities.append((entity_1, entity_2))
	with col2:
		if len(narratives_to_show) > 1:
			form3 = st.form(key='actions_to_be_same')
			with form3:
				'Actions to be treated as equal:'
				subcol4, subcol5, subcol6 =  st.columns([3,1,3])
				with subcol4:
					action_1 = st.selectbox('Actions to be treated as equal:', 
					actions[0], 
					key='action1', 
					label_visibility='collapsed'
					) 
				with subcol5:
					'=' 
				with subcol6:
					action_2 = st.selectbox('Actions to be treated as equal:', 
					actions[1],
					key='action2', label_visibility='collapsed')
				submitted3 = st.form_submit_button("Add")
				if submitted3 and (action_1, action_2) not in st.session_state.same_actions:
					st.session_state.same_actions.append((action_1, action_2))


def display_equalities(same_stuff):
	key = 'same_' + same_stuff
	if len(st.session_state[key]) > 0:
		temp = [f'{t[0]} = {t[1]}' for t in st.session_state[key]]
		for i in temp:
			st.write('- ' + i)
	else:
		st.write('None')

st.info(
	'For this comparison, the the following entities/actions will be treated as equal:'
	)
c1, c2 = st.columns(2)
with c1:
	# st.write('*Entities:*')
	display_equalities("entities")
	if st.button('Clear entities'):
		st.session_state.same_entities = []
with c2:
	# st.write('*Actions:*')
	display_equalities("actions")
	if st.button('Clear actions'):
		st.session_state.same_actions = []

def compare_hylemes(hyl1, hyl2, crit): # hyl1 and hyl2 are dicts 
	# print(hyl1)
	# print(hyl2)
	# print(f"criteria are: {crit}")
	result = True
	for c in crit:
		if hyl1[c] != hyl2[c] and (hyl1[c], hyl2[c]) not in st.session_state.same_actions and (hyl1[c], hyl2[c]) not in st.session_state.same_entities:
			result = False
	return result


def compare_narratives(seq1, seq2, crit): # crit is a list, seq1 and seq2 are dicts with everything including metadata
	# just extract hyleme sequences (list of dicts)
	hyl_seq1 = seq1["hyleme sequence"]
	hyl_seq2 = seq2["hyleme sequence"]
	new_hyl_seq = []
	# set stack
	stack1 = []
	stack2 = []
	last_match_j = -1
	matches = 0
	for elem1 in hyl_seq1:
		match_found = False
		for i in range(last_match_j+1, len(hyl_seq2)):
			elem2 = hyl_seq2[i]
			if compare_hylemes(elem1, elem2, crit):
				match_found = True
				matches += 1
				new_hyl_seq += stack1 
				new_hyl_seq += stack2
				new_hyl_seq.append({
					"subject1": elem1["subject"], 
					"predicate1": elem1["predicate"], 
					"object1": elem1["object"],
					"subject2": elem2["subject"], 
					"predicate2": elem2["predicate"], 
					"object2": elem2["object"]
					})
				# st.write(new_hyl_seq)
				stack1=[]
				stack2=[]
				last_match_j = i
				break
			else:
				stack2.append({
				"subject1": "", 
				"predicate1": "", 
				"object1": "",
				"subject2": elem2["subject"], 
				"predicate2": elem2["predicate"], 
				"object2": elem2["object"]})
		if not match_found:
			stack1.append({
					"subject1": elem1["subject"], 
					"predicate1": elem1["predicate"], 
					"object1": elem1["object"],
					"subject2": "", 
					"predicate2": "", 
					"object2": ""})
			stack2 = []
	new_hyl_seq += stack1
	for k in range(last_match_j+1, len(hyl_seq2)):
		elem2 = hyl_seq2[k]
		stack2.append({
				"subject1": "", 
				"predicate1": "", 
				"object1": "",
				"subject2": elem2["subject"], 
				"predicate2": elem2["predicate"], 
				"object2": elem2["object"]})
	new_hyl_seq += stack2
	print(new_hyl_seq)
	if len(hyl_seq1) >= len(hyl_seq2):
		seqsim = matches/len(hyl_seq2)
	else:
		seqsim = matches/len(hyl_seq1)
	return(new_hyl_seq, seqsim)

def highlight_rows(row):
	if '' in row.values:
		return(['']*len(row)) 
	else:
		return(['background-color: yellow']*len(row))

if "comparison_df" not in st.session_state:
	st.session_state.comparison_df = pd.DataFrame()

if "comparison_sim" not in st.session_state:
	st.session_state.comparison_sim = 0

if st.button("Compare!"):
	if len(narratives_to_show) >= 2:
		st.write('## Comparison table')
		test_comparison = compare_narratives(narratives_to_show[0], narratives_to_show[1], st.session_state.comparison_criteria)
		# print(test_comparison)
		# st.write(test_comparison)
		st.session_state.comparison_df = pd.DataFrame(test_comparison[0])
		st.session_state.comparison_sim = test_comparison[1]
	else:
		st.markdown(':red[Sorry, not enough narratives to compare :(]')

if len(st.session_state.comparison_df) > 0:
	if st.selectbox("Choose visualisation", ["Static", "Editable"]) == "Static":
		st.table(st.session_state.comparison_df.style.apply(highlight_rows, axis=1))
		st.download_button('Save this comparison',
		file_name=f'comparison_{timestamp}.csv',
		mime='text/csv',
		data=st.session_state.comparison_df.to_csv().encode('utf-8'))
	else:
		edited_df = st.experimental_data_editor(st.session_state.comparison_df, num_rows="dynamic", use_container_width=True)
		st.download_button('Save this comparison',
		file_name=f'comparison_{timestamp}.csv',
		mime='text/csv',
		data=edited_df.to_csv().encode('utf-8'))

# st.write(f'Similarity score: **{st.session_state.comparison_sim}**')