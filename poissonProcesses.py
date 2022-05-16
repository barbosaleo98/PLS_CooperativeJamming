# Baseado em scripts de H. Paul Keeler, 2019.
# Repositório: github.com/hpaulkeeler/posts

from numpy import random, repeat, pi, sin, cos, sqrt

def PLCP_points(mu,p,q,sin_theta,cos_theta,x0=0,y0=0):
    lengthLine = 2 * q  # comprimento de cada segmento
    massPoint = mu * lengthLine  # intensidade "efetiva" de cada PPP
    numbLinePoints = random.poisson(massPoint)  # Numero de pontos em cada linha
    numbLinePointsTotal = sum(numbLinePoints) # Numero total de pontos do PLCP
    uu = 2 * random.rand(numbLinePointsTotal) - 1  # distribuição uniforme U(-1,1)

    # replica os valores para simular todos pontos em um único passo
    x0_all = repeat(x0, numbLinePointsTotal)
    y0_all = repeat(y0, numbLinePointsTotal)
    p_all = repeat(p, numbLinePoints)
    q_all = repeat(q, numbLinePoints)
    sin_theta_all = repeat(sin_theta, numbLinePoints)
    cos_theta_all = repeat(cos_theta, numbLinePoints)

    # Posiciona os pontos nos segmentos lineares de Poisson
    xPP_all = x0_all + p_all * cos_theta_all + q_all * uu * sin_theta_all
    yPP_all = y0_all + p_all * sin_theta_all - q_all * uu * cos_theta_all

    return xPP_all, yPP_all, numbLinePointsTotal

def PPP_points(lambda_process, radius):
    area_circle = pi*radius**2
    mean = lambda_process*area_circle
    num_Points = random.poisson(mean)
    theta = 2*pi*random.uniform(0,1,num_Points)
    rho = radius*sqrt(random.uniform(0,1,num_Points))
    x = rho * cos(theta)
    y = rho * sin(theta)

    return x,y, num_Points