# https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.3
# https://www.freesion.com/article/6947771388/
root_path = r'C:\PaddleDetection\deploy\python'

import sys
sys.path.insert(0, root_path)

import time
import cv2 as cv
from infer import *

class FLAGS:
    pass
FLAGS.model_dir=r'C:\PaddleDetection\inference_model\faster_rcnn_swin_tiny_fpn_1x_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\faster_rcnn_swin_tiny_fpn_2x_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\faster_rcnn_swin_tiny_fpn_3x_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_l_320_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_l_416_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_l_640_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_m_320_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_m_416_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_s_320_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_s_416_coco'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_s_192_pedestrian'
# FLAGS.model_dir=r'C:\PaddleDetection\inference_model\picodet_s_320_pedestrian'
FLAGS.batch_size=1
FLAGS.camera_id=-1
FLAGS.cpu_threads=1
FLAGS.device='CPU'
FLAGS.enable_mkldnn=False
FLAGS.image_dir=None
FLAGS.image_file=None
FLAGS.output_dir='output'
FLAGS.reid_batch_size=50
FLAGS.reid_model_dir=None
FLAGS.run_benchmark=False
FLAGS.run_mode='fluid'
FLAGS.save_images=False
FLAGS.save_mot_txt_per_img=False
FLAGS.save_mot_txts=False
FLAGS.scaled=False
FLAGS.threshold=0.5
FLAGS.trt_calib_mode=False
FLAGS.trt_max_shape=1280
FLAGS.trt_min_shape=1
FLAGS.trt_opt_shape=640
FLAGS.use_dark=True
FLAGS.use_gpu=False
FLAGS.video_file=None

pred_config = PredictConfig(FLAGS.model_dir)
detector_func = 'Detector'
if pred_config.arch == 'SOLOv2':
    detector_func = 'DetectorSOLOv2'
elif pred_config.arch == 'PicoDet':
    detector_func = 'DetectorPicoDet'

detector = eval(detector_func)(
    pred_config,
    FLAGS.model_dir,
    device=FLAGS.device,
    run_mode=FLAGS.run_mode,
    batch_size=FLAGS.batch_size,
    trt_min_shape=FLAGS.trt_min_shape,
    trt_max_shape=FLAGS.trt_max_shape,
    trt_opt_shape=FLAGS.trt_opt_shape,
    trt_calib_mode=FLAGS.trt_calib_mode,
    cpu_threads=FLAGS.cpu_threads,
    enable_mkldnn=FLAGS.enable_mkldnn
)

def detect(img):
    results = detector.predict([image], FLAGS.threshold)
    im = visualize_box_mask(
        image,
        results,
        detector.pred_config.labels,
        threshold=FLAGS.threshold
    )
    return np.array(im)


if __name__ == "__main__":
    img_path = r'C:\yolov5\data\images\zidane.jpg'
    image = cv.imread(img_path)
    
    start = time.time()
    image = detect(image)
    end = time.time()
    print(end-start)
    
    cv.imshow('Result', image)
    cv.waitKey(0)
    cv.destroyAllWindows()