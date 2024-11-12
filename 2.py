import cv2
import numpy as np

# Fungsi untuk mengatur trackbar
def nothing(x):
    pass

# Buat jendela untuk trackbar
cv2.namedWindow("Trackbars")
cv2.createTrackbar("LH", "Trackbars", 35, 179, nothing)   # Hijau Lower Hue
cv2.createTrackbar("LS", "Trackbars", 100, 255, nothing)  # Hijau Lower Saturation
cv2.createTrackbar("LV", "Trackbars", 100, 255, nothing)  # Hijau Lower Value
cv2.createTrackbar("UH", "Trackbars", 85, 179, nothing)   # Hijau Upper Hue
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)  # Hijau Upper Saturation
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)  # Hijau Upper Value

cv2.createTrackbar("RH", "Trackbars", 0, 179, nothing)    # Merah Lower Hue
cv2.createTrackbar("RS", "Trackbars", 100, 255, nothing)  # Merah Lower Saturation
cv2.createTrackbar("RV", "Trackbars", 100, 255, nothing)  # Merah Lower Value
cv2.createTrackbar("URH", "Trackbars", 10, 179, nothing)  # Merah Upper Hue
cv2.createTrackbar("URS", "Trackbars", 255, 255, nothing) # Merah Upper Saturation
cv2.createTrackbar("URV", "Trackbars", 255, 255, nothing) # Merah Upper Value

# Menggunakan video atau kamera sebagai input 
cap = cv2.VideoCapture('VIDEONYAA.mp4')  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Konversi frame ke ruang warna HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Baca nilai trackbar untuk warna hijau
    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")
    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    # Baca nilai trackbar untuk warna merah
    rh = cv2.getTrackbarPos("RH", "Trackbars")
    rs = cv2.getTrackbarPos("RS", "Trackbars")
    rv = cv2.getTrackbarPos("RV", "Trackbars")
    urh = cv2.getTrackbarPos("URH", "Trackbars")
    urs = cv2.getTrackbarPos("URS", "Trackbars")
    urv = cv2.getTrackbarPos("URV", "Trackbars")

    # Masker untuk bola hijau
    lower_green = np.array([lh, ls, lv])
    upper_green = np.array([uh, us, uv])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Masker untuk bola merah
    lower_red = np.array([rh, rs, rv])
    upper_red = np.array([urh, urs, urv])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Cek apakah mask hijau ada
    # Menampilkan hasil mask hijau
    cv2.imshow("Mask Green", mask_green)
    
    # Deteksi kontur untuk bola hijau
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_green:
        area = cv2.contourArea(cnt)
        if area > 500:  # Filter berdasarkan ukuran area
            # Temukan lingkaran yang mengelilingi kontur hijau
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center_green = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center_green, radius, (0, 128, 0), 2)  # Lingkaran hijau lebih tua

    # Deteksi kontur untuk bola merah
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_red:
        area = cv2.contourArea(cnt)
        if area > 500:
            # Temukan lingkaran yang mengelilingi kontur merah
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center_red = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center_red, radius, (0, 0, 255), 2)  # Lingkaran merah mengelilingi bola merah

    # Tampilkan hasil
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask Red", mask_red)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()