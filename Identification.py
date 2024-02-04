import detectron2
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2
import threading
import time

class Detectron:
    def __init__(self, threshold):
        self.cfg = get_cfg()
        self.predictor = None
        self.result = None
        self.threshold = threshold

    def configure(self):
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.threshold
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu"

    def get_predictor(self):
        self.predictor = DefaultPredictor(self.cfg)
        return self.predictor

    def predict_on_image(self, img):
        img = cv2.resize(img, (0, 0), None, 0.75, 0.75)
        outputs = self.predictor(img[..., ::-1])
        visualizer = Visualizer(img[..., ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        result = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
        self.result = result
        return result

    def show_result(self):
        cv2.imshow("Result", self.result.get_image()[..., ::-1])
        key = cv2.waitKey(1)
        return key

class VideoProcessor(threading.Thread):
    def __init__(self, video_path, detectron_instance):
        threading.Thread.__init__(self)
        self.video_path = video_path
        self.detectron_instance = detectron_instance

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print("Error in Video")
            return

        while True:
            success, image = cap.read()
            if not success:
                break

            self.detectron_instance.predict_on_image(image)
            key = self.detectron_instance.show_result()
            if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) < 1:
                break

if __name__ == "__main__":
    setup_logger()
    Object = Detectron(0.6)
    Object.configure()
    Object.get_predictor()
    video_path = "video/video1.mp4"
    video_processor = VideoProcessor(video_path, Object)  # Pass Object instance
    video_processor.start()
