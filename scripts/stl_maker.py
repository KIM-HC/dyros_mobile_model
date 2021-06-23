'''
Copyright 2021 Kim Hyoung Cheol. All rights reserved.
author: Kim Hyoung Cheol (KIM-HC)

makes stl file from yaml file
'''
from __future__ import print_function

import numpy as np
from stl import mesh
import yaml

class StlMaker(object):
    def __init__(self, file_name = '../data/aml_data/test_out.yaml'):
        self.overlap_names = ['childs', 'renders', 'devices']
        self.num_shape = 0
        self.writer = open('../data/aml_data/stl_info.yaml','w')
        self.writer2 = open('../data/aml_data/stl_info_no_vertex.yaml','w')
        self.tab = 2
        with open(file_name, 'r') as stream:
            self.yaml_reader = yaml.safe_load(stream)

    def _print_space(self, count):
        for _ in range(count * self.tab):
            self.writer.write(" ")

    def _print_space2(self, count):
        for _ in range(count * self.tab):
            self.writer2.write(" ")

    def save_shape(self, dict_now, name, r, R):
        print("\n--------\nshape name:",name)
        print('r:',r)
        print('R:',R)
        vdx = dict_now['vertices']['index']  ## vertices_index
        vpt = dict_now['vertices']['point']  ## vertices_point
        self._print_space(1)
        self._print_space2(1)
        self.writer.write("- name: " + str(name) + "\n")
        self.writer2.write("- name: " + str(name) + "\n")
        self._print_space(2)
        self._print_space2(2)
        self.writer.write("r: " + str(r) + "\n")
        self.writer2.write("r: " + str(r) + "\n")
        self._print_space(2)
        self._print_space2(2)
        self.writer.write("R: " + str(R) + "\n")
        self.writer2.write("R: " + str(R) + "\n")
        self._print_space(2)
        self.writer.write("vertices:\n")
        self._print_space(3)
        self.writer.write("index: " + str(vdx) + "\n")
        self._print_space(3)
        self.writer.write("point: " + str(vpt) + "\n")

        num_vertex = len(vdx)/3
        meshes = np.zeros(num_vertex, dtype=mesh.Mesh.dtype)
        for i in range(num_vertex):
            id0 = vdx[i*3 + 0]
            id1 = vdx[i*3 + 1]
            id2 = vdx[i*3 + 2]
            meshes['vectors'][i] = np.array([[vpt[id0*3+0], vpt[id0*3+1], vpt[id0*3+2]],
                                             [vpt[id1*3+0], vpt[id1*3+1], vpt[id1*3+2]],
                                             [vpt[id2*3+0], vpt[id2*3+1], vpt[id2*3+2]]])
        mesh_this = mesh.Mesh(meshes, remove_empty_areas=False)
        mesh_this.normals
        mesh_this.save('../data/stl_files/'+str(name)+'.stl')

    def execute(self):
        self._print_space(0)
        self.writer.write("shapes:\n")
        self.writer2.write("shapes:\n")
        self.dfs_search(self.yaml_reader)
        print("total number of shapes:",self.num_shape)

    def dfs_search(self,dict_now):
        for name in dict_now:
            if name == 'shape':
                self.save_shape(dict_now['shape']['geometry']['mesh'], dict_now['name'], dict_now['r'], dict_now['R'])
                self.num_shape += 1
            elif name in self.overlap_names:
                for i in range(len(dict_now[name])):
                    if type(dict_now[name][i]) is dict:
                        self.dfs_search(dict_now[name][i])
            else:
                if type(dict_now[name]) is dict:
                    self.dfs_search(dict_now[name])

if __name__ == '__main__':
    maker = StlMaker()
    maker.execute()
