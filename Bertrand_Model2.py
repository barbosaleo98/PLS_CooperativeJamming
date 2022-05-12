# Script que produz uma demonstração gráfica do Modelo 2 do Paradoxo de Bertrand
# Utilizado para produzir ruas através de um PLP em uma área circular para redes V2X

import numpy as np 
import matplotlib.pyplot as plt  
from labellines import labelLines

# Dimensões do disco (posicao origem e raio)
x0 = 0  
y0 = 0 
r = 3000  

# Obtém um midpoint em coordenadas polares
theta = 2 * np.pi * np.random.rand()  # seleciona componente angular uniformemente
p = r * np.random.rand()  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2)  # distância do midpoint até a borda do círculo

# calcula componentes trigonométricas
sin_theta = np.sin(theta)
cos_theta = np.cos(theta)

# calcula os midpoints em coordenadas cartesianas
x_mid = p*cos_theta
y_mid = p*sin_theta

# calcula os pontos finais dos segmentos do PPP
x1 = x0 + p * cos_theta + q * sin_theta
y1 = y0 + p * sin_theta - q * cos_theta
x2 = x0 + p * cos_theta - q * sin_theta
y2 = y0 + p * sin_theta + q * cos_theta

# plota o círculo
c = np.linspace(0, 2 * np.pi, 200)
x_circle = r * np.cos(c)
y_circle = r * np.sin(c)
fig, ax = plt.subplots()
ax.plot(x0 + x_circle, y0 + y_circle, 'k--', alpha=0.5)
plt.axis('equal')

# PLOTA OS ELEMENTOS NO CIRCULO

ax.plot([x0, x_mid], [y0, y_mid], 'k--', label='P') # Plota o raio P

ax.scatter(x0,y0, marker='o',color='k', facecolors='none') # Plota origem

ax.scatter(x_mid,y_mid, marker='o', color='r') # Plota midpoint
ax.text(x_mid*1.1,y_mid*1.1,'(P,θ)',color='r')

ax.plot([x1,x2],[y1,y2],'b') # Plota segmento de PLP
ax.scatter([x1,x2],[y1,y2], marker='o', color='b', alpha=0.7)
ax.text(x1,y1*1.1,'(X1,Y1)',color='b')
ax.text(x2,y2*1.1,'(X2,Y2)',color='b')

# Quando verdadeiro, plota medidas trigonometricas adicionais
print_markers = True

if(print_markers):

    ax.plot([x0,x1],[y0,y1], color='darkorchid', linestyle='dashed', label='r') # Plota r

    ax.plot([x_mid,x1],[y_mid,y1], color='lime', linestyle='dashed', label='Q')

    # Gera uma label no meio dos segmentos
    labelLines(ax.get_lines(), align=False, xvals=((x0 + x_mid)/2, (x0 + x1)/2, (x_mid + x1)/2 ))
else:
    labelLines(ax.get_lines(), align=False, xvals=((x0 + x_mid)/2))

plt.title('Representação do Modelo 2 do Paradoxo de Bertrand')
plt.show()

