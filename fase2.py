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

# -------------------------------------
# Creación del objeto problema en PuLP
# -------------------------------------

m = lp.LpProblem("Horarios_salas", lp.LpMinimize)

# -----------------------------
# Variables de Decisión
# -----------------------------

#Variable de decisión de horario de inicio de la cirugía
x= {(i,j,k): lp.LpVariable(f"x_{i}_{j}_{k}", 0, None, lp.LpBinary) for i in C for j in F for k in S}

#Varibale de decisión de si la cirugía se esta realizado 
y= {(i,j,k): lp.LpVariable(f"y_{i}_{j}_{k}", 0, None, lp.LpBinary) for i in C for j in F for k in S}

z = lp.LpVariable("z", 0, None, lp.LpContinuous)

# -----------------------------
# Restricciones
# -----------------------------

#Cada cirugía se realiza una vez
for i in C:
    m += lp.lpSum(x[i,j,k] for j in F for k in S) == 1
    
#Cada cirugía debde durar el tiempo que se indica
for i in C:
    m += lp.lpSum(y[i,j,k] for j in F for k in S) == d[i]
    
#Cada sala y cada franja horaria solo se puede ocupar por una cirugía
for j in F:
    for k in S:
        m += lp.lpSum(y[i,j,k] for i in C) <= 1

# cada cirugia  se presenta en franjas consecutivas y no presenta durante franjas previas a la franja de inicio y en la misma sala.
for i in C:
    for j in F:
        for k in S:
            if j+d[i] <= 17:
                m +=lp.lpSum(y[i,u,k] for u in ( e for e in range(j, j+d[i])))  >=  x[i,j,k]*d[i]
            

# Ninguna cirugia puede iniciar si no se puede terminar 
for i in C:
    for j in F:
        for k in S:
            if j+d[i] > 17:
                m +=   x[i,j,k] == 0

# Ninguna cirugia se puede realizar si el doctor no esta disponible
for i in C:
    for j in F:
        for k in S:
            m += y[i,j,k] <= p[n[i],j]


# Contabilizar la maxima finalizacion de cirugias
for i in C:
    m+= z >= lp.lpSum(x[i,j,k]*(j+d[i]-1) for j in F for k in S)









    
    
# -----------------------------
# Función objetivo
# -----------------------------

m += z

# Optimizar modelo
# -----------------------------
# Optimizar el modelo con CBC (default de PuLP)
m.solve()


# -----------------------------
#    Imprimir resultados
# -----------------------------

# Imprimir variables de decisión

                
for i in C:
    for j in F:
        for k in S:
            if y[i,j,k].value() == 1:
                print(f"Cirugía {i} en franja {j} en sala {k}")