'''
Copyright 2021 Kim Hyoung Cheol. All rights reserved.
author: Kim Hyoung Cheol (KIM-HC)

reads aml file and saves it in dictionary
'''
from __future__ import print_function

class AmlReader(dict):
    def __init__(self, file_path):
        self.overlap_names = []
        self.no_print_names = ['index', 'point']
        self.to_int = ['index']
        self.to_float = ['R', 'r', 'point', 'specular', 'diffuse', 'scale', 'translation', 'center', 'rotation', 'transparency', 'ambient']
        self.tab = 2

        self.stack = []
        self.current_dict = self
        self.new_name = ''
        self.new_input_name = ''
        self.new_dict = False
        self.new_input = False
        self.xml_start = False
        self.writer = open('../data/aml_data/test_out.yaml','w')
        print("reading ", file_path)
        self._read_aml(file_path)

    def _print_space(self, count):
        for i in range(count * self.tab):
            if i % self.tab == 0:
                print("|",sep='',end='')
                self.writer.write(" ")
            else:
                print(" ",sep='',end='')
                self.writer.write(" ")

    def _print_dict(self, dict_now, count):
        for name in dict_now:
            if name in self.overlap_names:
                self._print_space(count)
                print('- ',name,'s',sep='')
                self.writer.write(name + "s: \n")
                if type(dict_now[name]) is list:
                    for i in range(len(dict_now[name])):
                        self._print_space(count + 1)
                        if type(dict_now[name][i]) is dict:
                            print('-',i+1,name)
                            self.writer.write("- \n")
                            self._print_dict(dict_now[name][i], count + 2)
                        else:
                            if name in self.no_print_names:
                                if len(dict_now[name][i]) == 1:
                                    print('-',i+1, name,dict_now[name][i][0])
                                    self.writer.write("- " + str(dict_now[name][i][0]) + "\n")
                                else:
                                    print('-',i+1, name,'...')
                                    self.writer.write("- " + str(dict_now[name][i]) + "\n")
                            else:
                                if len(dict_now[name][i]) == 1:
                                    print('-',i+1, name,dict_now[name][i][0])
                                    self.writer.write("- " + str(dict_now[name][i][0]) + "\n")
                                else:
                                    print('-',i+1, name,dict_now[name][i])
                                    self.writer.write("- " + str(dict_now[name][i]) + "\n")
                else:
                    self._print_space(count + 1)
                    if type(dict_now[name]) is dict:
                        print('-',name)
                        self.writer.write("- \n")
                        self._print_dict(dict_now[name], count + 2)
                    else:
                        print("==========\nERROR\n============\n==========\nERROR\n============\n==========\nERROR\n============\n")
            else:
                self._print_space(count)
                if type(dict_now[name]) is dict:
                    print('-',name)
                    self.writer.write(name + ": \n")
                    self._print_dict(dict_now[name], count + 1)
                else:
                    if name in self.no_print_names:
                        if len(dict_now[name]) == 1:
                            print('-', name, dict_now[name][0])
                            self.writer.write(name + ": " + str(dict_now[name][0]) + "\n")
                        else:
                            print('-', name,'...')
                            self.writer.write(name + ": " + str(dict_now[name]) + "\n")
                    else:
                        if len(dict_now[name]) == 1:
                            print('-', name, dict_now[name][0])
                            self.writer.write(name + ": " + str(dict_now[name][0]) + "\n")
                        else:
                            print('-', name, dict_now[name])
                            self.writer.write(name + ": " + str(dict_now[name]) + "\n")

    def __get_current_dict(self):
        self.current_dict = self
        for name in self.stack:
            if type(self.current_dict[name]) is list:
                self.current_dict = self.current_dict[name][-1]
            else:
                self.current_dict = self.current_dict[name]

    def __reset_reading(self):
        self.new_name = ''
        self.new_dict = False
        self.new_input = False
        self.__get_current_dict()

    def _read_aml(self, file_path):    
        reader = open(file_path, 'r')
        lines = reader.readlines()

        for line in lines:
            for char in line:
                ## end of dictionary
                if char == '/' and not self.new_input:
                    self.stack.pop()
                    self.__reset_reading()
                    break
                
                ## start and end of xml information
                elif char == '?':
                    if self.xml_start:
                        self.xml_start = False
                        self.stack.pop()
                        self.__reset_reading()
                        break
                    else:
                        self.__reset_reading()
                        self.new_dict = True
                        self.xml_start = True

                ## if between "" -> add for .split()
                elif (char == ' ' or char == '/') and self.new_input:
                    if char == ' ' and (self.new_input_name == "name"):
                        self.new_name += '_'
                    else:
                        self.new_name += char

                elif (char == ' ' or char == '>') and self.new_dict:
                    self.stack.append(self.new_name)
                    if self.current_dict.has_key(self.new_name):
                        if type(self.current_dict[self.new_name]) is dict:
                            backup = self.current_dict[self.new_name]
                            self.current_dict[self.new_name] = [backup]
                            if self.new_name not in self.overlap_names:
                                self.overlap_names.append(self.new_name)
                        self.current_dict[self.new_name].append({})
                    else:
                        if self.new_name in self.overlap_names:
                            self.current_dict[self.new_name] = [{}]
                        else:
                            self.current_dict[self.new_name] = {}
                    self.__reset_reading()

                elif char == ' ' or char == '>': pass

                ## start of line and dictionary
                elif char == '<':
                    self.__reset_reading()
                    self.new_dict = True

                ## start of value of new_input_name
                elif char == '=':
                    self.new_input_name = self.new_name
                    self.__reset_reading()

                ## start and end of new_input_value
                elif char == '"':
                    if self.new_input:
                        if self.new_input_name in self.to_int:
                            int_list = []
                            for val in self.new_name.split():
                                int_list.append(int(val))
                            self.current_dict[self.new_input_name] = int_list
                        elif self.new_input_name in self.to_float:
                            float_list = []
                            for val in self.new_name.split():
                                float_list.append(float(val))
                            self.current_dict[self.new_input_name] = float_list
                        elif self.new_input_name == "name":
                            self.current_dict[self.new_input_name] = self.new_name
                        else:
                            self.current_dict[self.new_input_name] = self.new_name.split()
                        self.__reset_reading()
                    else:
                        self.__reset_reading()
                        self.new_input = True

                ## add other characters
                else:
                    self.new_name += char
        reader.close()
        self._print_dict(dict_now=self, count=0)
        print('overlaped names:', self.overlap_names)

if __name__ == "__main__":
    reader = AmlReader(file_path='../data/aml_data/AllegroBaseOMNI_Virtual.aml')
