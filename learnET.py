# python code to learn hot the xml.etree.ElementTree 
# module works and deals with .xml and .gxl
# (graph exchange language) files. I am particularly
# interested in reading an .gxl and converting into an .swc file
# I learned most of the tools to code what's inside 
# with the following links

# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.findall
# https://stackabuse.com/reading-and-writing-xml-files-in-python/
# Leandro Scholz 29.08.2018

#details about the swc format 
# http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
import xml.etree.ElementTree as ET
import numpy as np

#read the file
tree=ET.parse('D:\\Leandro\\MEGA\\MestradoPPGEQ\\NEUBIAS\\image2\\tree_structure.gxl')
#tree=ET.parse('tree_structure.gxl')
root=tree.getroot()

# find all elements with name 'node' and 'edge'
# and store them 
nodes=root.findall('.//node')
edges=root.findall('.//edge')

# get the size of each of these lists, which will be the 
#number of nodes and edges in the file
num_nodes=len(nodes)
num_edges=len(edges)

print('there are ',num_nodes,' nodes in this graph')
print('there are ',num_edges,' edges in this graph')

swcArray=np.zeros((num_nodes,7))
# adds to the first column the node id's 
swcArray[:,0]=np.arange(num_nodes)
print(swcArray)

#testing what attributes are inside the nodes in this graph
for attribute in root.findall('.//node/attr'):
	print(attribute.tag,attribute.attrib)
# in this case, the attributes are 'nodeType' and 'position' 
for attribute in root.findall('.//edge/attr'):
	print(attribute.tag,attribute.attrib)
# in this case, the attribute shown is ' radius' 

# just for learning purposes (and sanity check) define 
# two count variables and compute the number of nodes
# and edges 
node_count=0
edge_count=0

print('the nodes of the graph are ')
#print all node id's of the graph
for node in tree.findall('.//node/[@id]'): 
	node_id=node.get('id')
	print(node_id)
	node_count+=1
	

# test to check how it is possible to get the values of the 
# node positions
print('the position of the nodes are ')
# print all node id's of the graph 
# THIS PART IS STILL NOT WORKING PROPERLY
for nodes in tree.findall(".//node/attr/[@name=' position']"):
	positions=nodes.findall('.//tup/float')
	for position in positions:
		node_pos=float(position.text)
		print(node_pos)
			
# With this, it's possible to visualize the positions of all nodes of the gxl file in the prompt
# what I want is to store each os these positions to the correct row in swcArray. 
# if node 2 position is [5,5,5] I want the second row of swcArray columns 3,4 and 5 (see .swc file format specification) to store this position
for node_id in range(0,num_nodes):
	xpath=".//node/[@id='n%s']/attr/[@name=' position']" %node_id
	for node in tree.findall(xpath):
		node_pos=node.findall('.//tup/float')
		for position in range(0,3):
			swcArray[node_id,position+2]=float(node_pos[position].text)

# now the positions are stored in swcArray properly 
print(swcArray)
# now a similar test to check how to get the radius of the edge
# for later, I will probably define the radius of a nodes as being the average radius of its edges
print('the radii of the edges are')
for edges in tree.findall(".//edge/attr/[@name=' radius']"):
	for edge in nodes:
		edge_rad=float(edges.find('.//float').text)
		print(edge_rad)

print(node_count,' nodes')
if node_count==num_nodes:
	print('node_count and num_nodes match')

#print all edge id's (from and to) of the graph
print('the edges of the graph are ')
for edge in tree.findall(".//edge"):
	start=edge.get('from')
	end=edge.get('to')
	print(start,' to',end)
	edge_count+=1
	
print(edge_count,' edges')
if edge_count==num_edges:
	print('edge_count and num_edges match')

