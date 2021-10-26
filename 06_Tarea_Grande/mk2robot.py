import numpy as np
from transformations import translation_along_zaxis, \
    rotation_around_zaxis, \
    rotation_around_yaxis
import serial
import time


class MK2Robot:
    HOME_0 = 0
    HOME_1 = np.pi
    HOME_2 = np.pi

    def __init__(self, link_lengths):
        self.a = link_lengths
        self.q = []
        self.T = []
        self.pose = []
        self.update_pose(MK2Robot.HOME_0, MK2Robot.HOME_1, MK2Robot.HOME_2)

    def update_pose(self, q0, q1, q2):
        """
        Este metodo calcula la pose de cada link del robot, usando las matrices T y R. Luego guarda el
        resultado para cada link como un elemento del arreglo self.pose
        """
        # Calcula las matrices T y Q
        self._update_transformation_matrices(q0, q1, q2)

        # re-escribe self.pose como una lista de 4 matrices nulas
        self.pose = [np.zeros((4, 4))] * 4

        self.pose[0] = np.linalg.multi_dot([self.T[0], self.R[0], self.T[1]])
        self.pose[1] = np.linalg.multi_dot([self.pose[0], self.R[1], self.T[2]])
        self.pose[2] = np.linalg.multi_dot([self.pose[1], self.R[2], self.T[3]])
        self.pose[3] = np.linalg.multi_dot([self.pose[2], self.R[3], self.T[4]])

    def _update_transformation_matrices(self, q0, q1, q2):
        """
        Este método calcula las matrices de rotación traslación del modelo de nuestro robot 
        y guarda sus valores como elementos de las listas self.R y self.T, en orden
        """
        q0 = q0 * np.pi / 180
        q1 = q1 * np.pi / 180
        q2 = q2 * np.pi / 180

        self.q = [q0, q1, q2]

        self.T = []
        self.R = []

        angulo_rotacion_l0 = q0
        angulo_rotacion_l1 = q1
        angulo_rotacion_l2 = -np.pi + q2
        angulo_rotacion_l3 = np.pi / 2 - q1 - q2

        # Link 1
        self.T.append(translation_along_zaxis(self.a[0]))
        self.R.append(rotation_around_zaxis(angulo_rotacion_l0))

        # Link 2
        self.T.append(translation_along_zaxis(self.a[1]))
        self.R.append(rotation_around_yaxis(angulo_rotacion_l1))

        # Link 3
        self.T.append(translation_along_zaxis(self.a[2]))
        self.R.append(rotation_around_yaxis(angulo_rotacion_l2))

        # Link 4
        self.T.append(translation_along_zaxis(self.a[3]))
        self.R.append(rotation_around_yaxis(angulo_rotacion_l3))

        # Link 5
        self.T.append(translation_along_zaxis(self.a[4]))

    def inverse_kinematics(self, x, y, z):
        # link_lengths=[55, 39, 135, 147, 66.3]
        l3 = 66.3
        l2 = 147
        l1 = 135
        z0 = 94

        q0_rad = np.arctan(y / x)
        q2_rad = np.arccos(((l1 * np.cos(q0_rad)) ** 2 + (l2 * np.cos(q0_rad)) ** 2 - (x - l3 * np.cos(q0_rad)) ** 2 - (
                z - z0) ** 2) / (2 * l1 * l2 * (np.cos(q0_rad)) ** 2))
        q1_rad = -np.arctan((x - l3 * np.cos(q0_rad)) / (z - z0)) + np.arccos(((l1 * np.cos(q0_rad)) ** 2 + (
                x - l3 * np.cos(q0_rad)) ** 2 + (z - z0) ** 2 - (l2 * np.cos(q0_rad)) ** 2) / (2 * l1 * np.cos(
            q0_rad) * np.sqrt(x ** 2 + z ** 2)))
        if z < 94:  # Experimentalmente funciona :)
            q1_rad = q1_rad - np.pi

        q0 = np.round(q0_rad * 180 / np.pi, 0)
        q1 = np.round(q1_rad * 180 / np.pi, 0)
        q2 = np.round(q2_rad * 180 / np.pi, 0)
        return [q0, q1, q2]

    def forward_kinematics(self, ang, q0=False, q1=False, q2=False, q3=False):
        if q0:
            angleData = str(int(abs(2 * ang)))
            ser.write(('&1:' + angleData).encode())
            time.sleep(0.02)
        elif q1:
            angleData = str(int(abs(ang)))
            ser.write(('&2:' + angleData).encode())
            time.sleep(0.02)
        elif q2:
            angleData = str(int(abs(ang)))
            ser.write(('&3:' + angleData).encode())
            time.sleep(0.02)
        elif q3:
            angleData = str(int(abs(ang)))
            ser.write(('&4:' + angleData).encode())
            time.sleep(0.02)

    def run_serial(self, COM):
        # BLOQUE SERIAL
        global ser
        ser = serial
        try:
            ser = serial.Serial(str(COM), 115200, timeout=1)  # ojito con la ruta
            # ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
            serial_port = "Open"
            print("The port is available")

        except serial.serialutil.SerialException:
            print("The port is at use")
            ser.close()
            ser.open()
        # BLOQUE SERIAL

    def get_joint_positions(self):
        """Este método entrega las coordenadas de cada joint en tres listas; es para que el codigo se vea mas limpio :)"""
        X_pos = np.zeros(4)
        Y_pos = np.zeros(4)
        Z_pos = np.zeros(4)

        for i in range(len(self.pose)):
            X_pos[i] = np.round(self.pose[i][0, 3], 3)
            Y_pos[i] = np.round(self.pose[i][1, 3], 3)
            Z_pos[i] = np.round(self.pose[i][2, 3], 3)

        return [X_pos, Y_pos, Z_pos]
