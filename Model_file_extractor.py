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
            'nodes': self._extract_nodes(model)
        }
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
    
    def _extract_nodes(self, model):
        """提取节点信息"""
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
    
