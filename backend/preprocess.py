import cv2
import numpy as np

def pil2cv(pil_image):
#    ''' PIL型 -> OpenCV型 '''
        cv_image = np.array(pil_image, dtype=np.uint8)
        if cv_image.ndim == 2:  # モノクロ
            pass
        elif cv_image.shape[2] == 3:  # カラー
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        elif cv_image.shape[2] == 4:  # 透過
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGBA2BGRA)
        return cv_image

def preprocess(img):
  cv_img = pil2cv(img)
  gray_img=0.299*cv_img[:,:,2]+0.587*cv_img[:,:,1]+0.114*cv_img[:,:,0]
  gray_img=np.expand_dims(gray_img,axis=2)
  gray_img=gray_img[:,:]
  resized_gray_img = cv2.resize(gray_img, (640, 640))
  rows = int(10)  # 行数
  cols = int(10)  # 列数

  patches = []
  for row_img in np.array_split(resized_gray_img, rows, axis=0):
    for patch in np.array_split(row_img, cols, axis=1):
      patches.append(patch)
  patches= np.array(patches)
  print(np.shape(patches))
  patches = patches.reshape(100, 64, 64, 1)
  return patches