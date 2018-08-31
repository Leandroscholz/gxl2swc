# python code to learn hot the xml.etree.ElementTree 
# module works and deals with .xml and .gxl
# (graph exchange language) files. I am particularly
# interested in reading an .gxl and converting into an .swc file
# I learned most of the tools to code what's inside 
# with the following links

# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.findall
# https://stackabuse.com/reading-and-writing-xml-files-in-python/
# Leandro Scholz 29.08.2018

import xml.etree.ElementTree as ET

#read the file
tree=ET.parse('tree_structure.gxl')
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
#print all node id's of the graph
for nodes in tree.findall(".//node/attr/[@name=' position']"):
	for node in nodes:
		print('node:')
		for position in node:
			node_pos=float(nodes.find('.//tup/float').text)
			print(node_pos)			

# now a similar test to check how to get the radius of the edge
# for later, I will probably define the radius of a nodes as being the average radius of its edges
print('the radius of the edges are')
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

