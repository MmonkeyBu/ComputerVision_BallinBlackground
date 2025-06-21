import cv2
import numpy as np
import time
import serial

#setado para branco
#-----------------------(Matriz, Saturação, brilho)-----------------------
LOWER_WHITE = np.array([0, 0, 130])
UPPER_WHITE = np.array([180, 50, 255])  
#----------------------------------------------------------------------------    
# Configuração da porta serial    
import serial
s = serial.Serial(
    port='COM1',
    baudrate=9600,
    bytesize=serial.EIGHTBITS, 
    parity=serial.PARITY_NONE,   
    stopbits=serial.STOPBITS_ONE 
) #Olhar o Read.me em caso de dúvidas
# Configuração da câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

print("Detector iniciado. Pressione 'q' para sair.")
time.sleep(1)

while True:
    ret, frame = cap.read() #ret é boleano(mostra se deu tudo certo), frame é a imagem capturada
    if not ret:
        print("Erro: Não foi possível ler o frame da câmera.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Converte a imagem de BGR para HSV
    mask = cv2.inRange(hsv, LOWER_WHITE, UPPER_WHITE) #pinta de branco os pixels que estão dentro do intervalo

#Pre processamento da máscara
    kernel = np.ones((5, 5), np.uint8) #cria um kernel 5x5 de uns
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)#expanse a area branca para tampar buracos
    mask = cv2.erode(mask, None, iterations=1)# Encolhe um pouco as áreas brancas, o que ajuda a eliminar pequenos ruídos brancos que estejam isolados no fundo
    mask = cv2.dilate(mask, None, iterations=2)#Expande as áreas brancas. Como isso vem depois da erosão, enquanto o ruído pequeno, que foi eliminado, não volta, mantendo somente a bola

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#encontra as bordas de todas as formas brancas que sobraram. retorna uma lista, sendo cada um "candidato" a ser a bola

    melhor_contorno = None
    melhor_circularidade = 0
    melhor_dados = (0, 0, 0, 0)

    for c in contours: # percorre todos os candidatos a bola
        ((x, y), radius) = cv2.minEnclosingCircle(c) #Encontra o círculo mínimo que envolve o contorno
        area = cv2.contourArea(c)
        perimetro = cv2.arcLength(c, True)
        circularidade = 4 * np.pi * (area / (perimetro * perimetro)) if perimetro > 0 else 0 #O quão perfeito é o ciruclo de 0 a 1, sendo 1 um círculo perfeito

        x_rect, y_rect, w, h = cv2.boundingRect(c) #Calcula a "proporção" do contorno, verificando se ele é mais "quadrado" (razão perto de 1) ou "achatado", fiz isso para evitar que o detector pegue meu mouse kkkkkkk
        razao = w / h if h > 0 else 0

        if 10 < radius < 50 and circularidade > melhor_circularidade: #aqui usamos um conjunto de condições para filtrar os contornos que não são a bola, como tamanho, circularidade e proporção
            melhor_contorno = c
            melhor_circularidade = circularidade
            melhor_dados = (x, y, radius, area) #o vencedor é usado como melhor_contorno, melhor_circularidade e melhor_dados

    if melhor_contorno is not None and melhor_circularidade > 0.65:# se o melhor contorno for encontrado, printamos as informações e desenhamos na imagem
        x, y, radius, area = melhor_dados
        cv2.drawContours(frame, [melhor_contorno], -1, (255, 0, 0), 3)# desenha o contorno da bola (verde)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)# desenha o círculo mínimo que envolve o contorno(azul)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)# desenha o centro da bola(ponto vermelho)
        s.write(f"{int(x)},{int(y)}\n".encode('utf-8'))
        print(f"Bola encontrada em: X={int(x)}, Y={int(y)} - Área: {int(area)} - Circularidade: {melhor_circularidade:.2f}")

    cv2.imshow('Detector de Bola', frame)
    cv2.imshow('Mascara', mask)

#apértar Q para sair do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Encerrando o programa...")
cap.release()#desliga a camera
cv2.destroyAllWindows()#fecha todas as janelas
