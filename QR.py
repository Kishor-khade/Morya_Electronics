from pyzbar.pyzbar import decode
import pyqrcode  
import cv2
import time


def generate_qr(text):
    try:
        url = pyqrcode.create(text) 
        url.png('myqr.png', scale = 6) 
        return True
    except:
        return False

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    try:
        temp = barcode[0].data.decode('ascii')
        return temp
    except:
        return False

def decode_qr():
    cap = cv2.VideoCapture(0)
    start = time.time()
    while True:
        ret, frame = cap.read()
        decoded_text = decoder(frame)
        cv2.imshow('Image', frame)
        code = cv2.waitKey(10)
        end = time.time()
        if decoded_text != False or (end-start)>5:
            cap.release()
            cv2.destroyAllWindows()
            break
    return decoded_text
