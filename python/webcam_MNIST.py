import numpy as np
import cv2
import tensorflow as tf

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

Size = np.shape(img)
model1 = tf.keras.models.load_model('output/model.keras')
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 30)
fontScale = 1
fontColor = (228, 200, 50)
lineType = 2

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = cv2.rectangle(frame, (100, 100), (200, 200), (255, 0, 0), 2)
    I1 = img[100:200, 100:200]
    th, I1 = cv2.threshold(I1, 32, 220, cv2.THRESH_OTSU)
    I = cv2.resize(I1, (28, 28), interpolation=cv2.INTER_AREA)
    I = np.float32(I) / 255
    I = np.abs(1 - I)
    I1 = I[np.newaxis, ..., np.newaxis]  # salida 1x28x28x1
    answer = model1.predict(I1, verbose=0)  # vector de 10 valores
    answer = np.array(answer).ravel()  # [[0.1 0.2 0.3 ... 0.4]]
    clasifica = np.argmax(answer)  # Así obtenemos la posición del valor máximo
    proba = np.max(answer)
    cv2.putText(frame, str(clasifica),
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    cv2.putText(frame, str(proba),
                (10, 60),
                font,
                fontScale,
                fontColor,
                lineType)

    #
    #    img_out = LBP(img, 3)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('ROI', I)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()