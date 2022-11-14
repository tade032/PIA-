# from modulos.layouts import +
#from modulos.randomKey import randomKey
# from modulos.date import +

#from modulos.randomKey import randomKey
#from .date import +
from time import strftime
from datetime import datetime
from collections import namedtuple

import xlsxwriter
import sqlite3
import os
import csv


listaClient = []
listaSala = []
reservaciones = []

GlbClient = None

db = 'coworking.sqlite3'

cnx = None

if not os.path.exists(db):
    cnx = sqlite3.connect(db)
    cnx.execute(
        "CREATE TABLE IF NOT EXISTS Clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);")
    cnx.execute(
        "CREATE TABLE IF NOT EXISTS Salas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, limite INTEGER NOT NULL, turno TEXT NOT NULL);")
    cnx.execute(
        "CREATE TABLE IF NOT EXISTS Reservaciones (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT NOT NULL,id_cliente INTEGER NOT NULL, id_sala INTEGER NOT NULL, nombre_evento TEXT NOT NULL);")
else:
    cnx = sqlite3.connect(db)


# menu()

# Partes del menu

# Reservaciones

# Registrar a un nuevo cliente
def newClient(idClient):
    idClient = idClient
    nameClient = input("Nombre del Cliente: ")
    return idClient, nameClient  # regresa lista (idClient, nombre)

# Registrar una sala


def newSala(idSala):
    idSala = idSala
    nameSala = input("Nombre de la Sala: ")
    capacidad = input("Capacidad de la Sala: ")
    # regresa lista (idSala, nombre de la sala, capacidad)
    return idSala, nameSala, capacidad

# Registrar reservacion de una sala


def newReservacion(listaClient, listaSala, reservaciones):
    nombreCliente = input("\nNombre del Cliente: ")
    if(validacionCliente(listaClient, nombreCliente)):
        nombreSala = input("Nombre de la Sala: ")
        if(validacionSala(listaSala, nombreSala)):
            nombreEvento = input("Nombre del evento: ")
            fechaEvento = input(
                "Fecha del evento en formato d/m/y. Ejemplo: 20/04/2019: ")
            fechaEvento = conversionFecha(fechaEvento)
            if(validacionDias(fechaEvento.day)):
                print("")
                """
                turno = input(
                    "Que turno desea reservar, Formato para turno, 'mañana, 'tarde', noche: ")
                if(turno == 'mañana' or turno == 'tarde' or turno == 'noche'):
                    # ('sala2', 'tarde', '18/09/2022', lista)
                    if(disponibilidadSala(nombreSala, turno, strFecha(fechaEvento), reservaciones) != True):
                        folio = randomKey()
                        return nombreCliente, nombreSala, nombreEvento, strFecha(fechaEvento), turno, folio
                    else:
                        print("sala no disponoble en ese turno en esa fecha\n")
                else:
                    print("formato del turno incorrecto\n")
                
                """
    return False


# a)    La reserva de la sala se debe hacer, por lo menos, dos días antes
def validacionDias(fechaApartada):
    if(fechaUnDia() != fechaApartada and fechaActual() != fechaApartada and fechaApartada > fechaActual()):
        print("Fecha disponible")
        return True
    else:
        print("Fecha no disponible.\n")
        print("Favor de reservar con dos dias de anticipacion\n")
        return False

# b)    Solamente pueden reservar una sala aquellos que son clientes registrados


def validacionCliente(listaClient, nameClient):
    if(len(listaClient) != 0):
        strClients = str(listaClient).strip("[]")
        strName = str(nameClient).strip("[]")
        if ",".join(strName) in ",".join(strClients):
            print("Cliente encontrado\n")
            return True
        else:
            print("cliente no registrado\n")
            return False
    else:
        print("ningun Cliente registrado\n")
        return False

# validacion de sala existente


def validacionSala(listaSala, nameSala):
    if(len(listaSala) != 0):
        strClients = str(listaSala).strip("[]")
        strName = str(nameSala).strip("[]")
        if ",".join(strName) in ",".join(strClients):
            print("Sala encontrada")
            return True
        else:
            print("Sala no registrada\n")
    else:
        print("ningun Sala registrada\n")
        return False

