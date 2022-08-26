import cv2
import time
import threading
from pyzbar import pyzbar

# from insert_data import insert_data

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(
            frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
        )
        # insert_data(barcodeData)
        time.sleep(2)
        barcodes = []
    cv2.imshow("Output", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
