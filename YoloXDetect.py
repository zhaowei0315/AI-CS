root_path = r'C:\yolox'

import sys
sys.path.insert(1, root_path)

import cv2 as cv
import torch
import time
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from tools import Predictor

class ARGS:
    pass
args = ARGS()
args.exp_file = r'C:\YOLOX\exps\default\nano.py'
args.ckpt = r'C:\YOLOX\weights\nano.pth'
args.conf = 0.5
args.device = torch.device("gpu" if torch.cuda.is_available() else "cpu")
args.name = ''
args.fp16 = False
args.legacy = False

exp = get_exp(args.exp_file, args.name)
model = exp.get_model()

if args.device == "gpu":
    model.cuda()
    if args.fp16:
        model.half()

ckpt = torch.load(args.ckpt, map_location=args.device)
model.load_state_dict(ckpt["model"])
model.eval()
predictor = Predictor(model, exp, COCO_CLASSES, None, None, args.device, args.fp16, args.legacy)

def detect(img):
    outputs, img_info = predictor.inference(img)
    if len(outputs) == 0:
        return img, []

    # filter class and keep person only
    class_mask = (outputs[0][:, 6] == 0)
    outputs[0] = outputs[0][class_mask]

    # filter confidence
    conf_mask = (outputs[0][:, 4] >= args.conf)
    outputs[0] = outputs[0][conf_mask]

    if outputs[0].shape[0] != 0:
        result_image = predictor.visual(outputs[0], img_info, args.conf)
    else:
        result_image = img

    return result_image, outputs[0]

if __name__ == "__main__":
    img_path = r'C:\yolov5\data\images\zidane.jpg'
    image = cv.imread(img_path)
    
    start = time.time()
    image, _ = detect(image)
    end = time.time()
    print(end-start)
    
    cv.imshow('Result', image)
    cv.waitKey(0)
    cv.destroyAllWindows()