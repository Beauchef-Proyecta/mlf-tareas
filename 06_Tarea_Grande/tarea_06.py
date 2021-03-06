import cv2
import matplotlib.pyplot as plt
import numpy as np

from shape_detector import ShapeDetector
from decision import Manager
from mk2robot import MK2Robot
from plotter import Plotter


def main():

    """ [1. Inicialización]
    Todo sistema de robots tiene varios subsistemas, cada cual con una responsabilidad única
    y funcionan de manera coordinada.
    En este caso, tenemos 5 sub-sistemas:
    1. camera: responsable de operar la cámara
    2. detector: procesa la imagen obtenida por el subsitema camera y entrega información útil para saber qué hacer con el robot
    3. manager: implementa una "estrategia" según lo que se detecta y genera una instrucción (command) para que el robot la ejecute
    4. robot: recibe la instrucción y la ejecuta (por sus propios medios)
    5. plotter: muestra lo que está pasando. No es esencial para el funcionamiento, pero nos permite a les humanes cachar qué está pasando o.o
    """
    camera = cv2.VideoCapture(2)  # Usar la que tengan disponible en su pc; por defecto es 0
    detector = ShapeDetector()
    manager = Manager()
    robot = MK2Robot(link_lengths=[55, 39, 135, 147, 66.3])
    plotter = Plotter()



    """ [2. Loop Infinito]
    Teniendo los objetos inicializados, mientras Plotter esté activado (plotter.is_enabled() == True), 
    el programa hará lo siguiente:
    1. Capturar una imagen
    2. Procesarla
    3. Decidir qué debe hacer el robot
    4. Ejecuta la acción
    5. Mostrar el resultado en un entorno de simulación
    """
    while plotter.is_enabled():
        
        # 1. Capturar imagen
        _, frame = camera.read()

        # 2. Procesar
        detector.update_image(frame)
        detector.process_image()
        shape = detector.whichShape()
        
        # 3. Decidir
        command, text = manager.decide_what_to_do(shape)
        
        # 4. Actuar
        robot.execute(command, text)

        # 5. Mostrar resultado
        processed_image = detector.img
        robot_pose = robot.current_joint_positions()
        plotter.update(img=processed_image, robot=robot_pose)
    
    # Una vez que se cierra el plot, se destruye todo para tener una salida limpia :)
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
