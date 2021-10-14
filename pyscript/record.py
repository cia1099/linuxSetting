import pyrealsense2 as rs
import numpy as np
import cv2
import sys, os, glob, shutil,time
import json
import argparse
from pathlib import Path
from enum import IntEnum


FRAME_MAX = 99999

class Preset(IntEnum):
    Custom = 0
    Default = 1
    Hand = 2
    HighAccuracy = 3
    HighDensity = 4
    MediumDensity = 5

def get_predictor(cfg, model_name: str, threshold:float=0.7):
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, model_name)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold  # set the testing threshold for this model
    predictor = DefaultPredictor(cfg)
    return predictor

def record(write_dir:str, fps=30,fillhole=False,predictor=None):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)
    # note: using 640 x 480 depth resolution produces smooth depth boundaries
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, fps)
    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, fps)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, fps)
    # Start streaming
    profile = pipeline.start(config)

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset, Preset.HighAccuracy)
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: ", depth_scale)
    #  clipping_distance_in_meters meters away
    clipping_distance_in_meters = 3  # 3 meter
    clipping_distance = clipping_distance_in_meters / depth_scale
    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)
    # camera intrinsic
    # intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

    # Filters
    hole_filter = rs.hole_filling_filter(2) if fillhole else None

    goningLoop = True
    capture = False
    frame = 0
    cv2.namedWindow('RGBD capture', cv2.WINDOW_NORMAL)
    while goningLoop:
        tic = time.time()
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()
        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue
        if hole_filter is not None:
            aligned_depth_frame = hole_filter.process(aligned_depth_frame)
        depth = np.asanyarray(aligned_depth_frame.get_data())
        image = np.asanyarray(color_frame.get_data())
        if capture:
            if frame == 0:
                # write path
                if os.path.exists(write_dir):
                    shutil.rmtree(write_dir, ignore_errors=True)
                os.makedirs(write_dir)
                image_dir = os.path.join(write_dir, 'image')
                depth_dir = os.path.join(write_dir, 'depth')
                os.makedirs(image_dir)
                os.makedirs(depth_dir)
                intr = color_frame.profile.as_video_stream_profile().intrinsics
                K_rowmajor = [intr.fx, 0, 0, 0, intr.fy, 0, intr.ppx, intr.ppy, 1]
                cam_dict = {'width': intr.width, 'height': intr.height, 'intrinsic_matrix': K_rowmajor}
                with open(os.path.join(write_dir, 'camera.json'), 'w') as f:
                    json.dump(cam_dict, f, indent=4)
            frame += 1
            if frame > FRAME_MAX:
                print(f'recording frames have exceeded MAX_FRAME({FRAME_MAX}:05d)')
                capture ^= True
                frame = 0
            else:
                cv2.imwrite(os.path.join(depth_dir, f'depth{frame:05d}.png'), depth)
                cv2.imwrite(os.path.join(image_dir, f'image{frame:05d}.png'), image)

        dd = depth.astype(float)
        depth8 = np.array(255 * (dd - np.min(dd)) / (np.max(dd) - np.min(dd)), dtype=image.dtype)
        depth8 = cv2.cvtColor(depth8, cv2.COLOR_GRAY2BGR)

        #----show record
        img = image.copy()
        if predictor is not None and not capture:
            outputs = predictor(img)
            RGB = Visualizer(img[:,:,::-1],metadata=MetadataCatalog.get("dataset_train"),instance_mode=ColorMode.IMAGE_BW)
            instances = outputs["instances"].to("cpu")
            out = RGB.draw_instance_predictions(instances)
            img[:] = out.get_image()[:,:,::-1][:]
            D = Visualizer(depth8,metadata=MetadataCatalog.get("dataset_train"),instance_mode=ColorMode.IMAGE_BW)
            depth8[:] = D.draw_instance_predictions(instances).get_image()[:,:,::-1][:]

        toc = time.time()
        display_txt = f'record: {frame:05d}' if capture else f'FPS: {round(1/(toc-tic)):d}'
        cv2.putText(img, display_txt,(40,60),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0),4)
        hstack = np.concatenate([img, depth8], axis=1)
        cv2.imshow('RGBD capture', hstack)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            goningLoop = False
        elif key == ord('r'):
            capture ^= True
            frame = 0

    pipeline.stop()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir_name',type=str,required = True,help='Desired write directory name')
    parser.add_argument('-f','--fill_hole',action='store_true',default=False,help='Turn on/off filling hole algorithm for depth data')
    parser.add_argument('--MRcnn_weight',type=str,default='',help='predict object before recording')
    parser.add_argument('-th','--threshold',type=float,default=0.8,help='detection model used threshold')
    args = parser.parse_args()

    write_dir = args.dir_name
    if len(write_dir.split('/')) == 1:
        write_dir = os.path.join(os.getcwd(),args.dir_name)
    print('Record files will write in folder:\n{}\n'.format(write_dir))
    predictor = None
    model_path = Path(args.MRcnn_weight)
    if model_path.is_file():
        from detectron2.config import get_cfg
        from detectron2.model_zoo import model_zoo
        from detectron2.data import MetadataCatalog
        from detectron2.utils.visualizer import Visualizer, ColorMode
        from detectron2.engine import DefaultPredictor
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
        cfg.MODEL.DEVICE = 'cuda'
        cfg.OUTPUT_DIR = str(model_path.parent)
        print('Inference by model of {}'.format(model_path.name))
        train_list = ['table','picture','bed','laptop','camera']
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(train_list)
        MetadataCatalog.get('dataset_train').set(thing_classes=train_list, stuff_classes=[])
        predictor = get_predictor(cfg,model_path.name,float(np.clip(args.threshold,0,1)))

    record(write_dir, 30,fillhole=args.fill_hole,predictor=predictor)
