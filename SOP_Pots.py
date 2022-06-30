import numpy as np  # Pacote NumPy para vetores, gerador de números aleatórios, etc
import matplotlib.pyplot as plt  # para plotagem
import math
from itertools import cycle
import poissonProcesses as pp
from full_extent import full_extent

plt.close('all')  

### ÁREA CIRCULAR ###

# Parametros circulo: origem em (x0,y0) e raio r
x0 = 0  
y0 = 0  
r = 3000  
areaTotal=np.pi*r**2 

### PROCESSO LINEAR DE POISSON (PLP) - RUAS DA REDE ###

lambda_roads = 1e-3/np.pi  # intensidade (densidade média) do PLP
massLine = 2 * np.pi * r * lambda_roads # Parâmetro da distribuicao de Poisson do PLP

# Simula o PPP dos midpoints
numbLines = np.random.poisson(massLine)  # Número de linhas/midpoints
theta = 2 * np.pi * np.random.rand(numbLines)  # seleciona componente angular uniformemente
p = r * np.random.rand(numbLines)  # seleciona componente radial uniformemente
q = np.sqrt(r ** 2 - p ** 2)  # distância do midpoint para a borda do círculo 

sin_theta = np.sin(theta)
cos_theta = np.cos(theta)

### SIMULACAO DA SOP ###

sim_size = 25 # Realizacoes da simulacao
num_cols = 25 # Numero de pontos na realizacao
alfa = 3
N = 4
Phi = np.linspace(0.00001,0.9999999,num_cols)
beta = 0 # dB

# Potencias
P_t_list = [0.01, 0.1, 1]

# Intensidades dos Eves
mu_eves = 1*1e-3 # PLCP
lambda_eves=1*1e-6 #PPP

# Intensidades dos Charlies
mu_charlies = 1*1e-3 # PLCP
lambda_charlies=1*1e-6 #PPP

SOP = np.zeros((sim_size, num_cols))
SOP_cj = np.zeros((sim_size, num_cols))

fig,ax = plt.subplots(1,2)
line_style = cycle(['solid', 'dashed', 'dashdot'])

for P_t in P_t_list:    
    for sim_i in range(sim_size):
        
        # Simula PPP e PLCP para charlies e eves
        x_vehicular_charlies, y_vehicular_charlies, num_vehicular_charlies = pp.PLCP_points(mu_charlies,p,q,sin_theta,cos_theta)
        x_vehicular_eves, y_vehicular_eves, num_vehicular_eves = pp.PLCP_points(mu_eves,p,q,sin_theta,cos_theta)
        x_planar_charlies, y_planar_charlies, num_planar_charlies = pp.PPP_points(lambda_charlies, r)
        x_planar_eves, y_planar_eves, num_planar_eves = pp.PPP_points(lambda_eves, r)
        
        # Totaliza nos planares e veiculares
        total_transmitters = num_planar_charlies + num_vehicular_charlies
        total_eves = num_planar_eves + num_vehicular_eves

        # Une as coordenadas dos nos planares e veiculares
        x_charlies = np.append(x_planar_charlies, x_vehicular_charlies)
        y_charlies = np.append(y_planar_charlies, y_vehicular_charlies)
        x_eves = np.append(x_planar_eves, x_vehicular_eves)
        y_eves = np.append(y_planar_eves, y_vehicular_eves)
     
        SOP_i = []
        SOP_i_cj = []
        
        for phi in Phi:
            aux_phi_a = P_t*(1-phi)/(N-1)
            aux_phi_c = P_t/(N-1)

            dist_eve_alice = np.sqrt(x_eves**2 + y_eves**2)

            SIR_e = []
            SIR_e_c = []

            for e in range(total_eves):
                q_e2 = np.random.exponential(1)
                norm_g_e = np.random.gamma(N-1,1)
                
                Sum_Ic = 0
                
                for x in range(total_transmitters):
                    dist_charlie_eve = np.sqrt((x_eves[e]-x_charlies[x])**2 + (y_eves[e]-y_charlies[x])**2)
                    I_c = aux_phi_a*norm_g_e*(dist_charlie_eve**(-alfa))
                    Sum_Ic = Sum_Ic + I_c

                num_SIR = phi*q_e2*(dist_eve_alice[e]**(-alfa))
                den_SIR = aux_phi_a*norm_g_e*(dist_eve_alice[e]**(-alfa))
                den_SIR_c = aux_phi_c*norm_g_e*(dist_eve_alice[e]**(-alfa))+Sum_Ic
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

    ax[0].plot(Phi,SOP_avg, label= r'$P_t$ = %.2f W' %P_t, linestyle= current_style, linewidth=2)
    ax[1].plot(Phi,SOP_avg_cj, label= r'$P_t$ = $P_c$ = %.2f W' %P_t, linestyle= current_style, linewidth=2)

ax[0].set_xlabel(r'$\phi$')
ax[0].set_ylabel('SOP')
#ax[0].set_title('Artificial Noise')
ax[0].set_ylim([-0.03,1.05])
ax[0].grid()
ax[0].legend(fontsize=8)

ax[1].set_xlabel(r'$\phi$')
ax[1].set_ylabel('SOP')
#ax[1].set_title('Cooperative Jamming')
ax[1].set_ylim([-0.03,1.05])
ax[1].grid()
ax[1].legend(fontsize=8)

plt.tight_layout()

# salva ambos os subplots em uma mesma figura 
#fig.subplots_adjust(bottom=0.2)
#fig.text(0.1,0.05,r'Realizações: %d, $\beta$: %d dB, $\alpha$: %d, $N_a$: %d' %(sim_size,beta, alfa, N))
fig.savefig('imgs/SOP_Pots_full.svg',bbox_inches='tight')  
fig.savefig('imgs/SOP_Pots_full.png',bbox_inches='tight') 

# salva cada subplot em um arquivo diferente
sub_AN = full_extent(ax[0], padx=-.15, pady=-.13).transformed(fig.dpi_scale_trans.inverted())
sub_AN = sub_AN.translated(-.18, -.15)
fig.savefig('imgs/SOP_Pots_AN.png', bbox_inches=sub_AN, dpi=300)
fig.savefig('imgs/SOP_Pots_AN.svg', bbox_inches=sub_AN)

sub_CJ = full_extent(ax[1], padx=-.15, pady=-.13).transformed(fig.dpi_scale_trans.inverted())
sub_CJ = sub_CJ.translated(-.18, -.15)
fig.savefig('imgs/SOP_Pots_CJ.png', bbox_inches=sub_CJ, dpi=300)
fig.savefig('imgs/SOP_Pots_CJ.svg', bbox_inches=sub_CJ)

plt.show()