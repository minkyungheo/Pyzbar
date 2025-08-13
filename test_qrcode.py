import qrcode
import cv2
import os

          
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# 1. QR 코드 생성
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4,
)
qr.add_data("https://www.naver.com/")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
file_path = os.path.join(output_folder, "qrcode.png")
img.save(file_path)
print("큐알 저장됨")


img_cv = cv2.imread("qrcode.png") 

# 3. OpenCV로 표시
cv2.imshow("QR Code", img_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()


