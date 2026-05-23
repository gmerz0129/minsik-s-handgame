# minsik-s-handgame
# Hand Game 

OpenCV와 MediaPipe를 이용한 실시간 손 인식 프로그램입니다.  
웹캠으로 양손을 인식하고, 손이 펴져 있으면 손 위에 한글 텍스트를 표시합니다.

왼손을 펴면 `hand`, 오른손을 펴면 `game`이 표시되도록 만들었습니다.
원하는 글자대로 수정도 가능합니다.

---

## 📌 소개

이 프로젝트는 웹캠 화면에서 사용자의 손을 실시간으로 인식하고, 손가락이 펴져 있는지 판단하여 손 위에 텍스트를 출력하는 간단한 손 인식 게임입니다.

MediaPipe Hands를 사용하여 손의 21개 랜드마크를 추출하고, 손가락 끝 위치와 중간 관절 위치를 비교하여 손이 펴져 있는지 판단합니다.

OpenCV의 기본 텍스트 출력 함수는 한글을 지원하지 않기 때문에, Pillow를 사용하여 한글 텍스트가 깨지지 않도록 구현했습니다.

---

## 🛠 사용 기술

- Python
- OpenCV
- MediaPipe
- Pillow
- NumPy

---

## ✨ 주요 기능

- 웹캠 실시간 영상 입력
- MediaPipe Hands 기반 손 랜드마크 인식
- 왼손 / 오른손 구분
- 손가락이 펴져 있는지 판단
- 손 위에 한글 텍스트 표시
- 텍스트 색상 설정
- `q` 키를 눌러 프로그램 종료

---

## 🖐 동작 방식

손가락 4개 중 3개 이상이 펴져 있으면 손이 열린 상태라고 판단합니다.

사용한 손가락 랜드마크는 다음과 같습니다.

| 손가락 | 끝 Landmark | 중간 Landmark |
|---|---:|---:|
| 검지 | 8 | 6 |
| 중지 | 12 | 10 |
| 약지 | 16 | 14 |
| 새끼 | 20 | 18 |

손가락 끝의 y좌표가 중간 관절의 y좌표보다 위에 있으면 해당 손가락이 펴진 것으로 판단합니다.

---

## 🎮 기본 표시 설정

| 손 | 표시 텍스트 | 색상 |
|---|---|---|
| 왼손 | hand | 노란색 |
| 오른손 | game | 보라색 |

---

## 📁 파일 구성

```text
hand-game/
├── hand_game.py
├── README.md
└── requirements.txt
```

---

## ⚙️ 설치 방법

먼저 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

또는 직접 설치할 경우:

```bash
pip install opencv-python mediapipe pillow numpy
```

---

## 📦 requirements.txt

```text
opencv-python
mediapipe
pillow
numpy
```

---

## ▶️ 실행 방법

```bash
python hand_game.py
```

프로그램이 실행되면 웹캠 창이 열립니다.  
종료하려면 키보드에서 `q`를 누르면 됩니다.

---

## 🔧 설정 변경 방법

### 표시되는 글자 바꾸기

코드에서 아래 부분을 수정하면 손 위에 표시되는 글자를 바꿀 수 있습니다.

```python
hand_label = "hand"
hand_label = "game"
```

예시:

```python
hand_label = "공격"
hand_label = "방어"
```

---

### 색상 바꾸기

Pillow를 사용한 텍스트 색상은 RGB 순서를 사용합니다.

```python
text_color = (255, 255, 0)  # 노란색
text_color = (255, 0, 255)  # 보라색
```

자주 쓰는 색상은 다음과 같습니다.

```python
(255, 0, 0)      # 빨간색
(0, 255, 0)      # 초록색
(0, 0, 255)      # 파란색
(255, 255, 255)  # 흰색
(255, 255, 0)    # 노란색
(255, 0, 255)    # 보라색
```

---

## ⚠️ 주의사항

### 한글이 깨지는 경우

OpenCV의 `cv2.putText()`는 한글을 제대로 출력하지 못합니다.  
따라서 이 프로젝트에서는 Pillow의 `ImageDraw.text()`를 사용하여 한글을 출력합니다.

Windows에서는 기본적으로 다음 폰트를 사용합니다.

```python
FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
```

Mac이나 Linux에서는 본인 환경에 맞는 한글 폰트 경로로 수정해야 합니다.

---

### 카메라가 열리지 않는 경우

기본 카메라 번호는 `0`입니다.

```python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

카메라가 열리지 않으면 `0`을 `1` 또는 `2`로 바꿔볼 수 있습니다.

```python
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

또한 Windows 설정에서 카메라 권한이 허용되어 있는지 확인해야 합니다.

---

## 🚀 향후 개선 아이디어

- 다양한 손동작 인식 추가
- 점수 시스템 추가
- 제한 시간 게임 기능 추가
- 효과음 추가
- 배경 이미지 추가
- 웹앱 형태로 확장

---

## 📝 License

This project is licensed under the MIT License.
