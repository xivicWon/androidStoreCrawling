# 앱 스토어 스크래핑
## v1.0.0
    - mobileIndexRank.py, scrapingGoogleStore.py, scrapingAppleStore.py 에 대한 수집기능 적용.
    - 멀티 프로세스, 멀티 스레드를 활용한 스크랩핑 작업.
### mobileIndexRank.py
    - mobileIndex에서 제공해주는 앱의 매칭 정보를 수집하여 DB 에 등록한다. ( 이미지 제외 )
### scrapingGoogleStore.py
    - 현재 DB 에 저장된 package ID 를 기반하여, 상세페이지를 조회하여 데이터를 업데이트 한다.
### scrapingAppleStore.py
    - 앱스토어에서 제공하는 카테고리 전체에 대한 Top100 을 수집하여, 앱의 정보를 업데이트 한다.