# PLS_CooperativeJamming 

Scripts em python para realizar simulações de PLS (Physical Layer Security) utilizando as técnicas de Cooperative Jamming em redes V2X.

## Detalhamento de cada Script

### Bertrand_Model2.py

Produz uma representação gráfica do Modelo 2 do Paradoxo de Bertrand para geração de retas distribuídas uniformemente em uma área circular. Em redes V2X, é uma das técnicas para se produzir ruas em uma dada região.

![Uma realização de Bertrand_Model2.py](https://user-images.githubusercontent.com/64433982/156959802-e9ad59b5-8cc7-4ad9-9eca-cd33db863e86.png)

*Realização do script*

Nela, um midpoint (ponto vermelho) é gerado com ângulo &theta; e um raio P obtidos por distribuições uniformes independentes. A reta é então gerada ao traçar um segmento perpendicular à P e que cruza o midpoint, terminando quando ele atinge as extremidades da área circular. Os pontos finais (X1,Y1) e (X2,Y2) são calculados por trigonometria simples dado que a distância entre cada um deles e o midpoint é dada por Q. Nota-se que estes pontos são distribuídos uniformemente ao longo do perímetro da circunferência.  

<img src="https://user-images.githubusercontent.com/64433982/156960904-25f2732b-8845-4f99-a691-b95e1508e740.png" alt="Mesma realização de Bertrand_Model2.py com anotações trigonométrica" width="600"/>

*Mesma realização do script, mas com as medidas trigonométricas mencionadas acima*

### Spatial_Sim.py

Produz os nós veiculares e planares inspirada na rede C-V2X apresentada no artigo "Physical Layer Security Enhancement Using Artificial Noise in Cellular Vehicle-to-Everything (C-V2X) Networks" de Wang et. al, disponível em: https://doi.org/10.48550/arXiv.2009.14500. 

![Uma realização de Spatial_Sim.py](https://user-images.githubusercontent.com/64433982/167932432-1ddd74de-7c9a-402a-a684-0d6dfce78366.png)

<img src="https://user-images.githubusercontent.com/64433982/167931972-496e9e0e-4582-4b7a-9492-56bef98b18f1.png" alt="Símbolos do modelo simulado" width="600"/>

A quantia de cada elementos é obtida por uma distribuição de Poisson, cujo parâmetro é dado pelo produto da medida de Lebesgue (que em espaços euclidianos de n=[1,2,3] corresponde ao comprimento, área e volume, respectivamente) vezes a intensidade do processo.

* As ruas são geradas por um Processo Linear de Poisson (PLP) baseado no Modelo 2 do Paradoxo de Bertrand. A medida de Lebesgue é o perímetro da área circular.

* Os nós planares (pedestres e infraestruturas) são gerados por Processos Pontuais de Poisson (PPPs) e a medida de Lebesgue neste caso é a área do círculo. A posição de cada ponto é determinado por distribuições uniformes de suas coordenadas polares.

* Os nós veiculares são obtidos por Processos Lineares Cox Poisson (PLCPs) em que cada rua obtida pelo PLP é então populada com um PPP 1-D ao longo de seu comprimento (medida de Lebesgue). A posição de cada nó é dada por uma distribuição uniforme U(-1,1) que varre todo o segmento entre (X1,Y1) e (X2,Y2). 
