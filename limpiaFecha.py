# Importa las librerias necesarias para abrir un archivo csv
import csv
# Importa librerias para trabajar con fechas
import datetime
# Abre el archivo csv
with open('pl402.csv', 'r') as csvFile:
    # Lee el archivo csv
    reader = csv.reader(csvFile)
    # Crea un archivo csv para escribir
    with open('pl402_limpio.csv', 'w', newline='') as csvFile2:
        # Escribe en el archivo csv, formato de delimitador de campos es la coma, y el formato de delimitador de texto es las comillas dobles, forzar a que se escriban las comillas dobles
        writer = csv.writer(csvFile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        # Guarda el encabezado del archivo csv
        header = next(reader)
        # Escribe el encabezado en el archivo csv, agregando una columna para la hora
        writer.writerow([header[0], header[1], header[2], "Date", 'Time'])

        # Recorre el archivo csv
        for row in reader:
            fecha = row[3]
            try:
                # Convierte la fecha a formato datetime
                fecha_org = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                # Resta 6 horas a la fecha
                fecha_org = fecha_org - datetime.timedelta(hours=6)
                # Convierte la fecha a formato string
                fecha = fecha_org.strftime('%Y-%m-%d')
                hora = fecha_org.strftime('%H:%M')
                # Escribe la fecha en el archivo csv
                writer.writerow([row[0], row[1], row[2], fecha, hora])  
            except:
                try:
                    # Intenta convertir la fecha con el formato 28 Jan 2009 23:18 a formato datetime
                    fecha_org = datetime.datetime.strptime(fecha, '%d %b %Y %H:%M')
                    # Resta 6 horas a la fecha
                    fecha_org = fecha_org - datetime.timedelta(hours=6)
                    # Convierte la fecha a formato string
                    fecha = fecha_org.strftime('%Y-%m-%d')
                    hora = fecha_org.strftime('%H:%M')
                    # Escribe la fecha en el archivo csv
                    writer.writerow([row[0], row[1], row[2], fecha, hora])
                except:
                    # Imprime la linea que no se pudo convertir
                    print(row)
                    pass
        # Cierra el archivo csv
        csvFile.close()