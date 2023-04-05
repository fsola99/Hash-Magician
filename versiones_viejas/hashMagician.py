import argparse #para ejecucion personalizada con argumentos
import hashlib
import os #para manipulacion de archivos
import csv

# Configuración de argumentos
parser = argparse.ArgumentParser(description='Obtener el hash de todos los archivos en una carpeta')
parser.add_argument('-p', '--path', type=str, default='.', help='Carpeta objetivo (por defecto: carpeta actual)')
parser.add_argument('-a', '--algoritmo', type=str, default='sha1', choices=['sha1', 'sha256', 'md5'], help='Algoritmo hash a utilizar (por defecto: sha1)')
args = parser.parse_args()

# Obtenemos todos los archivos de la carpeta seleccionada
folder_path = args.path
file_list = os.listdir(folder_path)
hash_list = []
algoritmoOutput = "SHA-1" #solucion momentanea para que quede lindo

# Calcula los hashes jaja
def calcularHashes(folder_path,file_list,hash_list):
    global algoritmoOutput
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        #si es un archivo
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file_current:
                content = file_current.read()
                #------------------------------------------------------------
                if args.algoritmo == 'md5':
                    algoritmoOutput = "MD5"
                    hash_value = hashlib.md5(content).hexdigest()
                   
                elif args.algoritmo == 'sha256':
                    hash_value = hashlib.sha256(content).hexdigest()
                    algoritmoOutput = "SHA-256"
                else:
                    hash_value = hashlib.sha1(content).hexdigest()
                hash_list.append({'filename': file_name, 'hash': hash_value})
                #---------------------------------------------------------------
        else: 
            calcularHashes(file_path, os.listdir(file_path), hash_list)
    
       
    return hash_list
        
hashes = calcularHashes(folder_path,file_list,hash_list)

# Mostrar en una tabla
print(">>--------------- Hashes ---------------------<<")
print('{:<30}{}'.format('Archivo', algoritmoOutput))
for unHash in hashes:
    print('{:<30}{}'.format(unHash['filename'], unHash['hash']))

# Exportar como CSV
csv_path = os.path.join(folder_path, args.algoritmo + '.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Archivo', algoritmoOutput])
    for item in hash_list:
        writer.writerow([item['filename'], item['hash']])

print("\nLos hashes han sido exportados como un archivo CSV en la siguiente ruta: " + (csv_path))

