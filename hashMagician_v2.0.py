import argparse #para ejecucion personalizada con argumentos
import hashlib
import os #para manipulacion de archivos
import csv

# Configuración de argumentos
parser = argparse.ArgumentParser(description='Obtener el hash de todos los archivos en una carpeta')
parser.add_argument('-p', '--path', type=str, default='.', help='Carpeta objetivo (por defecto: carpeta actual)')
parser.add_argument('-a', '--algoritmo', nargs='+', default=['sha1'], choices=['sha1', 'sha256', 'md5'], help='Algoritmo(s) hash a utilizar (por defecto: sha1)')
args = parser.parse_args()

# Obtenemos todos los archivos de la carpeta seleccionada
folder_path = args.path
file_list = os.listdir(folder_path)
hash_list = []
algoritmoOutput = "SHA-1" #solucion momentanea para que quede lindo

# Calcula los hashes jaja
def calcularHashes(folder_path, file_list, hash_list, algoritmos):
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        #si es un archivo
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file_current:
                content = file_current.read()

 		#Checkeo por algoritmo y hago append en cada instancia de for
                for algoritmo in algoritmos:
                    if algoritmo == 'md5':
                        hash_value = hashlib.md5(content).hexdigest()
                    elif algoritmo == 'sha256':
                        hash_value = hashlib.sha256(content).hexdigest()
                    else:
                        hash_value = hashlib.sha1(content).hexdigest()
                    hash_list.append({'filename': file_name, 'hash': hash_value, 'algoritmo': algoritmo})
        else: #subcarpeta
            calcularHashes(file_path, os.listdir(file_path), hash_list, algoritmos)
    return hash_list
        
hashes = calcularHashes(folder_path, file_list, hash_list, args.algoritmo)

# Mostrar en una tabla
print(">>--------------- Hashes ---------------------<<")
print('{:<30}{:<10}{}'.format('Archivo', 'Algoritmo', 'Hash'))
for unHash in hashes:
    print('{:<30}{:<10}{}'.format(unHash['filename'], unHash['algoritmo'], unHash['hash']))

# Exportar como CSV
csv_path = os.path.join(folder_path, '_'.join(args.algoritmo) + '.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Archivo', 'Algoritmo', 'Hash'])
    for item in hash_list:
        writer.writerow([item['filename'], item['algoritmo'], item['hash']])

print("\nLos hashes han sido exportados como un archivo CSV en la siguiente ruta: " + (csv_path))
