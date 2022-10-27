# 앱 스토어 스크래핑
## v1.5.1
    - 전체 경로 수정 
        - 앱(apps) 별 경로 설정 ( appleScrap, googleScrap, mobileIndex )
        - 각 기능별 docker-compose 구조 설정.
        - 변경된 경로에 맞는 docker-compose 반영
## v1.4.4
    - mobileIndexAppSearch
        - 대상이 될 데이터에 대한 업데이트 처리. (insertAppScanningForMapping)
        - 대상조회 에러 수정.
## v1.4.3
    - docker-compose 
        - 샘플 명령문구 수정.
## v1.4.2
    - MobileIndex SecretKey Playwright 반영
        - mobileIndexSecretKey : 키 생성 파일
        - 기존 mobileIndex 관련 스크랩핑에서 키 조회방식 변경.
        - MIRequestDto 에서 불필요한 함수 제거.
    - DockerFile 
        - DockerFile -> 삭제 
        - DockerFileInUbuntu -> DockerFile 
## v1.4.1
    - DockerFile 
        - Ubuntu 20.04 
        - python3.10 -> python3.8 
        - playwright 
## v1.3.4
    - Playwright 모듈 추가.
        - mobileindex 에서 _secret 값을 조회하기위해서.
    - mobileIndex SecretCode 생성규칙 수정.
## v1.3.3
    - 모바일 인덱스 secret-key 생성 함수 작성.
    - 모바일 인덱스에서 앱 등록시 mapping 데이터가 없는경우에도 값이 등록되는 오류 수정.
    - 파일 저장시 3개 공간에 나누어서 저장
    - ISOCountryCode 적용시 처리 오류 수정 
    - Magic 적용 제거. (linux 에서 잘 안됨.)
## v1.3.2
    - 모바일인덱스에서 데이터 없을 때 예외처리

## v1.3.1
    - 미사용 파일 제거.
    - ISOCountryCode 추가.
        - 연관 Entity 에 데이터 추가. (AppEntity.countryCodeNum)
## v1.3.0
    - mobileIndex 의 앱개별 조회API 추가. 
        - mapping정보가 없는 데이터만 조회해서 IOS App 정보 및 mapping_code 를 등록.
        - apple_id 가 None 으로 반환되는 내역에 대한 예외처리.
    - 구글 앱 등록시 에러 로그 수정.
## v1.2.2
    - mapping_code 초기화 문제 수정(mobileIndex 에서 초기화해주는 코드 확인 및 수정)
    - 이미지 조회 및 데이터 업데이트 파일 ( checkIconExist.py)
    - Remove deprecated Files 
    - Files Rename : snake > camel
    - Create New Container => appleScrapBySavedID.py
    - apple category 처리시 App 정보만 저장(developer x, icon x ) 
    - Resource 파일저장경로 개선 (날짜[Ym] + random( 1~20))
    - Images 생성시 권한 및 사용자(daemon) 변경 
    - Images webp -> png 로 변경 추가.
    - convertImagesInDirectory.py 추가 [특정디렉토리의 이미지를 png 로 변경]
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