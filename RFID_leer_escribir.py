import RFID_RW as rfid
import matriz 
print("Acerque la tarjeta al lector")
menu = "Menu Gestión de Puesto de trabajo \n\t1. Asignar Tarjeta a empleado.\n\t2. Leer tarjeta de empleado."

def main():
    while True:
        option = input(menu)
        if option == "1":
            nombre = input('Ingrese el nombre del empleado: \n')
            apellidos = input('Ingrese los apellidos del empleado: \n')
            cargo = input('Ingrese el cargo del empleado: \n')
            codigo = input('Ingrese el codigo del empleado: \n')
            edad = input('Ingrese el edad del empleado: \n')
            conc = nombre + apellidos + " Cargo " + cargo + " Codigo " + codigo + " Edad " + edad
            print("Acerque el dispositivo RFID")
            rfid.write(conc)
            
        
        elif option == "2":
            print("Acerque el dispositivo RFID")
            empleado = rfid.read()
            msgBienvenida = 'Bienvenido {}'.format(empleado.rstrip())
            print(msgBienvenida)
            matriz.main(1, 0, 3, msgBienvenida)

main()