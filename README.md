# 앱 스토어 스크래핑
## v1.2.1 
    - update DockerFile, docker-compose 
        - 역할 분리( docker, docker-compose )
        - add Window 용 docker-compose
        - set container timezone, command
        - update resource path
    - update mobileIndex 수집시 전날데이터를 요청 (당일 데이터 업데이트 안됨)
    - fix GoogleImage Download Process
    - fix apps_resource query for duplicate key error
    - add app.env in docker-compose 

## v1.1.1 
    - update datetime in log files [working]
## v1.1.0
    - add Apple 의 미등록앱 업데이트 파일 (updateAppleApp.py) 
    - update AppDto 
        - update method to staticmethod
            - [method] ofAppleCategory
            - [method] ofAppleAppDetail
    - add Domparser
        - AppleScrapService 에 적용
        - GoogleScrapService 에 적용
    - expand ErrorDto - 원복
        - add ErrorCodeLevel 에러코드 레벨 설정 - 제거
        - add ErrorCodeValue 에러코드 값 - 제거
    - mobileIndex MappingCode 생성오류 수정.
## v1.0.2
    - add bin/ 
        - add docker-compose_apple_category_scrap.yml
        - add docker-compose_google_saved_package_scrap.yml
        - add docker-compose_mobileIndex_rank_api.yml
        - add docker-compose_all.yml
    - delete sample/

## v1.0.1
    - 스크래핑 개별 동작으로 변경.
    - sample 폴더 추가. 
        - docker-compose.yml
        - .env-sample => 프로젝트 root 디렉토리에 이동 후 .env 로 변경하여 사용.
## v1.0.0
    - mobileIndexRank.py, scrapingGoogleStore.py, scrapingAppleStore.py 에 대한 수집기능 적용.
    - 멀티 프로세스, 멀티 스레드를 활용한 스크랩핑 작업.
    - mobileIndexRank.py
        - mobileIndex에서 제공해주는 앱의 매칭 정보를 수집하여 DB 에 등록한다. ( 이미지 제외 )
    - scrapingGoogleStore.py
        - 현재 DB 에 저장된 package ID 를 기반하여, 상세페이지를 조회하여 데이터를 업데이트 한다.
    - scrapingAppleStore.py
        - 앱스토어에서 제공하는 카테고리 전체에 대한 Top100 을 수집하여, 앱의 정보를 업데이트 한다.