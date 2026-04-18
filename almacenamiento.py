# Importamos las librerias y modulos necesarios
# write_deltalake: Modulo que permite escribir un DataFrame en un archivo Delta Lake
# DeltaTable: Modulo para manipular archivos Delta Lake

from deltalake import write_deltalake, DeltaTable
import pyarrow as pa

# Creamos dos procedimientos para el almacenamiento de los datos extraídos, uno para la extracción full y otro para la extracción incremental. 
# Ambos procedimientos utilizan el módulo write_deltalake para escribir los datos en archivos Delta Lake, 
# con diferentes modos de escritura (overwrite para la extracción full y append para la extracción incremental).

def almacenamiento_full(route, data):
    write_deltalake(route, data, mode="overwrite")

def almacenamiento_incremental(route, data, particion):
    write_deltalake(route, data, mode="append", partition_by=[particion])