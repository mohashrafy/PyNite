## -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""
from PyNite import FEModel3D, Visualization
import itertools
import os, csv
from Examples.large_grid_frame import inputfiles

# Constants for the member properties
E, G, Iy, Iz, J, A = 30*10**6, 12*10**6, 0.00100, 0.00100, 50, 0.010

# Initialize the model
model = FEModel3D()

# Import nodes from file
path = os.path.join(os.path.dirname(__file__), 'gridnodes.csv')
nodes_list = inputfiles.nodes_from_csv(path)

# Add the nodes to the model
for node in nodes_list:
    model.add_node(*node)

# Import members from file
path = os.path.join(os.path.dirname(__file__), 'gridmembers.csv')
member_list = inputfiles.read_csv(path)

# Add the members to the model
for member in member_list:
    Name, i_node, j_node = member
    model.add_member(Name, i_node, j_node, E, G, Iy, Iz, J, A)

# Import supports from file
path = os.path.join(os.path.dirname(__file__), 'gridsupports.csv')
support_list = inputfiles.read_dict_from_csv(path)
for row in support_list:
    model.def_support(**row)

# Import node loads from file
path = os.path.join(os.path.dirname(__file__), 'gridnodesloads.csv')
node_loads = inputfiles.read_csv(path)
for load in node_loads:
    Node, Direction, P = load
    # Add node loads
    model.add_node_load(Node, Direction, float(P))

# Analyze the model
model.analyze(check_statics=True)

# Render the model
Visualization.RenderModel(model,
                          deformed_shape=True,
                          text_height=0.25,
                          render_loads=True)
