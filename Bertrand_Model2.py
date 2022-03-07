# Script que produz uma demonstração gráfica do Modelo 2 do Paradoxo de Bertrand
# Utilizado para produzir ruas através de um PLP em uma área circular para redes V2X

import numpy as np;  # Pacote NumPy para vetores, gerador de números aleatórios, etc
import matplotlib.pyplot as plt  # para plotagem
from matplotlib import collections  as mc  # para plotar segmentos de linhas

# Dimensões do disco
x0 = 0;  # Centro x do disco
y0 = 0;  # Centro y do disco
r = 3000;  # Raio do disco

# Obtém um midpoint em coordenadas polares
theta = 2 * np.pi * np.random.rand();  # seleciona componente angular uniformemente
p = r * np.random.rand();  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2);  # distância do midpoint até a borda do círculo

# calcula componentes trigonométricas
sin_theta = np.sin(theta);
cos_theta = np.cos(theta);

# calcula os midpoints em coordenadas cartesianas
x_mid = p*cos_theta
y_mid = p*sin_theta

# calcula os pontos finais dos segmentos do PPP
x1 = x0 + p * cos_theta + q * sin_theta;
y1 = y0 + p * sin_theta - q * cos_theta;
x2 = x0 + p * cos_theta - q * sin_theta;
y2 = y0 + p * sin_theta + q * cos_theta;

# plota o círculo
c = np.linspace(0, 2 * np.pi, 200);
x_circle = r * np.cos(c);
y_circle = r * np.sin(c);
fig, ax = plt.subplots();
ax.plot(x0 + x_circle, y0 + y_circle, 'k--');
plt.axis('equal');

# plota os elementos no círculo
plt.plot([x0, x_mid], [y0, y_mid], 'k--') # Plota o raio P
plt.scatter(x0,y0, marker='o',color='k', facecolors='none') # Plota origem
plt.scatter(x_mid,y_mid, marker='o', color='red') # Plota midpoint
plt.plot([x1,x2],[y1,y2],'b') # plota segmentos de PLP

plt.title('Representação do Modelo 2 do Paradoxo de Bertrand')
plt.show()

