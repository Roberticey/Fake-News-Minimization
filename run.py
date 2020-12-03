#Importing the required libraries
import numpy as np
import snap
import random
import math
from collections import deque
import networkx as nx
import pandas as pd
import pickle
import copy

#For selecting the set of nodes that act as the activators
def deploy_activators(n, outdegree, G3, required, state, set_node, edges_per_bot, exponent):
	visited = []
	bot_number = n
	current_bot_edges = 0
	out_degree = []

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

#For selecting the set of nodes that are going to be monitored by the oracle bot nodes
def deploy_bots(n, outdegree, G3, required, state, set_node, edges_per_bot, exponent):
	visited = []
	bot_number = n
	current_bot_edges = 0
	out_degree = []

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
				visited[prob_select[i][1]] = 1
				G3.add_edge(prob_select[i][1], bot_number, weights = 1)
				current_bot_edges += 1
				if current_bot_edges > edges_per_bot:
					bot_number += 1
					current_bot_edges = 0
				break
		done += 1

#Reservior Sampling (Used in building of the graph)
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

#Probability with which any bot node reports a node spreading misinformation 
def report_prob_generator(level):																	
	report_prob = float(1.0/(1 + np.exp(-float(level))))
	return report_prob

# Simulation of the game (using multisource BFS)
def game_play(G, weights, set_node, gullibilty, state, n, level):	
	visited = []
	queue = deque()
	count_influenced = []												
	for i in range(n):
		count_influenced.append(1)
		visited.append(False)
		if set_node[i] == 'ACTIVATOR' or state[i] == 'MISINFORMED':
			queue.append(i)
			visited[i] = True
	while queue:
		node = queue.popleft()
		if set_node[node] == 'ORACLE' or state[node] == 'DOUBTFUL':
			continue
		visited[node] = True
		oracle_found = False

		for i in G[node]:										
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
			#Probability with which a node is influenced (misinformed) by someone who it follows
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

#No of nodes in the graph#
n = int(input("Enter the size of the graph (No. of vertices): "))


#Maximum number of edges that can be given to a node
m = int(input("Enter the average degree of each node of the graph): "))


#No of oracle bot nodes deployed by the platform
num_bots = int(input("Enter the number of bots in the graph: "))


#No of edges given to each oracle bot node
edges_per_bot = int(input("Enter the number of edges per bot: "))


#Size of the activator set in terms of the total number of edges going out of the activator set
size_activator = int(input("Enter the size of the activator set (Sum of outdegrees of all nodes in the activator set): "))


# Value of Activator exponent used by the misinformation spreader to choose the activator set
exponent_activators = int(input("Enter the value of the activator exponent: "))


# Value of oracle exponent used by the platform to choose the modes to be directly connected by the bots
exponent_bots = int(input("Enter the value of the bot exponent: "))


# Number of iterations of spread of the misinformation from the source, i.e. the activators
num_iters = int(input("Enter the number of iterations of the misinformation spread for each graph: "))


#Generating the required random (or real life social media) and changing it to a weighted directed graph 
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
		w = random.uniform(0,1)									
		outdegree[i] += 1
		G3.add_edge(i, j, weight = w)


#Initialization
arr = []
set_node = [] 													
gullibilty = [] 												
state = [] 														
for i in range(n):
	set_node.append('COMMON')
	state.append('UNINFORMED')
	gullibilty.append(random.uniform(0,1))

for i in range(n, n+num_bots, 1):
	state.append('BOT')
	set_node.append('ORACLE')

#Determines the underlying probability with which a particular node will be selected to act as an activator
exponent_activators = 0
#Determines the underlying probability with which a particular node will be selected to be monitored by an oracle bot node
exponent_bots = 0

#Get the set of nodes to act as activators
deploy_activators(n,outdegree,G3,size_activator, state, set_node, edges_per_bot,exponent_activators)

#Compute total out-degree of the activator set (>= size_of_activators) and the number of nodes in the activator set
act_sum = 0
act_ctr = 0
for i in range(n):
	if set_node[i] == 'ACTIVATOR':
		act_sum += outdegree[i]
		act_ctr += 1

#Get the set of nodes that will be monitored by the oracle bot nodes
deploy_bots(n, outdegree, G3, num_bots * edges_per_bot, state, set_node, edges_per_bot,exponent_bots)


#Part of the implementation (Border Case Handling)
for i in range(n):
	if set_node[i] == 'X':
		set_node[i] = 'COMMON'


#Store weight of each edge of the graph
weights = nx.get_edge_attributes(G3,'weight')
G = []

#Implemetation details
for i in range(n):
	x = G3.neighbors(i)
	G4 = []
	for j in x:
		G4.append(j)
	G.append(G4)

level = []

#Implementation details
for i in range(n):
	level.append(0)

#Run the simulation for "TIMES" times on the graph 
for iteration in range(10):

	#Play the game with the decided strategies
	game_play(G, weights, set_node, gullibilty, state, n, level)

	#Counter Variables
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
	#Stores the % misinformed in each iteration
	arr.append(float(float(100)*float(cnt_M)/float(n)))
	
#Average value of the % misinformed over all the iterations
arr = np.array(arr)

#Utility of the platform with \alpha_T = 1 and \beta_T = 100/n
utility = (100 - np.mean(arr)) - 100*float(num_bots)*edges_per_bot / n

#Output
print("Average = ", 100 - np.mean(arr), "Variance = ",utility)
