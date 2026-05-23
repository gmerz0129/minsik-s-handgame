import cv2
import mediapipe as mp
from PIL import ImageFont, ImageDraw, Image
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# 한글 폰트 경로
# Windows 기본 한글 폰트: 맑은 고딕
FONT_PATH = "C:/Windows/Fonts/malgun.ttf"


def is_hand_open(hand_landmarks):
    """손가락 4개 중 3개 이상 펴져 있으면 True"""
    tips = [8, 12, 16, 20]
    mids = [6, 10, 14, 18]

    open_fingers = sum(
        hand_landmarks.landmark[t].y < hand_landmarks.landmark[m].y
        for t, m in zip(tips, mids)
    )

    return open_fingers >= 3


def draw_korean_text(frame, text, position, font_size=70, color=(255, 255, 0)):
    """
    OpenCV frame 위에 한글 텍스트 출력
    color는 RGB 기준
    예: 노란색 (255, 255, 0), 보라색 (255, 0, 255)
    """
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    font = ImageFont.truetype(FONT_PATH, font_size)

    draw.text(position, text, font=font, fill=color)

    frame[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def put_text_above_hand(frame, hand_landmarks, text, color):
    """손 위쪽에 한글/영어 글자 표시"""
    h, w, _ = frame.shape

    xs = [lm.x for lm in hand_landmarks.landmark]
    ys = [lm.y for lm in hand_landmarks.landmark]

    min_x = int(min(xs) * w)
    max_x = int(max(xs) * w)
    min_y = int(min(ys) * h)

    center_x = (min_x + max_x) // 2

    font_size = 70

    # 글자 길이에 따라 대략 중앙 정렬
    text_x = center_x - (len(text) * font_size) // 3
    text_y = min_y - 80

    # 화면 밖으로 나가지 않게 보정
    text_x = max(10, min(text_x, w - 200))
    text_y = max(10, text_y)

    draw_korean_text(
        frame,
        text,
        (text_x, text_y),
        font_size=font_size,
        color=color
    )


print("카메라 여는 중...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    print("카메라 번호를 1 또는 2로 바꿔보세요.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("카메라 열림!")
print("q를 누르면 종료됩니다.")

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        ret, frame = cap.read()

        if not ret:
            print("프레임을 읽지 못했습니다.")
            break

        # 거울 모드
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = hands.process(rgb)
        rgb.flags.writeable = True

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_lm, hand_info in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):
                mp_draw.draw_landmarks(
                    frame,
                    hand_lm,
                    mp_hands.HAND_CONNECTIONS
                )

                side = hand_info.classification[0].label

                if is_hand_open(hand_lm):

                    # 거울 반전했기 때문에
                    # MediaPipe 기준 Right = 실제 왼손
                    # MediaPipe 기준 Left = 실제 오른손
                    if side == "Right":
                        hand_label = "game"          # 두 번째 글자
                        text_color = (255, 255, 0) # 노란색, RGB
                    elif side == "Left":
                        hand_label = "Hand"          # 첫 번째 글자
                        text_color = (255, 0, 255) # 보라색, RGB
                    else:
                        hand_label = ""
                        text_color = (255, 255, 255)

                    if hand_label:
                        put_text_above_hand(
                            frame,
                            hand_lm,
                            hand_label,
                            text_color
                        )

        cv2.imshow("Hand Game - Korean Text", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
