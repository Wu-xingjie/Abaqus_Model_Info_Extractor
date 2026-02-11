#coding=utf-8
import Model_file_extractor
import gen_solver_input

if __name__ == "__main__":
    # 创建提取器
    extractor = Model_file_extractor.ModelFileExtractor(r'D:\Abaqus\download_address\temp\test')
    
    # 创建转换器
    transfer = gen_solver_input.GenSolverInput(extractor)

    transfer.GenInput()

    # extractor.show_db()