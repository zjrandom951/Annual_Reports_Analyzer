# Annual Reports Analyzer 

# 基于Python的金融报告文本挖掘



## Description

## 简介

Annual Reports Analyzer is a Python-based project that automates the process of downloading and analyzing annual reports of companies listed in an Excel file. The program extracts URLs of annual reports, downloads PDFs, and calculates the frequency of specific keywords (related to technology and financial sectors) in the reports.

Annual Reports Analyzer 是一个基于 Python 的项目，可以自动下载和分析 Excel 文件中列出的公司的年度报告。 该程序提取年度报告的 URL，下载 PDF，并计算报告中特定关键字（与技术和金融部门相关）的频率。

## Features

## 特点

- Reads company codes from an Excel file
- Extracts annual report URLs for given company codes
- Downloads PDFs of annual reports and saves them in a local folder
- Analyzes the content of the annual reports to calculate the frequency of specific keywords

- 从 Excel 文件中读取公司代码
- 提取给定公司代码的年度报告 URL
- 下载年度报告的 PDF 并将其保存在本地文件夹中
- 分析年度报告的内容以计算特定关键字的频率

## Requirements

## 要求

- Python 3.6+
- PyPDF2
- jieba
- pandas
- openpyxl
- requests

To install the required libraries, use the following command:

要安装所需的库，请使用以下命令：

```shell
pip install PyPDF2 jieba pandas openpyxl requests
```

## Usage

## 使用方法

1. Make sure to have an Excel file named `codes.xlsx` with a column called "证券代码" that contains the company codes.
2. Run the `main.py` script, which will extract annual report URLs, download the PDFs, and save them in a folder named `pdf_files`.
3. The script will then analyze the PDFs to calculate the frequency of the specified keywords and save the results in a CSV file named `frequency_table.csv`.

1. 确保有一个名为“codes.xlsx”的 Excel 文件，其中包含包含公司代码的名为“证券代码”的列。
2. 运行 `main.py` 脚本，它将提取年度报告 URL，下载 PDF，并将它们保存在名为 `pdf_files` 的文件夹中。
3. 然后脚本将分析 PDF 以计算指定关键字的频率并将结果保存在名为“frequency_table.csv”的 CSV 文件中。

## Contributing

## 贡献

Please feel free to submit issues or pull requests for bug fixes or new features.

请随时提交问题或请求错误修复或新功能。

## License

## 许可

This project is licensed under the MIT License.

这个项目是根据麻MIT许可证获得许可的。