import requests
import json
import math

def crawl_single_page(productId, page_index, start_year, end_year):
    url = 'https://np-anotice-stock.eastmoney.com/api/security/ann'

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Host': 'np-anotice-stock.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    params = {
        'cb': 'jQuery112305935577465837112_1679209738877',
        'sr': '-1',
        'page_size': '50',
        'page_index': page_index,
        'ann_type': 'A',
        'client_source': 'web',
        'stock_list': productId,
        'f_node': '1',
        's_node': '0'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        jsonp_str = response.text
    else:
        print(f"Error: {response.status_code}")
        return

    # Extract the JSON string from the JSONP string
    json_str = jsonp_str[jsonp_str.index('(') + 1:jsonp_str.rindex(')')]

    data = json.loads(json_str)
    total_hits = data['data']['total_hits']

    column_name = "年度报告全文"
    years = [str(year) for year in range(start_year, end_year)]

    years_found = []
    pdf_urls = []

    for item in data['data']['list']:
        if any(col['column_name'] == column_name for col in item['columns']):
            for year in years:
                if year in item['title']:
                    years_found.append(year)
                    pdf_urls.append(f"https://pdf.dfcfw.com/pdf/H2_{item['art_code']}_1.pdf")
                    break
    
    return years_found, pdf_urls, total_hits

    
def crawl_company(productId, start_year, end_year):
    years_found, pdf_urls, total_hits = crawl_single_page(productId, 1, start_year, end_year)
    pdf_urls_all = pdf_urls
    years_found_all = years_found
    

    pages = math.ceil(total_hits / 50)

    for i in range(2, pages + 1):
        years_found, pdf_urls, _ = crawl_single_page(productId, i, start_year, end_year)

        pdf_urls_all = pdf_urls_all + pdf_urls
        years_found_all = years_found_all + years_found
        
        if str(start_year) in years_found_all:
            break

    return pdf_urls_all, years_found_all

def remove_duplicates_and_sort(pdf_urls_all, years_found_all):
    unique_years = []
    unique_urls = []

    for i, year in enumerate(years_found_all):
        if year not in unique_years:
            unique_years.append(year)
            unique_urls.append(pdf_urls_all[i])

    # Sort the lists by years
    sorted_indices = sorted(range(len(unique_years)), key=lambda k: unique_years[k])
    sorted_urls = [unique_urls[i] for i in sorted_indices]
    sorted_years = [unique_years[i] for i in sorted_indices]

    return sorted_urls, sorted_years

def crawl_and_process(productId, start_year = 2016, end_year = 2021):
    pdf_urls_all, years_found_all = crawl_company(productId, start_year, end_year)
    sorted_urls, sorted_years = remove_duplicates_and_sort(pdf_urls_all, years_found_all)

    return sorted_years, sorted_urls

if __name__ == "__main__":
    start_year = 2016
    end_year = 2021
    sorted_urls, sorted_years = crawl_and_process('000012', start_year, end_year)
    print("Sorted urls:", sorted_urls)
    print("Sorted Years:", sorted_years)
