import os
import cv2
import numpy as np
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 이미지 경로 설정
file_path = 'C:/Users/INTELLIZ Corp/Desktop/pyzbar/img/20250804_194940_926.png'

# 1. 파일 존재 확인
if not os.path.exists(file_path):
    logging.error("파일이 존재하지 않습니다.")
    exit()
logging.info(f"파일 존재 확인: {file_path}")

# 2. 이미지 읽기
img = cv2.imread(file_path)
if img is None:
    logging.error("이미지를 읽을 수 없습니다.")
    exit()
logging.info("이미지 읽기 성공")

# 3. 밝기 및 대비 조정
alpha, beta = 2.0, 40  # 밝기(alpha), 대비(beta)
adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
logging.info("밝기 및 대비 조정 완료")

# 4. QR 코드 탐지 객체 생성
qr_detector = cv2.QRCodeDetector()

# 5. 초기 QR 코드 탐지
data, points, _ = qr_detector.detectAndDecode(adjusted)
found = False

if points is not None:
    logging.info("초기 QR 코드 영역 감지됨")
    color = (0, 255, 0) if data else (0, 0, 255)

    pts = points.astype(int).reshape(-1, 2)
    for i in range(len(pts)):
        pt1 = tuple(pts[i])
        pt2 = tuple(pts[(i + 1) % len(pts)])
        cv2.line(adjusted, pt1, pt2, color, 2)

    window_title = "QR 인식 성공" if data else "QR 형태 감지 (데이터 없음)"
    cv2.imshow(window_title, adjusted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if data:
        logging.info(f"초기 QR 코드 감지 성공 → 데이터: {data}")
        found = True
    else:
        logging.warning("QR 형태는 감지됐지만 데이터는 없음")

else:
    logging.warning("초기 QR 코드 감지 실패")

# 6. QR 코드가 감지되지 않으면 회전하면서 재시도
if not found:
    logging.info("QR 코드 회전 탐색 시작...")
    h, w = adjusted.shape[:2]

    for angle in range(0, 360, 5):
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(adjusted, M, (w, h), flags=cv2.INTER_NEAREST)

        data, points, _ = qr_detector.detectAndDecode(rotated)

        if points is not None:
            logging.info(f"[{angle}도] QR 코드 영역 감지됨")

            # 외곽선 그리기 (데이터 유무에 따라 색상 구분)
            color = (0, 255, 0) if data else (0, 0, 255)
            pts = points.astype(int).reshape(-1, 2)
            for i in range(len(pts)):
                pt1 = tuple(pts[i])
                pt2 = tuple(pts[(i + 1) % len(pts)])
                cv2.line(rotated, pt1, pt2, color, 2)

            window_title = f"{angle}도 - QR 인식 성공" if data else f"{angle}도 - QR 형태 감지 (데이터 없음)"
            cv2.imshow(window_title, rotated)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if data:
                logging.info(f"QR 코드 인식 성공 (각도: {angle}도) → 데이터: {data}")
                found = True
                break
            else:
                logging.warning(f"[{angle}도] QR 형태는 감지됐지만 데이터는 없음")
        else:
            logging.debug(f"[{angle}도] QR 감지 실패")

# 7. 최종 실패 처리
if not found:
    logging.error("QR 코드 인식 실패")
