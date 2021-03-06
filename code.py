from graph_tool.all import *
import numpy as np
import math
import matplotlib.pyplot as plt
import sys,csv
g = Graph(directed=False)

# node and edge property maps
v_age = g.new_vertex_property("int")
v_lifetime = g.new_vertex_property("int")
v_betweenness = g.new_vertex_property("double")

divideby = 1000

# model parameters for ANSWERS
def n(t):
    return math.floor(max((16)*(t**2) + 3000*t - 40000, 0)/divideby) # to avoid negative values and divide by assugned value above

a = 0.92
b = 0.00032
l = 0.0052
tau = 0.7 # for selecting first node to add

# model functions
def set_lifetime(u):
    '''
    node lifetime for node u sampled from exponential distribution
    nodes stop initiating edges once lifetime expires
    '''
    v_lifetime[u] = np.random.exponential(1.0/l)

def connect_to_first(u):
    '''
    connects to the first neighbour for some new node
    probability of node being selected is proportional to degree
    '''
    nodes = []
    probs = []
    for node in g.vertices(): # this is O(n), might be better to use arrays?
        nodes.append(node)
        probs.append(node.out_degree()**tau)

    if(g.num_vertices() == 1):
        return
    elif(g.num_vertices() == 2):
        v = g.vertex(0)
    else:
        s = sum(probs)
        norm = [float(i)/s for i in probs]
        v = np.random.choice(nodes, p=norm)
    
    g.add_edge(u,v)

def gap(u):
    '''
    sets time gap until next edge initiation
    '''
def close_triangle(u):
    '''
    returns endpoints to join for node triangle
    '''
    nodes = []
    for node in u.all_neighbours():
        nodes.append(node)

    intermediate = np.random.choice(nodes)

    nodes = []
    for node in intermediate.all_neighbours():
        if(node != u):
            nodes.append(node)

    v = np.random.choice(nodes)

    g.add_edge(u,v)
        
def update_state():
    # add new nodes
    num = n(timer)
    for i in range(num):
        #print(i)
        u = g.add_vertex()
        set_lifetime(u)
        connect_to_first(u)

    # process nodes which are awake

file = open("betweenness1.txt","w")
timer = 0
node_counter = 0
steps = 50 # this is the number of steps until program terminates
while(timer < steps):
    '''	
    print("-----")
    file.write("-----\n")
    print("step: " + str(timer))
    file.write("step: "+str(timer)+"\n")
    '''
    node_counter = node_counter + n(timer)
    '''
    print("node_counter: " + str(node_counter))
    file.write("node_counter: " + str(node_counter) +"\n")
    '''
    update_state()
    betweenness(g=g,vprop=v_betweenness)
    sum_betweenness = 0
    for v in g.vertices():
        sum_betweenness += v_betweenness.a[v]
    if(node_counter != 0):
        sum_betweenness /= node_counter
    print(str(timer) + ": " + str(sum_betweenness) + " node: " + str(node_counter))
    file.write(str(timer) + ": " + str(sum_betweenness) + " node: " + str(node_counter) + "::\n")
    timer += 1
	
file.close()

# uncomment line below to draw final graph
#graph_draw (g, output_size=(10000, 10000),output="a.png")

#betweenness(g=g,vprop=v_betweenness)
#v_betweenness =betweenness(g)[0]

#counter = 0

#file = open("betweenness.txt","w")
#for v in g.vertices():
    #counter += 1
    #file.write(str(v_betweenness.a[v]))
    #file.write("\n")
    

#print(counter)
