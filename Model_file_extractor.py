#coding=utf-8
import sys
import os

sys.path.append("D:\Abaqus\download_address\win_b64\code\python2.7\lib")

from abaqus import *
from abaqusConstants import *

class ModelFileExtractor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model_data = {}
    
    # 提取模型所有信息
    def extract_all_info(self):
        mdb = openMdb(self.model_name)
        model = mdb.models['Model-1']
        self.model_data = {
            'model_name': model.name,
            'nodes': self._extract_nodes(model),
            "elements" : self._extract_elements(model),
            "materials" : self._extract_materials(model)
        }
        self._extract_sections(model)
        self._extract_materials(model)
        mdb.close()
        return self.model_data
    
    def show_db(self):
        with open("show.log", "w") as log:
            data = self.model_data
            log.write("="*50 + "\n")
            log.write("Model: {}\n".format(data['model_name']))
            log.write("="*50 + "\n")

            # 打印节点
            for data_key in data["nodes"].keys():
                data_val = data["nodes"][data_key]
                if len(data_val) == 0:
                    log.write("node empty")
                else:
                    for node_info in data_val:
                        log.write("lable = {}; coord = {}; instance = {}\n".format(str(node_info["label"]), str(node_info["coordinates"]), str(node_info["instance"])))



    # 提取节点信息
    def _extract_nodes(self, model):
        nodes_info = {}
        assembly = model.rootAssembly
        
        for instance_name, instance in assembly.instances.items():
            nodes = instance.nodes
            nodes_info[instance_name] = []
            
            for node in nodes:
                nodes_info[instance_name].append({
                    'label': node.label,
                    'coordinates': node.coordinates,
                    'instance': instance_name
                })
        return nodes_info
    
    # 提取单元信息
    def _extract_elements(self, model):
        elements_info = {}
        assembly = model.rootAssembly
        
        for instance_name, instance in assembly.instances.items():
            elements = instance.elements
            elements_info[instance_name] = []
            
            for element in elements:
                # 临时代码
                with open("test.log", "w") as log:
                    log.write("type(element.label):{}\n".format(str(type(element.label))))
                    log.write("type(element.type):{}\n".format(str(type(element.type))))
                    log.write("type(element.elem_nodes):{}\n".format(str(type(element.connectivity))))
                    log.write("element.type = {}\n".format(element.type))
                    log.write("element.elem_nodes = {}\n".format(element.connectivity))
                    # log.write("type(element.section):{}\n".format(str(type(element.section))))
                    
                elements_info[instance_name].append({
                    'label': element.label,
                    'type': element.type,
                    'elem_nodes': element.connectivity,
                })
        return elements_info
    
    def _extract_sections(self, model):
        sections = model.sections
        with open("section_test.log", "w") as log:
            log.write("key type -> {};\n".format(str(type(sections))))
            for k, v in sections.items():
                log.write("key type -> {}; \n".format(str(type(k))))
                log.write("key      -> {}; \n".format(k))
                log.write("val type -> {}; \n".format(str(type(v))))
                log.write("val      -> {}; \n".format(v))
                log.write("materil  -> {}; \n".format(v.material))
    
    def _extract_materials(self, model):
        materials_info = {}
        
        materials = model.materials
        for mat_name, mat_val in materials.items():
            mat_data = {}
            mat_data["E"] = mat_val.elastic.table[0][0]
            mat_data["NU"] = mat_val.elastic.table[0][1]
            materials_info[mat_name] = mat_data
        
        # 临时代码 
        # materials = model.materials
        # with open("material_test.log", "w") as log:
        #     for mat_name, mat_val in materials.items():
        #         log.write("name -> {}\n".format(mat_name))
        #         log.write("value-> {}\n".format(mat_val))
        #         log.write("mat_data-> {}\n".format(mat_val.elastic.table))

        return materials_info