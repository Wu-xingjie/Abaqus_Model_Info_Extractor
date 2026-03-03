#coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.curdir))
# sys.path.append("D:\FEA_solver\Abaqus_Model_Info_Extractor")
import Model_file_extractor
import tool

class GenSolverInput:
    def __init__(self, extractor):
        self._model_info = extractor.getModelData()
    
    # 生成求解器计算文件
    def GenInput(self):
        input_string = []
        # 生成节点
        node_list = self.GenNodeInfo()
        input_string.extend(node_list)
        # 生成单元
        elem_list= self.GenElemInfo()
        input_string.extend(elem_list)
        # 生成材料
        mat_list = self.GenMatInfo()
        input_string.extend(mat_list)
        # 生成属性
        props_list = self.GenPropertyInfo()
        input_string.extend(props_list)

        input_dir = os.path.abspath(os.curdir)
        input_path = os.path.join(input_dir, "sovler.input")
        with open(input_path, "w") as input:
            input.writelines(input_string)

    # 生成属性信息
    def GenPropertyInfo(self):
        input_string = []
        properties_info = self._model_info["sections"]
        for section_name, section_val in properties_info.items():
            sec_id = tool.GetItemId(section_name)
            mat_id = tool.GetItemId(section_val["material"])
            input_string.append("PSOLID,{},{}".format(sec_id, mat_id))
        return input_string

    # 生成材料信息
    def GenMatInfo(self):
        input_string = []
        materials_info = self._model_info["materials"]
        for mat_name, mat_val in materials_info.items():
            mat_id = tool.GetItemId(mat_name)
            input_string.append("MAT1,{},{},{}\n".format(mat_id, mat_val["E"], mat_val["NU"]))
        return input_string

    # 生成单元信息
    def GenElemInfo(self):
        input_string = []
        elems_info = self._model_info["elements"]
        for key, elems in elems_info.items():
            for elem in elems:
                pid = elem["prop_id"]
                lab = elem["label"]
                elem_type = ""
                if type == "C3D8R":
                    elem_type = "CHEXA8"
                input_string.append("CHEXA8,{},{},{},{},{},{},{},{},{}\ncontinue,{}\n".format(lab, pid, \
                                                                    elem["elem_nodes"][0],\
                                                                    elem["elem_nodes"][1],\
                                                                    elem["elem_nodes"][2],\
                                                                    elem["elem_nodes"][3],\
                                                                    elem["elem_nodes"][4],\
                                                                    elem["elem_nodes"][5],\
                                                                    elem["elem_nodes"][6],\
                                                                    elem["elem_nodes"][7]))

        # for data_key in elems_info.keys():
        #     data_val = elems_info[data_key]
        #     if len(data_val) == 0:
        #         input_string.append("node empty")
        #     else:
        #         for node in data_val:
        #             nid = node["label"]
        #             x_val = node["coordinates"][0]
        #             y_val = node["coordinates"][1]
        #             z_val = node["coordinates"][2]
        #             input_string.append("GRID,{},,{},{},{}\n".format(str(nid), str(x_val), str(y_val), str(z_val)))
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