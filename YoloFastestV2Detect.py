root_path = r'C:\yolo_fastest_v2'

import sys

sys.path.insert(1, root_path)

import os
import cv2 as cv
import time

import torch
import model.detector
import utils.utils

data = os.path.join(root_path, 'data','coco.data')
weights = os.path.join(root_path, 'modelzoo','coco2017-0.241078ap-model.pth')

# 模型加载
cfg = utils.utils.load_datafile(data)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.detector.Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
model.load_state_dict(torch.load(weights, map_location=device))
model.eval()


def detect(img):
    if isinstance(img, str):
        raw_img = cv.imread(img)
    else:
        raw_img = img

    # 数据预处理
    res_img = cv.resize(raw_img, (cfg["width"], cfg["height"]), interpolation=cv.INTER_LINEAR)
    img = res_img.reshape(1, cfg["height"], cfg["width"], 3)
    img = torch.from_numpy(img.transpose(0, 3, 1, 2))
    img = img.to(device).float() / 255.0

    # 模型推理
    preds = model(img)

    # 特征图后处理
    output = utils.utils.handel_preds(preds, cfg, device)
    output_boxes = utils.utils.non_max_suppression(output, conf_thres=0.3, iou_thres=0.4)

    # 加载label names
    LABEL_NAMES = []
    with open(os.path.join(root_path, cfg["names"]), 'r') as f:
        for line in f.readlines():
            LABEL_NAMES.append(line.strip())

    h, w, _ = raw_img.shape
    scale_h, scale_w = h / cfg["height"], w / cfg["width"]

    # filter class and keep person only
    class_mask = (output_boxes[0][:, 5] == 0)
    output_boxes[0] = output_boxes[0][class_mask]

    # filter confidence
    conf_mask = (output_boxes[0][:, 4] >= 0.7)
    output_boxes[0] = output_boxes[0][conf_mask]

    output = []
    for box in output_boxes[0]:
        box = box.tolist()
        obj_score = box[4]
        category = LABEL_NAMES[int(box[5])]

        x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
        x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)
        output.append([x1, y1, x2, y2, obj_score])

        cv.rectangle(raw_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
        #         cv.putText(raw_img, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)
        cv.putText(raw_img, category + ':%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)

    return raw_img, output


if __name__ == "__main__":
    img_path = r'C:\yolov5\data\images\zidane.jpg'
    image = cv.imread(img_path)

    start = time.time()
    image, _ = detect(image)
    end = time.time()
    print(end - start)

    cv.imshow('Result', image)
    cv.waitKey(0)
    cv.destroyAllWindows()
