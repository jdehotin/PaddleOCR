import os
import paddle
from operator import index, itemgetter
from paddleocr import PaddleOCR
import natsort as ns
import numpy as np


ocr = PaddleOCR(use_gpu=False, lang="ch", type="structure", det_db_box_thresh=0.05, det_db_thresh=0.05, det_db_unclip_ratio=3.0, max_batch_size=10, use_mp=True)
path = "/Users/vx/Documents/GitHub/BigoneMR/imgs/kano"


for img_path in ns.natsorted(os.listdir(path), reverse=False):
    if img_path.endswith(".jpg"):
        index = str(img_path).strip(".jpg")
        result = ocr.ocr(os.path.join(path, img_path),
                         cls=True)

        texts = []
        if result is not None:
            result = sorted(result, key=lambda x: x[0][0][1])

            num_boxes = np.array(result).shape[0]
            _boxes = result

            for i in range(1, num_boxes):
                if abs(_boxes[i][0][0][1] - _boxes[i - 1][0][0][1]) < 10 and \
                        (_boxes[i-1][0][0][0] > _boxes[i][0][0][0]):
                    tmp = _boxes[i-1]
                    _boxes[i-1] = _boxes[i]
                    _boxes[i] = tmp

            for i in range(1, num_boxes):
                if abs(_boxes[i][0][0][1] - _boxes[i - 1][0][0][1]) < 10 and \
                        (_boxes[i-1][0][0][0] > _boxes[i][0][0][0]):
                    tmp = _boxes[i-1]
                    _boxes[i-1] = _boxes[i]
                    _boxes[i] = tmp

            result = _boxes

            for line in result:
                if line[1][0] is not None:
                    output = open("/Users/vx/Documents/GitHub/PaddleOCR/ppstructure/output/table/26/res.txt", "a+")
                    output.writelines(str(line)+"\n")
                else:
                    texts = "Not recognized"
        else:
            texts = "Not recognized"
