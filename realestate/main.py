#!/usr/bin/env python3
# coding: utf-8
import time
import configparser
import os
import pandas as pd
import xml.etree.ElementTree as ET

import requests

HOST = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/"

URLS = {
    'apt-trade': {
        'url': HOST + "getRTMSDataSvcAptTrade?",
        'header': "resultCode, resultMsg, 거래금액, 건축년도, 년, 법정동, 아파트, 월, 일, 전용면적, 지번, 지역코드, 층"
    },
    'apt-rent': {
        'url': HOST + "getRTMSDataSvcAptRent?",
        'header': "resultCode, resultMsg, 건축년도, 년, 법정동, 보증금액, 아파트, 월, 월세금액, 일, 전용면적, 지번, 지역코드, 층"
    },
    'office-trade': {
        'url': 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiTrade?',
        # 'url':  HOST + "getRTMSDataSvcOffiTrade?"
        'header': "resultCode, resultMsg, 거래금액, 년, 단지, 법정동, 시군구, 월, 일, 전용면적, 지번, 지역코드, 층"
    },
    'office-rent': {
        'url': 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent?',
        # 'url': HOST + "getRTMSDataSvcOffiRent?"
        'header': "resultCode, resultMsg, 년, 단지, 법정동, 보증금, 시군구, 월, 월세, 일, 전용면적, 지번, 지역코드, 층"
    }
}


def get_data(url, rcode, date, service_key):
    querystring = {
        "pageNo": "1",
        "startPage": "1",
        "numOfRows": "99999",
        "pageSize": "10",
        "LAWD_CD": str(rcode),
        "DEAL_YMD": str(date),
        "type": "xml",
        "serviceKey": service_key}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "e8d4c5d9-9287-549d-b5bc-9cdd60e76e1d"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


def get_items(response):
    root = ET.fromstring(response.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            # print tag, text
            data[tag] = text
        item_list.append(data)
    return item_list


def get_months(year):
    import datetime
    import dateutil.relativedelta
    now = datetime.datetime.now()
    month = 12
    if year == now.year:
        month = datetime.datetime.now().month - 1
    d = datetime.datetime.strptime(str(year) + str(month), "%Y%m")
    delta = 1
    ymd_list = []
    for idx in range(0, month):
        ymd_list.append(d.strftime('%Y%m'))
        d = d - dateutil.relativedelta.relativedelta(months=delta)
    return ymd_list


def get_result_code_msg(response):
    # print response
    root = ET.fromstring(response.content)
    return root.find('header').find('resultCode').text, root.find('header').find('resultMsg').text


def get_road_codes():
    f = open("road_codes.csv", "r")
    lines = [x[:-1].split(',') for x in f.readlines()]
    road_codes = [x[0] for x in lines]
    road_codes = sorted(list(set(road_codes)))
    f.close()
    return road_codes


def data_exists(dir_path, filename):
    import os
    file_list = os.listdir(dir_path)
    for f in file_list:
        # print f, filename
        if filename in f:
            print(filename, 'is already exist')
            return True
    return False


def load_service_key():
    config = configparser.ConfigParser()
    conf_path = os.path.join(os.path.dirname(__file__), "conf", "config.ini")
    config.read(conf_path)
    return config['REAL_ESTATE_TRADE']['service_key']


def save_csv_result(url, road_code, date, service_key, dir_path):
    filename = '{}.csv'.format(date)
    if data_exists(dir_path, filename):
        return "ex", "already exist"

    response = get_data(url, road_code, date, service_key)

    try:
        result_code, response_msg = get_result_code_msg(response)
        if '00' != result_code:
            return result_code, response_msg
    except Exception as e:
        # send_msg_to_slack(sale_type + "," + rcode + "," + date + ": " + str(e))
        # continue
        raise

    item_list = get_items(response)
    time.sleep(1)
    items = pd.DataFrame.from_dict(item_list)

    items['date'] = date
    items.to_csv(os.path.join(dir_path, filename), index=False, encoding='utf8')

    return result_code, response_msg


def main():
    try:
        service_key = load_service_key()
    except Exception:
        print("Failed to get the service key")
        raise

    road_codes = get_road_codes()

    for sale_type in URLS:
        is_limit = False
        print(sale_type)
        url = URLS[sale_type]['url']

        for road_code in road_codes:
            print(road_code)
            for year in ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']:
                print(year)
                for date in sorted(get_months(year)):
                    dir_path = './data/{}/{}'.format(sale_type, road_code)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    result_code, response_msg = save_csv_result(url, road_code, date, service_key, dir_path)
                    if "ex" == result_code:  # already querying
                        continue
                    elif '00' != result_code:
                        print("today is up to limit", result_code, response_msg)
                        is_limit = True
                        break
                    else:
                        print(date, road_code, "is processed")

                if is_limit:
                    break
            if is_limit:
                break


if __name__ == '__main__':
    main()
