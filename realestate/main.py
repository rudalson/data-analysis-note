import requests

SERVICE_KEY = ""
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


def get_data(url, rcode, date):
    querystring = {
        "pageNo": "1",
        "startPage": "1",
        "numOfRows": "99999",
        "pageSize": "10",
        "LAWD_CD": str(rcode),
        "DEAL_YMD": date,
        "type": "json",
        "serviceKey": SERVICE_KEY}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "e8d4c5d9-9287-549d-b5bc-9cdd60e76e1d"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


def main():
    apt_trade = URLS.get("apt-trade")

    response = get_data(apt_trade.get("url"), 11110, "201512")

    print(response)


if __name__ == '__main__':
    main()
