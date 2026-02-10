#coding=utf-8
import Model_file_extractor

if __name__ == "__main__":
    # 创建提取器
    extractor = Model_file_extractor.ModelFileExtractor(r'D:\Abaqus\download_address\temp\test')
    
    # 提取所有信息
    model_data = extractor.extract_all_info()
    
    # 打印摘要
    # extractor.print_summary()
    
    # # 保存为JSON
    # extractor.save_to_json('model_info.json')