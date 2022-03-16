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
        self.whole_body = ['011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '032', '033', '177', '489']
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
        w1 = np.array([[dx, dy, 0.0], [dx, dy, 0.0], [dx, dy, 0.0]])
        w2 = np.array([[-dx, dy, 0.0], [-dx, dy, 0.0], [-dx, dy, 0.0]])
        w3 = np.array([[-dx, -dy, 0.0], [-dx, -dy, 0.0], [-dx, -dy, 0.0]])
        w4 = np.array([[dx, -dy, 0.0], [dx, -dy, 0.0], [dx, -dy, 0.0]])
        self.mv_wheel = [w1, w2, w3, w4]

        print("reading",file_name, ".....")
        with open(file_name, 'r') as stream:
            self.yaml_reader = yaml.safe_load(stream)
            self.yaml_reader = self.yaml_reader['shapes']


    def save_shape(self, mesh_list, name, is_wheel=False):
        if is_wheel:
            print("\nmaking:", name)
            start_vertex = 0
            wheel_list = ['336', '337', '347']
            for idx in range(len(mesh_list)):
                part_name = 'VIFS' + mesh_list[idx]
                for ch in range(len(self.yaml_reader)):
                    if self.yaml_reader[ch]['name'] == part_name:
                        print("adding:", part_name)
                        start_vertex += len(self.yaml_reader[ch]['vertices']['index'])
                        break
            start_vertex = int(start_vertex / 3)
            print("total vertices:",start_vertex)

            meshes = np.zeros(start_vertex, dtype=mesh.Mesh.dtype)
            mesh_idx = 0

            for iter in range(1):
                for idx in range(len(wheel_list)):
                    part_name = 'VIFS' + wheel_list[idx]
                    for ch in range(len(self.yaml_reader)):
                        if self.yaml_reader[ch]['name'] == part_name:
                            len_idx = int(len(self.yaml_reader[ch]['vertices']['index']) / 3)
                            vdx = self.yaml_reader[ch]['vertices']['index']  ## vertices_index
                            vpt = self.yaml_reader[ch]['vertices']['point']  ## vertices_point
                            for i in range(len_idx):
                                id0 = vdx[i*3 + 0]
                                id1 = vdx[i*3 + 1]
                                id2 = vdx[i*3 + 2]
                                point = np.array([[vpt[id0*3+0], vpt[id0*3+1], vpt[id0*3+2], 1.0],
                                                [vpt[id1*3+0], vpt[id1*3+1], vpt[id1*3+2], 1.0],
                                                [vpt[id2*3+0], vpt[id2*3+1], vpt[id2*3+2], 1.0]])
                                if wheel_list[idx] == '337':
                                    point = np.transpose(np.dot(self.T_w1, np.transpose(point)))
                                else:
                                    point = np.transpose(np.dot(self.T_c1, np.transpose(point)))
                                if wheel_list[idx] == '337':
                                    ttz = -0.052
                                    ttx = -0.02
                                    point[:, 0:3] += np.array([[ttx, 0.0, ttz], [ttx, 0.0, ttz], [ttx, 0.0, ttz]])
                                meshes['vectors'][mesh_idx + i] = point[:, 0:3]
                            mesh_idx += len_idx
                            break
                mesh_this = mesh.Mesh(meshes, remove_empty_areas=False)
                mesh_this.normals

            mesh_this.save('../data/modified_stl_files/'+str(name)+'.stl')

        else:
            print("\nmaking:", name)
            start_vertex = 0
            wheel_list = ['336', '337', '347']
            for idx in range(len(mesh_list)):
                part_name = 'VIFS' + mesh_list[idx]
                for ch in range(len(self.yaml_reader)):
                    if self.yaml_reader[ch]['name'] == part_name:
                        print("adding:", part_name)
                        start_vertex += len(self.yaml_reader[ch]['vertices']['index'])
                        break
            for idx in range(len(wheel_list)):
                part_name = 'VIFS' + wheel_list[idx]
                for ch in range(len(self.yaml_reader)):
                    if self.yaml_reader[ch]['name'] == part_name:
                        print("adding:", part_name)
                        start_vertex += len(self.yaml_reader[ch]['vertices']['index']) * 4
                        break

            start_vertex = int(start_vertex / 3)
            print("total vertices:",start_vertex)

            meshes = np.zeros(start_vertex, dtype=mesh.Mesh.dtype)
            mesh_idx = 0
            print('starting')
            for iter in range(1):
                for idx in range(len(mesh_list)):
                    part_name = 'VIFS' + mesh_list[idx]
                    for ch in range(len(self.yaml_reader)):
                        if self.yaml_reader[ch]['name'] == part_name:
                            len_idx = int(len(self.yaml_reader[ch]['vertices']['index']) / 3)
                            vdx = self.yaml_reader[ch]['vertices']['index']  ## vertices_index
                            vpt = self.yaml_reader[ch]['vertices']['point']  ## vertices_point
                            for i in range(len_idx):
                                id0 = vdx[i*3 + 0]
                                id1 = vdx[i*3 + 1]
                                id2 = vdx[i*3 + 2]
                                point = np.array([[vpt[id0*3+0], vpt[id0*3+1], vpt[id0*3+2], 1.0],
                                                [vpt[id1*3+0], vpt[id1*3+1], vpt[id1*3+2], 1.0],
                                                [vpt[id2*3+0], vpt[id2*3+1], vpt[id2*3+2], 1.0]])
                                point = np.transpose(np.dot(self.T_bd, np.transpose(point)))
                                meshes['vectors'][mesh_idx + i] = point[:, 0:3]
                            mesh_idx += len_idx
                            break

            for iter in range(4):
                for idx in range(len(wheel_list)):
                    part_name = 'VIFS' + wheel_list[idx]
                    for ch in range(len(self.yaml_reader)):
                        if self.yaml_reader[ch]['name'] == part_name:
                            len_idx = int(len(self.yaml_reader[ch]['vertices']['index']) / 3)
                            vdx = self.yaml_reader[ch]['vertices']['index']  ## vertices_index
                            vpt = self.yaml_reader[ch]['vertices']['point']  ## vertices_point
                            for i in range(len_idx):
                                id0 = vdx[i*3 + 0]
                                id1 = vdx[i*3 + 1]
                                id2 = vdx[i*3 + 2]
                                point = np.array([[vpt[id0*3+0], vpt[id0*3+1], vpt[id0*3+2], 1.0],
                                                [vpt[id1*3+0], vpt[id1*3+1], vpt[id1*3+2], 1.0],
                                                [vpt[id2*3+0], vpt[id2*3+1], vpt[id2*3+2], 1.0]])
                                if wheel_list[idx] == '337':
                                    point = np.transpose(np.dot(self.T_w1, np.transpose(point)))
                                else:
                                    point = np.transpose(np.dot(self.T_c1, np.transpose(point)))
                                point[:, 0:3] += self.mv_wheel[iter]
                                if wheel_list[idx] == '337':
                                    ttz = -0.052
                                    ttx = -0.02
                                    point[:, 0:3] += np.array([[ttx, 0.0, ttz], [ttx, 0.0, ttz], [ttx, 0.0, ttz]])
                                meshes['vectors'][mesh_idx + i] = point[:, 0:3]
                            mesh_idx += len_idx
                            break
                mesh_this = mesh.Mesh(meshes, remove_empty_areas=False)
                mesh_this.normals

            mesh_this.save('../data/modified_stl_files/'+str(name)+'.stl')

    def execute(self):
        self.save_shape(self.whole_body, "whole_body")
        self.save_shape(['336', '337', '347'], "whole_wheel",True)

if __name__ == '__main__':
    maker = StlModifier()
    maker.execute()
