# 딥러닝 기반의 무인 매장 시스템
<p align="center">
  <img src="images/readme_demo.gif" width="90%" style="float:left"/>
</p>

---
## Index
- [📖 프로젝트 개요](#📖-프로젝트-개요)
- [👨‍👧‍👦 팀원 및 역할](#👨‍👧‍👦-팀원-및-역할)
- [📆 프로젝트 기간](#📆-프로젝트-기간)
- [🎯 기술 스택](#🎯-기술-스택)
- [🥇 프로젝트 소개](#🥇-프로젝트-소개)
  - [🥇 시스템 구성](#🥇-시스템-구성)
  - [기능 리스트](#기능-리스트)
  - [USE CASE Diagram](#use-case-diagram)
  - [Sequence Diagram](#sequence-diagram)
- [🧠 딥러닝 인식 시스템](#🧠-딥러닝-인식-시스템)
- [📶 통신 모듈](#📶-통신-모듈)
- [🖌️ GUI](#🖌️-gui)
  - [GUI 설명](#gui-설명)
  - [GUI 사용 방법](#gui-사용-방법)
- [🏅 DBMS 구성도](#🏅-dbms-구성도)
- [DB 테이블 기능](#db-테이블-기능)
- [🏁 발표 자료 링크](#🏁-발표-자료-링크)
- [⚙️개발 환경 설정](#⚙️-개발-환경-설정)

---

## 📖 프로젝트 개요
딥러닝 기반의 행동 인식 및 객체 인식 모델을 사용하여 매장에 입장한 고객이 별도의 계산 절차 없이 물건을 구매하고, 관리자는 GUI를 통해 출입 상태, 재고 상태 등을 확인할 수 있는 시스템

## 👨‍👧‍👦 팀원 및 역할
|구 분|이 름|역 할|
|------|------|------|
|팀장|김준표|딥러닝 기반 고객 행동 인식 모델 학습 및 Test(Rule-based), 시스템 하드웨어 구성도 제작(일부), roslibpy 기반 영상 이미지 통신 및 PyQt 출력(일부)|
|팀원|강한얼|객체 인식 모델 YOLOv8 학습, 딥러닝 기반 고객 행동 인식 모델 학습, 중앙 시스템 Main 함수 설계, 시스템 구성도 / Use case/ Sequence diagram 제작|
|팀원|조태상|매대의 과일 종류별 수량 인식 딥러닝 모델(일부), 시스템 데이터 저장을 위한 DB 개발, 관리자 시스템 GUI 개발
|팀원|조홍기|매대의 과일 종류별 수량 인식 딥러닝 모델 개발(전체), 무인 매장 시스템 - 중앙 관리 시스템간 통신 모듈 개발, 전체 시스템 통합|
|팀원|최규호|시스템 데이터 저장을 위한 DB 개발|


## 📆 프로젝트 기간
2023.11.16 ~ 2023.12.15 (中 10일)


## 🎯 기술 스택
|      |      |      |      |
|------|------|------|------|
|개발 환경|<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white"> ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white) ![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)|언어|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">|
|딥러닝|<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white"> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white">|DB|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white">|
|GUI|<img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">|통신|![ROS2](https://img.shields.io/badge/ROS2-22314E?style=for-the-badge&logo=ROS&logoColor=white)|
|커뮤니케이션|![Jira](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white) ![Confluence](https://img.shields.io/badge/Confluence-172B4D?style=for-the-badge&logo=Confluence&logoColor=white) ![Slack](https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)|
---

## 🥇 프로젝트 소개 

### 🥇 시스템 구성
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/de7222e0-8f16-41d1-b555-d392aa396d1d" width="80%" style="float:left"/>
</p>

### 기능 리스트
- **매장 내 영상 인식 시스템**
  - Action Recognition Program : 카메라 영상으로부터 고객의 구매 행동을 인식
  - Stand Counter Program : 카메라 영상으로부터 매대 위의 상품 수량을 카운트

- **중앙 시스템**
  - 통신 : ROS Bridge Server의 Topic을 Subscribe하여 Cam 영상 및 데이터 수신
  - Main : 매장 내 영상 인식 시스템의 인식 결과를 취합하여 처리
  - DB : 매장 이용 기록, 시스템 로그 저장
  - File storage : CCTV 영상을 저장

- **사용자**
  - System GUI : 관리자가 매장 상태, 구매 기록, 재고 상태 등을 조회
  - CCTV Viewer : CCTV 영상 조회


### USE CASE Diagram

<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/61872888/ed9649ac-6de4-4751-8814-f932d642550c" width="90%" style="float:left">
</p>

### Sequence Diagram
- **출입 시나리오**
  - 고객이 신용 카드를 태그하여 매장에 입장
  - DB로부터 고객 정보를 조회하여 시스템 상의 가상의 장바구니를 생성
  - 고객 출입 기록을 저장
    
- **쇼핑 시나리오**
  - 고객이 매장 내 카메라에 인식 될 경우, 고객 행동을 인식하고 행동 로그를 기록
  - 고객의 구매 행동을 인식하는 경우, 매대 위 상품 수량 변화와 비교하여 불일치가 발생하는지 확인 (불일치 로그 기록)
  - 행동 인식 결과를 바탕으로 고객의 가상의 장바구니 업데이트
    
- **퇴장 및 구매 시나리오**
  - 고객이 출구에 신용 카드를 태그하여 매장에서 퇴장
  - 가상의 장바구니 내 품목별 가격을 DB에서 조회하여 총 금액 계산
  - 구매 기록을 DB에 저장
  - 고객의 퇴장 기록을 저장
    
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/a4fd1508-cc41-45e2-bbb0-19b58027f95b" width="90%" style="float:left">
</p>

## 🧠 딥러닝 인식 시스템
- 매장 내 고객 구매 행동 인식
- 매대 위 상품 카운트하여 재고 파악

### 구매 행동 인식 모델
#### 수행 태스크
  - Task 1 : 고객 행동 인식
  - Task 2 : 집은 상품 인식

#### 모델 선택
아래 3가지 Model architecture를 설계하여 가장 높은 성능을 보이는 **Separated inference model**을 선택 [세부 설명 (URL)]
- Rule-basd model
- Multi-task model
- Separated-inference model

#### Separated-inference model architecture
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/61872888/33b39051-fc54-4fc9-9a97-ed2ed1a74342" width="70%" style="float:left">
</p>

#### Inference
- 행동 인식
  - 카메라 영상을 입력으로 받음
  - Human pose estimation model, object detection model을 통해 관절 key points 좌표와 상품 좌표를 추출
  - 추출된 좌표 값들을 action recognition model인 LSTM의 input으로 사용
  - 50 frame(sequence length of LSTM)이 마다 고객 행동을 예측
    
- 집은 상품 인식
  - 예측된 행동이 "Holding"이면 마지막 프래임(이미지)을 CNN의 입력으로 사용
  - CNN을 통해 고객이 집은 상품을 인식

#### Components
|Components|Model|Training|
|------|------|------|
|Human pose estimation model|Mediapipe|Pre-trained|
|Object detection model|YOLOv8|From scratch|
|Action recognition model|LSTM|From scratch|
|CNN model|MobileNet-V3|From scratch|



### 매대 위 상품 카운트 모델
YOLO v8 기반 SuperVision 사용
```utils/make_ROI.py```로 매대 영역의 Polygon을 제작하여 save_roi.txt로 저장 후 Polygon 영역 내의 객체 개수 인식.
[자세한 내용](https://whghdrl9977.atlassian.net/wiki/spaces/T3/blog/2023/12/06/3244062)

---

## 📶 통신 모듈
- 사용 모듈
  - ROS2
  - ROS bridge(Websocket Server)
  - roslibpy

### roslibpy
  - Non-ROS system에서 Topic, Service, Action 작업을 하기 위한 library
  - Cam 시스템 경량화를 위해 사용
  - Json 형태로 데이터 전송

### ROS bridge
  - Non-ROS2 시스템과의 통신을 위해 사용

### Custom Message - ImgNData
  - sensor_msgs/msg/CompressedImage 기반, 매대 Data, 행동 Data를 추가한 Custom Message 제작

  - CompressedImg를 만들어서 보내고 수신하여 이미지로 만드는 일련의  과정 라이브러리 참고하여 직접 구현

  - 참조 : 
    - [sensor_msgs/msg/Image](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html)
    - [sensor_msgs/msg/CompressedImage](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/CompressedImage.html)
    - [github : cv_bridge - compressed_imgmsg_to_cv2](https://github.com/ros-perception/vision_opencv/blob/rolling/cv_bridge/python/cv_bridge/core.py#L106)

  - 구조

  |타입|변수명|비고|
  |---|---|---|
  |uint16|img_width||
  |uint16|img_width||
  |uint16|img_width||
  |uint8[]|img_data|320 x 320 resize 후 전송|
  |string|action_data|dict를 str로 dump하여 전송|
  |string|stand_data|dict를 str로 dump하여 전송|

---

## 🖌️ GUI

<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/104709955/21814471-3aca-42fe-8dc0-d7824f4a837e" width="90%" style="float:left">
</p>  

### GUI 설명
① 특정 고객 ID 검색(ID가 없을 경우 검색되지 않음)

② 입장/퇴장 시간 선택(달력으로 년월일 선택) 

③ 검색 결과 및 검색 필터(고객 ID, 입장/퇴장 시간) 초기화 

④ 검색 : 현재 입력된 조건으로 DB 조회 

⑤ DB 조회 결과 표시 

⑥ 매대에 있는 과일과 결제된 과일의 불일치 로그 표시 

⑦ 매대에 남아있는 종류별 과일 개수 표시 

⑧ 과일이 팔린 시간, 종류, 개수를 DB에서 조회후 표시 

⑨ CCTV 현재 화면 

### GUI 사용 방법
고객이 매장에 입장하면, DB에 고객정보가 update

입장한 고객을 결과화면에서 보고싶으면 search 버튼 클릭

고객이 원하는 과일을 고르고 매장 밖으로 나가면 DB에 결제할 과일이 update

고객이 결제한 과일과 매대에서 사라진 과일이 다르면 불일치 로그에 정보가 보임

매대에 남아있는 과일을 보고싶으면 search 버튼 push

팔린 과일의 log를 보고싶으면 search 버튼 push

cctv는 매대와 고객이 과일을 고르는 영상을 실시간으로 보고 있음

---

## 🏅 DBMS 구성도
![ERD drawio](https://github.com/addinedu-ros-3rd/deeplearning-repo-3/assets/104709955/e7916564-5a40-4a7f-9cbb-9a284ca5601b)

### DB 테이블 기능
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

---

## 🏁 발표 자료 링크
https://docs.google.com/presentation/d/1L9lDK6GptjHDVC1pk5et46PFg5JRmc-w_r4A61HhIeM/edit#slide=id.g263d5bba2a3_0_5

---

## ⚙️ 개발 환경 설정

OS : Ubuntu 22.04

> __Main PC__
  1. install pytorch 2.1.1 (https://pytorch.org/get-started/previous-versions/)
  2. pip install -r requirements/main_requirements.txt
  3. install ros2 humble (https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
  4. sudo apt-get install ros-humble-rosbridge-server 
  5. cd ros_ws
  6. source /opt/ros/humble/setup.bash
  7. colcon build
  8. source install/local_setup.bash
  9. 중앙 PC (cmd 1) -> ros2 launch rosbridge_server rosbridge_websocket_launch.xml
  10. 중앙 PC (cmd 2) -> ros2 run auto_store_package auto_store_subscriber

> __관제 PC__
  1. pip install -r requirements/control_requirements.txt
  2. python3 UIController.py

> __Cam__
  1. pip install -r requirements/cam_requirements.txt
  2. python3 -m main main.py
