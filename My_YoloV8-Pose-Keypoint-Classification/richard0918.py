import cv2
import streamlit as st
import numpy as np

from PIL import Image

from My_src.detection_keypoint import DetectKeypoint
from My_src.classification_keypoint import KeypointClassification

import datetime
check_time = datetime.datetime.now()
from check_pose0918 import check_pose
cp = check_pose()

# import time

# Streamlit設定
st.set_page_config(
    layout="wide",
    page_title="Real-time Webcam Stream",
)
st.title("Real-time Webcam Stream")

# 開始捕獲攝像頭畫面stream
video_capture = cv2.VideoCapture(0)  # 0表示預設攝像頭

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 設定寬度
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 設定高度
video_capture.set(cv2.CAP_PROP_FPS, 30)  # 設定幀速率

# 設定要減小的畫面大小
new_width = 828  # 新的寬度
new_height = 621  # 新的高度

# 初始化關鍵點檢測和分類模型
detection_keypoint = DetectKeypoint()
classification_keypoint = KeypointClassification(
    './My_models/My_pose_classification.pt'
)

# Create layout
#canvMain = st.empty()
can1, can2, can3 = st.columns(3)

ph1 = can1.empty()
ph2 = can2.empty()
ph3 = can3.empty()

# 創建一個用於顯示攝像頭畫面的Streamlit元素
#frame_placeholder = st.empty()
#frame_placeholder = st.container()

while True:

    ret, frame = video_capture.read()  # 讀取攝像頭畫面
    if not ret:
        break

    # 調整畫面大小
    frame = cv2.resize(frame, (new_width, new_height))

    # 進行關鍵點檢測
    image_cv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 將畫面轉換為RGB格式
    try:
        results = detection_keypoint(image_cv)  # 使用關鍵點檢測模型進行檢測
        # if "keypoints" not in results._keys:  # 檢查是否存在關鍵點
        #     # 如果未檢測到關鍵點，繼續顯示攝像頭畫面並跳過後面的處理
        #     ph2.image(frame, channels="RGB", use_column_width=False)
        #     continue

        # 獲取關鍵點信息
        results_keypoint = detection_keypoint.get_xy_keypoint(results)

        # 進行姿勢分類
        input_classification = results_keypoint[10:]  # 選取用於分類的部分
        results_classification = classification_keypoint(input_classification)  # 使用關鍵點分類模型進行分類

        # 可視化結果
        image_draw = results.plot(boxes=False)  # 根據檢測結果繪製圖像

        # if len(results.boxes.xyxy) > 0:
        #     x_min, y_min, x_max, y_max = results.boxes.xyxy[0].numpy()  # 獲取檢測框的座標
        # # 繼續處理
        # else:
        # # 如果沒有檢測到任何框，可以執行一些處理
        #     x_min, y_min, x_max, y_max = 0, 0, 0, 0  # 或者根據需要設置其他預設值

        x_min, y_min, x_max, y_max = results.boxes.xyxy[0].numpy()  # 獲取檢測框的座標
        image_draw = cv2.rectangle(
            image_draw,
            (int(x_min), int(y_min)), (int(x_max), int(y_max)),
            (0, 0, 255), 2
        )  # 在圖像上繪製檢測框
        (w, h), _ = cv2.getTextSize(
            results_classification.upper(),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
        )  # 獲取文本的大小
        image_draw = cv2.rectangle(
            image_draw,
            (int(x_min), int(y_min) - 20), (int(x_min) + w, int(y_min)),
            (0, 0, 255), -1
        )  # 繪製文本背景框
        image_draw = cv2.putText(image_draw,
                                f'{results_classification.upper()}',
                                (int(x_min), int(y_min) - 4),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255),
                                thickness=2
                                )  # 在圖像上添加文本

        # 顯示攝像頭畫面
        #frame_placeholder.image(image_draw, channels="RGB", use_column_width=False)
        ph2.image(image_draw, channels="RGB", use_column_width=True)
    
    except IndexError:
        ph2.image(image_cv, channels="RGB", use_column_width=True)
    
    # time.sleep(1)

    # on left, display standard pose image, according to predit rsult   
    image = Image.open("./My_images/2.jpeg")
    ph1.image(image, caption="標準姿勢", use_column_width=True)

    # on right display check function
    d = datetime.datetime.now() - check_time
    if d.seconds > 5:
        check_time = datetime.datetime.now()
        ph3.markdown(cp.check(results_classification.upper(),results_keypoint), unsafe_allow_html = True)


# 關閉攝像頭
video_capture.release()
