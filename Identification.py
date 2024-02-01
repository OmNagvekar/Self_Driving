import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
import numpy as np
import os, json, cv2, random
import matplotlib.pyplot as plt


class Detectron:
    def __init__(self,threshold):
        self.cfg = get_cfg()
        self.predictor = None
        self.results = None
        self.threshold=threshold

    def I_S_configure(self):
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.threshold
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu"

    def get_predictor(self):
        self.predictor = DefaultPredictor(self.cfg)
        return self.predictor
    

    def predictOnImage(self,img):
        #img = cv2.imread(image)
        img =cv2.resize(img,(0,0),None,0.75,0.75)
        outputs = self.predictor(img[...,::-1])
        visual = Visualizer(img[...,::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),scale = 1.2)
        result = visual.draw_instance_predictions(outputs["instances"].to("cpu"))
        self.result = result
        return result
    

    def show_result(self):
        cv2.imshow("Result",self.result.get_image()[...,::-1])
        key = cv2.waitKey(1)
        return key
    
    def predictOnVideo(self,video):
        cap = cv2.VideoCapture(video)
        if (cap.isOpened()==False):
            print("Error in Video")
            return
        
        while True:
            (sucess, image)= cap.read()
            
            result = self.predictOnImage(image)
            
            key = self.show_result()
            if key == True:
                break
            
    

if __name__ == "__main__":
        Object = Detectron(0.6)
        Object.I_S_configure()
        Object.get_predictor()
        #Object.predictOnImage(image = './image/4.jpg')
        #Object.show_result()
        Object.predictOnVideo("video/video1.mp4")




