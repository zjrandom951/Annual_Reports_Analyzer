from functions import read_and_process_xlsx, generate_url_table, download_pdfs_from_excel, create_frequency_table



if __name__ == "__main__":
    # 示例代码
    company_codes = read_and_process_xlsx("codes.xlsx", "证券代码")  # 假设给定公司代码列表
    all_years = list(map(str, range(2016, 2022)))  # 生成年份列表，从2016年到2021年
    generate_url_table(company_codes, start_year=2016, end_year=2021, url_table_path="url_table.xlsx")
    
    # 下载所有PDF文件并保存到本地
    download_pdfs_from_excel('url_table.xlsx', folder_name="pdf_files")

    feature_words = [
        "人工智能", "商业智能", "图像理解", "投资决策辅助系统", "智能数据分析", "智能机器人", "机器学习", "深度学习",
        "语义搜索", "生物识别技术", "人脸识别", "语音识别", "身份验证", "大数据", "数据挖掘", "文本挖掘", "数据可视化",
        "异构数据", "征信", "增强现实", "云计算", "流计算", "图计算", "内存计算", "多方安全计算", "类脑计算", "绿色计算",
        "认知计算", "融合架构", "亿级并发", "EB级存储", "物联网", "信息物理系统", "区块链", "数字货币", "分布式计算",
        "差分隐私技术", "智能金融合约", "移动互联网", "工业互联网", "移动互联", "互联网医疗", "电子商务", "移动支付",
        "第三方支付", "NFC支付", "智能能源", "B2B", "B2C", "C2B", "C2C", "O2O", "网联", "智能穿戴", "智慧农业",
        "智能交通", "智能医疗", "智能客服", "智能家居", "智能投顾", "智能文旅", "智能环保", "智能电网", "智能营销",
        "数字营销", "无人零售", "互联网金融", "数字金融", "Fintech", "金融科技", "量化金融", "开放银行"
    ]
    
    root_folder = 'pdf_files'

    # 创建表格
    frequency_table = create_frequency_table(root_folder, feature_words)



