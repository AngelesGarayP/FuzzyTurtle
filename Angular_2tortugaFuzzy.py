import numpy as np
import skfuzzy as sk
import random
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Variables y rangos de acción
# A qué velocidad cruzar la calle?
vela = np.arange(0, 181, 1) #velocidad del otro vehículo 0 a 100km/h
dist = np.arange(0, 15, 1) #distancia al otro vehículo 20 a 80m
velp = np.arange(0, 180, 1) #distancia al otro vehículo 20 a 80m

def fis(va,da):
#Definición de universos de discurso
#Conjuntos del universo de velocidades del auto (3-input)
    vela_low = sk.trimf(vela, [0, 0, 90])
    vela_med = sk.trimf(vela, [0, 90, 180])
    vela_high = sk.trimf(vela, [90, 180, 180])
        #if(True):
        #with plt.xkcd():
    '''    
    plt.figure(1)
    plt.subplot(141)
    plt.plot(vela,vela_low, label='baja')
    plt.plot(vela,vela_med, label='media')
    plt.plot(vela,vela_high, label='alta')
    plt.title("Velocidad del auto")
    plt.xlabel("km/h")
    plt.ylabel(r'$\mu$')
    plt.legend()
    '''    
        #Conjuntos del universo de distancias (3-input)
    dist_short = sk.trapmf(dist, [0, 0, 5, 7])
    dist_mod = sk.trapmf(dist, [5, 7, 9, 10])
    dist_long = sk.trapmf(dist, [9, 10, 16, 16])
        #if(True):
        #with plt.xkcd(randomness=1):
    '''   
    plt.subplot(142)
    plt.plot(dist,dist_short, label='corta')
    plt.plot(dist,dist_mod, label='moderada')
    plt.plot(dist,dist_long, label='larga')
    plt.title("Distancia al auto")
    plt.xlabel("m")
    plt.ylabel(r'$\mu$')
    plt.legend()
    '''   
        #Conjuntos del universo de velocidades del peatón (5-output)
    #     velp_low = sk.gaussmf(velp, 0, 0.707)
    #     velp_mlow = sk.gaussmf(velp, 3, 0.707)
    #     velp_med = sk.gaussmf(velp, 6, 0.707)
    #     velp_mhigh = sk.gaussmf(velp, 9, 0.707)
    #     velp_high = sk.gaussmf(velp, 12, 0.707)
    velp_low = sk.gbellmf(velp, .1,.3,0)
    velp_mlow = sk.gbellmf(velp, .1,.3,45)
    velp_med = sk.gbellmf(velp, .1,.3,90)
    velp_mhigh = sk.gbellmf(velp, .1,.3,135)
    velp_high = sk.gbellmf(velp, .1,.3,180)
        #if(True):
        #with plt.xkcd():
    '''    
    plt.subplot(143)
    plt.plot(velp,velp_low, label='baja')
    plt.plot(velp,velp_mlow, label='media-baja')
    plt.plot(velp,velp_med, label='media')
    plt.plot(velp,velp_mhigh, label='media-alta')
    plt.plot(velp,velp_high, label='alta')
    plt.title("Velocidad del peatón")
    plt.xlabel("km/h")
    plt.ylabel(r'$\mu$')
    plt.legend()
        #plt.show()
    '''

    #Entrada
    #va = int(input("Introduzca la velocidad del auto: "))
    #da = int(input("Introduzca la distancia al auto: "))
    #Reglas de inferencia
    R1 = min(vela_low[va], dist_long[da])
    R2 = min(vela_med[va], dist_long[da])
    R3 = min(vela_high[va], dist_long[da])

    R4 = min(vela_low[va], dist_mod[da])
    R5 = min(vela_med[va], dist_mod[da])
    R6 = min(vela_high[va], dist_mod[da])

    R7 = min(vela_low[va], dist_short[da])
    R8 = min(vela_med[va], dist_short[da])
    R9 = min(vela_high[va], dist_short[da])

    #print(R1, R2, R3, R4, R5, R6, R7, R8, R9)

    #Maxmin
    #Cortes de máximos
    max_velp_low = max(R1,0)
    max_velp_mlow = max(R2,R4) 
    max_velp_med = max(R3,R5)
    max_velp_mhigh = max(R6,R7)
    max_velp_high = max(R8,R9)

    #print(max_velp_low, max_velp_mlow, max_velp_med, max_velp_mhigh , max_velp_high)

    #Agregado
    agr=[]
    for i in range(len(velp)):
        velp_low[i] = min(velp_low[i],max_velp_low)
        velp_mlow[i] = min(velp_mlow[i],max_velp_mlow)
        velp_med[i] = min(velp_med[i],max_velp_med)
        velp_mhigh[i] = min(velp_mhigh[i],max_velp_mhigh)
        velp_high[i] = min(velp_high[i],max_velp_high)
        agr.append(max(velp_low[i],velp_mlow[i],velp_med[i],velp_mhigh[i],velp_high[i])) 
    #if(True):
    #with plt.xkcd():
    '''
    plt.subplot(144)
    plt.plot(velp,agr, color='black', label='agregado')
    plt.title("Agregado")
    plt.xlabel("velocidad del peatón")
    plt.ylabel(r'$\mu$')
    plt.ylim([-0.05, 1.05])
    plt.legend()
    '''

    #Defuzz
    num = 0.0
    den = 0.0
    for i in range(len(velp)):
        num += velp[i]*agr[i]
        den += agr[i]
    defuzz = round(num/den,1)

    print("La velocidad del peatón debe ser aproximadamente",defuzz,"km/h")
    #plt.show()
    return(defuzz)
    #Entrada



# va = int(input("Introduzca la velocidad del auto: "))
# da = int(input("Introduzca la distancia al auto: "))
#va = random.randrange(0,101)
#da = random.randrange(20,81)
#print("La velocidad del vehículo es de",va,"km/h")
#print("La distancia al vehículo es de",da,"m")
#print("\n")
#fis(va,da)

mesh = np.zeros([181, 15], dtype = float)

for i in range(0,181):
    #print(i)
    for j in range(0,15):
        #j_mesh.append(j)
        print("Va: ", i, " __ Vd: ", j)
        high = fis(i,j)
        mesh[i,j] = high
print (mesh)

np.savetxt("./angular_x.csv", mesh, delimeter=",", fmt="%s")

# TRY 

X, Y = np.meshgrid(dist, vela) #mesh grid x,y
Z = mesh #matrix (list of lists) to array

plt.figure(1)
ax = plt.axes(projection = '3d') #ax definition
##Select one of three plot options:
#ax.contour3D(x,y,surf,50,cmap="plasma")

# YA JALA AQUPI JASDJAJSD 
#ax.plot_wireframe(X, Y, Z, color='black')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='inferno', edgecolor='none')
#labeling
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel('z')
plt.title('Mesh')
plt.show()
print("Finished")
