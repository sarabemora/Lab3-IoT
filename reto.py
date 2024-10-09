import re
import time
import RFID_RW as rfid
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def matriz(cascaded, block_orientation, rotate):
    # Inicializa la matriz de LEDs
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 1)
    print("[-] Matrix inicializando")
    return device


menu = "Menu Gestión de Puesto de trabajo \n\t1. Asignar llegada.\n\t2. Marcar salida."

def actualizar_puestos_ocupados(division, device):
    """Ilumina todos los puestos ocupados al mismo tiempo"""
    with canvas(device) as draw:
        for i in division:
            if division[i][1] == 1:
                draw.rectangle(division[i][0], fill="white")  # Ilumina los cuadrantes ocupados
            else:
                draw.rectangle(division[i][0], fill="black")  # Apaga los cuadrantes libres
                
def alarma_visual(device):
    """Alerta visual que enciende los LEDs del borde de la matriz de manera intermitente"""
    
    # Dibuja el rectángulo externo una vez y lo deja encendido
    with canvas(device) as draw:
        draw.rectangle((0, 0, 7, 7), outline="white")
    
    for _ in range(5):  # Repite la secuencia 5 veces
        with canvas(device) as draw:
            # Dibuja el rectángulo externo
            draw.rectangle((0, 0, 7, 7), outline="white")
            # Enciende el rectángulo interno
            draw.rectangle((1, 1, 6, 6), fill="white")
        
        time.sleep(0.5)  # Espera medio segundo

        with canvas(device) as draw:
            # Dibuja el rectángulo externo
            draw.rectangle((0, 0, 7, 7), outline="white")
            # Apaga el rectángulo interno
            draw.rectangle((1, 1, 6, 6), fill="black")
        
        time.sleep(0.5)  # Espera medio segundo
      



def main(division, device):
    # Diccionario para almacenar la asignación de cada empleado a un puesto
    empleados_asignados = {}

    while True:
        option = input(menu)
        if option == "1":  # Asignar llegada
            print("Acerque el dispositivo RFID")
            empleado = rfid.read()
            
            # Verificamos si el empleado ya tiene un puesto asignado
            if empleado in empleados_asignados:
                print(f"El empleado ya tiene asignado el puesto {empleados_asignados[empleado]}")
                continue  # Evitamos asignar un nuevo puesto si ya tiene uno

            puesto = 1
            while puesto < 5:
                if division[puesto][1] == 0:  # Verifica si el puesto está libre
                    division[puesto][1] = 1  # Marca el puesto como ocupado
                    empleados_asignados[empleado] = puesto  # Guarda el puesto asignado para el empleado
                    print(f"Puesto {puesto} asignado al empleado {empleado}")
                    actualizar_puestos_ocupados(division, device)  # Actualiza la visualización de todos los puestos ocupados
                    break
                puesto += 1

            if puesto >= 5:
                # Todos los puestos están ocupados, activar la alarma
                print("Todos los puestos están ocupados. Activando alarma visual.")
                alarma_visual(device)

        elif option == "2":  # Marcar salida
            print("Acerque el dispositivo RFID")
            empleado = rfid.read()

            if empleado in empleados_asignados:
                puesto = empleados_asignados[empleado]  # Obtiene el puesto asignado al empleado
                print(f"Marcando salida del puesto {puesto} asignado al empleado {empleado}")
                division[puesto][1] = 0  # Libera el puesto
                actualizar_puestos_ocupados(division, device)  # Actualiza la visualización de todos los puestos ocupados
                del empleados_asignados[empleado]  # Elimina el registro del empleado
            else:
                print(f"El empleado {empleado} no tiene ningún puesto asignado.")

if __name__ == "__main__":
    try:
        # Definimos los cuadrantes en la matriz de 8x8
        division = {
            1: [(0, 0, 3, 3), 0],  # Primer cuadrante
            2: [(4, 0, 7, 3), 0],  # Segundo cuadrante
            3: [(0, 4, 3, 7), 0],  # Tercer cuadrante
            4: [(4, 4, 7, 7), 0]   # Cuarto cuadrante
        }
        
        device = matriz(1, 0, 3)
        main(division, device)
        
    except KeyboardInterrupt:
        pass
