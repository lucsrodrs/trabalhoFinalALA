This is a final work of the Algorithmic Linear Algebra discipline.
We, Lucas de Campos and I, prepared a report on the topic.

 -   **Sobre o tema**:

Decidimos fazer, para este trabalho de Álgebra Linear Algorítmica, um sistema de recomendação de apartamentos, focado naqueles que querem trocar de cidade e/ou estado. Para isso, criamos o nosso próprio banco de dados, pesquisando nos principais sites de aluguel de casas e apartamentos. Em cada linha, guardamos, na respectiva ordem: estado, cidade, metros quadrados, valor do aluguel, número de quartos, número de banheiros, número de vagas de estacionamento, se há metrô próximo, se há mercado próximo, se há escola próxima, valor do condomínio, valor do IPTU, o código no site (caso o usuário queira pesquisar e encontrar a oferta), e o site em que encontramos o apartamento.

Para realizar essa tarefa, usamos como principal conceito de Álgebra Linear Algorítmica o distanciamento euclidiano, complementado pela normalização dos vetores e o cálculo de correlação entre eles. Adicionamos pesos para que determinadas características pudessem ter maior influência no resultado. É importante ressaltar que o objetivo do programa não é retornar apenas apartamentos com uma área exata solicitada, mas sim priorizar apartamentos mais próximos da área desejada, considerando também outros critérios.

Os únicos campos excludentes são os de verdadeiro ou falso, como proximidade ao metrô, mercado e escola, pois, se o usuário considera esses fatores indispensáveis, apartamentos que não atendam a esses critérios são automaticamente descartados. Após os cálculos, o programa exibe as 5 melhores opções, detalhando cada aspecto do apartamento e apresentando a sua distância até o "ideal". Além disso, dois gráficos são gerados: um gráfico de dispersão com uma reta e um mapa de calor.

O gráfico de dispersão mostra como os apartamentos estão posicionados em relação ao ideal. Cada ponto representa um apartamento, e a reta marca o "ponto ideal". Quanto mais próximo da reta, melhor o apartamento atende aos requisitos do usuário. Já o mapa de calor analisa os vetores representando os apartamentos, exibindo o cosseno do ângulo formado entre eles. Este mapa permite identificar dependências entre os vetores. Valores próximos de 1 indicam forte relação positiva (quando uma variável aumenta, a outra também aumenta). Valores próximos de -1 indicam forte relação negativa (quando uma variável aumenta, a outra diminui). Valores próximos de zero indicam fraca ou nenhuma relação linear.
-   **Solucoes**:

Para seguirmos adiante com o tema, foi necessário utilizar o distanciamento euclidiano para identificar quais apartamentos eram ideais de acordo com os requisitos do usuário. As perguntas de sim/não foram utilizadas para filtrar os apartamentos com base nos critérios fornecidos pelo solicitante. Caso o usuário deixasse algum campo vazio, considerávamos todos os apartamentos do banco de dados, sempre respeitando as opções disponíveis.

A construção do vetor para calcular o distanciamento foi realizada com os seguintes dados:

    Área;
    Orçamento (preço do imóvel + condomínio + impostos);
    Quantidade de quartos;
    Quantidade de banheiros;
    Quantidade de vagas de estacionamento.

Esses critérios foram escolhidos porque são mensuráveis, ou seja, descritos em números.

Sabemos que é preciso se criar uma vetor ideal para que assim calculássemos a distância entre cada apartamento e esse ideal, e por conta disso escolhemos que caso o usuário não definisse no campo o que ele gostaria que fosse, pegaríamos a média de todos os valores, já nos dados filtrados, pois sabemos que se ela quer São Paulo, por exemplo, a média do valor dos algueis tende a ser maior, e montamos assim, o ideal.

Na etapa seguinte, foi definida a seleção das 5 melhores opções, mas para isso foi necessário construir o vetor correspondente e calcular os distanciamentos euclidianos. O cálculo foi baseado na seguinte fórmula:


$$
    d = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}
$$

Onde:

    x é o vetor do apartamento sendo avaliado;
    y é o vetor base (definido pelos critérios do usuário);
    n é o número de características avaliadas (área, orçamento, etc.).

Com esse método, somamos as diferenças ao quadrado para cada atributo, calculamos a raiz quadrada do resultado e, assim, obtivemos a distância euclidiana de cada apartamento em relação aos requisitos. Por fim, selecionamos as opções com as menores distâncias, representando os apartamentos mais adequados ao perfil do usuário. Para garantir uma comparacao entre os valores igualitario usamos a funcao normaliza_vetor.

A função normaliza_vetor serve para normalizar valores de um conjunto de dados, ou seja, ajustar os números de uma variável para que fiquem em uma escala comum, facilitando a comparação entre eles.  Isso nos ajuda no cálculo do distanciamento euclidiano dentro da função distanciamento_euclidiano. Ao normalizar as variáveis, evitamos que variáveis com escalas maiores (como preço ou área) dominem o cálculo das distâncias, garantindo que todas as características tenham uma influência equilibrada.

- **Problemas**:

Como esperado, a maioria dos problemas não ocorreu na execução do trabalho em si, mas na transformação das ideias em algo concreto e programável. Tivemos certa dificuldade inicial em manipular a tabela e aprender como trabalhar com esse tipo de dado em Python, pois ainda não tínhamos contato prévio com manipulação de dados usando bibliotecas como Pandas. Após algumas horas de estudo, conseguimos superar esse desafio.

Outro problema foi o peso excessivo atribuído ao preço do aluguel ao usar apenas o distanciamento euclidiano. Por estar na casa dos milhares, o valor do aluguel influenciava muito mais que outros critérios, como número de quartos e banheiros (valores em dezenas ou unidades). Mesmo após normalizar os valores, outros problemas surgiram, como a baixa influência dos campos "número de quartos" e "número de banheiros". Resolvemos isso ajustando os pesos manualmente.




- **Observações**:

Para a execução do código, utilizamos algumas funções de bibliotecas externas, como:
    
    Pandas: para integrar o banco de dados ao código e manipular a tabela, realizar filtros e resgatar elementos;
    
    Matplotlib: para a criação dos gráficos;
    
    Numpy e Math: para cálculos matemáticos e manipulações numéricas;
    Seaborn: para calcular a correlação entre vetores.


Nosso método de pesquisa foi desenvolvido manualmente, com base nos critérios que consideramos essenciais para estruturar o banco de dados em um arquivo .csv. Definimos esses critérios pensando não apenas no objetivo imediato do trabalho, mas também em como eles poderiam ser úteis em análises futuras.

Aproveitamos a oportunidade proporcionada por este projeto para ampliar nosso entendimento sobre as características de apartamentos. Além de atender às necessidades específicas do algoritmo, focamos em criar uma base de dados versátil, que pudesse oferecer percepção sobre imóveis fora do Rio de Janeiro, algo alinhado ao nosso interesse em no futuro.

Ao longo da pesquisa, analisamos diferentes regiões, avaliando dados como valores de mercado, infraestrutura, e características demográficas, com o objetivo de capturar uma visão abrangente do mercado imobiliário. Essa abordagem nos permitiu não apenas estruturar o banco de dados de forma robusta, mas também adquirir um conhecimento mais profundo sobre as variáveis que influenciam a escolha de um apartamento em diferentes localidades.
