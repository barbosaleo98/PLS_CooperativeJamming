# Realiza a simulação geométrica estocástica para representação espacial dos eleemntos
# Baseado em um script  do Autor: H. Paul Keeler, 2019.
# Repositório: github.com/hpaulkeeler/posts
# Post utilizado como base: hpaulkeeler.com/simulating-a-cox-point-process-based-on-a-poisson-line-process/

import numpy as np;  # Pacote NumPy para vetores, gerador de números aleatórios, etc
import matplotlib.pyplot as plt  # para plotagem
from matplotlib import collections  as mc  # para plotar segmentos de linhas

plt.close('all');  # fecha as figuras já abertas

###START -- Parâmetros -- START###
# Parâmetros do processo de Cox (PLP) 
# O processo de pontos de Cox é realizado primeiramente simulando um PLP
# Em cada linha (ou segmento) um PLP independente é então simulado

lambda0 = 1e-3/np.pi;  # intensidade (densidade média) do PLP
mu = 1e-3; # intensidade (densidade média) do PPP 

# Dimensões do disco
xx0 = 0;  # Centro x do disco
yy0 = 0;  # Centro y do disco
r = 3000;  # Raio do disco
massLine = 2 * np.pi * r * lambda0;
areaTotal=np.pi*r**2; # Área do disco
###END -- Parâmetros -- END###

###START -- Simula um PLP no disco -- START###
# Simula o PPP
numbLines = np.random.poisson(massLine);  # Número de pontos de Poisson

theta = 2 * np.pi * np.random.rand(numbLines);  # seleciona componente angular uniformemente
p = r * np.random.rand(numbLines);  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2);  # distância da borda do círculo (alonge line)

# calcula componentes trigonométricas
sin_theta = np.sin(theta);
cos_theta = np.cos(theta);

# calcula os pontos finais dos segmentos do PPP
xx1 = xx0 + p * cos_theta + q * sin_theta;
yy1 = yy0 + p * sin_theta - q * cos_theta;
xx2 = xx0 + p * cos_theta - q * sin_theta;
yy2 = yy0 + p * sin_theta + q * cos_theta;
###END Simula um PLP no disco END###

def PPP_roads(mu,p,q,sin_theta,cos_theta,xx0,yy0):
    ###START Simula um PPP em cada linha START###
    lengthLine = 2 * q;  # length of each segment
    massPoint = mu * lengthLine;  # mass on each line
    numbLinePoints = np.random.poisson(massPoint);  # Poisson number of points on each line
    numbLinePointsTotal = sum(numbLinePoints);
    uu = 2 * np.random.rand(numbLinePointsTotal) - 1;  # uniform variables on (-1,1)

    # replica os valores para simular todos pontos em um único passo
    xx0_all = np.repeat(xx0, numbLinePointsTotal);
    yy0_all = np.repeat(yy0, numbLinePointsTotal);
    p_all = np.repeat(p, numbLinePoints);
    q_all = np.repeat(q, numbLinePoints);
    sin_theta_all = np.repeat(sin_theta, numbLinePoints);
    cos_theta_all = np.repeat(cos_theta, numbLinePoints);

    # Posiciona os pontos nos segmentos lineares de Poisson
    xxPP_all = xx0_all + p_all * cos_theta_all + q_all * uu * sin_theta_all;
    yyPP_all = yy0_all + p_all * sin_theta_all - q_all * uu * cos_theta_all;
    ### FIM Simula um PPP em cada linha  ###
    return xxPP_all, yyPP_all


xxPP_transmitter, yyPP_transmitter = PPP_roads(mu,p,q,sin_theta,cos_theta,xx0,yy0)
xxPP_eves, yyPP_eves = PPP_roads(1e-3,p,q,sin_theta,cos_theta,xx0,yy0)

### START Plotaegem do PLP ###
# plota o círculo
t = np.linspace(0, 2 * np.pi, 200);
xp = r * np.cos(t);
yp = r * np.sin(t);
fig, ax = plt.subplots();
ax.plot(xx0 + xp, yy0 + yp, 'r--');
plt.axis('equal');

# plota segmentos de PLP
# Cria uma lista para plotar os segmentos
segments = [[(xx1[i], yy1[i]), (xx2[i], yy2[i])] for i in range(numbLines)];
lc = mc.LineCollection(segments, colors='b')
ax.add_collection(lc)  # plota os segmentos criados

# plota pontos de Poisson nas linhas
plt.plot(xxPP_transmitter, yyPP_transmitter, 'g^');
plt.plot(xxPP_eves, yyPP_eves, 'ko');

###END Plotagem do PLP END###

## Criação de função que cria os pontos de um PPP
def PPP_points(lambda_process, area_circle, radius):
    num_Points = np.random.poisson(lambda_process*area_circle)
    theta = 2*np.pi*np.random.uniform(0,1,num_Points)
    rho = radius*np.sqrt(np.random.uniform(0,1,num_Points))
    xx = rho * np.cos(theta)
    yy = rho * np.sin(theta)
    return xx,yy

# Parâmetros do PPP para Alices
lambda_transmitter=1e-6; # Intensidade (densidade média) do PPP
 
# Simula PPP para Alices
xx_transmitter, yy_transmitter = PPP_points(lambda_transmitter, areaTotal, r)
 
#Plotta os Alices
plt.scatter(xx_transmitter,yy_transmitter, marker='s', color='cyan' );

# Parâmetros do PPP para Eves
lambda_eves=1e-6; # Intensidade (densidade média) do PPP
 
# Simula PPP para Eves
xx_eves, yy_eves = PPP_points(lambda_eves, areaTotal, r)
 
#Plota os Eves
plt.scatter(xx_eves,yy_eves, marker='*', color='purple')
plt.title('Simulação Espacial baseada em (WANG, C. et al., 2020)')
plt.show()