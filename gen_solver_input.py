#coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.curdir))
# sys.path.append("D:\FEA_solver\Abaqus_Model_Info_Extractor")
import Model_file_extractor

class GenSolverInput:
    def __init__(self, extractor):
        self._extractor = extractor
    
    # 生成求解器计算文件
    def GenInput(self):
        input_string = []
        # 生成节点
        input_list = self.GenNodeInfo()
        input_string.extend(input_list)

        input_dir = os.path.abspath(os.curdir)
        input_path = os.path.join(input_dir, "sovler.input")
        with open(input_path, "w") as input:
            input.writelines(input_string)

    # 生成节点信息
    def GenNodeInfo(self):
        input_string = []
        model_data = self._extractor.extract_all_info()
        nodes_info = model_data["nodes"]
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