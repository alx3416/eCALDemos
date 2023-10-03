
import time
import tkinter
from tkinter import *
import sys

import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
import proto.mensaje_main_pb2 as mensaje_main_pb2
import lz4.frame


# Clase principal que contendrá todos los llamados
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # Activa webcam
        self.vid = MyVideoCapture(self.video_source)
        ecal_core.initialize(sys.argv, "Python webcam Publisher")

        self.pub = ProtoPublisher("webcam_data",
                             mensaje_main_pb2.webcam)
        self.protobuf_message = mensaje_main_pb2.webcam()

        # tomamos características de frame para construir panel
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack(side=TOP)

        # Botón para guardar snapshots
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=128, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.S, expand=True)

        # Botón para original
        self.btn_orig = tkinter.Button(window, text="Original", width=128, command=self.orig_image)
        self.btn_orig.pack(anchor=tkinter.CENTER, expand=False)

        # Botón para bordes
        icon5 = PIL.ImageTk.PhotoImage(file="gui_files/edges.png")
        self.btn_edge = tkinter.Button(window, image=icon5, width=64, command=self.edge_image)
        self.btn_edge.pack(side=LEFT)

        # Botón para blurring
        icon1 = PIL.ImageTk.PhotoImage(file="gui_files/blur.png")
        self.btn_blur = tkinter.Button(window, image=icon1, width=64, command=self.blur_image)
        #        self.btn_blur.pack(anchor=tkinter.W, expand=True)
        self.btn_blur.pack(side=LEFT)
        # Botón para Hough rectas
        icon2 = PIL.ImageTk.PhotoImage(file="gui_files/lines.png")
        self.btn_lines = tkinter.Button(window, image=icon2, width=64, command=self.lines_image)
        self.btn_lines.pack(side=LEFT)

        # Botón para Laplaciano
        icon3 = PIL.ImageTk.PhotoImage(file="gui_files/laplacian.png")
        self.btn_grad = tkinter.Button(window, image=icon3, width=64, command=self.grad_image)
        self.btn_grad.pack(side=LEFT)

        # Botón para circulos
        icon6 = PIL.ImageTk.PhotoImage(file="gui_files/circles.png")
        self.btn_circles = tkinter.Button(window, image=icon6, width=64, command=self.circles_image)
        self.btn_circles.pack(side=LEFT)

        # Checkbox para eCAL
        self.checkbox_ecal = tkinter.BooleanVar()
        self.chkbox_ecal = tkinter.Checkbutton(window, text='eCAL Send', variable=self.checkbox_ecal)
        self.chkbox_ecal.pack(side=LEFT)

        # Después de ser llamado 1 ves, el método esperará un delay y repetirá el proceso
        self.delay = 1  # en milisegundos
        self.proc = 1
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Callback para botón de snapshot
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def orig_image(self):
        self.proc = 1

    def edge_image(self):
        self.proc = 2

    def blur_image(self):
        self.proc = 3

    def lines_image(self):
        self.proc = 4

    def grad_image(self):
        self.proc = 5

    def circles_image(self):
        self.proc = 6

    def update(self):
        # toma nuevo frame de webcam
        ret, frame = self.vid.get_frame()

        if ret:
            if self.proc == 1:  # Caso original
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            elif self.proc == 2:  # Caso bordes
                frame = cv2.Canny(frame, 75, 150)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            elif self.proc == 3:
                frame = cv2.blur(frame, (7, 7))
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            elif self.proc == 4:
                cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cimg = cv2.medianBlur(cimg, 7)
                #    cimg = cv2.bilateralFilter(cimg,11,25,25)
                edges = cv2.Canny(cimg, 75, 150)
                lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, maxLineGap=50)
                if lines is not None:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            elif self.proc == 5:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.medianBlur(frame, 7)
                G = cv2.Laplacian(frame, cv2.CV_64F)
                frame = ((G - G.min()) / (G.max() - G.min())) * 255
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            elif self.proc == 6:
                cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cimg = cv2.medianBlur(cimg, 7)
                #    cimg = cv2.bilateralFilter(cimg,11,25,25)
                edges = cv2.Canny(cimg, 75, 150)
                circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 50,
                                           param1=80, param2=30, minRadius=30, maxRadius=70)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0, :]:
                        # draw the outer circle
                        cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        # draw the center of the circle
                        cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            else:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

        # If activated, send ecal message
        if self.checkbox_ecal.get():
            # eCAL-protobuff related
            self.protobuf_message.frame.height = frame.shape[0]
            self.protobuf_message.frame.width = frame.shape[1]
            self.protobuf_message.frame.name = "logitech C920"
            self.compress_image(frame, 'JPEG')
            self.pub.send(self.protobuf_message)

        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

    def compress_image(self, img, compression):
        if compression == 'UNCOMPRESSED':
            self.protobuf_message.frame.data = img.data.tobytes()
        elif compression == 'JPEG':
            _, image_bytes = cv2.imencode('.jpg', img)
            self.protobuf_message.frame.data = image_bytes.tobytes()
        elif compression == 'LZ4':
            self.protobuf_message.frame.data = lz4.frame.compress(img.data.tobytes())
        self.protobuf_message.frame.imagecompression = (
            mensaje_main_pb2.mensaje__data__pb2.compression.Value(compression))
        self.protobuf_message.frame.imageformat = (
            mensaje_main_pb2.mensaje__data__pb2.format.Value('RGB'))


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Se prueba fuente de video
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("No fue posible encontrar objeto de video", video_source)

        # Tomamos dimensiones de video
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        ret = False
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Si existe captura de webcam, convierte de BGR a RGB
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Al cerrar la ventana debe desactivar la webcam
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Crea ventana y pasa los parámetros para su creación
App(tkinter.Tk(), "Tkinter y OpenCV")
