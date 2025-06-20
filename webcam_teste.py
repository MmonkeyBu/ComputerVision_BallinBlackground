import cv2
import numpy as np
import time

# --- CONFIGURAÇÕES ---
LOWER_WHITE = np.array([0, 0, 130])
UPPER_WHITE = np.array([180, 50, 255])  # Branco em HSV

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

print("Detector iniciado. Pressione 'q' para sair.")
time.sleep(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro: Não foi possível ler o frame da câmera.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_WHITE, UPPER_WHITE)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    melhor_contorno = None
    melhor_circularidade = 0
    melhor_dados = (0, 0, 0, 0)

    for c in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        area = cv2.contourArea(c)
        perimetro = cv2.arcLength(c, True)
        circularidade = 4 * np.pi * (area / (perimetro * perimetro)) if perimetro > 0 else 0

        x_rect, y_rect, w, h = cv2.boundingRect(c)
        razao = w / h if h > 0 else 0

        if 10 < radius < 50 and circularidade > melhor_circularidade:
            melhor_contorno = c
            melhor_circularidade = circularidade
            melhor_dados = (x, y, radius, area)

    if melhor_contorno is not None and melhor_circularidade > 0.65:
        x, y, radius, area = melhor_dados
        cv2.drawContours(frame, [melhor_contorno], -1, (255, 0, 0), 3)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        print(f"Bola encontrada em: X={int(x)}, Y={int(y)} - Área: {int(area)} - Circularidade: {melhor_circularidade:.2f}")

    cv2.imshow('Detector de Bola', frame)
    cv2.imshow('Mascara', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Encerrando o programa...")
cap.release()
cv2.destroyAllWindows()
