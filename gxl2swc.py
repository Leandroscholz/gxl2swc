"""
# python function gxl2swc to learn how the xml.etree.ElementTree module works and deals with
#   .xml and .gxl (graph exchange language) files. The intention is to read a
#   .gxl file and convert it into an .swc file of the graph. The .gxl file was generated
#   by VascuSynth, an algorithm and accompanying software for synthesizing vascular
#   or other tubular, tree-like structures.
# http://vascusynth.cs.sfu.ca/Welcome.html
# I learned most of the tools to code what's inside from the following links
#   https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.findall
#   https://stackabuse.com/reading-and-writing-xml-files-in-python/
# Leandro Scholz 29.08.2018
# Information about the swc format
#   http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
"""
import xml.etree.ElementTree as ET
import numpy as np

def gxl2swc(swcPath):
        
    #read the file
	#TREE=ET.parse('D:\\Leandro\\MEGA\\MestradoPPGEQ\\NEUBIAS\\image2\\tree_structure.gxl')
    TREE = ET.parse(swcPath)
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

if __name__ == '__main__'
    import argparse

    # argument parser
    ap  = argparse.ArgumentParser()
    ap.add_argument("-f", "--file_path", required = True, help = "Path to image file")
    args = vars(ap.parse_args())

    # run gxl2swc
    gxl2swc(args['file_path'])