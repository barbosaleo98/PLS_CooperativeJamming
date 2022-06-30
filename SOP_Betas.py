import numpy as np;  # Pacote NumPy para vetores, gerador de números aleatórios, etc
import matplotlib.pyplot as plt  # para plotagem
from matplotlib import collections  as mc  # para plotar segmentos de linhas
import math
from scipy.stats import expon, gamma
from itertools import cycle

plt.close('all');  # fecha as figuras já abertas

lambda_roads = 1e-3/np.pi;  # intensidade (densidade média) do PLP
mu_cox = 1e-3; # intensidade (densidade média) do PPP 1-D 

xx0 = 0;  # Centro x do disco
yy0 = 0;  # Centro y do disco
r = 3000;  # Raio do disco
massLine = 2 * np.pi * r * lambda_roads; # Parâmetro da distribuicao de Poisson do PLP
areaTotal=np.pi*r**2; # Área do disco

# Simula o PPP dos midpoints
numbLines = np.random.poisson(massLine);  # Número de linhas/midpoints

theta = 2 * np.pi * np.random.rand(numbLines);  # seleciona componente angular uniformemente
p = r * np.random.rand(numbLines);  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2);  # distância do midpoint para a borda do círculo 

# calcula componentes trigonométricas
sin_theta = np.sin(theta);
cos_theta = np.cos(theta);

# calcula os pontos finais dos segmentos do PLP
xx1 = xx0 + p * cos_theta + q * sin_theta;
yy1 = yy0 + p * sin_theta - q * cos_theta;
xx2 = xx0 + p * cos_theta - q * sin_theta;
yy2 = yy0 + p * sin_theta + q * cos_theta;

def PPP_roads(mu,p,q,sin_theta,cos_theta,xx0,yy0):
    ###START Simula um PPP em cada linha START###
    lengthLine = 2 * q;  # comprimento de cada segmento
    massPoint = mu * lengthLine;  # intensidade "efetiva" de cada PPP
    numbLinePoints = np.random.poisson(massPoint);  # Numero de pontos em cada linha
    numbLinePointsTotal = sum(numbLinePoints); # Numero total de pontos do PLCP
    uu = 2 * np.random.rand(numbLinePointsTotal) - 1;  # distribuição uniforme U(-1,1)

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
    return xxPP_all, yyPP_all, numbLinePointsTotal

def PPP_points(lambda_process, radius):
    area_circle = np.pi*radius**2
    num_Points = np.random.poisson(lambda_process*area_circle)
    mean = lambda_process*area_circle
    theta = 2*np.pi*np.random.uniform(0,1,num_Points)
    rho = radius*np.sqrt(np.random.uniform(0,1,num_Points))
    xx = rho * np.cos(theta)
    yy = rho * np.sin(theta)
    return xx,yy, num_Points

# Parâmetros da simulacao do SOP
sim_size = 50
num_cols = 15
alfa = 3
N = 4

Phi = [0.4, 0.6, 0.8]
Beta = np.linspace(-10,15,num_cols)

# Potencias
P_t = 0.1
P_c = 0.1

ce_ratio = 1

# Parâmetros dos PLCPs
mu_transmitter = ce_ratio*1e-3
mu_eves = 1*1e-3

# Parâmetros dos PPPs 
lambda_transmitter= ce_ratio*1e-6; # Intensidade (densidade média) do PPP
lambda_eves=1*1e-6;

SOP = np.zeros((sim_size, num_cols))
SOP_cj = np.zeros((sim_size, num_cols))

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)

line_style = cycle(['solid', 'dashed', 'dashdot'])

