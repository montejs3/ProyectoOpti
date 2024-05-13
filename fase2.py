import pulp as lp
import pandas as pd

# Guardamos el archivo en una variable
file_name = 'data/Salas de cirugía.xlsx'

# -----------------
# Conjuntos
# -----------------
# Variable de las cirugías
cirugias = pd.read_excel(file_name, sheet_name='Tabla 1')
doctores = pd.read_excel(file_name, sheet_name='Tabla 2')
#get the columns names
columns = doctores.columns
#print(columns)

# Cirugías
C = [i for i in cirugias['ID de la cirugía'] if not pd.isna(i)]

# Franjas horarias
F = [t for t in range(1, 17)]

# Salas de cirugía
S = [i for i in range(1, 8)]

# Doctores 
D = [i for i in doctores['ID del doctor'] if not pd.isna(i)]


# -----------------
# Parámetros
# -----------------

# Horario de disponibilidad de los doctores
doctores = pd.read_excel(file_name, sheet_name='Tabla 2',index_col=0).squeeze()
p= {(i, j): doctores[j][i] for i in D for j in F}

#Duracion de cirugias 
cirugias = pd.read_excel(file_name, sheet_name='Tabla 1',index_col=0)
d= {i: cirugias['Duración (en horas)'][i] for i in C}

#Doctor que realiza la cirugia
cirugias = pd.read_excel(file_name, sheet_name='Tabla 1',index_col=0)
n= {i: cirugias['ID del doctor'][i] for i in C}

