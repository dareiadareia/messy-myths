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

multiple_choice = [f'{seq["metadata"]["title"]} ({seq["metadata"]["passage reference"]})' for seq in list_of_seqs if f'{seq["metadata"]["title"]} ({seq["metadata"]["passage reference"]})' not in selected_narratives]

# selected_narratives = []
for i in range(number_of_narratives):
	selected_narratives.append(st.selectbox('Choose a story to compare',
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

# narratives_to_show

cols = st.columns(number_of_narratives)

# def style_similar(v, props):
# 	return props if v 

for i, col in enumerate(cols):
	# print(i)
	with col:
		st.table(pd.DataFrame.from_records(narratives_to_show[i]["hyleme sequence"])
			)

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

entities = []
actions = []
for seq in narratives_to_show:
	entities += extract_entities(seq['hyleme sequence'])
	actions += extract_actions(seq['hyleme sequence'])

entities.sort()
actions.sort()

# print('Entities are:')
# print(entities)
# print(actions)

col1, col2 = st.columns(2)
with col1:
	form1 = st.form(
		key='for_comparison')
	with form1:
		st.write('Choose comparison parametres')
		compare_subj = st.checkbox('subject', key='checkbox_subj')
		compare_pred = st.checkbox('predicate', key='checkbox_pred')
		compare_obj = st.checkbox('object', key='checkbox_obj')
		submitted1 = st.form_submit_button("Save")
with col2:
	st.write('If you want to treat entities/actions as identical for this comparison, select them here.')
	currently_same = []
	form2 = st.form(key='entities_to_be_same')
	with form2:
		'Entities:'
		subcol1, subcol2, subcol3 =  st.columns([3,1,3])
		with subcol1:
			st.selectbox('', entities,
			key='entity1', label_visibility='collapsed') 
		with subcol2:
			'=' 
		with subcol3:
			st.selectbox(
			'', 
			entities,
			key='entity2', label_visibility='collapsed')
		submitted3 = st.form_submit_button("Save")
	form3 = st.form(key='actions_to_be_same')
	with form3:
		'Actions:'
		subcol4, subcol5, subcol6 =  st.columns([3,1,3])
		with subcol4:
			st.selectbox('', 
			actions, 
			key='action1', label_visibility='collapsed') 
		with subcol5:
			'=' 
		with subcol6:
			st.selectbox('', 
			actions,
			key='action2', label_visibility='collapsed')
		submitted3 = st.form_submit_button("Save")

comparison_criteria = []
if compare_subj:
	comparison_criteria.append("subject")
if compare_pred:
	comparison_criteria.append("predicate")
if compare_obj:
	comparison_criteria.append("object")

comparison_str = ', '.join(comparison_criteria)

'Current settings:'
if submitted1:
	st.write(
	f'- comparing by **{comparison_str}**.'
	)
else:
	st.write('no settings yet (please enter and save settings in the form above)')


def compare_hylemes(hyl1, hyl2, crit): # hyl1 and hyl2 are dicts 
	result = True
	for c in crit:
		if hyl1[c] != hyl2[c]:
			result = False
	return result


def compare_narratives(seq1, seq2, crit): # crit is a list, seq1 and seq2 are dicts with everything including metadata
	# just extract hyleme sequences (list of dicts)
	# print('...starting comparison...')
	hyl_seq1 = seq1["hyleme sequence"]
	hyl_seq2 = seq2["hyleme sequence"]
	# print(hyl_seq1)
	# print(hyl_seq2)
	# set stack
	stack = []
	i = 0
	new_hyl_seq = []
	for elem in hyl_seq1:
		if compare_hylemes(elem, hyl_seq2[i], crit):
			# new_hyl_seq.append(stack)
			new_hyl_seq.append({
				"subject1": elem["subject"], 
				"predicate1": elem["predicate"], 
				"object1": elem["object"],
				"subject2": hyl_seq2[i]["subject"], 
				"predicate2": hyl_seq2[i]["predicate"], 
				"object2": hyl_seq2[i]["object"]
				})
			stack=[]
		else:
			# new_hyl_seq.append({"subject1": elem["subject"], 
				# "predicate1": elem["predicate"], 
				# "object1": elem["object"],
				# "subject2": "", 
				# "predicate2": "", 
				# "object2": ""})
			# stack.append({
			# 	"subject1": "", 
			# 	"predicate1": "", 
			# 	"object1": "",
			# 	"subject2": hyl_seq2[i]["subject"], 
			# 	"predicate2": hyl_seq2[i]["predicate"], 
			# 	"object2": hyl_seq2[i]["object"]
			# 	})
			i+=1
	return new_hyl_seq

st.write(f'Length of narr to show is {len(narratives_to_show)}')

if len(narratives_to_show) >= 2:
	st.write('## Comparison table')
	test_comparison = compare_narratives(narratives_to_show[0], narratives_to_show[1], comparison_criteria)
	# print(test_comparison)
	st.table(pd.DataFrame(test_comparison))
# comparison_df = pd.DataFrame(comparison_dict)

# comparison_df_editable = st.experimental_data_editor(comparison_df)

