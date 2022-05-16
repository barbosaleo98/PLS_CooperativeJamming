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
P_t = 0.01 # W
P_c = 0.01 # W

# Razao Charlies/Eves
CE_ratio = [0.1, 0.5, 1, 5]

# Intensidades dos Eves
mu_eves = 1*1e-3 # PLCP
lambda_eves=1*1e-6 #PPP

SOP_cj = np.zeros((sim_size, num_cols))

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)

for ce in CE_ratio:
    # Intensidades dos Charlies
    mu_charlies = ce*mu_eves # PLCP
    lambda_charlies= ce*lambda_eves # PPP
    
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
     
        SOP_i_cj = []
        
        for phi in Phi:
            aux_phi_a = P_t*(1-phi)/(N-1)
            aux_phi_c = P_c/(N-1)

            dist_eve_alice = np.sqrt(x_eves**2 + y_eves**2)

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
                den_SIR_c = aux_phi_c*norm_g_e*(dist_eve_alice[e]**(-alfa))+Sum_Ic
                SIR_c_db = 10*math.log10(num_SIR/den_SIR_c)
                SIR_e_c.append(SIR_c_db)

            so_cj = 0
                        
            for sir_c in SIR_e_c:
                if sir_c > beta:
                    so_cj = so_cj + 1        

            SOP_i_cj.append(so_cj/total_eves)   

        SOP_cj[sim_i] = SOP_i_cj

    SOP_avg_cj = np.average(SOP_cj, axis=0)
    ax.plot(Phi,SOP_avg_cj, label= r'CJ $\eta$ = %.1f' %ce)

plt.xlabel(r'$\phi$')
plt.ylabel('SOP')
plt.legend() 

fig.text(0.1,0.05,r'Realizações: %d, $\beta$: %d dB, $\alpha$: %.1f, $P_t :$ %.2f W, $P_c :$ %.2f W ' %(sim_size, beta, alfa, P_t, P_c))
plt.show()