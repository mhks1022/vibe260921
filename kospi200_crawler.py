"""
네이버 증권(stock.naver.com)에서 코스피200 지수 데이터를 수집하는 스크립트

참고
----
https://stock.naver.com/market/stock/kr/ 페이지는 Next.js로 클라이언트 사이드
렌더링되는 SPA라서, 최초 응답 HTML에는 실제 데이터가 들어있지 않다
(표의 <tbody>가 빈 채로 내려온다). 즉 BeautifulSoup으로 이 URL의 HTML을
그대로 파싱해서는 데이터를 얻을 수 없다.

또한 예전에 많이 쓰이던 finance.naver.com의 코스피200 구성종목 페이지
(entryJongmok.naver)는 현재 서비스가 종료(HTTP 410)되어 더 이상 사용할 수 없다.

대신 이 페이지가 화면을 그릴 때 내부적으로 호출하는 JSON API를 직접
호출해서 데이터를 가져온다.

- 지수 요약 정보: https://m.stock.naver.com/api/index/KPI200/integration
- 구성종목 목록:  https://m.stock.naver.com/api/index/KPI200/enrollStocks
"""

import csv
import time

import requests

INDEX_CODE = "KPI200"  # 네이버 증권 내부 코스피200 지수 코드
BASE_URL = "https://m.stock.naver.com/api/index"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}

PAGE_SIZE = 50  # 네이버 API가 한 번에 허용하는 최대 페이지 크기
REQUEST_DELAY = 0.3  # 초 단위, 페이지 요청 사이 대기 시간

CHANGE_SIGN = {"RISING": "+", "FALLING": "-", "UNCHANGED": ""}

SUMMARY_LABELS = [
    ("lastClosePrice", "전일"),
    ("openPrice", "시가"),
    ("highPrice", "고가"),
    ("lowPrice", "저가"),
    ("accumulatedTradingVolume", "거래량"),
    ("accumulatedTradingValue", "거래대금"),
    ("highPriceOf52Weeks", "52주 최고"),
    ("lowPriceOf52Weeks", "52주 최저"),
]


def fetch_summary():
    """코스피200 지수 자체의 요약 정보(시가/고가/저가/거래량/52주 최고·최저 등)를 가져온다."""
    url = f"{BASE_URL}/{INDEX_CODE}/integration"
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    data = res.json()

    values_by_code = {info["code"]: info["value"] for info in data.get("totalInfos", [])}
    return {
        "지수명": data.get("stockName", ""),
        **{label: values_by_code.get(code, "") for code, label in SUMMARY_LABELS},
    }


def fetch_constituent_stocks():
    """코스피200 구성종목 전체 목록을 페이지 단위로 끝까지 순회하며 모두 가져온다.

    네이버 API는 한 번에 최대 PAGE_SIZE(50)개까지만 내려주므로, 응답이
    빈 배열로 올 때까지(=마지막 페이지를 지날 때까지) page 번호를 1씩
    늘려가며 반복 요청해 코스피200 약 200개 종목 전체를 수집한다.
    """
    stocks = []
    page = 1

    while True:
        url = f"{BASE_URL}/{INDEX_CODE}/enrollStocks"
        res = requests.get(
            url, headers=HEADERS, params={"page": page, "pageSize": PAGE_SIZE}, timeout=10
        )
        res.raise_for_status()

        page_items = res.json() if res.text.strip() else []
        if not page_items:
            break

        for item in page_items:
            sign = CHANGE_SIGN.get(item.get("compareToPreviousPrice", {}).get("name", ""), "")
            stocks.append({
                "종목코드": item.get("itemCode", ""),
                "종목명": item.get("stockName", ""),
                "현재가": item.get("closePrice", ""),
                "전일대비": f"{sign}{item.get('compareToPreviousClosePrice', '')}",
                "등락률(%)": item.get("fluctuationsRatio", ""),
                "거래량": item.get("accumulatedTradingVolume", ""),
                "거래대금(백만)": item.get("accumulatedTradingValue", ""),
                "시가총액(억)": item.get("marketValue", ""),
            })

        print(f"  {page}페이지 수집 완료 (누적 {len(stocks)}건)")
        page += 1
        time.sleep(REQUEST_DELAY)

    return stocks


def save_to_csv(stocks, csv_path="kospi200_stocks.csv"):
    if not stocks:
        return
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(stocks[0].keys()))
        writer.writeheader()
        writer.writerows(stocks)


def main():
    print("코스피200 지수 요약 정보를 가져오는 중...")
    summary = fetch_summary()
    print(f"\n[{summary['지수명']}]")
    for _, label in SUMMARY_LABELS:
        print(f"  {label}: {summary.get(label, '')}")

    print("\n코스피200 구성종목을 가져오는 중...")
    stocks = fetch_constituent_stocks()
    print(f"총 {len(stocks)}개 종목을 수집했습니다.\n")

    for s in stocks[:10]:
        print(f"{s['종목코드']} {s['종목명']:10s} 현재가 {s['현재가']:>10s}  등락률 {s['등락률(%)']}%")
    if len(stocks) > 10:
        print(f"... 외 {len(stocks) - 10}개 종목")

    save_to_csv(stocks)
    print("\n결과를 'kospi200_stocks.csv' 파일로 저장했습니다.")


if __name__ == "__main__":
    main()
