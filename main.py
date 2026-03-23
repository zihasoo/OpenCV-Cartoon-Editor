import cv2

img_dir = 'imgs'
img_src = 'tiger.jpg'
img = cv2.imread(f'{img_dir}/{img_src}')

if img is None:
    raise FileNotFoundError(f"{img_dir}/{img_src} 파일을 찾을 수 없습니다.")

median_ksize = 7   # <, >
block_size = 9     # [, ]
c_value = 2        # -, +

while True:
    color = cv2.bilateralFilter(img, d=9, sigmaColor=120, sigmaSpace=120)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, median_ksize)
    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        block_size,
        c_value,
    )

    cartoon = cv2.bitwise_and(color, color, mask=edges)

    display = cartoon.copy()
    cv2.putText(
        display,
        f"C(+/-): {c_value}  blockSize([/]): {block_size}  medianBlur(</>): {median_ksize}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        display,
        "Enter: Save  |  Q or ESC: Exit",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow('Cartoon', display)

    key = cv2.waitKey(30) & 0xFF
    if key in (27, ord('q')):
        break

    if key in (10, 13):
        save_name = f"{img_dir}/cartoon_{img_src}"
        cv2.imwrite(save_name, cartoon)
        print(f"저장 완료: {save_name}")

    if key == ord('-'):
        c_value -= 1
    elif key in (ord('+'), ord('=')):
        c_value += 1

    elif key == ord('['):
        block_size = max(3, block_size - 2)
    elif key == ord(']'):
        block_size += 2

    elif key in (ord(','), ord('<')):
        median_ksize = max(3, median_ksize - 2)
    elif key in (ord('.'), ord('>')):
        median_ksize += 2

cv2.destroyAllWindows()
