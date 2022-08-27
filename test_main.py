import time
import threading
import cv2
from pyzbar import pyzbar

from insert_data import insert_data


class Iot_attendance:
    def __init__(self):
        self.processingScans = set()
        self.recent_scans = dict()
        self.exit = False
        self.successMessage = ''
        self.errorMessage = ''

    def handle_recent_scans(self):
        while True:
            if self.exit:
                break
            current_time = time.time()
            for (roll, scan_time) in list(self.recent_scans.items()):
                duration = current_time - scan_time
                if duration >= 15:
                    del self.recent_scans[roll]
            time.sleep(10)
            self.successMessage = ''
            self.errorMessage = ''

    def handle_attendance(self, roll: str):
        self.processingScans.remove(roll)
        insert_data(roll)
        text = roll + ' -> DONE'
        self.successMessage = self.successMessage + '\n' + text

    def start_scan(self):
        vid = cv2.VideoCapture(0)

        
        while True:
            _, frame = vid.read()
            barcodes = pyzbar.decode(frame)
            y0, dy = 15, 30
            for i, line in enumerate(self.successMessage.split('\n'), 0):
                y = y0 + i*dy
                cv2.putText(frame, line, (15, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            for barcode in barcodes:
                barcodeData, barcodeType = barcode.data.decode(
                    "utf-8"), barcode.type
                roll_number = "{} ({})".format(
                    barcodeData, barcodeType).split(' ')[0]
                if roll_number not in self.processingScans and roll_number not in self.recent_scans.keys():
                    self.recent_scans[roll_number] = time.time()
                    self.processingScans.add(roll_number)
                    card_scan = threading.Thread(
                        target=self.handle_attendance, args=(roll_number,))
                    card_scan.start()
            cv2.imshow("Output", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.exit = True
                break
        vid.release()
        cv2.destroyAllWindows()


attendace = Iot_attendance()

manage_recent_scan = threading.Thread(target=attendace.handle_recent_scans)
manage_recent_scan.start()

attendace.start_scan()
