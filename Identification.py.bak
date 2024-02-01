from detectron2.utils.logger import setup_logger
setup_logger()

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
import numpy as np
import  cv2

class Detectron:
    def __init__(self):
        self.cfg = get_cfg()
        self.predictor = None
        self.results = None

    def I_S_configure(self,threshold):
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold 
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu"

    def get_predictor(self):
        self.predictor = DefaultPredictor(self.cfg)
        return self.predictor
    

    def predict(self,image):
        img = cv2.imread(image)
        outputs = self.predictor(img[...,::-1])
        visual = Visualizer(img[...,::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),scale = 1.2)
        result = visual.draw_instance_predictions(outputs["instances"].to("cpu"))
        self.result = result
    

    def show_result(self):
        cv2.imshow("Result",self.result.get_image()[...,::-1])
        cv2.waitKey(0)

if __name__ == "__main__":
        Object = Detectron()
        Object.I_S_configure(0.5)
        Object.get_predictor()
        Object.predict(image = './image/2.jpeg')
        Object.show_result()




