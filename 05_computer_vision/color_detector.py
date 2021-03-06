import cv2
import numpy as np


class ColorDetector:

    def __init__(self, img):
        self.img = img

        # Inicializamos en cero todas las imagenes que guardaremos
        self.mask = np.zeros(img.shape)
        self.img_masked = np.zeros(img.shape)
        self.img_eroded = np.zeros(img.shape)
        self.img_dilated = np.zeros(img.shape)
        self.img_filtered = np.zeros(img.shape)
        self.img_gray = np.zeros(img.shape)
        self.img_threshold = np.zeros(img.shape)
        self.img_contoured = np.zeros(img.shape)

    def process_image(self, lower_color, upper_color, kernel, threshold):
        self.mask_image(lower_color, upper_color)
        self.filter_image(kernel)
        self.draw_contours(threshold)

    def mask_image(self, lower_color, upper_color):
        print("mask_image: implementame :c")

    def filter_image(self, kernel):
        print("filter_image: implementame :c")


    def draw_contours(self, threshold):
        """
        Para hacer esta función se deben seguir los siguientes pasos:
        1. convertir una imagen filtrada a escala de grises
        2. aplicar un umbral (threshold). Se sugiere truncado: type=cv2.THRESH_TRUNC
        3. usar la funcion cv2.findContours:
            contours, hierarchy = cv2.finContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        4. copiar la imagen original
        5. usar cv2.drawContours(img, contours, -1, color=(0, 255,0), thickness=4)
        Para mas info, consultar
        https://learnopencv.com/contour-detection-using-opencv-python-c/
        """
        print("draw_contours: implementame :c")


    def draw_bounding_boxes(self):
        """
        [Propuesto]
        1. Con el resultado de los contornos del metodo anterior,
        encontrar aquellos contornos cuya area encerrada sea superior a un
        numero arbitrario (por ej: 900 pixeles).

        2. Luego, iterar sobre cada grupo de contornos y usar las
        funciones cv2.boundingRect y cv2.rectangle:

         Mas o menos así
            for contour in contours:
                  x, y, w, h = cv2.boundingRect(contour)
                  cv2.rectangle(img, (x1, y1), (x2, y2), COLOR, line_width)

        Ojo que cv2.boundingRect entrega un origen (x, y) y el alto y ancho
        del rectangulo, pero cv2.rectangle toma dos esquinas opuestas como
        argumentos.

        """
        print("draw_bounding_boxes: implementame :c")
