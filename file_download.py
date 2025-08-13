
import boto3
import os
import cv2



## s3파일에서 업로드 
os.makedirs('image', exist_ok=True)
file_name = 'image/20250610_110408_066.png'
bucket = 'plant-vision-project'
key ='2025-06-10/bottom/original/20250610_110408_066.png'

client = boto3.client('s3')
client.download_file(bucket, key, file_name)

print("파일 다운로드 완료 : {file_name}")


img = cv2.imread(file_name)

img = cv2.resize(img,(0,0), fx=0.5, fy=0.5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5,5),0)

qr = cv2.QRCodeDetector()
data,box,straight_qrcode = qr.detectAndDecode(img)


if data:
    print('QR코드 데이터: {}'.format(data))
    print('QR코드 위치: {}'.format(box))

    if box is not None:
        box = box[0]
        lefttop = int(box[0][0]), int(box[0][1]) ##좌상단 첫 번째 점
        rightbottom = int(box[2][0]), int(box[2][1]) ##우하단 세 번째 점
        
        ## 사각형 그리기
        cv2.rectangle(img, lefttop, rightbottom, (0, 255, 0), 3) 


    cv2.imshow('코드 인식 결과', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("인식 오류!")





