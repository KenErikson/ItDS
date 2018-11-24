import networkx as nx
import re
import matplotlib.pyplot as plt
import collections
from networkx.algorithms.community import k_clique_communities

###
# Ken Erikson
###

#Init graph
graph = nx.Graph()

#Read data from file, put in graph
with open('CE-LC.txt') as f:
    for line in f:
        lineArray = re.split(r'\t+', line.strip())
        node1 = lineArray[0]
        node2 = lineArray[1]
        edgeWeight = lineArray[2]
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(node1, node2, weight=float(edgeWeight))
        if 'str' in line:
            break

#Draw original graph
nx.draw(graph, node_size=2)
plt.show()

#Number of nodes and edges
numberOfNodes = len(graph.nodes())
numberOfEdges = len(graph.edges())
print("2.1 Number of nodes: "+ str(numberOfNodes))
print("2.2 Number of edges: "+str(numberOfEdges))

#Average degree of nodes
totalDegrees = 0
for degree in graph.degree():
    totalDegrees += degree[1]
averageDegrees = totalDegrees/(numberOfNodes*1.0)
print("2.3 Average degree of nodes: " +str(averageDegrees))

#Network Density
print("3. Network density: "+str(nx.density(graph)))
minSpanTreeGraph = nx.minimum_spanning_tree(graph)
nx.draw_networkx(minSpanTreeGraph, with_labels=False, node_size = 2)
plt.show()

#Drawing degree distribution histogram
degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')
plt.title("Degree Distribution Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
plt.show()

#Getting largest subgraph
subGraphs = nx.connected_component_subgraphs(graph)
for subGraph in subGraphs:
    #Drawing largest subgraph
    nx.draw(subGraph, node_color='red', node_size=2)

    #Getting graph diameter
    print("6.2. LC graph diameter: "+str(nx.diameter(subGraph)))

    #Printing center
    print("6.3. Center of LC graph: "+str(nx.center(subGraph)))

    #Printing number of clique communities
    c = list(k_clique_communities(subGraph, 3))
    print("6.4. Number of clique communities with 3 nodes in LC: "+str(len(c[0])))
    plt.show()

    #Only interested in first subGraph
    break