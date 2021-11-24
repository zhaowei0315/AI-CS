# https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.3
# https://www.freesion.com/article/6947771388/
root_path = r'C:\PaddleDetection\deploy\python'

import sys
sys.path.insert(0, root_path)

import time
import cv2 as cv
from det_keypoint_unite_infer import *

class FLAGS:
    pass
FLAGS.camera_id=-1
FLAGS.cpu_threads=1
FLAGS.det_model_dir=r'C:\PaddleDetection\inference_model\picodet_s_320_pedestrian'
FLAGS.det_threshold=0.5
FLAGS.device='CPU'
FLAGS.enable_mkldnn=False
FLAGS.image_dir=None
FLAGS.image_file=r''
FLAGS.keypoint_batch_size=1
FLAGS.keypoint_model_dir=r'C:\PaddleDetection\inference_model\tinypose_256x192'
FLAGS.keypoint_threshold=0.5
FLAGS.output_dir=''
FLAGS.run_benchmark=False
FLAGS.run_mode='fluid'
FLAGS.save_res=False
FLAGS.trt_calib_mode=False
FLAGS.trt_max_shape=1280
FLAGS.trt_min_shape=1
FLAGS.trt_opt_shape=640
FLAGS.use_dark=True
FLAGS.video_file=None

pred_config = PredictConfig(FLAGS.det_model_dir)
detector_func = 'Detector'
if pred_config.arch == 'PicoDet':
    detector_func = 'DetectorPicoDet'

detector = eval(detector_func)(
    pred_config,
    FLAGS.det_model_dir,
    device=FLAGS.device,
    run_mode=FLAGS.run_mode,
    trt_min_shape=FLAGS.trt_min_shape,
    trt_max_shape=FLAGS.trt_max_shape,
    trt_opt_shape=FLAGS.trt_opt_shape,
    trt_calib_mode=FLAGS.trt_calib_mode,
    cpu_threads=FLAGS.cpu_threads,
    enable_mkldnn=FLAGS.enable_mkldnn
)

pred_config = PredictConfig_KeyPoint(FLAGS.keypoint_model_dir)
topdown_keypoint_detector = KeyPoint_Detector(
    pred_config,
    FLAGS.keypoint_model_dir,
    device=FLAGS.device,
    run_mode=FLAGS.run_mode,
    batch_size=FLAGS.keypoint_batch_size,
    trt_min_shape=FLAGS.trt_min_shape,
    trt_max_shape=FLAGS.trt_max_shape,
    trt_opt_shape=FLAGS.trt_opt_shape,
    trt_calib_mode=FLAGS.trt_calib_mode,
    cpu_threads=FLAGS.cpu_threads,
    enable_mkldnn=FLAGS.enable_mkldnn,
    use_dark=FLAGS.use_dark
)

def detect(img):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.predict([img2], FLAGS.det_threshold)
    keypoint_res = predict_with_given_det(
        img2, 
        results, 
        topdown_keypoint_detector, 
        FLAGS.keypoint_batch_size,
        FLAGS.det_threshold, 
        FLAGS.keypoint_threshold, 
        FLAGS.run_benchmark
    )

    im = draw_pose(
            img,
            keypoint_res,
            visual_thread=FLAGS.keypoint_threshold,
            returnimg=True
        )
    
    return im


if __name__ == "__main__":
#     img_path = r'C:\PaddleDetection\demo\hrnet_demo.jpg'
#     image = cv.imread(img_path)
#     
#     start = time.time()
#     image = detect(image)
#     end = time.time()
#     print(end-start)
#     
#     cv.imshow('Result', image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
    
    # 监控摄像头 
    capture = cv.VideoCapture(0)
    while (1):
        ret, image = capture.read()
        image = detect(image)
        cv.imshow('Mask Detection', image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break