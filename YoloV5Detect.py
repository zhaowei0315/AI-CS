root_path = r'C:\yolov5'
ckpt_path = r'C:\yolov5\weights\yolov5m.pt'

import sys
sys.path.insert(1, root_path)

import numpy as np
import cv2 as cv
import time
from torchvision import transforms
from utils.general import non_max_suppression
from models.experimental import attempt_load
from utils.plots import Annotator, colors

IMG_SIZE = (640, 640)
tf = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor()
])


model = attempt_load(ckpt_path)
model.eval()
names = model.names


def detect(img):
    if isinstance(img, str):
        raw_img = cv.imread(img)
    else:
        raw_img = img
        
    h, w, _ = raw_img.shape
    scale_h, scale_w = h / IMG_SIZE[1], w / IMG_SIZE[0]

    img_tensor = tf(raw_img)
    pred = model(img_tensor[None])[0]
    pred = non_max_suppression(pred,0.3,0.5)

    annotator = Annotator(np.ascontiguousarray(raw_img), line_width=1, example=str(names))
    for boxes in pred[:1]:
        for *xyxy, conf, cls in reversed(boxes):
            c = int(cls)
            if c != 0:# 0 means person
                continue
            label = f'{names[c]} {conf:.2f}'
            
            xyxy[0], xyxy[1] = int(xyxy[0] * scale_w), int(xyxy[1] * scale_h)
            xyxy[2], xyxy[3] = int(xyxy[2] * scale_w), int(xyxy[3] * scale_h)

            annotator.box_label(xyxy, label, color=colors(c, True))
    img = annotator.result()
    return raw_img


if __name__ == "__main__":
    img_path = r"C:\yolov5\data\images\zidane.jpg"
    image = cv.imread(img_path)

    start = time.time()
    image = detect(image)
    end = time.time()
    print(end-start)

    cv.imshow('Result', image)
    cv.waitKey(0)
    cv.destroyAllWindows()