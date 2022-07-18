
import numpy as np
import cv2 as cv

def draw_str(dst, target, s, color,fuente,negrita):
    x, y = target
    #cv.putText(dst, s, (x+1, y+1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv.LINE_AA)
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, fuente,color, negrita,lineType=cv.LINE_AA)

def draw_strApe(dst, target, s,color):
    x, y = target
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 2, color, 1,lineType=cv.LINE_AA)    

def clock():
    return cv.getTickCount() / cv.getTickFrequency()

def draw_rectangulo(img, rects, color):
    color = (80, 170, 250)
    color1 = (210, 190, 120)
    width = 640
    height = 480
    anchoLinea = 1
    anchoLinea1 = 2
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)


def draw_rects(img, rects, color):
    color = (80, 170, 250)
    color1 = (210, 190, 120)
    width = 720
    height = 490
    anchoLinea = 1
    anchoLinea1 = 2
    for x1, y1, x2, y2 in rects:

        arriba_1 = (int((x1 + x2) / 2), 0)
        arriba_2 = (int((x1 + x2) / 2), y1)

        abajo_1 = (int((x1 + x2) / 2), y2)
        abajo_2 = (int((x1 + x2) / 2), height)

        izquierda_1 = (0, int((y1 + y2) / 2))
        izquierda_2 = (x1,int((y1 + y2) / 2))

        derecha_1 = (x2, int((y1 + y2) / 2))
        derecha_2 = (width, int((y1 + y2) / 2))

        derecha_1 = (x2, int((y1 + y2) / 2))
        derecha_2 = (width, int((y1 + y2) / 2))                

        #angulo superior izquierdo
        centroizquierda_arriba_1 = (x1, y1)
        centroizquierda_arriba_2 = (int(int((x2 + x1) / 2) * 0.95), y1)
        centroizquierda_abajo_1 = (x1, y1)
        centroizquierda_abajo_2 = (x1, int(int((y2 + y1) / 2) * 0.95))

        #angulo superior derecho
        centroderecha_arriba_1 = (int(int((x2 + x1) / 2) * 1.05), y1)
        centroderecha_arriba_2 = (x2, y1)
        centroderecha_abajo_1 = (x2, y1)
        centroderecha_abajo_2 = (x2, int(int((y2 + y1) / 2) * 0.95))

        #angulo inferior izquierdo
        centroizquierda_arriba1_1 = (x1, y2)
        centroizquierda_arriba1_2 = (x1, int(int((y2 + y1) / 2) * 1.05))
        centroizquierda_abajo1_1 = (x1, y2)
        centroizquierda_abajo1_2 = (int(int((x2 + x1) / 2) * 0.95) , y2)

        #angulo inferior derecho
        centroderecha_arriba1_1 = (x2, y2)
        centroderecha_arriba1_2 = (x2, int(int((y2 + y1) / 2) * 1.05))
        centroderecha_abajo1_1 = (x2, y2)
        centroderecha_abajo1_2 = (int(int((x2 + x1) / 2) * 1.05) , y2)

        cruzvertical_1 = (int((x1 + x2) / 2),  int(int((y2 + y1) / 2) - 10))
        cruzvertical_2 = (int((x1 + x2) / 2), int(int((y2 + y1) / 2)) + 10)
        cruzorizontal_1 = (int(int((x2 + x1) / 2)) -10, int((y1 + y2) / 2))
        cruzorizontal_2 = (int(int((x2 + x1) / 2)) + 10, int((y1 + y2) / 2)) 

        cv.line(img, arriba_1, arriba_2, color, anchoLinea)          # |
        cv.line(img, abajo_1, abajo_2, color, anchoLinea)            # |
        cv.line(img, izquierda_1, izquierda_2, color, anchoLinea)    # ─
        cv.line(img, derecha_1, derecha_2, color, anchoLinea)        # ─

        #cruz central
    #    cv.line(img, cruzvertical_1, cruzvertical_2, color, anchoLinea1)    # |
    #    cv.line(img, cruzorizontal_1, cruzorizontal_2, color, anchoLinea1)        # ─

        #centro
        cv.line(img, centroizquierda_arriba_1, centroizquierda_arriba_2, color, anchoLinea)  # | centro izquierda arriba
        cv.line(img, centroizquierda_abajo_1, centroizquierda_abajo_2, color, anchoLinea)  # | centro izquierda abajo
        cv.line(img, centroderecha_arriba_1, centroderecha_arriba_2, color, anchoLinea)  # | centro derecha arriba
        cv.line(img, centroderecha_abajo_1, centroderecha_abajo_2, color, anchoLinea)  # | centro derecha abajo

        cv.line(img, centroizquierda_arriba1_1, centroizquierda_arriba1_2, color, anchoLinea)  # | centro izquierda arriba
        cv.line(img, centroizquierda_abajo1_1, centroizquierda_abajo1_2, color, anchoLinea)  # | centro izquierda abajo
        cv.line(img, centroderecha_arriba1_1, centroderecha_arriba1_2, color, anchoLinea)  # | centro derecha arriba
        cv.line(img, centroderecha_abajo1_1, centroderecha_abajo1_2, color, anchoLinea)  # | centro derecha abajo

        #cv.circle(img, (int((x2 + x1) / 2),int((y2 + y1) / 2)), int((x2 - x1) * 0.40) ,color, anchoLinea)
        #cv.circle(img, (int((x2 + x1) / 2),int((y2 + y1) / 2)), int((x2 - x1) * 0.30) ,color, anchoLinea)
        
def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

