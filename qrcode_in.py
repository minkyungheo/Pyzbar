import os
import cv2
import numpy as np
import logging
import json

output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

# 로그 설정
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 이미지 경로 설정
file_path = 'C:/Users/INTELLIZ Corp/Desktop/pyzbar/img/20250804_194952_003.png'

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

# 3. 밝기 및 대비 조정 함수 정의
def adjust_brightness_contrast(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# 4. QR 코드 탐지 객체 생성
qr_detector = cv2.QRCodeDetector()

# 5. 여러 밝기/대비 조합으로 초기 QR 코드 탐지
found = False
alphas = [1.5, 2.0, 2.5, 3.0]
betas = [20, 40, 60]

for a in alphas:
    for b in betas:
        adjusted = adjust_brightness_contrast(img, a, b)
        data, points, _ = qr_detector.detectAndDecode(adjusted)

        if points is not None:
            logging.info(f"밝기/대비 조정 (alpha={a}, beta={b}) 후 QR 코드 영역 감지됨")
            color = (0, 255, 0) if data else (0, 0, 255)

            pts = points.astype(int).reshape(-1, 2)
            for i in range(len(pts)):
                pt1 = tuple(pts[i])
                pt2 = tuple(pts[(i + 1) % len(pts)])
                cv2.line(adjusted, pt1, pt2, color, 2)

        

            if data:
                window_title = f"밝기/대비 ({a},{b}) - QR 인식 성공" if data else f"밝기/대비 ({a},{b}) - QR 형태 감지 (데이터 없음)"
                cv2.imshow(window_title, adjusted)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                logging.info(f"QR 코드 인식 성공 → 데이터: {data}")
                found = True
                break
            else:
                logging.warning("QR 형태는 감지됐지만 데이터는 없음")
    if found:
        break

# 6. QR 코드가 감지되지 않으면 회전하면서 재시도
if not found:
    logging.info("QR 코드 회전 탐색 시작...")
    h, w = img.shape[:2]

    for angle in range(0, 360, 10):
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 2.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_NEAREST)

        for a in alphas:
            for b in betas:
                adjusted = adjust_brightness_contrast(rotated, a, b)
                data, points, _ = qr_detector.detectAndDecode(adjusted)

                if points is not None:
                    logging.info(f"[{angle}도] 밝기(alpha={a}, beta={b}) 조정 후 QR 코드 영역 감지됨")
                    color = (0, 255, 0) if data else (0, 0, 255)

                    pts = points.astype(int).reshape(-1, 2)
                    for i in range(len(pts)):
                        pt1 = tuple(pts[i])
                        pt2 = tuple(pts[(i + 1) % len(pts)])
                        cv2.line(adjusted, pt1, pt2, color, 2)


                    if data:
                        window_title = f"{angle}도 - 밝기({a},{b}) - QR 인식 성공" if data else f"{angle}도 - QR 형태 감지 (데이터 없음)"
                        cv2.imshow(window_title, adjusted)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        logging.info(f"QR 코드 인식 성공 (각도: {angle}도) → 데이터: {data}")


                        json_data = {
                            "filename" : os.path.basename(file_path),
                            "data" : data
                        }

                        json_filename = os.path.splitext(os.path.basename(file_path))[0] + '.json'
                        json_path = os.path.join(output_dir, json_filename)

                        try: 
                            with open(json_path, 'w') as f:
                                json.dump(json_data, f, ensure_ascii=False, indent=4)

                            logging.info(f"QR 데이터가 JSON으로 저장되었습니다: {json_path}")
                            found = True
                            break

                        except Exception as e:
                            logging.error(f"JSON 저장 실패: {e}")
                    else:
                        logging.info(f"[{angle}도] QR 형태는 감지됐지만 데이터 없음")
            if found:
                break
        if found:
            break

# 7. 최종 실패 처리
if not found:
    logging.error("QR 코드 인식 실패")
