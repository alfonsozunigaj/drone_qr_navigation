from pyzbar.pyzbar import decode


def read_qr_code(input_image):
    return decode(input_image)[0][0].decode("utf-8")
