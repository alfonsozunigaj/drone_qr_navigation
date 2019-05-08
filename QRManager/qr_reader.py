from cv2 import QRCodeDetector


def read_qr_code(input_image):
    qr_decoder = QRCodeDetector()
    data = qr_decoder.detectAndDecode(input_image)[0]
    if data:
        return data
    return None
