import cv2


#이미지 읽기 
#img = cv2.imread('불러올 이미지 경로', cv2.IMREAD_COLOR)
#이미지 파일을 읽어오는 방식
#   cv2.IMREAD_COLOR : 디폴트 플래그, 컬러 이미지로 로드한다. 투명한 부분은 무시된다. 정수 값 -1로 대체 사용이 가능
#   cv2.IMREAD_GRAYSCALE : 흑백 이미지로. 실제 이미지 처리 시 중간단계로 사용
#   cv2.IMREAD_UNCHANGED : 원본을 사용하여 이미지 그대로 로드한다. 정수값 1로 대체 사용이 가능
#   cv2.IMREAD_ANYCOLOR : 색상 이미지로 로드한다. 
#   cv2.IMREAD_ANYCOLOR : 색상 이미지로 로드한다. 
#   cv2.IMREAD_REDUCED_GRAYSCALE_4 : 크기를 1/4로 축소하고, 흑백을 적용하여 로드
# 
#이미지 쓰기
#cv2.imwrite('저장할 파일명',이미지 객체)
#  
#읽은 이미지 보기 
#cv2.imshow('apple', img) ----> imshow 함수는 image를 가져와서 read 한 뒤 객체를 리턴하는 함수 

#디코딩
#암호화된 형태의 데이터를 이해할 수 있는 형태로 번역하거나 해석하는 과정을 말함.
#pzbar.decode() 함수 : 이미지나 영상 프레임에서 QR 코드 혹은 바코드를 탐지해서 내용을 추출


img = cv2.imread('img/82_SIDE1.png', cv2.IMREAD_COLOR)
cv2.imshow('photo',img) #이미지 창 띄우기

cv2.waitKey(0) #이미지나 영상을 띄운 후 사용자 입력을 기다리고 창을 닫기 위한 용도 
cv2.destroyAllWindows()
