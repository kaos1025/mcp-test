import requests
from bs4 import BeautifulSoup
import csv
import time

# 크롤링할 스마트스토어 상품 URL 리스트 예시
PRODUCT_URLS = [
    'https://smartstore.naver.com/스토어아이디/products/상품번호',
    # 여기에 추가 상품 URL 입력
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def crawl_product(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[ERROR] {url} 접속 실패: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 상품명 예시 
    # (실제 클래스명은 페이지에서 확인 필요)
    name_tag = soup.select_one('h3._3oDjSvLwq9')
    product_name = name_tag.text.strip() if name_tag else ''
    
    # 가격 예시 (실제 클래스명은 페이지에서 확인 필요)
    price_tag = soup.select_one('span._1LY7DqCnwR')
    price = price_tag.text.strip() if price_tag else ''
    
    # 평점 예시 (실제 클래스명은 페이지에서 확인 필요)
    rating_tag = soup.select_one('em._15NU42F3kT')
    rating = rating_tag.text.strip() if rating_tag else ''
    
    # 리뷰수 예시 (실제 클래스명은 페이지에서 확인 필요)
    review_tag = soup.select_one('span._3OX3yV2u5d')
    review_count = review_tag.text.strip() if review_tag else ''
    
    return {
        'url': url,
        '상품명': product_name,
        '가격': price,
        '평점': rating,
        '리뷰수': review_count
    }

def main():
    results = []
    for url in PRODUCT_URLS:
        print(f"크롤링 중: {url}")
        data = crawl_product(url)
        if data:
            results.append(data)
        time.sleep(1)  # 서버 부하 방지
    
    # 결과를 CSV로 저장
    with open('smartstore_products.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['url', '상품명', '가격', '평점', '리뷰수'])
        writer.writeheader()
        writer.writerows(results)
    print('크롤링 완료! smartstore_products.csv 파일 생성됨')

if __name__ == '__main__':
    main() 