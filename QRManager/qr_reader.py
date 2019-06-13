from pyzbar.pyzbar import decode


def read_qr_code(input_image):
    decoded_image = decode(input_image)
    if decoded_image:
        print("[QR DETECTION]", decoded_image)
        return decoded_image[0][0].decode("utf-8")
    return None
