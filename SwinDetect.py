# How to install Swin
# pip install mmcv-full
# git clone https://github.com/SwinTransformer/Swin-Transformer-Object-Detection
# cd Swin-Transformer-Object-Detection-master
# pip install -r requirements/build.txt
# pip install -v -e .

from mmdet.apis import inference_detector, init_detector
import cv2 as cv
import time
import torch

# config_file = r'C:\swin\configs\mask_rcnn\mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py'
# checkpoint_file = r'C:\swin\weights\mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'

# config_file = r'C:\swin\configs\faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
# checkpoint_file = r'C:\swin\weights\faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'

# if with CPU，you need to replace "SyncBN" with "BN" in config_file
# config_file = r'C:\swin\configs\swin\cascade_mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco.py'
# checkpoint_file = r'C:\swin\weights\cascade_mask_rcnn_swin_tiny_patch4_window7.pth'

# if with CPU，you need to replace "SyncBN" with "BN" in config_file
# config_file = r'C:\swin\configs\swin\cascade_mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_1x_coco.py'
# checkpoint_file = r'C:\swin\weights\cascade_mask_rcnn_swin_tiny_patch4_window7_1x.pth'

# if with CPU，you need to replace "SyncBN" with "BN" in config_file
# config_file = r'C:\swin\configs\swin\cascade_mask_rcnn_swin_small_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco.py'
# checkpoint_file = r'C:\swin\weights\cascade_mask_rcnn_swin_small_patch4_window7.pth'

# config_file = r'C:\swin\configs\swin\mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_adamw_3x_coco.py'
# checkpoint_file = r'C:\swin\weights\mask_rcnn_swin_tiny_patch4_window7.pth'

# config_file = r'C:\swin\configs\swin\mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_adamw_1x_coco.py'
# checkpoint_file = r'C:\swin\weights\mask_rcnn_swin_tiny_patch4_window7_1x.pth'

config_file = r'C:\swin\configs\swin\mask_rcnn_swin_small_patch4_window7_mstrain_480-800_adamw_3x_coco.py'
checkpoint_file = r'C:\swin\weights\mask_rcnn_swin_small_patch4_window7.pth'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = init_detector(config_file, checkpoint_file, device=device)# cuda:0

def detect(img):
    result = inference_detector(model, img)
    return model.show_result(
                img,
                result,
                score_thr=.5,
                show=False,
                wait_time=0,
                win_name='result',
                bbox_color=(72, 101, 241),
                text_color=(72, 101, 241)
    )
 
if __name__ == "__main__":

#     img_path = r"C:\swin\demo\demo.jpg"
    img_path = r"C:\yolov5\data\images\zidane.jpg"
    image = cv.imread(img_path)
 
    start = time.time()
    image = detect(image)
    end = time.time()
    print(end-start)
 
    cv.imshow('Result', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

        
        
        