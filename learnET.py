"""
#python code to learn how the xml.etree.ElementTree module works and deals with
#.xml and .gxl (graph exchange language) files. The intention is to read a
#.gxl file and convert it into an .swc file of the graph. The .gxl file was generated
#by VascuSynth, an algorithm and accompanying software for synthesizing vascular
#or other tubular, tree-like structures.
#http://vascusynth.cs.sfu.ca/Welcome.html
#I learned most of the tools to code what's inside from the following links
#https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.findall
#https://stackabuse.com/reading-and-writing-xml-files-in-python/
#Leandro Scholz 29.08.2018
#Information about the swc format
#http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
"""
import xml.etree.ElementTree as ET
import numpy as np

#read the file
#TREE=ET.parse('D:\\Leandro\\MEGA\\MestradoPPGEQ\\NEUBIAS\\image2\\tree_structure.gxl')
TREE = ET.parse('tree_structure.gxl')
ROOT = TREE.getroot()

# find all elements with name 'node' and 'edge'
# and store them
NODES = ROOT.findall('.//node')
EDGES = ROOT.findall('.//edge')

# get the size of each of these lists, which will be the
#number of nodes and edges in the file
NUM_NODES = len(NODES)
NUM_EDGES = len(EDGES)

print('there are ', NUM_NODES, ' nodes in this graph')
print('there are ', NUM_EDGES, ' edges in this graph')

swcArray = np.zeros((NUM_NODES, 7))
# adds to the first column the node id's
swcArray[:, 0] = np.arange(NUM_NODES)
print(swcArray)

#testing what attributes are inside the nodes in this graph
for attribute in ROOT.findall('.//node/attr'):
    print(attribute.tag, attribute.attrib)
# in this case, the attributes are 'nodeType' and 'position'
for attribute in ROOT.findall('.//edge/attr'):
    print(attribute.tag, attribute.attrib)
# in this case, the attribute shown is ' radius'

# just for learning purposes (and sanity check) define
# two count variables and compute the number of nodes
# and edges
node_count = 0
edge_count = 0

print('the nodes of the graph are ')
#print all node id's of the graph
for node in TREE.findall('.//node/[@id]'):
    node_id = node.get('id')
    print(node_id)
    node_count += 1

# test to check how it is possible to get the values of the
# node positions
print('the position of the nodes are ')
# print all node id's of the graph

for NODES in TREE.findall(".//node/attr/[@name=' position']"):
    positions = NODES.findall('.//tup/float')
    for position in positions:
        node_pos = float(position.text)
        print(node_pos)

# With this, it's possible to visualize the positions of all
# nodes of the gxl file in the prompt. What I want is to
# store each of these positions to the correct row in swcArray.
# if node 2 position is [5,5,5] I want the second row of
# swcArray columns 3,4 and 5 (see .swc file format specification)
# to store this position
for node_id in range(0, NUM_NODES):
    xpath = ".//node/[@id='n%s']/attr/[@name=' position']" %node_id
    for node in TREE.findall(xpath):
        node_pos = node.findall('.//tup/float')
        for position in range(0, 3):
            swcArray[node_id, position+2] = float(node_pos[position].text)
# now the positions are stored in swcArray properly
print(swcArray)
# now a similar test to check how to get the radius of the edge
# for later, I will probably define the radius of a nodes as being the average radius of its edges
print('the radii of the edges are')
for EDGES in TREE.findall(".//edge/attr/[@name=' radius']"):
    for edge in NODES:
        edge_rad = float(EDGES.find('.//float').text)
        print(edge_rad)

print(node_count, ' nodes')
if node_count == NUM_NODES:
    print('node_count and NUM_NODES match')

#print all edge id's (from and to) of the graph
print('the edges of the graph are ')
for edge in TREE.findall(".//edge"):
    start = edge.get('from')
    end = edge.get('to')
    print(start, ' to', end)
    edge_count += 1

print(edge_count, ' edges')
if edge_count == NUM_EDGES:
    print('edge_count and NUM_EDGES match')

# It is now necessary to get the radius of the edges
# and store on the nodes, since the swc format
# does not store radii in edges, but in the nodes themselves
# As a starting point, the node N will receive the radius
# from the edge where N is the target ('to').
# with the exception of the root node, all nodes have
# an edge in which they are targets.

for node_id in range(0, NUM_NODES):
    node_type = TREE.find(".//node/[@id='n%s']/attr/[@name=' nodeType']/string" %node_id).text
    if node_type == ' root node ':
        print(node_id, ' is a root node')
        xpath = ".//edge/[@from='n%s']" %node_id
        root_edge = TREE.find(xpath)
        edge_rad = float(root_edge.find(".//attr/[@name=' radius']/float").text)
        swcArray[node_id, 5] = edge_rad
        #root nodes have parent defined as '-1'
        swcArray[node_id, 6] = -1
    else:
        xpath = ".//edge/[@to='n%s']" %node_id
        for edge in TREE.findall(xpath):
            edge_rad = float(edge.find(".//attr/[@name=' radius']/float").text)
            swcArray[node_id, 5] = edge_rad
            parent_node = edge.get('from')
            parent_node = parent_node[1:]
            swcArray[node_id, 6] = parent_node
#check if the radii were properly stored
print(swcArray)

np.savetxt('test.swc', swcArray, delimiter=' ', newline='\n', fmt='%i %i %4.3f %4.3f %4.3f %4.3f %i')
