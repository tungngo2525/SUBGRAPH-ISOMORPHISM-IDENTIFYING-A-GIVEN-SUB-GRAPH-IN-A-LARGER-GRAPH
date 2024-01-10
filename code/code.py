import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

def create_graph_from_file(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            try:
                u, v = map(int, line.strip().split())
                G.add_edge(u, v)
            except ValueError:
                print(f"Couldn't convert line to edge: {line}")
    return G
#file: com-amazon.ungraph.txt || facebook_combined.txt
file_path = 'facebook_combined.txt'
G = create_graph_from_file(file_path)
num_tri_G = sum(nx.triangles(G).values())//3
graph_for_print_ktruss = nx.Graph()

#User input
node_input = input("\nEnter the user ID number: ")
node = int(node_input)
k = int(input("Enter the relevancy: "))
print("The program will find a group of people")
print("who know each other so that everyone knows at least k friends and this group contains the entered users.")
print("\n==================================================\n")
#function for finding maximal k-trusse containing entered node
def find_maximal_k_trusses_containing_node(g, k, node):
        change = True
        while change:
                change = False 
                for e in list(g.edges()):
                        a,b = e
                        if len(set(g.neighbors(a)).intersection(set(g.neighbors(b))))< k-2:
                                g.remove_edge(a,b)
                                change = True
        trusses = list(nx.connected_components(g))
        return [truss for truss in trusses if node in truss]
#Function for read edges from file and add them to array
def create_list_edge(filename):
        f=open(filename,'r')
        edgelist = []
        with open(filename, 'r') as f:
                for line in f:
                        edgelist.append(list(map(str, line.split('\t'))))
        f.close()
        return np.asarray(edgelist)
#Function for drawing graph
def draw_ktruss(edge_ktrusses):       
        graph = nx.Graph()
        list_edge = [(row[0], row[1]) for row in edge_ktrusses]
        graph.add_edges_from(list_edge)
        node_colors = ['red' if node == node_input else 'skyblue' for node in graph.nodes(default= int)]
        nx.draw(graph, with_labels=True, node_color = node_colors, font_size = 8)
        plt.show()
        return 


start_time = time.perf_counter()
#find maximal k-trusses containing node
maximal_k_trusses_containing_node = find_maximal_k_trusses_containing_node(G, k, node)
end_time = time.perf_counter()
#Write results to file
output_file_path1 = 'maximal_fktrusses.txt'
output_file_path2 = 'edge_fktrusses.txt'
with open(output_file_path1, 'w')as f:
       f.write(f"User related with user ID {node} :\n")
       for truss in maximal_k_trusses_containing_node:
              f.write(f"{truss}\n")

#Print message
print(f"The relevant users are written into the file: {output_file_path1}")
print(f"Their relationships are written in the file: {output_file_path2}")
print("\n==================================================\n")
#Print, write edges of maximal k-trusses containing node into file
for i,truss in enumerate(maximal_k_trusses_containing_node):
        print(f"\nEdges of maximal {k}-truss containing node {node}:")
        #global subgraph 
        subgraph= G.subgraph(truss)
        with open(output_file_path2, 'w')as f:
                for edge in subgraph.edges():
                        print(edge)
                        (u,v) = edge
                        f.write(f"{u}\t{v}\n")

        print(subgraph)

#Print accuracy and performance information
print("\nAccuracy:") 
print(f"- Number of triangles in the graph: {num_tri_G}")
print(f"- all vertices contained in the k-truss contain the input node {node}: {maximal_k_trusses_containing_node}")
print("Performance:")
edges  = G.number_of_edges()
execution_time = end_time - start_time
rate = edges / execution_time
print(f"- Total number of edges in k-truss graph (edges): {subgraph.number_of_edges()}")
print(f"- This subgraph include: {subgraph}")
print(f"- Execution time (seconds): {execution_time}")
print(f"- Rate (edges/second):{rate}")

#Copyright
print("\n@Copyright 2023 belongs to group BTL-CTRR. All rights reserved by HCMUT.")
#Draw k-trusses 

graph_ktruss = create_list_edge(output_file_path2)
draw_ktruss(graph_ktruss)
