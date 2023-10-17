import numpy as np
import cv2
import keras

# Declaramos la red a utilizar, su rutina de preprocesamiento y decodificación de resultado
# Cada red se baja en automatico de internet y se guarda en la instalación de keras en su primer uso
# catalogo de redes disponibles https://keras.io/api/applications/
# A mayor cantidad de parámetros mas procesamiento, si hay GPU disponible en automatico se usará

from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input, decode_predictions

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

Size = np.shape(img)
# Cargamos modelo previamente entrenado, con los pesos del aprendizaje con base de datos ImageNet
# Las clases con su nombre están en el archivo IMAGENET_labels.py
model1 = Xception(weights='imagenet')

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 30)
fontScale = 1
fontColor = (0, 0, 250)
lineType = 2

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Our operations on the frame come here

    # Haremos recorte de 200x200, que será reescalado a 299x299 que es la entrada
    # para la red Xception, cada red tiene su tamaño de entrada predefinido
    frame = cv2.rectangle(frame, (100, 100), (300, 300), (255, 0, 0), 2)
    I1 = img[100:300, 100:300, :]
    I = cv2.resize(I1, (299, 299), interpolation=cv2.INTER_AREA)
    # Agregamos dimensión adicional para que nuestra imagen sea 1x299x299x3
    I = np.expand_dims(I, axis=0)
    # Cada red tiene su rutina antes de la clasificación, puede ser mejora de contraste
    # emborronamientos o rangos distintos (0 a 1, 1 a -1, 0 a 255, etc)
    I = preprocess_input(I)  # Preprocess y decode son propios de cada red, estan declarados en linea 12
    preds = model1.predict(I, verbose=0)  # predicción entrega vector de 1000 valores
    # Seleccionamos la mas alta, x será un listado de 3 valores, indicando el numero de categoria, texto y probabilidad
    x = decode_predictions(preds, top=1)[0]
    # Seleccionamos solamente el texto de la categoria clasificada
    y = x[0]

    # Agregamos como texto la categoria clasificada
    cv2.putText(frame, y[1],
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
