'''
Copyright 2021 Kim Hyoung Cheol. All rights reserved.
author: Kim Hyoung Cheol (KIM-HC)

makes modified stl file from stl_info.yaml
'''
from __future__ import print_function

import numpy as np
from stl import mesh
import yaml

class StlModifier(object):
    def __init__(self, file_name = '../data/aml_data/stl_info.yaml'):
        self.body_side = ['011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '032', '033']
        self.body_bottom = ['177']
        self.body_top = ['489']
        T_bd_outer = np.array([[1.0, 0.0, 0.0, 0.0],
                               [0.0, 0.0, -1.0, 0.0],
                               [0.0, 1.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0, 1.0]])
        T_bd_inner = np.array([[1.0, 0.0, 0.0, 0.0],
                               [0.0 ,1.0 ,0.0, 0.0],
                               [0.0, 0.0 ,1.0, 0.0],
                               [0.0, 0.0, 0.0, 1.0]])
        self.T_bd = np.dot(T_bd_outer, T_bd_inner)

        T_c1_outer = np.array([[1.0, 0.0, 0.0, 0.0195],
                               [0.0, 1.0, 0.0, 0.025],
                               [0.0, 0.0, 1.0, 0.0],
                               [0.0, 0.0, 0.0, 1.0]])
        T_c1_inner = np.array([[-0.642843, 0.0, 0.765998, 0.2145],
                               [0.765998, 0.0, 0.642843, -0.10935],
                               [0.0, 1.0, 0.0, 9.17912e-10],
                               [0.0, 0.0, 0.0, 1.0]])
        self.T_c1 = np.dot(T_c1_outer, T_c1_inner)

        self.T_w1 = np.array([[-0.642843, 0.0, 0.765998, 0.254],
                              [0.765998, 0.0, 0.642843, -0.08435],
                              [0.0, 1.0, 0.0, 0.052],
                              [0.0, 0.0, 0.0, 1.0]])

        print("T_bd:\n", self.T_bd)
        print("T_c1:\n", self.T_c1)
        print("T_w1:\n", self.T_w1)

        dx = 0.215
        dy = 0.125
        self.move_wheel = np.array([[-dx, -dy, 0], [-dx, -dy, 0], [-dx, -dy, 0]])
        zeros = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        w1 = np.array([[dx, dy, 0.0], [dx, dy, 0.0], [dx, dy, 0.0]])
        w2 = np.array([[-dx, dy, 0.0], [-dx, dy, 0.0], [-dx, dy, 0.0]])
        w3 = np.array([[-dx, -dy, 0.0], [-dx, -dy, 0.0], [-dx, -dy, 0.0]])
        w4 = np.array([[dx, -dy, 0.0], [dx, -dy, 0.0], [dx, -dy, 0.0]])
        self.mv_wheel = [zeros, w1, w2, w3, w4]

        print("reading",file_name, ".....")
        with open(file_name, 'r') as stream:
            self.yaml_reader = yaml.safe_load(stream)
            self.yaml_reader = self.yaml_reader['shapes']


    def save_shape(self, mesh_list, name, is_wheel=False):
        print("\nmaking:", name)
        num_do = 1
        if is_wheel:
            num_do = 1
        start_vertex = 0
        for idx in range(len(mesh_list)):
            part_name = 'VIFS' + mesh_list[idx]
            for ch in range(len(self.yaml_reader)):
                if self.yaml_reader[ch]['name'] == part_name:
                    print("adding:", part_name)
                    start_vertex += len(self.yaml_reader[ch]['vertices']['index'])
                    break

        start_vertex = start_vertex / 3
        print("total vertices:",start_vertex)

        for iter in range(num_do):
            meshes = np.zeros(start_vertex, dtype=mesh.Mesh.dtype)
            mesh_idx = 0
            for idx in range(len(mesh_list)):
                part_name = 'VIFS' + mesh_list[idx]
                for ch in range(len(self.yaml_reader)):
                    if self.yaml_reader[ch]['name'] == part_name:
                        len_idx = len(self.yaml_reader[ch]['vertices']['index']) / 3
                        vdx = self.yaml_reader[ch]['vertices']['index']  ## vertices_index
                        vpt = self.yaml_reader[ch]['vertices']['point']  ## vertices_point
                        for i in range(len_idx):
                            id0 = vdx[i*3 + 0]
                            id1 = vdx[i*3 + 1]
                            id2 = vdx[i*3 + 2]
                            point = np.array([[vpt[id0*3+0], vpt[id0*3+1], vpt[id0*3+2], 1.0],
                                              [vpt[id1*3+0], vpt[id1*3+1], vpt[id1*3+2], 1.0],
                                              [vpt[id2*3+0], vpt[id2*3+1], vpt[id2*3+2], 1.0]])
                            if is_wheel:
                                if mesh_list[idx] == '337':
                                    point = np.transpose(np.dot(self.T_w1, np.transpose(point)))
                                else:
                                    point = np.transpose(np.dot(self.T_c1, np.transpose(point)))
                                point[:, 0:3] += self.mv_wheel[iter]

                            else:
                                point = np.transpose(np.dot(self.T_bd, np.transpose(point)))

                            meshes['vectors'][mesh_idx + i] = point[:, 0:3]

                        mesh_idx += len_idx
                        break

            mesh_this = mesh.Mesh(meshes, remove_empty_areas=False)
            mesh_this.normals
            if is_wheel:
                if iter == 0:
                    mesh_this.save('../data/modified_stl_files/base_wheel_'+str(name)+'.stl')
                else:
                    mesh_this.save('../data/modified_stl_files/wheel_'+str(iter)+'_'+str(name)+'.stl')
            else:
                mesh_this.save('../data/modified_stl_files/'+str(name)+'.stl')

    def execute(self):
        self.save_shape(self.body_side, "body_side")
        self.save_shape(self.body_bottom, "body_bottom")
        self.save_shape(self.body_top, "body_top")

        self.save_shape(['347', '336'], "body", True)
        self.save_shape(['337'], "rotate", True)


if __name__ == '__main__':
    maker = StlModifier()
    maker.execute()
