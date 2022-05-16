import numpy as np  # Pacote NumPy para vetores, gerador de números aleatórios, etc
import matplotlib.pyplot as plt  # para plotagem
import math
import poissonProcesses as pp

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
P_t_list = [0.5, 1, 2, 4]

# Intensidades dos Eves
mu_eves = 1*1e-3 # PLCP
lambda_eves=1*1e-6 #PPP

SOP = np.zeros((sim_size, num_cols))

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)

for P_t in P_t_list:    
    for sim_i in range(sim_size):
        
        # Simula PPP e PLCP para eves
        x_vehicular_eves, y_vehicular_eves, num_vehicular_eves = pp.PLCP_points(mu_eves,p,q,sin_theta,cos_theta)
        x_planar_eves, y_planar_eves, num_planar_eves = pp.PPP_points(lambda_eves, r)
        
        # Totaliza nos planares e veiculares
        total_eves = num_planar_eves + num_vehicular_eves

        # Une as coordenadas dos nos planares e veiculares
        x_eves = np.append(x_planar_eves, x_vehicular_eves)
        y_eves = np.append(y_planar_eves, y_vehicular_eves)
     
        SOP_i = []
        
        for phi in Phi:
            aux_phi_a = P_t*(1-phi)/(N-1)

            dist_eve_alice = np.sqrt(x_eves**2 + y_eves**2)

            SIR_e = []

            for e in range(total_eves):
                q_e2 = np.random.exponential(1)
                norm_g_e = np.random.gamma(N-1,1)
                
                
                num_SIR = phi*q_e2*(dist_eve_alice[e]**(-alfa))
                den_SIR = aux_phi_a*norm_g_e*(dist_eve_alice[e]**(-alfa))
                SIR_e_db = 10*math.log10(num_SIR/den_SIR)
                SIR_e.append(SIR_e_db)
     
            so = 0
                
            for sir_e in SIR_e:
                if sir_e > beta:
                    so = so + 1
         
            SOP_i.append(so/total_eves)  

        SOP[sim_i] = SOP_i

    SOP_avg = np.average(SOP, axis=0)
    ax.plot(Phi,SOP_avg, label= r'AN $P_t$ = %.2f W' %P_t)

plt.xlabel(r'$\phi$')
plt.ylabel('SOP')
plt.legend() 

fig.text(0.1,0.05,r'Realizações: %d, $\beta$: %d dB, $\alpha$: %d, $N_a$: %d' %(sim_size,beta, alfa, N))  
plt.show()