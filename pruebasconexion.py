#importamos pymysql
import pymysql

#creamos la conexion
conexion = pymysql.connect(host='localhost', user='root', password='', db='sakila')

'''try:
    with conexion.cursor() as cursor:
        #creamos la consulta
        consulta = "SELECT * FROM actor"
        #ejecutamos la consulta
        cursor.execute(consulta)
        #obtenemos los resultados
        resultados = cursor.fetchall()
        #recorremos los resultados
        for fila in resultados:
            print(fila)
except Exception as e:
    print("Ocurrió un error al consultar: ", e)
    
finally:
    conexion.close()
    print("Conexion cerrada")'''
    
try:
    with conexion.cursor() as cursor:
        # Definir la consulta SQL para insertar datos
        query = "INSERT INTO actor  (first_name,last_name) VALUES (%s, %s)"
        
        # Datos a insertar
        first_name = "Nati"
        last_name = "Hermida"
        
        # Ejecutar la consulta pasando los valores como parámetros
        cursor.execute(query, (first_name,last_name))
        
        # Confirmar los cambios (commit)
        conexion.commit()
        print("Datos insertados correctamente")
except Exception as e:
    print(f"Error al insertar datos: {e}")
finally:
    conexion.close()