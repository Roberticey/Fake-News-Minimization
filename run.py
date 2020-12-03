import numpy as np
import snap
import random
import math
from collections import deque
import networkx as nx
import pandas as pd
import pickle
import copy

def deploy_activators(n, outdegree, G3, required, state, set_node, edges_per_bot, exponent):
	visited = []
	bot_number = n
	current_bot_edges = 0
	out_degree = []
	ss = 0

	for i in range(n):
		visited.append(False)
		out_degree.append(0.0)
		out_degree[i] = outdegree[i]
		if out_degree[i] == 0:
			pass
		else:
			out_degree[i] = pow(out_degree[i],exponent)

	done = 0
	while done < required:
		total_outdegree = 0
		for i in range(n):
			if visited[i] == False:
				total_outdegree += out_degree[i]

		prob_select = []
		cnt_valid_nodes = 0
		prob_range = 0
		for i in range(n):
			if visited[i] == True:
				continue
			prob_range += out_degree[i]/total_outdegree
			prob_select.append([prob_range,i])
			cnt_valid_nodes += 1

		temp = random.uniform(0,1)


		for i in range(cnt_valid_nodes):
			if temp < prob_select[i][0]:
				done += outdegree[i]
				visited[prob_select[i][1]] = 1
				set_node[prob_select[i][1]] = 'ACTIVATOR'
				state[prob_select[i][1]] = 'MISINFORMED'
				break
		# done += 1


def deploy_bots(n, outdegree, G3, required, state, set_node, edges_per_bot, exponent):
	visited = []
	bot_number = n
	current_bot_edges = 0
	out_degree = []

	for i in range(n):
		visited.append(False)
		out_degree.append(0.0)
		# if set_node[i] == 'ACTIVATOR':
		# 	visited[i] = True
		out_degree[i] = outdegree[i]
		if out_degree[i] == 0:
			pass
		else:
			out_degree[i] = pow(out_degree[i],exponent)
		# out_degree[i] = pow(out_degree[i],exponent)

	done = 0
	while done < required:
		total_outdegree = 0
		for i in range(n):
			if visited[i] == False:
				total_outdegree += out_degree[i]

		prob_select = []
		cnt_valid_nodes = 0
		prob_range = 0
		for i in range(n):
			if visited[i] == True:
				continue
			prob_range += out_degree[i]/total_outdegree
			prob_select.append([prob_range,i])
			cnt_valid_nodes += 1

		temp = random.uniform(0,1)

		for i in range(cnt_valid_nodes):
			if temp < prob_select[i][0]:
				visited[prob_select[i][1]] = 1
				G3.add_edge(prob_select[i][1], bot_number, weights = 1)
				current_bot_edges += 1
				if current_bot_edges > edges_per_bot:
					bot_number += 1
					current_bot_edges = 0
				break
		done += 1



	#GetOutDegCnt


def selectKItems(stream, n, k): 
	i=0;  
	reservoir = [0]*k; 
	for i in range(k): 
	    reservoir[i] = stream[i] 
	while(i < n): 
	    j = random.randrange(i+1)
	    if(j < k): 
	        reservoir[j] = stream[i] 
	    i+=1; 
	return reservoir


def report_prob_generator(level):																	#report_prob_generator
	# report_prob = 2.0 * (float(1.0/(1 + np.exp(-float(level)))) - 0.5)
	report_prob = float(1.0/(1 + np.exp(-float(level))))
	# report_prob = np.tanh(float(level))
	# report_prob = (np.tanh(float(level)) + 1) / 2.0
	# report_prob = 1
	return report_prob


