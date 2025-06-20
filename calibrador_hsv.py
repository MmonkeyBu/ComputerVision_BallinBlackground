# calibrador_hsv.py
import cv2
import numpy as np

def DUMMY_FUNCTION(x):
    # Esta função não faz nada. É apenas um requisito da função createTrackbar do OpenCV.
    pass

# Cria a janela de controles e a redimensiona para um tamanho confortável
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)

# Cria os 6 controles deslizantes (trackbars) para os limites de HSV
# Argumentos: (Nome do controle, Nome da janela, Valor inicial, Valor máximo, Função de callback)
cv2.createTrackbar("L - H", "Trackbars", 0, 179, DUMMY_FUNCTION)   # Lower Hue (Matiz Mínimo)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, DUMMY_FUNCTION)   # Lower Saturation (Saturação Mínima)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, DUMMY_FUNCTION)   # Lower Value (Brilho Mínimo)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, DUMMY_FUNCTION) # Upper Hue (Matiz Máximo)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, DUMMY_FUNCTION) # Upper Saturation (Saturação Máxima)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, DUMMY_FUNCTION) # Upper Value (Brilho Máximo)

# Inicia a captura da webcam
cap = cv2.VideoCapture(0)

print("--- Ferramenta de Calibração HSV ---")
print("Posicione o objeto na frente da câmera.")
print("Ajuste os controles até que SOMENTE o objeto apareça branco na janela 'Mascara'.")
print("Anote os 6 valores finais (L-H, L-S, L-V, U-H, U-S, U-V).")
print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte o frame da câmera para o espaço de cores HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Pega os valores atuais dos 6 controles deslizantes
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Define os limites inferior e superior da cor com base nos controles
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Cria a máscara usando os valores atuais
    mask = cv2.inRange(hsv_frame, lower_range, upper_range)

    # (Opcional) Mostra o resultado da máscara aplicada à imagem original
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Exibe as janelas na tela
    cv2.imshow("Original", frame)
    cv2.imshow("Mascara", mask)
    # cv2.imshow("Resultado Filtrado", result) # Descomente esta linha para ver a bola colorida e o fundo preto

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()