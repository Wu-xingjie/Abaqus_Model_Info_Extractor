#coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.curdir))
# sys.path.append("D:\FEA_solver\Abaqus_Model_Info_Extractor")
import Model_file_extractor
import tool

class GenSolverInput:
    def __init__(self, extractor):
        self._model_info = extractor.extract_all_info()
    
    # 生成求解器计算文件
    def GenInput(self):
        input_string = []
        # 生成节点
        node_list = self.GenNodeInfo()
        input_string.extend(node_list)
        # 生成材料
        mat_list = self.GenMatInfo()
        input_string.extend(mat_list)

        input_dir = os.path.abspath(os.curdir)
        input_path = os.path.join(input_dir, "sovler.input")
        with open(input_path, "w") as input:
            input.writelines(input_string)

    # 生成材料信息
    def GenMatInfo(self):
        input_string = []
        materials_info = self._model_info["materials"]
        for mat_name, mat_val in materials_info.items():
            mat_id = tool.GetItemId(mat_name)
            input_string.append("MAT1,{},{},{}\n".format(mat_id, mat_val["E"], mat_val["NU"]))
        return input_string

    # 生成节点信息
    def GenNodeInfo(self):
        input_string = []
        nodes_info = self._model_info["nodes"]
        for data_key in nodes_info.keys():
            data_val = nodes_info[data_key]
            if len(data_val) == 0:
                input_string.append("node empty")
            else:
                for node in data_val:
                    nid = node["label"]
                    x_val = node["coordinates"][0]
                    y_val = node["coordinates"][1]
                    z_val = node["coordinates"][2]
                    input_string.append("GRID,{},,{},{},{}\n".format(str(nid), str(x_val), str(y_val), str(z_val)))
        return input_string