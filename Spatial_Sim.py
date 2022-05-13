# Realiza a simulação geométrica estocástica para representação espacial de uma rede V2X

# Busca reproduzir resultados de Wang et al, 2020
# https://doi.org/10.48550/arXiv.2009.14500

# Baseado em scripts de H. Paul Keeler, 2019.
# Repositório: github.com/hpaulkeeler/posts

import numpy as np;  
import matplotlib.pyplot as plt  
from matplotlib import collections  as mc 

plt.close('all')

### ÁREA CIRCULAR ###

# Parâmetros: origem em (x0,y0) e raio r
x0 = 0
y0 = 0 
r = 3000 

# Plota o círculo com um 'x' na origem
t = np.linspace(0, 2 * np.pi, 200)
xp = r * np.cos(t)
yp = r * np.sin(t)
fig, ax = plt.subplots()
ax.plot(x0 + xp, y0 + yp, 'k--', alpha=0.7)
#ax.scatter(x0,y0, marker='x',color='k', label='Nó Alice')
ax.scatter(x0,y0, marker='x',color='k', label='Alice node')
ax.axis('equal')


### PROCESSO PONTUAL DE POISSON (PPP) - NÓS PLANARES ###

## Função que produz os nós planares através de um PPP
def planarNodes(lambda_PPP, radius):
    area_circle = np.pi*radius**2
    num_Points_PPP = np.random.poisson(lambda_PPP*area_circle)
    theta_PPP = 2*np.pi*np.random.uniform(0,1,num_Points_PPP)
    rho_PPP = radius*np.sqrt(np.random.uniform(0,1,num_Points_PPP))
    x_planar = rho_PPP * np.cos(theta_PPP)
    y_planar = rho_PPP * np.sin(theta_PPP)
    return x_planar,y_planar, num_Points_PPP

# Geração dos nós planares 
lambda_alices=1*1e-6; 
lambda_eves=1*1e-6; 
x_planar_alices, y_planar_alices , num_planar_alices = planarNodes(lambda_alices, r)
x_planar_eves, y_planar_eves, num_eves = planarNodes(lambda_eves, r)
 
#Plotta os nós planares
#ax.scatter(x_planar_alices, y_planar_alices, marker='o', edgecolor='g', facecolor='none', label='Charlies Planares')
#ax.scatter(x_planar_eves, y_planar_eves, marker='o', edgecolor='r', facecolor='none', label='Eves Planares')
ax.scatter(x_planar_alices, y_planar_alices, marker='o', edgecolor='g', facecolor='none', label='Planar Charlies')
ax.scatter(x_planar_eves, y_planar_eves, marker='o', edgecolor='r', facecolor='none', label='Planar Eves')

### PROCESSO LINEAR DE POISSON (PLP) - RUAS DA REDE ###

lambda_roads = 1e-3/np.pi;  # intensidade do PLP

# Simula um PLP na área circular
massLine = 2 * np.pi * r * lambda_roads 
numLines = np.random.poisson(massLine)  
theta_PLP = 2 * np.pi * np.random.rand(numLines)  # seleciona componente angular uniformemente
p = r * np.random.rand(numLines)  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2)  # distância do midpoint para a borda do círculo 
sin_theta_PLP = np.sin(theta_PLP)
cos_theta_PLP = np.cos(theta_PLP)

# calcula os pontos finais dos segmentos do PLP
x1 = x0 + p * cos_theta_PLP + q * sin_theta_PLP
y1 = y0 + p * sin_theta_PLP - q * cos_theta_PLP
x2 = x0 + p * cos_theta_PLP - q * sin_theta_PLP
y2 = y0 + p * sin_theta_PLP + q * cos_theta_PLP

# plota segmentos do PLP
segments = [[(x1[i], y1[i]), (x2[i], y2[i])] for i in range(numLines)]
lc = mc.LineCollection(segments, colors='b', cmap='jet', alpha=0.7)
ax.add_collection(lc)  

## Pontos para definir e plotar a rua lo (opcional, descomentar para habilitar)
#xo_1 = -r
#xo_2 = r 
#ax.plot((xo_1, xo_2), (y0,y0), color='darkorchid', linewidth=1.5)


### PROCESSO LINEAR COX DE POISSON (PLCP) - NÓS VEICULARES ###

# Função que gera os nós veiculares através de um PLCP
def vehicularNodes(mu,p,q,sin_theta,cos_theta,x0,y0):
    lengthLine = 2 * q  
    massPoint = mu * lengthLine;  # intensidade de cada PPP
    num_Points_PLCP = np.random.poisson(massPoint)
    Total_Points_PLCP = sum(num_Points_PLCP)
    uu = 2 * np.random.rand(Total_Points_PLCP) - 1  

    # replica os valores para simular todos pontos em um único passo
    x0_all = np.repeat(x0, Total_Points_PLCP)
    y0_all = np.repeat(y0, Total_Points_PLCP)
    p_all = np.repeat(p, num_Points_PLCP)
    q_all = np.repeat(q, num_Points_PLCP)
    sin_theta_all = np.repeat(sin_theta, num_Points_PLCP)
    cos_theta_all = np.repeat(cos_theta, num_Points_PLCP)

    # Posiciona os pontos nos segmentos lineares 
    x_vehicular_all = x0_all + p_all * cos_theta_all + q_all * uu * sin_theta_all
    y_vehicular_all = y0_all + p_all * sin_theta_all - q_all * uu * cos_theta_all

    return x_vehicular_all, y_vehicular_all

# Gera os nós veiculares Alices e Eves
mu_alices = 1e-3
mu_eves = 1e-3
x_vehicular_alices, y_vehicular_alices = vehicularNodes(mu_alices,p,q,sin_theta_PLP,cos_theta_PLP,x0,y0)
x_vehicular_eves, y_vehicular_eves = vehicularNodes(mu_eves,p,q,sin_theta_PLP,cos_theta_PLP,x0,y0)

# plota os nós veiculares
#ax.scatter(x_vehicular_alices, y_vehicular_alices, marker = '^', edgecolor = 'g', facecolor='none', label='Charlies Veiculares')
#ax.scatter(x_vehicular_eves, y_vehicular_eves, marker='^', edgecolor='r', facecolor='none', label='Eves Veiculares')
ax.scatter(x_vehicular_alices, y_vehicular_alices, marker = '^', edgecolor = 'g', facecolor='none', label='Vehicular Charlies')
ax.scatter(x_vehicular_eves, y_vehicular_eves, marker='^', edgecolor='r', facecolor='none', label='Vehicular Eves')

#ax.legend(bbox_to_anchor=(0.52,0), loc="lower center", bbox_transform=fig.transFigure, ncol=1, borderpad=0.6)
ax.legend(ncol=1, loc="upper left", fontsize=7)
#plt.title('Rede V2X modelada para simulações de PLS')
plt.title('V2X Network modeled for PLS simulations')
plt.tight_layout()

plt.show()