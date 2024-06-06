<img width="631" alt="image" src="https://github.com/EYaan/Project/assets/81665544/7c95f520-0797-42e3-9fd2-322636136eea">


- 헬멧에 라즈베리파이 모듈인 카메라 장착
- 고객클라이언트, 키오스크클라이언트, 서버로 이루어짐
- 고객클라이언트가 카메라로 접시 안에 있는 qrcode 인식시 클라이언트 주문 진행 준비 완료
- 서버에서 준비 완료 데이터를 받은 후 서버에서 키오스크로 데이터를 보내 화면 자동 변경

<br/>
<br/>

<img width="666" alt="image" src="https://github.com/EYaan/Project/assets/81665544/41af70f1-a2be-405f-bea3-0bed20ee85a2">


- OpenCV를 활용해 카메라로 키오스크 위 손가락 좌표 확인 후 원하는 메뉴위에 손가락이 있다는 사운드 출력
- 사운드가 들리면 V표시로 그 메뉴를 선택하여 서버로 메뉴 전송 
<br/>
<br/>

<img width="656" alt="image" src="https://github.com/EYaan/Project/assets/81665544/0d94c5e9-4711-4c2b-97fd-014ccc64c708">


- 결제버튼 위 좌표가 확인되면 마찬가지로 손가락 V표시로 결제 선택


<img width="727" alt="서버 클라이언트_순서도" src="https://github.com/EYaan/Project/assets/81665544/812677da-1c93-4b79-9023-a3b822077dbe">
- 고객이 키오스크를 이용하는 동안 서버 클라이언트의 관계도