# validacion de sala con disponibilidad


def disponibilidadSala(sala, turno, fecha, listaReservacion):
    if(len(listaReservacion) != 0):
        for itemReservacion in listaReservacion:
            stritemReservacion = str(itemReservacion).strip("[]")
            strNameSala = str(sala).strip("[]")
            strFecha = str(fecha).strip("[]")
            strTurno = str(turno).strip("[]")
            if ",".join(strFecha) in ",".join(stritemReservacion):
                if ",".join(strNameSala) in ",".join(stritemReservacion):
                    if ",".join(strTurno) in ",".join(stritemReservacion):
                        print('turno encontrado')
                        print(itemReservacion)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    else:
        # print("Ninguna reservacion\n")
        return False


# Consultar las reservaciones existentes para una fecha específica.
def consultaReservaciones(reservaciones):
    fecha = input("que fecha deseas consultar: ")
    fecha = conversionFecha(fecha)
    fecha = strFecha(fecha)
    print("++ Reporte de Reservaciones para el dia ", fecha, " ++++\n")
    print("Cliente\t", "Sala\t", "Evento\t", "Turno\t",)
    if(len(reservaciones) != 0):
        for itemReservacion in reservaciones:
            stFecha = str(fecha).strip("[]")
            if stFecha in ",".join(itemReservacion):
                print(itemReservacion[0], "\t", itemReservacion[1],
                      "\t", itemReservacion[2], "\t", itemReservacion[4])
            else:
                print("error")
        print("++++ FIN DEL REPORTE ++++++\n")
    else:
        print("No hay reservaciones aun")
        return False

# consultar la disponibilidad de las salas para una fecha especifica


def disponibilidadSalasfecha(reservaciones, salas):
    fecha = input("que fecha deseas consultar: ")
    fecha = conversionFecha(fecha)
    fecha = strFecha(fecha)
    print("++ Reporte de Reservaciones para el dia ", fecha, " ++++\n")
    print("Sala\t", "Turno\t")
    if(len(reservaciones) != 0):

        for itemSalas in salas:
            for itemReservacion in reservaciones:
                stFecha = str(fecha).strip("[]")
                stsala = str(itemSalas[1]).strip("[]")
                if stFecha in ",".join(itemReservacion) and stsala in ",".join(itemReservacion):
                    if not 'mañana' in ",".join(itemReservacion):
                        print(stsala, " Matutino")
                    if not 'tarde' in ",".join(itemReservacion):
                        print(stsala, " Tarde")
                    if not 'noche' in ",".join(itemReservacion):
                        print(stsala, " Noche")
                    print(itemReservacion)

                elif(not stsala in ",".join(itemReservacion)):
                    print(stsala, " Matutino")
                    print(stsala, " Tarde")
                    print(stsala, " Noche")

                else:
                    break

        #     if stFecha in ",".join(itemReservacion):
        #         print(itemReservacion[0], "\t", itemReservacion[1], "\t", itemReservacion[2], "\t", itemReservacion[4])
        #     else:
        #         print("error")
        # print("++++ FIN DEL REPORTE ++++++\n")
    else:
        print("No hay reservaciones aun")
        return False


# Editar evento existente
def editEvento(reservaciones):
    elemento = input("Nombre del evento a modificar: ")
    nuevoElemento = input("Nuevo Nombre: ")
    if(len(reservaciones) != 0):
        for itemReservacion in reservaciones:
            strElement = str(elemento).strip("[]")
            if strElement in ",".join(itemReservacion):
                copia = list(itemReservacion)
                copia[2] = nuevoElemento
                itemReservacion = tuple(copia)
                print(itemReservacion)
                print("Nombre cambiado")
                return reservaciones
            else:
                print("error")

    else:
        print("No hay reservaciones aun")
        return False

# Excel


