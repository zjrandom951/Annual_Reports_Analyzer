import PyPDF2
import jieba
import re
import os
import requests
import pandas as pd
from crawl_single_company import crawl_and_process

def read_and_process_xlsx(file_path, column_name):
    # 读取xlsx文件
    df = pd.read_excel(file_path, engine='openpyxl')

    # 提取名为column_name的列的所有元素
    extracted_data = df[column_name].tolist()

    # 将所有提取的数字转换为6位长度字符串
    formatted_data = [str(code).zfill(6) for code in extracted_data]

    return formatted_data

# 生成表格数据
def generate_url_table(company_codes, start_year=2016, end_year=2021, url_table_path = "url_table.xlsx"):
    # 构造表格数据
    url_table_data = []
    all_years = list(map(str, range(2016, 2022)))
    for code in company_codes:
        years, urls = crawl_and_process(code, start_year, end_year)  # 调用crawl_and_process函数，获取年份和URL链接列表
        url_dict = dict(zip(years, urls))  # 将年份和URL链接合并成一个字典
        row_data = []
        for year in all_years:
            url = url_dict.get(year, '')  # 获取对应年份的URL链接，如果没有则填充空字符串
            row_data.append(url)
            print(url)
        url_table_data.append(row_data)

    # 构造表格并输出
    df = pd.DataFrame(url_table_data, index=company_codes, columns=all_years)
    df.to_excel(url_table_path)

def download_pdf(url, file_path):
    """
    下载PDF文件并保存到本地文件。
    """
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def download_pdfs_from_excel(excel_path, folder_name = "pdf_files"):
    """
    根据给定的Excel文件路径，将其中所有PDF文件下载到本地pdf_files文件夹中。
    """
    # 读取Excel文件，并将第一列作为索引列
    df = pd.read_excel(excel_path, index_col=0)

    # 创建pdf_files文件夹（如果不存在）
    
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # 遍历每个公司代码和每个年份的URL链接，并下载PDF文件
    for code, row in df.iterrows():
        code_str = f"{code:0>6}"  # 将公司代码转换为6位字符串，并在不足6位时在前面补0
        sub_folder_name = folder_name + '/' + code_str
        if not os.path.exists(sub_folder_name):
            os.mkdir(sub_folder_name)
        for year, url in row.iteritems():
            if pd.notna(url):
                file_name = f"{year}.pdf"
                file_path = sub_folder_name + '/' + file_name
                if os.path.exists(file_path):
                    print(f"{file_path} already exists")
                else:
                    download_pdf(url, file_path)
                    print(f"{file_path} downloaded")
            else:
                print(f"No URL for {year} of {code_str}")
    
def calculate_feature_word_frequency(pdf_file, feature_words):
    try:
        # 读取 PDF 文件
        with open(pdf_file, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            # 查找符合模式的部分
            start_page, end_page = None, None
            num_pages = min(5, len(pdf_reader.pages))
            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                content = page_obj.extract_text()

                if start_page is None:
                    start_match = re.search(r'第三节.*?(\d+)', content)
                    if start_match:
                        start_page = int(start_match.group(1)) - 1

                if end_page is None:
                    end_match = re.search(r'第四节.*?(\d+)', content)
                    if end_match:
                        end_page = int(end_match.group(1)) - 1

                if start_page is not None and end_page is not None:
                    break

            # 提取指定范围内的PDF文本
            if start_page is not None and end_page is not None:
                text = ""
                for page in range(start_page, end_page):
                    page_obj = pdf_reader.pages[page]
                    text += page_obj.extract_text()
            else:
                text = ""
                start_page, end_page = 10, min(31, len(pdf_reader.pages))
                for page in range(start_page, end_page):
                    page_obj = pdf_reader.pages[page]
                    text += page_obj.extract_text()

        # 统计特征词出现的次数
        feature_word_count = sum(text.count(word) for word in feature_words)

        # 对文本进行分词
        words = list(jieba.cut(text))

        # 过滤掉非汉字词汇（如数字、字母、标点等）
        filtered_words = [word for word in words if all(u'\u4e00' <= char <= u'\u9fff' for char in word)]

        # 去除常用词（可根据需要添加其他常用词）
        common_words = ['的', '是', '和', '了', '在', '有', '这', '一个', '为', '我']
        filtered_words = [word for word in filtered_words if word not in common_words]

        # 计算总词数
        total_word_count = len(filtered_words)
        # 计算特征词频率
        
        feature_word_frequency = feature_word_count / total_word_count if total_word_count > 0 else 0

        feature_word_frequency = feature_word_frequency * 1000

        print(feature_word_frequency)
        return feature_word_frequency
        
    except Exception as e:
        print(f"Error while processing {pdf_file}: {e}")
        return 0.0


def create_frequency_table(root_folder, feature_words, start_company_code=None, save_path = "frequency_table.xlsx"):
    company_codes = []
    years = list(range(2016, 2022))
    
    # 获取公司代码列表
    for item in os.listdir(root_folder):
        if os.path.isdir(os.path.join(root_folder, item)):
            company_codes.append(item)

    # 如果文件已存在，则从文件中读取表格
    if os.path.isfile(save_path):
        frequency_table = pd.read_excel(save_path)
    else:
        # 初始化 DataFrame
        data = {'Company_Code': company_codes}
        for year in years:
            data[str(year)] = [0.0] * len(company_codes)
        frequency_table = pd.DataFrame(data)

    # 确定从哪个公司开始计算
    if start_company_code:
        start_index = company_codes.index(start_company_code)
    else:
        start_index = 0

    # 遍历公司文件夹，计算频率
    for index, company_code in enumerate(company_codes[start_index:], start=start_index):
        company_folder = os.path.join(root_folder, company_code)
        print(company_code)
        for year in years:
            pdf_file = os.path.join(company_folder, f'{year}.pdf')
            if os.path.isfile(pdf_file):
                frequency = calculate_feature_word_frequency(pdf_file, feature_words)
                frequency_table.at[index, str(year)] = frequency
        
        # 每计算5个公司保存表格到 xlsx 文件
        if index % 5 == 0:
            frequency_table.to_excel('frequency_table.xlsx', index=False)

    frequency_table.to_excel('frequency_table.xlsx', index=False)

if __name__ == "__main__":
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
    # # 测试url表格能否正常生成
    # company_codes = read_and_process_xlsx("codes.xlsx", "证券代码")  # 假设给定公司代码列表
    # all_years = list(map(str, range(2016, 2022)))  # 生成年份列表，从2016年到2021年
    # generate_url_table(company_codes, start_year=2016, end_year= 2022, url_table_path="url_table.xlsx")

    # # 下载所有PDF文件并保存到本地
    # download_pdfs_from_excel('url_table.xlsx', folder_name="pdf_files")

    # 计算词频

    feature_word_frequency = calculate_feature_word_frequency(r'pdf_files\000008\2016.pdf', feature_words)

    # # 计算所有文件的词频，保存到表格
    # root_folder = 'pdf_files'

    # create_frequency_table(root_folder, feature_words)

    # # 如果中断，则从中断的地方继续计算
    # root_folder = 'pdf_files'

    # create_frequency_table(root_folder, feature_words, "000401")
