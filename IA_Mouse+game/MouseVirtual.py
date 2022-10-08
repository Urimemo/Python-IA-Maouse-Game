import cv2
from cv2 import VideoCapture
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import cvzone
import random

######################

wCam, hCam = 640, 480
frameR = 100
smoothering = 60

######################


detector = htm.handDetector(maxHands=1)


cap = VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

wScr, hScr = autopy.screen.size()
print(wScr,hScr)
print(wScr,hScr)

class Program():

    def game(self):
        #variables para usar
        startGame = False
        timer = 0
        stateResult = False
        initialTime = 0
        score = [0,0] #[AI, jugador]

        #comienza el bucle
        while True:

            #activamos camara, activamos el detector de manos, activamos al posición de los dedos, 
            #damos la vuelta a la grabacion, de forma que haga efecto espejo. Todo respectivamente
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            imgFliped = cv2.flip(img, 1)
            
            #si el juego comienza (comienza pulsando la tecla s)
            if startGame:
                
                #hacer que se pueda leer la posicion de los dedos de las manos
                if len(lmList) != 0:
                    x1,y1 = lmList[8][1:]
                    x2,y2 = lmList[12][1:]

                    #activar la lectura de si los dedos estan o no levantados
                    fingers = detector.fingersUp()
        
                if stateResult is False:

                    #contador del tiempo
                    timer = time.time() - initialTime
                    cv2.putText(imgFliped, str(int(timer)), (300,100), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,0), 4)

                    #cuenta hasta 3, en el segundo 3 se ejecuta el resto de la operacion
                    if timer > 3:
                        
                        stateResult = True
                        playerMove = None

                        if fingers == [0,0,0,0,0]: #<-- piedra
                            playerMove = 1  
                        
                        if fingers == [1,1,1,1,1]: #<-- papel
                            playerMove = 2
                        
                        if fingers == [0,1,1,0,0]: #<-- tijera
                            playerMove = 3
                        
                        if fingers == None:
                            print("Error")

                        if score[0] < 3:
                            #creamos un numero aletorio entre 1 y 3 (incluidos) para que nos muestre 
                            # una imagen de forma aleatoria
                            randomNumber = random.randint(1,3)
                            image = cv2.imread(f'images/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                            imageResized = cv2.resize(image, (150,150))

                            #Jugador suma 1 punto
                            if playerMove == 1 and randomNumber == 3 or \
                                playerMove == 2 and randomNumber == 1 or \
                                    playerMove ==3 and randomNumber == 2:
                                score[1] += 1
                                if randomNumber == 1:
                                    print(f'Jugador: papel // IA: piedra - JUGADOR GANA 1PT')
                                
                                if randomNumber == 2:
                                    print(f'Jugador: tijera // IA: papel - JUGADOR GANA 1PT')
                                
                                if randomNumber == 3:
                                    print(f'Jugador: piedra // IA: tijera - JUGADOR GANA 1PT')
                            
                            #IA Suma un punto
                            if randomNumber == 1 and playerMove == 3 or \
                                randomNumber == 2 and playerMove == 1 or \
                                    randomNumber == 3 and playerMove == 2:
                                score[0] += 1

                                if randomNumber == 1:
                                    print(f'Jugador: tijera // IA: piedra - IA GANA 1PT')
                                
                                if randomNumber == 2:
                                    print(f'Jugador: piedra // IA: papel - IA GANA 1PT')
                                
                                if randomNumber == 3:
                                    print(f'Jugador: papel // IA: tijera - IA GANA 1PT')
                        else:
                            if playerMove == 1:
                                image = cv2.imread(f'images/2.png', cv2.IMREAD_UNCHANGED)
                                imageResized = cv2.resize(image, (150,150))
                                score[0] += 1
                                print("Jugador: piedra // IA: papel - IA GANA 1PT")
                            
                            if playerMove == 2:
                                image = cv2.imread(f'images/3.png', cv2.IMREAD_UNCHANGED)
                                imageResized = cv2.resize(image, (150,150))
                                score[0] += 1
                                print("Jugador: papel // IA: tijera - IA GANA 1PT")
                            
                            if playerMove == 3:
                                image = cv2.imread(f'images/1.png', cv2.IMREAD_UNCHANGED)
                                imageResized = cv2.resize(image, (150,150))
                                score[0] += 1
                                print("Jugador: tijera // IA: piedra - IA GANA 1PT")
                        
                            

            if stateResult:
                imgFliped = cvzone.overlayPNG(imgFliped, imageResized, (2,2))

            #Marcador de los puntos actuales
            cv2.putText(imgFliped, str(score[0]),(2,450), cv2.FONT_HERSHEY_PLAIN, 6, (0,255,255), 4)
            cv2.putText(imgFliped, str(score[1]),(570,450), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            #empezar juego pulsando tecla s
            startKey = cv2.waitKey(1)
            if startKey == ord("s"):
                    print("empieza el juego")
                    startGame = True
                    initialTime = time.time()
                    stateResult = False
            
            #mostrar imagen-espejo
            cv2.imshow("imagen", imgFliped)

            #finalitzar el programa pulsant k
            k = cv2.waitKey(2)
            if k == 27:
                cv2.destroyAllWindows()   
                break
                 
    def mouse(self):

        pTime = 0
        
        plocX, plocY = 0,0
        clocX, clocY = 0,0

        while True:

            #1. mantenim encesa la càmara i amg vdetector.findHands(img) indiquem que reconegui les mans a la imatge que 
            #s'està reproduint
            success, img = cap.read()
            detector = htm.handDetector(maxHands=1)
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)

            #2. Aconseguir la punta del sdits mitjà i índex
            
            if len(lmList) != 0:
                x1,y1 = lmList[8][1:]
                x2,y2 = lmList[12][1:]
                #print(x1,y1,x2,y2)

            #3. Trobar quin dit és amunt
                fingers = detector.fingersUp()
                #print(fingers)

                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                #4. Aquí treballem només amb el dit índex
                if fingers[1] == 1 and fingers[2] == 0:

                    #5. Convertir las coordenadas
                    x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
                    y3 = np.interp(y1, (frameR, hCam-frameR), (0,hScr))

                    #6. Suavitzar el moviment del cursor
                    clocX = plocX + (x3-plocX) / smoothering
                    clocY = plocY + (y3-plocY) / smoothering


                    #7. Moure el mouse fent servir autopy.move(wScr-x3,y3)
                    autopy.mouse.move(wScr-x3,y3)
                    cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                #8. Comprovar si els dos dits estan amunt
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:

                #9. Trobar la distància entre els dits i emmagatzemar-la a la variable length
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                
                #10. si la distància és menor a 30 unitats el ratolí farà click i dibuixarà un cercle entre mig dels dits
                #  índex i mitjà. les unitats de separació dels dits pot variar depenent de la persona, però per normalment
                #  30 unitats és més que suficient, a menys que algú tyingui els dits molt grossos.
                    if length < 30:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255, 0), cv2.FILLED)
                        autopy.mouse.click() 
            
            #11. Aquí calculem i mostrem els FPS
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0))

            #12. Per últim però no menys important, mostrarem per pantalla la càmara.

            cv2.imshow("Yo", img)
            
            #aquestes 2 últimes línies serveixen per a tancar el programa fent ús de la tecla esc.
            k = cv2.waitKey(1)
            
            if k == 27:
                cv2.destroyAllWindows()
                break