def excelExport(reservaciones):
    print(reservaciones)
    Auto = namedtuple("Reservas", "sala, clientes, evento, turno")
    datos_a_grabar = dict()
    e = 0
    for strElement in reservaciones:
        datos_a_grabar[e] = Auto(
            strElement[1], strElement[0], strElement[2], strElement[4])
        print(datos_a_grabar)
        e = e + 1

    # Paso 3: Abrir, en modo de escritura, el archivo destino
    archivo = open("eventos.csv", "w", newline="")
    # Paso 4: Establecer una salida de escritura
    grabador = csv.writer(archivo)

    # Paso 5: Grabar el encabezado (OPCIONAL)
    grabador.writerow(("Clave", "Sala", "Cliente", "Evento", "Turno"))

    # Paso 6: Iterar sobre los elementos de los datos a grabar o bien pedir de golpe que se graben todos los elementos
    grabador.writerows([(clave, datos.sala, datos.clientes, datos.evento, datos.turno)
                       for clave, datos in datos_a_grabar.items()])

    archivo.close()


def excelImport():

    # Solamente si se está trabajando en otro código diferente al de la creación
    Auto = namedtuple("Reservas", "sala, clientes, evento, turno")
    datos_a_leer = dict()

    with open("eventos.csv", "r", newline="") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        lista = []
        for clave, sala, clientes, evento, turno in lector:
            datos_a_leer[int(clave)] = Auto(sala, clientes, evento, turno)
            print(datos_a_leer)
    listOfValues = datos_a_leer.values()
    listOfValues = list(listOfValues)


fecha = datetime.now()

dt_string = fecha.strftime("%d/%m/%Y %H:%M:%S")


# print("date and time =", dt_string)
def fechaDosDias():
    fechaRes = fecha.day + 2
    return fechaRes


def fechaUnDia():
    diaActual = fecha.day
    return diaActual + 1


def fechaActual():
    diaActual = fecha.day
    return diaActual


def conversionFecha(fechaConvertida):
    # una_fecha = '20/04/2019'
    fecha_dt = datetime.strptime(fechaConvertida, '%d/%m/%Y')
    return fecha_dt


def strFecha(fechastr):
    stringFecha = fechastr.strftime("%d/%m/%Y")
    return stringFecha


def randomKey():
    numero = 100
    folio = format(id(numero), "x")
    return folio


def validaInput(str):
    if not str:
        input("Este Valor no Puede Omitirse")
    else:
        return str


# Funcion para agregar un cliente a la cnx
def agregarCliente(nombre):
    cnx.cursor().execute('''INSERT INTO Clientes(nombre)
                  VALUES(?)''', (nombre,))
    cnx.commit()

    id = cnx.cursor().execute(
        '''SELECT MAX(id) id from Clientes''').fetchone()[0]

    return id


# Funcion para agregar una sala a la cnx
def agregarSala(nombre, ocupacion):
    for turno in ['Matutino', 'Vespertino', 'Nocturno']:
        cnx.cursor().execute('''INSERT INTO Salas(nombre,limite,turno)
                        VALUES(?,?,?)''', (nombre, ocupacion, turno))
    cnx.commit()


# Funcion para agregar una reservacion a la cnx
def agregarReservacion(nombre, fecha, sala, client):
    cnx.cursor().execute('''INSERT INTO Reservaciones(nombre_evento,fecha,id_sala,id_cliente)
                  VALUES(?,?,?,?)''', (nombre, fecha, sala, client))
    cnx.commit()

    folio = cnx.cursor().execute(
        '''SELECT MAX(id) id from Reservaciones''').fetchone()[0]

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        "+" + f"{'Reserva con Folio [{folio}]' : >50} Generado".format(folio=id) + f"{'+' : >52}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    return folio


# Funcion para editar una reservacion
def editarReservacion(folio, nombre):
    cnx.cursor().execute(
        '''UPDATE Reservaciones SET nombre_evento = ? WHERE id = ?''', (nombre, folio))
    cnx.commit()


# Funcion para eliminar una reservacion
def eliminarReservacion(folio):
    today = datetime.datetime.now()
    eventDay = cnx.cursor().execute(
        '''SELECT fecha FROM Reservaciones Where id = ? ''', (folio,)).fetchone()
    if eventDay:
        delta = convertirFecha(eventDay[0]) - today
        print(delta.days)
        if(delta.days >= 3):
            opcion = input("[+ ¿Desea Borrar la Reservacion? Y/N +]")
            if opcion == 'Y' or opcion == 'y':
                cnx.cursor().execute('''Delete FROM Reservaciones WHERE id = ?''', (folio,))
                cnx.commit()
            if opcion == 'N' or opcion == 'n':
                return
        else:
            print("[+ Es Necesario 3 Dias Anticipacion para Eliminar Reservacion +]")


