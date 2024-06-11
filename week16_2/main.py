import requests
import pandas as pd
import re

base_url = 'https://exam.naer.edu.tw'
headers = ["index", "縣市", "學校名稱", "年級", "學年度", "領域/群科", "科目", "種類", "下載試卷", "下載答案"]


def sort_data(df, sort_by):
    if sort_by in df.columns:
        sorted_df = df.sort_values(by=sort_by)
        return sorted_df
    else:
        print(f"欄位 '{sort_by}' 不存在於資料中。")
        return df

def get_web_data(start=0, end=5):
    data = []
    for i in range(start, end):
        url = f'https://exam.naer.edu.tw/searchResult.php?page={i+1}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
        res = requests.get(url)
        html_datas = res.text.split('\n')[687].split('</tr><tr><td bgcolor="#FFFFFF" class="t4">')
        html_datas = html_datas[1:]
        for html_data in html_datas:
            data_element = html_data.split('</td><td bgcolor="#FFFFFF" class="t4">')
            data_element = data_element[:7] + data_element[9:11]
            if re.findall("<a href=\"(\S\S+)\"", data_element[7]):
                data_element[7] = base_url + re.findall("<a href=\"(\S\S+)\"", data_element[7])[0]
            else:
                data_element[7] = ""
            if re.findall("<a href=\"(\S\S+)\"", data_element[8]):
                data_element[8] = base_url + re.findall("<a href=\"(\S\S+)\"", data_element[8])[0]
            else:
                data_element[8] = ""
            data.append(data_element)
    return data

def main():
    start_page = 0
    end_page = 5
    select_num = 0
    select_str = "排列方式:"
    select_num_limit = 7

    for idx, content in enumerate(headers):
        if idx > select_num_limit:
            break
        select_str += f'{idx}.{content}, '
    data = get_web_data()
    df = sort_data(pd.DataFrame(data, columns=headers[1:]), headers[select_num])

    while(True):
        print("=================================================current data=================================================")
        print(df)
        print("==============================================================================================================")
        print("command:")
        print(select_str)
        print(f"p:前一頁 n:下一頁 其他:關閉")
        try:
            select = input("請輸入指令:")
            select_num = int(select)
            if select_num > select_num_limit:
                break
            elif select_num == 0:
                df = df.sort_index()
            else:
                df = sort_data(df, headers[select_num])
        except:
            if select == "n":
                if end_page+1 > 1910:
                    print("This is the end of datas.")
                else:
                    start_page += 1
                    end_page += 1
                    data = get_web_data(start_page, end_page)
                    df = sort_data(pd.DataFrame(data, columns=headers[1:]), headers[select_num])
            elif select == "p":
                if start_page - 1 < 0:
                    print("This is the begin of datas.")
                else:
                    start_page -= 1
                    end_page -= 1
                    data = get_web_data(start_page, end_page)
                    df = sort_data(pd.DataFrame(data, columns=headers[1:]), headers[select_num])
            else:
                print("Wrong command!!")
    
if __name__ == "__main__":
    main()