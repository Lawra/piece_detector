from image_detection import ImageDetection
from PLC_comunication import Comunication


# Adreça del Automat
IP = '192.168.1.17'
Rack = 0
Slot = 1

# configuracio comunicació
plc = Comunication(IP, Rack, Slot)         # (IP, Rack, Slot)

# configuració camara
# NOTA: si es volgues es podria passar la resolució o altres paràmetres que vulguesem
img_detect = ImageDetection()

while True:
    trigger = plc.reading_bool(10, 0, 0)       # (Ndb, PosM, trigger)
    if trigger:
        busy = True
        plc.writing_bool(10, 0, 3, busy)       # (Ndb, PosM, bit, busy)

        # Fem la foto:
        img_detect.start_camera()
        img_detect.image_capture()
        img_detect.stop_camera()

        # Enviem la imatge a la API
        result = img_detect.get_pieces_position()

        # comprobem si hi ha hagut algun error:
        error = result['success'] == "false"

        if error:
            print('error: ' + result['error'])
            plc.writing_bool(10, 0, 4, error)    # (Ndb, PosM, bit, Error)
            busy = False
            plc.writing_bool(10, 0, 3, busy)     # (Ndb, PosM, bit, busy)

            reset = False
            while not reset:  # (Ndb, PosM, reset)
                reset = plc.reading_bool(10, 0, 2)  # (Ndb, PosM, reset)

            error = False
            plc.writing_bool(10, 0, 4, error)  # (Ndb, PosM, bit, Error)

        else:
            # aguardem el numero de peces trobades:
            num_pieces = result['num_pieces']
            print('numero de peces trobades: ' + str(num_pieces))
            # (Ndb, PosM, NumPecesTotal)
            plc.writing_byte(10, 2, num_pieces)

            # aguardem el llistat de peces a la variable pieces:
            pieces_list = result['list']
            busy = False
            plc.writing_bool(10, 0, 3, busy)  # (Ndb, PosM, bit, busy)

            # iterem per cada peça de la llista:
            # fer un while i esperar els steps???
            for piece in pieces_list:
                Step = False
                while not Step:
                    Step = plc.reading_bool(10, 0, 1)     # (Ndb, PosM, Step)
                    # reset = plc.reading_bool(10, 0, 2)              # (Ndb, PosM, reset)

                # separador visual per el text a la terminal
                print('---------')
                # imprimim per pantalla la informació de la peça
                print('x: ' + str(piece['x']))
                print('y: ' + str(piece['y']))
                # enviar x i y
                # plc.writing_byte(10, 4, piece)          # (Ndb, PosM, NumPeça)
                # (Ndb, PosM, TipoPeça)
                plc.writing_byte(10, 6, 0)
                plc.writing_real(10, 8, piece['x'])      # (Ndb, PosM, ValorX)
                plc.writing_real(10, 12, piece['y'])      # (Ndb, PosM, ValorY)
                plc.writing_real(10, 16, 0)              # (Ndb, PosM, Angle)