# Funcion para mostrar salas disponibles dada una fecha en especifico
def mostrarSalasDisp(fecha):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        "+" + f"{'Salas Disponibles {fecha}' : >50}".format(fecha=fecha) + f"{'+' : >58}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    salas = cnx.cursor().execute(
        "SELECT id, nombre, turno FROM salas WHERE id NOT IN(SELECT id_sala FROM Reservaciones where fecha != ?) ", (fecha,)).fetchall()
    print(f"{'Sala' : <40}{'Nombre' : <40}{'Turno' : <40}")
    for sala in salas:
        print(f"{sala[0] : <40}{sala[1] : <40}{sala[2] : <40}")
    print("\n\n")

    return len(salas)

# Funcion para mostrar clientes


def mostrarClientesDisp():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        "+" + f"{'Clientes Disponibles' : >50}" + f"{'+' : >68}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    clientes = cnx.cursor().execute(
        "SELECT id, nombre FROM Clientes ").fetchall()
    print(f"{'Id' : <40}{'Nombre' : <40}")
    for cliente in clientes:
        print(f"{cliente[0] : <40}{cliente[1] : <40}")
    print("\n\n")

    return len(clientes)


def mostrarReserDisp():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        "+" + f"{'Reservas Disponibles' : >50}" + f"{'+' : >68}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    reservas = cnx.cursor().execute(
        "SELECT id, nombre_evento FROM Reservaciones ").fetchall()
    print(f"{'Id' : <40}{'Nombre' : <40}")
    for reserva in reservas:
        print(f"{reserva[0] : <40}{reserva[1] : <40}")
    print("\n\n")

    return len(reservas)


# Funcion para mostrar reservaciones dada una fecha en especifico
def obtenerReporteReservacion(fecha):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        "+" + f"{'Reservaciones {fecha}' : >50}".format(fecha=fecha) + f"{'+' : >58}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"{'Folio' : <35}{'Cliente' : <35}{'Evento' : <35}{'Turno' : <35}")
    eventos = cnx.cursor().execute('''SELECT sala.nombre, client.nombre, reserva.nombre_evento, sala.turno from Reservaciones reserva join Salas sala on reserva.id_sala = sala.id join Clientes client on client.id = reserva.id_cliente where reserva.fecha = ?''', (fecha,)).fetchall()
    for evento in eventos:
        print(
            f"{evento[0] : <35}{evento[1] : <35}{evento[2] : <35}{evento[3] : <35}")
    print("\n\n")


# Funcion para exportar reservaciones dada una fecha en especifico a xlsx
def exportarReporteReservacion(fecha):
    eventos = cnx.cursor().execute('''SELECT sala.nombre, client.nombre, reserva.nombre_evento, sala.turno from Reservaciones reserva join Salas sala on reserva.id_sala = sala.id join Clientes client on client.id = reserva.id_cliente where reserva.fecha = ?''', (fecha,)).fetchall()
    workbook = xlsxwriter.Workbook('reservaciones.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(0,  1):
        worksheet.write(i, 0, 'Folio')
        worksheet.write(i, 1, 'Cliente')
        worksheet.write(i, 2, 'Evento')
        worksheet.write(i, 3, 'Turno')
    for i, row in enumerate(eventos):
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, value)
    workbook.close()
    
