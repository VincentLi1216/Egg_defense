import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法

cap = cv2.VideoCapture(1)


def distance(x1, y1, x2, y2):
    return math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))


# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, img = cap.read()
        size = img.shape   # 取得攝影機影像尺寸
        w = size[1]        # 取得畫面寬度
        h = size[0]        # 取得畫面高度
        if not ret:
            print("Cannot receive frame")
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        results = hands.process(img2)                 # 偵測手掌
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 將節點和骨架繪製到影像中
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                x8 = hand_landmarks.landmark[8].x * w  # 取得食指末端 x 座標
                y8 = hand_landmarks.landmark[8].y * h  # 取得食指末端 y 座標
                x4 = hand_landmarks.landmark[4].x * w  # 取得食指末端 x 座標
                y4 = hand_landmarks.landmark[4].y * h  # 取得食指末端 y 座標
                x0 = hand_landmarks.landmark[0].x * w  # 取得食指末端 x 座標
                y0 = hand_landmarks.landmark[0].y * h  # 取得食指末端 y 座標
                x5 = hand_landmarks.landmark[5].x * w  # 取得食指末端 x 座標
                y5 = hand_landmarks.landmark[5].y * h  # 取得食指末端 y 座標
                if distance(x8, y8, x4, y4)/distance(x0, y0, x5, y5) <= 0.2:
                    print(f'tapped{x8}')
                # print(distance(x8, y8, x4, y4)/distance(x0, y0, x5, y5))

        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break    # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()
