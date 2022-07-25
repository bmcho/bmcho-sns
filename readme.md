# Social Networking Service(SNS)
프리온보딩 4주차 개인과제 입니다.   
게시글작성 및 수정,삭제가 가능하며 좋아요 관리, 해시태그 관리를 할 수 있습니다.

## 📚 Skills
<br>

 - Language

    ![python](https://img.shields.io/badge/python-3.8-3670A0?logo=python&logoColor=white)

 - FrameWork

    ![Django](https://img.shields.io/badge/django-3.2.14-%23092E20?&logo=Django&logoColor=white)
    ![DjangoRest](https://img.shields.io/badge/DJANGOREST-3.13.1-ff1709?logo=django&logoColor=white&color=ff1709&labelColor=gray)
    
 - DataBase 

    ![MySQL](https://img.shields.io/badge/mysql-8.0-4479A1.svg?logo=mysql&logoColor=white)
    ![Redis](https://img.shields.io/badge/redis-DC382D.svg?logo=redis&logoColor=white)

 - Deploy 

    ![AWS](https://img.shields.io/badge/AWSE2-%23FF9900.svg?logo=amazon-aws&logoColor=white)
    ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
    ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?logo=nginx&logoColor=white)
    ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?logo=gunicorn&logoColor=white)

 - ETC

    ![GitHub](https://img.shields.io/badge/github-%23121011.svg?logo=github&logoColor=white)
    ![Git](https://img.shields.io/badge/-git-F05032?logo=git&logoColor=white)
    
    <br>

## ✅ 프로젝트 소개
<br>

- 본 과제에서 요구하는 서비스는 SNS(Social Networking Service)입니다.
- 사용자는 본 서비스에 접속하여, 본인의 게시글을 업로드하고 관리(수정/삭제/복구)할 수 있습니다.
- 사용자는 본 서비스에 접속하여, 모든 게시글을 확인하고 좋아요 기능을 사용할 수 있습니다.

<br>

## 📌 요구 사항

<br>

- 유저관리
    - 유저 회원가입: 이메일을 ID로 사용합니다.
    - 유저 로그인 및 인증: JTW 토큰을 발급받으며, 이를 추후 사용자 인증으로 사용합니다.
- 게시글
    - 게시글 생성
        - 제목, 내용, 해시태그 등을 입력하여 생성합니다.
        - 제목, 내용, 해시태그는 필수 입력사항입니다.
        - 작성자 정보는 request body에 존재하지 않고 해당 API를 요청한 인증정보에서 추출합니다.    
          (API 단에서 토큰에서 얻은 사용자 정보를 게시글 생성때 작성자로 넣어사용)
        - 해시태그는 #로 시작되고 ','로 구분되는 텍스트가 입력됩니다.    
          ex) { “hashtags”: “#맛집,#서울,#브런치 카페,#주말”, …}  
    - 게시글 수정
        - 작성자만 수정할 수 있습니다.
    - 게시글 삭제
        - 작성자만 삭제할 수 있습니다.
        - 작성자는 삭제된 게시글을 다시 복구 할 수 있습니다.
    - 게시글 상세보기
        - 모든 사용자는 모든 게시물에 보기권한이 있습니다.
        - 작성자를 포함한 사용자는 본 게시글에 좋아요를 누를 수 있습니다.
        - 좋아요된 게시물에 다시 좋아요를 누르면 취소됩니다.
        - 작성자를 포함한 사용자가 게시글을 상세보기하면 조회수가 1증가합니다.(횟수 제한 없음)
    - 게시글 목록
        - 모든 사용자는 모든 게시물에 보기권한이 있습니다.
        - 게시글 목록에는 제목, 작성자, 해시태그, 작성일, 좋아요 수, 조회수 가 포함됩니다.
    - 게시글 검색 조건
        - 쿼리 파라미터로 구현. ex) ?search=..&orderBy=..  (예시이며 해당 변수는 직접 설정)
        - 아래 4가지 동작은 각각 동작 할 뿐만 아니라, 동시에 적용될 수 있어야 합니다.
            - Ordering (= Sorting, 정렬)
                - 사용자는 게시글 목록을 원하는 값으로 정렬할 수 있습니다.
                - (default: 작성일,  / 작성일, 좋아요 수, 조회수 중 1개 만 선택가능)
                - 오름차 순, 내림차 순을 선택할 수 있습니다.
            - Searching (= 검색)
                - 사용자는 지정한 키워드로 해당 키워드를 포함한 게시물을 필터링할 수 있습니다.    
                  예시 1) some-url?hastags=서울 >> “서울" 해시태그를 가진 게시글 목록.    
                  예시 2) some-url?hastags=서울,맛집 >> “서울" 과 “맛집” 해시태그를 모두 가진 게시글 목록.     
                  [ex. “서울” 검색 시 > #서울(검색됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]    
                  [ex. “서울,맛집” 검색 시 > #서울(검색안됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
            - Pagination (= 페이지 기능)
                - 사용자는 1 페이지 당 게시글 수를 조정할 수 있습니다. (default: 10건)

<br>

## 🔑 기능구현

**1. 유저생성**

- 유저를 생성합니다.

**2. 유저로그인 / 로그아웃**
- JWT 인증방식을 사용하여 로그인/로그아웃을 합니다.

**3. 유저 정보 업데이트**
- 유저는 개인정보를 업데이트 할 수 있습니다.

**5. 게시글 저장**
- 인증된 유저에 한하여 게시글을 작성 할 수 있습니다.
- 다수의 해시태그를 저장 할 수 있습니다.

**5. 게시글 조회**
- 게시글을 검색, 정렬 조건에 맞춰 검색합니다.
- search: 제목, 내용이 포함된 게시글 검색
- hashtag: 해시태그가 포함된 게시글 검색
- page: 한 페이지 당 10개의 게시글 검색
- ordering: 작성일, 좋아요, 조회수를 내림차순, 오름차순으로 게시글 검색

**6. 게시글 상세 조회**
- 해당 게시글에 좋아요를 누를 수 있습니다.
- 해당 게시글의 리뷰를 볼 수 있습니다.
- 작성자는 해당 게시글을 수정하고 삭제 할 수 있습니다.

**7. 게시글 리뷰 작성**
- 인증된 유저에 한하여 해당 게시글에 리뷰작성이 가능합니다.
- 작성자는 해당 리뷰를 수정하고 삭제 할 수 있습니다.

**8. 랭킹 조회**
- 모든 유저의 레이드 점수 총점을 기반으로 TOP10 정보를 조회합니다.
- 로그인한 유저의 개인 순위를 조회합니다.
- TOP10 순위는 5분마다 업데이트됩니다.
- TOP10 순위는 1 ~ 10위가 아닌 0~9위 순으로 반환합니다.

<br>

## 📁API Doc
<br>

|Index|Method|URL|QueryParams|Permission|Description|
|----|----|----|----|----|----|
|<td colspan=2>유저관리</td>|
|1|POST|/api/sign-up||AllowAny|회원가입|
|2|POST|/api/sign-in||AllowAny|로그인|
|3|PUT|/api/sign-out||Authenticated|로그아웃|
|<td colspan=2>게시글 관리</td>|
|4|POST|/api/posts||Authenticated|게시글 작성
|5|GET|/api/posts/<post_id:int>||AllowAny|게시글 상세 조회
|6|PATCH|/api/posts/<post_id:int>||Authenticated|게시글 수정
|7|DELETE|/api/posts/<post_id:int>||Authenticated|게시글 삭제
|8|GET|/api/posts|search,ordering,hashtag,page|AllowAny|게시글 조회
|9|PATCH|/api/posts/<post_id:int>/like||Authenticated|게시글 좋아요
|10|POST|/api/posts/<post_id:int>/review||Authenticated|게시글 리뷰작성
|11|PATCH|/api/posts/<post_id:int>/review||Authenticated|게시글 리뷰수정
|12|DELETE|/api/posts/<post_id:int>/review||Authenticated|게시글 리뷰삭제


## [API Request, Response 목록 링크](https://docs.google.com/spreadsheets/d/1st5T2e4sgkV5qdnSBGpoKJ7NW37wvOCVNX8LAcB_ayg/edit#gid=0)

<br>

## 💾ERD
<br>

![image](https://user-images.githubusercontent.com/57892199/180805129-d2299276-6087-4ca8-a504-1b10e1505fbf.png)

<br>