def esFechaValida(fecha):
    try:
        if not fecha:
            return False
            
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def menu():
    print("1.-Reservaciones")
    print("2.-Reportes")
    print("3.-Regsitrar cliente nuevo")
    print("4.-Registrar una sala")
    print("5.-salir")
    menuOpcion = int(input("Seleccione una opcion: "))
    if(menuOpcion == 1):
        # reservaciones
        print("1.-Registrar una reservacion")
        print("2.-Modificar una reservacion")
        print("3.-Cosultar disponibilidad de salas para una fecha")  # funcion nueva
        opcionResaervaciones = int(input("Selecione una opcion"))
        if(opcionResaervaciones == 1):
            """
            reservacion = newReservacion(listaClient, listaSala, reservaciones)
            if(reservacion != False):
                reservaciones.append(reservacion)
                print(reservaciones)
            """
            nombreEvento = ''
            fechaEvento = ''
            while not nombreEvento or not fechaEvento or not esFechaValida(fechaEvento): 
                nombreEvento = validaInput(input("Nombre del evento: "))
                fechaEvento = validaInput(
                    input("Fecha del evento en formato d/m/y. Ejemplo: 20/04/2019: "))

            salas = mostrarSalasDisp(fechaEvento)
            if(salas > 0):
                sala = validaInput(input("Selecciona una Sala Disponible."))
            else:
                input("No hay Salas Disponibles para Reservar")

            clientes = mostrarClientesDisp()
            if(clientes > 0):
                cliente = validaInput(
                    input("Selecciona un Cliente Disponible."))
                agregarReservacion(nombreEvento, fechaEvento, sala, cliente)
            else:
                input("No hay Clientes Disponibles para Reservar")

            menu()
        elif(opcionResaervaciones == 2):
            # editEvento(reservaciones)
            folio = ''
            nombre = ''
            mostrarReserDisp()
            while not folio or not nombre:
                folio = validaInput(input("Ingresa folio a Editar."))
                nombre = validaInput(input("Ingresa Nombre a Editar."))
            editarReservacion(folio, nombre)
            menu()
        elif(opcionResaervaciones == 3):
            # nueva funcion disponibilidad de la salas para una fecha
            # disponibilidadSalasfecha(reservaciones, listaSala)
            fechaEvento = ''
            while not fechaEvento and not esFechaValida(fechaEvento):
                fechaEvento = validaInput(input("Fecha del evento en formato d/m/y. Ejemplo: 20/04/2019: "))

            mostrarSalasDisp(fechaEvento)
            menu()
        else:
            menu()
    elif(menuOpcion == 2):
        # Reportes
        print("1.-Reporte en pantalla de reservaciones de salas para una fecha")
        print("2.-Exportar reporte tabular en Excel")
        opcionReportes = int(input("Selecione una opcion"))
        if(opcionReportes == 1):
            # consultaReservaciones(reservaciones)
            fechaReporte = ''
            while not fechaReporte and not esFechaValida(fechaReporte):
                fechaReporte = validaInput(
                    input("Fecha de reserva en formato d/m/y. Ejemplo: 20/04/2019: "))

            obtenerReporteReservacion(fechaReporte)
            menu()
        elif(opcionReportes == 2):
            # nueva funcion exportar excel
            # excelExport(reservaciones) TODO
            fechaReporte = ''
            while not fechaReporte and not esFechaValida(fechaReporte):
                fechaReporte = validaInput(
                    input("Fecha de reserva en formato d/m/y. Ejemplo: 20/04/2019: "))

            exportarReporteReservacion(fechaReporte)
            menu()
            menu()
        else:
            menu()
        menu()
    elif(menuOpcion == 3):
        # Registro de clientes
        # cliente = newClient(randomKey())
        # listaClient.append(cliente)
        # print(listaClient)
        name = ''
        while not name:
            name = validaInput(input("Nombre del Cliente: "))
        id = agregarCliente(name)
        menu()
    elif(menuOpcion == 4):
        # Regristro de salas
        # sala = newSala(randomKey())
        # listaSala.append(sala)
        # print(listaSala)
        nameSala = ''
        capacidad = ''
        while not nameSala or not capacidad:
            nameSala = validaInput(input("Nombre de la Sala: "))
            capacidad = validaInput(input("Capacidad de la Sala: "))

        if int(capacidad) > 0:
            agregarSala(nameSala, int(capacidad))
            menu()
        else:
            input("La Capacidad de la Sala debe ser mayor a 0")
    elif(menuOpcion == 5):
        return 0
    else:
        print("++\tSeleccione una opcion valida\t++")
        menu()


menu()
