# PLS_CooperativeJamming 

Scripts em python para realizar simulações de PLS (Physical Layer Security) utilizando as técnicas de Cooperative Jamming em redes V2X.

## Detalhamento de cada Script

### Bertrand_Model2.py

Produz uma representação gráfica do Modelo 2 do Paradoxo de Bertrand para geração de retas distribuídas uniformemente em uma área circular. Em redes V2X, é uma das técnicas para se produzir ruas em uma dada região.

![Uma realização de Bertrand_Model2.py](https://user-images.githubusercontent.com/64433982/156959802-e9ad59b5-8cc7-4ad9-9eca-cd33db863e86.png)

Nela, um midpoint (ponto vermelho) é gerado com ângulo $\theta$ e um raio $P$ obtidos por distribuições uniformes independentes. A reta é então gerada ao traçar um segmento perpendicular à P e que cruza o midpoint, terminando quando ele atinge as extremidades da área circular. Os pontos finais (X1,Y1) e (X2,Y2) são calculados por trigonometria simples dado que a distância entre cada um deles e o midpoint é dada por Q.   

### Spatial_Sim.py

Produz os nós veiculares e planares inspirada na rede C-V2X apresentada por Wang et. al em https://doi.org/10.48550/arXiv.2009.14500. 

![Uma realização de Spatial_Sim.py](https://user-images.githubusercontent.com/64433982/156959919-e9ec95fc-763e-4a57-8383-7b7ef9d1ae97.png)

[Símbolos do modelo simulado](https://user-images.githubusercontent.com/64433982/156960143-24c94a4f-4cc4-4927-a0e7-cba612d0a79d.png)

* As ruas são geradas por um Processo Linear de Poisson (PLP) baseado no Modelo 2 do Paradoxo de Bertrand.

* Os nós planares (pedestres e infraestruturas) são gerados por Processos Pontuais de Poisson (PPPs) em que a quantidade de pontos é uma distribuição de Poisson parametrizada pela medida de Lebesgue (neste caso a área do círculo) vezes a intensidade desejada para cada tipo de nó. A posição de cada ponto é determinado por distribuições uniformes de suas coordenadas polares.

* Os nós veiculares são obtidos por Processos Lineares Cox Poisson (PLCPs) em que cada rua obtida pelo PLP é então populada com um PPP 1-D ao longo de seu comprimento. !