def game_play(G, weights, set_node, gullibilty, state, n, level):	
	visited = []
	queue = deque()
	count_influenced = []													#subject to change  
	for i in range(n):
		count_influenced.append(1)
		visited.append(False)
		if set_node[i] == 'ACTIVATOR' or state[i] == 'MISINFORMED':
			queue.append(i)
			visited[i] = True
	while queue:
		node = queue.popleft()
		# print(node)
		if set_node[node] == 'ORACLE' or state[node] == 'DOUBTFUL':
			continue
		visited[node] = True
		oracle_found = False

		for i in G[node]:											#change
			if set_node[i] == 'ORACLE':
				oracle_found = True
				break

		report_success = oracle_found
		report_prob = report_prob_generator(level[node])
		temp = random.uniform(0, 1)

		if temp > report_prob:
			report_success = False

		if report_success:
			state[node] = 'DOUBTFUL'
			count_influenced[node] += 1
			for i in G[node]:
				if set_node[i] == 'ORACLE' or set_node[i] == 'ACTIVATOR':
					continue
				state[i] = 'DOUBTFUL'
				count_influenced[i] += 1
			continue

		for i in G[node]:
			if set_node[i] == 'ORACLE' or set_node[i] == 'ACTIVATOR' or state[i] == 'MISINFORMED':
				continue
			prob_misinformed = 1.0
			prob_misinformed /= float(count_influenced[i])
			prob_misinformed *= float(gullibilty[i] + weights[(node,i)] + 2.0)/4.0

			temp = random.uniform(0,1)
			if temp > prob_misinformed:
				state[i] = 'DOUBTFUL'
			else:
				state[i] = 'MISINFORMED'
				queue.append(i)
				level[i] = level[node] + 1






n = 1000
m = 100
num_bots = 10
edges_per_bot = 4
size_activator = 500

temp_G2 = snap.GenRndGnm(snap.PNGraph, n, m)
G3 = nx.DiGraph()


for i in range(n + num_bots):
	G3.add_node(i)

G3 = nx.DiGraph()
one_to_n = []
outdegree = []
for i in range(n):
	outdegree.append(0)
	one_to_n.append(i)

for i in range(n + num_bots):
	G3.add_node(i)

for i in range(n):
	to_vertices = []
	k = random.randint(1, m+1)
	to_vertices = selectKItems(one_to_n, n, k)
	for j in to_vertices:
		if j == i:
			continue
		w = random.uniform(0,1)									#initialization of w
		outdegree[i] += 1
		G3.add_edge(i, j, weight = w)



arr = []
set_node = [] 													# A, T, C activator, valididator, ....
gullibilty = [] 												# gullibilty index -> 1-lamda
state = [] 														# uninformed, misinformed, correct doubtful, immune
for i in range(n):
	set_node.append('COMMON')
	state.append('UNINFORMED')
	gullibilty.append(random.uniform(0,1))

for i in range(n, n+num_bots, 1):
	state.append('BOT')
	set_node.append('ORACLE')

exponent_activators = 0
exponent_bots = 0

deploy_activators(n,outdegree,G3,size_activator, state, set_node, edges_per_bot,exponent_activators)


act_sum = 0
act_ctr = 0
for i in range(n):
	if set_node[i] == 'ACTIVATOR':
		act_sum += outdegree[i]
		act_ctr += 1

# print( "Activator average outdegree: ",float(act_sum)/act_ctr)


deploy_bots(n, outdegree, G3, num_bots * edges_per_bot, state, set_node, edges_per_bot,exponent_bots)


for i in range(n):
	if set_node[i] == 'X':
		set_node[i] = 'COMMON'

weights = nx.get_edge_attributes(G3,'weight')
G = []

for i in range(n):
	x = G3.neighbors(i)
	G4 = []
	for j in x:
		# if i < n and j >= n:
		# 	print(i,j,"dadadada success")
		G4.append(j)
	G.append(G4)

level = []

for i in range(n):
	level.append(0)

for iteration in range(10):

	game_play(G, weights, set_node, gullibilty, state, n, level)


	cnt_U = 0
	cnt_M = 0
	cnt_D = 0
	cnt_I = 0
	for i in state:
		if i == 'UNINFORMED':
			cnt_U += 1
		if i == 'MISINFORMED':
			cnt_M += 1
		if i == 'DOUBTFUL':
			cnt_D += 1
		if i == 'BOT':
			cnt_I += 1
	arr.append(float(float(100)*float(cnt_M)/float(n)))
	# print("Activators = ", cnt_imp, "Validators = ", cnt_val, "U = ", float(float(100)*float(cnt_U)/float(n)), "M = ", float(float(100)*float(cnt_M)/float(n)), "D = ", float(float(100)*float(cnt_D)/float(n)), "I = ", float(float(100)*float(cnt_I)/float(n)))

arr = np.array(arr)

# print("Average = ", np.mean(arr), "Variance = ",np.std(arr))
utility = (100 - np.mean(arr)) - 100*float(num_bots)*edges_per_bot / n

print("Average = ", 100 - np.mean(arr), "Variance = ",utility)
# print(n, num_bots*edges_per_bot)