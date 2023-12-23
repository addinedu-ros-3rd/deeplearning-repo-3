# deeplearning-repo-3

# 딥러닝 기반의 무인 매장 시스템
## 📖 프로젝트 개요
### Action recognition 기반으로 어떤 과일을 샀는지 인식하면 DB 및 PyQt를 이용하여 해당 물건을 자동으로 결제
### Yolov8 기반 Object counting을 활용하여 매대별 과일 종류 및 개수 파악


## 🥇 시스템 구성
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/de7222e0-8f16-41d1-b555-d392aa396d1d" width="80%" style="float:left">
</p>


## 👨‍👧‍👦 팀원 및 역할
|이름|역할|
|------|------|
|강한얼|객체 인식 모델 YOLOv8 학습, 딥러닝 기반 고객 행동 인식 모델 학습, 중앙 시스템 Main 함수 설계, 시스템 구성도/ Use case/ Sequence diagram 제작|
|김준표|딥러닝 기반 고객 행동 인식 모델 학습 및 Test(Rule-based), 시스템 하드웨어 구성도 제작(일부), roslibpy 기반 영상 이미지 통신 및 PyQt 출력(일부)|
|조태상|매대의 과일 종류별 수량 인식 딥러닝 모델(일부), 시스템 데이터 저장을 위한 DB 개발, 관리자 시스템 GUI 개발
|조홍기|매대의 과일 종류별 수량 인식 딥러닝 모델 개발(전체), 무인 매장 시스템 - 중앙 관리 시스템간 통신 모듈 개발|
|최규호|시스템 데이터 저장을 위한 DB 개발|


## 📆 프로젝트 기간
### 2023.11.16~2023.12.15


## 🎯 기술 스택



|      |      |
|------|------|
|개발 환경|<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white">, <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white">, <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white">|
|언어|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">|
|DB|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">, <img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white">|
|GUI|<img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">|
|통신|<img src="https://img.shields.io/badge/ROS-22314E?style=for-the-badge&logo=ROS&logoColor=white">|


## 🥇 프로젝트 소개 
### - USE CASE Diagram
<p align="center">
  <img src="https://github.com/haneol0415/calculator/assets/61872888/4819b346-45ac-46a7-9ddc-0a321045a179" width="90%" style="float:left">
</p>


### - Sequence Diagram
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/a4fd1508-cc41-45e2-bbb0-19b58027f95b" width="90%" style="float:left">
</p>



## 🖌️ GUI
![gui_num](https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/104709955/21814471-3aca-42fe-8dc0-d7824f4a837e)
### - GUI 설명
① 특정 고객 ID 검색(ID가 없을 경우 검색되지 않음)

② 입장/퇴장 시간 선택(달력으로 년월일 선택) 

③ 검색 결과 및 검색 필터(고객 ID, 입장/퇴장 시간) 초기화 

④ 검색 : 현재 입력된 조건으로 DB 조회 

⑤ DB 조회 결과 표시 

⑥ 매대에 있는 과일과 결제된 과일의 불일치 로그 표시 

⑦ 매대에 남아있는 종류별 과일 개수 표시 

⑧ 과일이 팔린 시간, 종류, 개수를 DB에서 조회후 표시 

⑨ CCTV 현재 화면 

### - GUI 사용 방법
고객이 매장에 입장하면, DB에 고객정보가 update

입장한 고객을 결과화면에서 보고싶으면 search 버튼 push

고객이 원하는 과일을 고르고 매장 밖으로 나가면 DB에 결제할 과일이 update

고객이 결제한 과일과 매대에서 사라진 과일이 다르면 불일치 로그에 정보가 보임

매대에 남아있는 과일을 보고싶으면 search 버튼 push

팔린 과일의 log를 보고싶으면 search 버튼 push

cctv는 매대와 고객이 과일을 고르는 영상을 실시간으로 보고 있음

## 🏅 DBMS 구성도
![ERD drawio](https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/104709955/e7916564-5a40-4a7f-9cbb-9a284ca5601b)

### - DB 테이블 기능
productIn : 입고되는 과일을 관리하기 위한 테이블

enterence : 고객이 입장하는 정보를 저장하기 위한 테이블

payment : 고객이 매장 밖으로 나가면 결제된 정보들을 저장하기 위한 테이블

fruits : 현재 매장에 남아있는 과일을 관리하기 위한 테이블

customer : 고객을 관리하기 위한 테이블

shoppingBasket : 고객이 매장에서 과일을 선택하고 매장밖으로 나가기 전까지 선택한 과일을 저장하는 테이블

actionRecognition : 고객이 구매를 하기위한 인식된 행동을 저장하는 테이블

productOut : 고객이 사간 과일의 정보를 저장하기 위한 테이블

actionType : 고객이 과일을 사기 위한 4가지 타입의 행동을 정의한 테이블

mistmatchActionStand : 고객이 사간 과일과 매대에서 사라진 과일의 종류와 개수가 다를 때 정보를 알기 위해 각 정보를 저장하는 테이블


## 🏁 발표 자료 링크
https://docs.google.com/presentation/d/1L9lDK6GptjHDVC1pk5et46PFg5JRmc-w_r4A61HhIeM/edit#slide=id.g263d5bba2a3_0_5


## 개발 환경 설정



> Main 시스템
Ubuntu 22.04
ROS2 Humble
    1. install ros2 humble
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
    2. sudo apt-get install ros-humble-rosbridge-server
    3. cd ros_ws
    4. source /opt/ros/humble/setup.bash
    5. colcon build
    6. source install/local_setup.bash
    7. cmd 1 -> ros2 launch rosbridge_server rosbridge_websocket_launch.xml
    8. cmd 2 -> ros2 run auto_store_package auto_store_subscriber


> 전체 python requirements
    numpy
    opencv-python
    roslibpy
    torch
    mysql-connector-python
    PyQt5==5.14.2
    PyQt5-sip
