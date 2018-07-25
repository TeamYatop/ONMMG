# ONMMG

- 2018년 02월 - 현재
- ONMMG: 오늘뭐먹지
- 자주가는 음식점(Hangout)을 등록하고 맞춤형 검색을 하는 사이트

### 기술 스택

- Python (3.6.3)
- Django (2.0.2)
- Djangorestframework (3.7.7)
- Requests (2.18.4)
- [Daum Maps API](http://apis.map.daum.net)
- [PythonAnywhere](https://www.pythonanywhere.com)

### 설명

- 친구들과 모일 때 마다 무엇을 먹을지 고민하는 시간을 줄이기 위해 기획한 프로젝트
- 자주 가는 음식점(Hangout)과 연관 태그를 등록하고 검색한다
- 검색 결과중 하나를 임의로 선택할 수 있다
- 특정 태그에 위치 정보를 등록해서 원하는 지역(지하철역)을 기준으로 검색한다
	- 지하철 역을 기준으로 위치를 등록한다

### 기능 설명

- Hangout 을 등록할 때 주소를 입력으로 받으면 위도 경도로 변환해서 저장한다
- 지도상에 Hangout 객체를 지속적으로 추가 삭제 하지 않고, 처음 한번만 등록하고 이후로는 검색 결과에 따라서 hide/show toggle 한다
- Hangout 생성시 태그를 입력할때 빈칸을 이용해서 각 태그를 구분한다
- PythonAnywhere 를 이용한 호스팅

### API

| api                                       | description    | examples                          |
|-------------------------------------------|----------------|-----------------------------------|
| ```/api/detail/<slug>```                  | get hangout    | /api/detail/vbmwgQtv5BT           |
| ```/api/areas```                          | get all areas  | /api/areas                        |
| ```/api/tags```                           | get all tags   | /api/tags                         |
| ```/api/search?area=<area>&tags=<tags>``` | search hangout | /api/search?area=야탑&tags=튀김,비쌈 |

- ```<slug>``` 숫자와 알파벳(대소문자 구분) 으로 구성된 길이 11의 문자열
- ```<area>``` 지역을 속성을 같고있는 태그 1개
- ```<tags>``` 쉼표로 구분된 1개 이상의 태그

### 모델

**Hangout**

| field_name  | field_type      | options               |
|-------------|-----------------|-----------------------|
| slug        | SlugField       | max=11                |
| title       | CharField       | max=100               |
| description | CharField       | max=140               |
| address     | CharField       | max=140               |
| latitude    | DecimalField    | digits=20, decimal=15 |
| longitude   | DecimalField    | digits=20, decimal=15 |
| tags        | ManyToManyField |                       |

**Tag**

| name | field      | description    |
|------|------------|----------------|
| word | CharField  | max=50, unique |
| area | ForeignKey | Area, Nullable |

**Area**

| name      | field          | description           |
|-----------|----------------|-----------------------|
| name      | CharField      | max=100               |
| address   | CharField      | max=140               |
| latitude  | DecimalField   | digits=20, decimal=15 |
| longitude | DecimalField   | digits=20, decimal=15 |
| tag_set   | OneToManyField | Tag                   |
