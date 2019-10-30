import base64
import configparser
import os

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

    params = {
        "LAWD_CD": str(rcode),
        "DEAL_YMD": str(date),
        "serviceKey": service_key
    }

    response = requests.request("GET", url, params=params)
    return response


def load_service_key():
    config = configparser.ConfigParser()
    conf_path = os.path.join(os.path.dirname(__file__), "conf", "config.ini")
    config.read(conf_path)
    return config['REAL_ESTATE_TRADE']['service_key']


def main():
    encoded_service_key = load_service_key()
    service_key = base64.b64decode(encoded_service_key).decode('utf-8')
    print(service_key)
    apt_trade = URLS.get("apt-trade")

    response = get_data(apt_trade.get("url"), 11110, 201512, service_key)

    print(response.content)


if __name__ == '__main__':
    main()
