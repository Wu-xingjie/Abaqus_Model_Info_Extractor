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
        # 提取所有模型信息
        mdb = openMdb(self.model_name)
        model = mdb.models['Model-1']
        
        self.model_data = {
            'model_name': model.name,
            'nodes': self._extract_nodes(model)
        }
        
        mdb.close()
        return self.model_data
    
    def _extract_nodes(self, model):
        """提取节点信息"""
        nodes_info = {}
        assembly = model.rootAssembly
        
        for instance_name, instance in assembly.instances.items():
            nodes = instance.nodes
            nodes_info[instance_name] = {
                'count': len(nodes),
                'nodes': []
            }
            
            for node in nodes:
                nodes_info[instance_name]['nodes'].append({
                    'label': node.label,
                    'coordinates': node.coordinates,
                    'instance': instance_name
                })
        
        return nodes_info
    
