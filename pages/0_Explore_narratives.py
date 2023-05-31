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
	clean_hyleme_sequence = pd.DataFrame.from_records(sequence["hyleme sequence"])#.applymap(lambda x: x[0])
	st.table(clean_hyleme_sequence)

list_of_seqs = []
for filename in os.listdir(directory_data):
	f = os.path.join(directory_data, filename)
	if os.path.isfile(f):
		with open(f) as file:
			list_of_seqs += json.loads(file.read())

with open('sequences.json') as file:
	list_of_seqs += json.loads(file.read())

human_references = [f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' for seq in list_of_seqs]

selected_narrative_human = st.selectbox("Select a narrative to display:",
	human_references
	)

selected_narrative = [seq for seq in list_of_seqs if f'{seq["metadata"]["passage reference"]}: {seq["metadata"]["title"]}' == selected_narrative_human]

show_narrative(selected_narrative[0])

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

def look_for_similar_narratives(narrative):