for phi in Phi:
    for sim_i in range(sim_size):
        
        xxPP_transmitter, yyPP_transmitter, numPP_transmitter = PPP_roads(mu_transmitter,p,q,sin_theta,cos_theta,xx0,yy0)

        xxPP_eves, yyPP_eves, numPP_eves = PPP_roads(mu_eves,p,q,sin_theta,cos_theta,xx0,yy0)
     
        # Simula PPP para Alices
        xx_transmitter, yy_transmitter, num_transmitters = PPP_points(lambda_transmitter, r)
        
        # Simula PPP para Eves
        xx_eves, yy_eves, num_eves = PPP_points(lambda_eves, r)
        
        # Totaliza nos planares e veiculares
        total_transmitters = num_transmitters + numPP_transmitter
        #print(total_transmitters)
        total_eves = num_eves + numPP_eves

        # Une as coordenadas dos nos alices e eves
        xx_transmitter = np.append(xx_transmitter, xxPP_transmitter)
        yy_transmitter = np.append(yy_transmitter, yyPP_transmitter)
        
        xx_eves = np.append(xx_eves, xxPP_eves)
        yy_eves = np.append(yy_eves, yyPP_eves)
     
        SOP_i = []
        SOP_i_cj = []
        
        for beta in Beta:
            aux_phi_a = P_t*(1-phi)/(N-1)
            aux_phi_c = P_c/(N-1)

            dist_eo = np.sqrt(xx_eves**2 + yy_eves**2)

            SIR_e = []
            SIR_e_c = []

            for e in range(total_eves):
                q_e2 = np.random.exponential(1)
                norm_g_e = np.random.gamma(N-1,1)
                norm_g_c = np.random.gamma(N-1,1)
                
                Sum_Ic = 0
                
                for x in range(total_transmitters):
                    dist_xe = np.sqrt((xx_eves[e]-xx_transmitter[x])**2 + (yy_eves[e]-yy_transmitter[x])**2)
                    I_c = aux_phi_a*norm_g_e*(dist_xe**(-alfa))
                    Sum_Ic = Sum_Ic + I_c
                
                num_SIR = phi*q_e2*(dist_eo[e]**(-alfa))
                den_SIR = aux_phi_a*norm_g_e*(dist_eo[e]**(-alfa))
                den_SIR_c = aux_phi_c*norm_g_e*(dist_eo[e]**(-alfa))+Sum_Ic
                SIR_e_db = 10*math.log10(num_SIR/den_SIR)
                SIR_c_db = 10*math.log10(num_SIR/den_SIR_c)
                SIR_e.append(SIR_e_db)
                SIR_e_c.append(SIR_c_db)

            so = 0
                
            for sir_e in SIR_e:
                if sir_e > beta:
                    so = so + 1
         
            SOP_i.append(so/total_eves)
            
            so_cj = 0
                        
            for sir_c in SIR_e_c:
                if sir_c > beta:
                    so_cj = so_cj + 1        

            SOP_i_cj.append(so_cj/total_eves)   

        SOP[sim_i] = SOP_i
        SOP_cj[sim_i] = SOP_i_cj

    SOP_avg = np.average(SOP, axis=0)
    SOP_avg_cj = np.average(SOP_cj, axis=0)
    
    current_style = next(line_style)

    #ax.plot(Beta,SOP_avg, label= r'AN: $\phi$ = %.1f' %phi)
    #ax.plot(Beta,SOP_avg_cj, label= r'CJ: $\phi$ = %.1f' %phi)

    ax.semilogy(Beta,SOP_avg, label= r'AN: $\phi$ = %.1f' %phi, linestyle= current_style, linewidth=2)
    ax.semilogy(Beta,SOP_avg_cj, label= r'CJ: $\phi$ = %.1f' %phi, linestyle= current_style, linewidth=2)


plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--', alpha=.7)
plt.xlabel(r'$\beta$')
plt.ylabel('SOP')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=9)

#fig.text(0.1,0.05,r'Realizações: %d, $\phi$: %.2f dB, $\alpha$: %d' %(sim_size, phi, alfa))
plt.savefig('imgs/SOP_Betas.svg', bbox_inches='tight')
plt.savefig('imgs/SOP_Betas.png', bbox_inches='tight')
plt.show()