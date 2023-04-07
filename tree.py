#!/usr/bin/env python
import networkx as nx
import matplotlib.pyplot as plt

# Read the file and parse each line to extract the person, mother, and father
with open('families.txt', 'r') as file:
    lines = file.readlines()

people = []
parents = {}
for line in lines:
    person, mother, father = line.strip().split()
    people.append(person)
    parents[person] = (mother, father)

# Create a graph to represent the family tree
graph = nx.DiGraph()

# Add nodes to the graph for each person and their parents
for person in people:
    graph.add_node(person)
    mother, father = parents[person]
    if mother != '0':
        graph.add_node(mother)
        graph.add_edge(mother, person)
    if father != '0':
        graph.add_node(father)
        graph.add_edge(father, person)

# Draw the graph
pos = nx.fruchterman_reingold_layout(graph)
nx.draw_networkx_nodes(graph, pos, node_size=1000, alpha=0.8)
nx.draw_networkx_edges(graph, pos, arrows=True)
nx.draw_networkx_labels(graph, pos, font_size=16, font_family='sans-serif')
plt.axis('off')
plt.show()