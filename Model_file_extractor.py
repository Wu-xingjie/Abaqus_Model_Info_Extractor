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
        self.model_data["model_name"] = model.name
        # 截面指派抓取需要放在单元抓取之前
        self.model_data["assignments"] = self._extract_section_assignments(model)
        self.model_data["nodes"] = self._extract_nodes(model)
        self.model_data["elements"] = self._extract_elements(model)
        self.model_data["sections"] = self._extract_sections(model)
        self.model_data["materials"] = self._extract_materials(model)
        mdb.close()
    
    def getModelData(self):
        self.extract_all_info()
        return self.model_data
    
    def show_db(self):
        with open("show.log", "w") as log:
            data = self.model_data
            # 打印节点
            for data_key in data["nodes"].keys():
                data_val = data["nodes"][data_key]
                if len(data_val) == 0:
                    log.write("node empty")
                else:
                    for node_info in data_val:
                        log.write("lable = {}; coord = {}; instance = {}\n".format(str(node_info["label"]), str(node_info["coordinates"]), str(node_info["instance"])))

    # 获取截面指派信息
    def _extract_section_assignments(self, model):
        all_assignments = []
        with open("assign.log", "w") as log:
            # 遍历部件中截面指派信息
            for part_name, part in model.parts.items():
                if hasattr(part, 'sectionAssignments') and part.sectionAssignments:
                    for i, assignment in enumerate(part.sectionAssignments):
                        # 获取指派信息
                        sec_name = assignment.sectionName
                        
                        # 通过截面名称获取截面对象
                        section = model.sections[sec_name]
                        material_name = None
                        if section and hasattr(section, 'material'):
                            material_name = section.material
                        # 整理信息

                        log.write("assignment -> {}\n".format(assignment))
                        
                        assign_info = {
                            'location': 'part',
                            'part_name': part_name,
                            'assignment_index': i,
                            'section_name': sec_name,
                            'material_name': material_name,
                            'region': assignment.region,  # 这是一个Set对象
                            'suppressed': assignment.suppressed,
                        }
                        all_assignments.append(assign_info)
                        
            # 整理all_assignments中section_name和part_name信息
            part_sec_pairs = {}
            for assign in all_assignments:
                part_sec_pairs[assign["part_name"]] = assign["material_name"]
            for part_name, mat_name in part_sec_pairs.items():
                log.write("{} -> {}\n".format(part_name, mat_name))
        return all_assignments
    
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
                with open("element_test.log", "w") as log:
                    log.write("type(element.label):{}\n".format(str(type(element.label))))
                    log.write("type(element.type):{}\n".format(str(type(element.type))))
                    log.write("type(element.elem_nodes):{}\n".format(str(type(element.connectivity))))
                    log.write("element.type = {}\n".format(element.type))
                    log.write("element.elem_nodes = {}\n".format(element.connectivity))
                    log.write("element = {}\n".format(element))

                elements_info[instance_name].append({
                    # 暂时写死
                    'prop_id': 1,
                    'label': element.label,
                    'type': element.type,
                    'elem_nodes' : element.connectivity,
                })
                # 获取单元属性
                
        return elements_info
    
    def _extract_sections(self, model):
        sections_info = {}
        sections = model.sections
        for sec_key, sec_val in sections.items():
            temp_section = {}
            temp_section["material"] = sec_val.material
            temp_section["thickness"] = sec_val.thickness
            sections_info[sec_val.name] = temp_section   
        return sections_info
    
    def _extract_materials(self, model):
        materials_info = {}
        materials = model.materials
        for mat_name, mat_val in materials.items():
            mat_data = {}
            mat_data["E"] = mat_val.elastic.table[0][0]
            mat_data["NU"] = mat_val.elastic.table[0][1]
            materials_info[mat_name] = mat_data
        with open("mat_test.log", "w") as log:
            for mat_name, mat in materials_info.items():
                log.write("mat_name : {}".format(mat_name))
        return materials_info