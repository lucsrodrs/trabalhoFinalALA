import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

#1R,2L,3A,4P,5Q,6B,7E,8M,9MK,10EC,11CO,12IP,13CODIGO,14SITE
url = "https://raw.githubusercontent.com/lucsrodrs/trabalhoFinalALA/main/apartamentos.csv"

df_ap = pd.read_csv(url)

df = pd.DataFrame(
    {
    "Regiao" : df_ap.iloc[:, 0],
    "Local" : df_ap.iloc[:, 1],
    "Area" : df_ap.iloc[:, 2],
    "Preco" : df_ap.iloc[:, 3],
    "Quartos" : df_ap.iloc[:, 4],
    "Banheiros" : df_ap.iloc[:, 5],
    "Estacionamento" : df_ap.iloc[:, 6],
    "Metro" : df_ap.iloc[:, 7],
    "Mercado" : df_ap.iloc[:, 8],
    "Escola" : df_ap.iloc[:, 9],
    "Condominio" : df_ap.iloc[:, 10],
    "Imposto" : df_ap.iloc[:, 11],
    "Codigo" : df_ap.iloc[:, 12],
    "Site" : df_ap.iloc[:, 13],
    }
)

# Dicionario atualizado
criterios = {
    1: ["Regiao pretendida", None],
    2: ["Local pretendido", None],
    3: ["Estimativa de orcamento", None],
    4: ["Area do apartamento", None],
    5: ["Numero de quartos", None],
    6: ["Numero de banheiros", None],
    7: ["Estacionamento", None],
    8: ["Proximidade ao metro", None],
    9: ["Mercado proximo", None],
    10: ["Escola proxima", None],
}

def exibir_menu():
    print("\nEscolha:")
    for chave, (nome, valor) in criterios.items():
        nome_formatado = nome.ljust(25)  # Nome alinhado a esquerda
        status = "\033[32m[*]\033[0m" if valor is not None else "[-]"
        if(valor is not None):
            print(f"\033[32m[{chave:>{2}}] - {nome_formatado} {status}\033[m")
        else:
            print(f"[{chave:>{2}}] - {nome_formatado} {status}")
    print(f"[{'0':>{2}}] - Pesquisar")


def media_lista(a, pos):
    total = j = 0

    for vetor in a:
        try:
            valor = float(vetor[pos])   # Tenta converter o valor para float
        except ValueError:
            if vetor[pos] == "-":       # Se o valor for "-", trata como 0
                valor = 0
            else:
                continue                # Se nao for um numero e nao for "-", ignora a linha
        total += valor                  # Adiciona o valor convertido à soma
        j += 1                          # Conta o numero de valores validos

    return total / j if j > 0 else 0

def construir_list_base():
    media_orca = media_area = media_quartos = media_estacionamento = media_banheiros = 0
    ideal = list()

    df_filtrado = df

    # Se o criterio nao for None, filtra a coluna; caso contrario, mantem a coluna original
    if criterios[1][1] is not None:
        df_filtrado = df_filtrado[df_filtrado["Regiao"] == str(criterios[1][1])]

    if criterios[2][1] is not None:
        df_filtrado = df_filtrado[df_filtrado["Local"] == str(criterios[2][1])]

    if criterios[8][1] is not None:
        if(criterios[8][1] == "Sim"):
            df_filtrado = df_filtrado[df_filtrado["Metro"] == "V"]
        elif(criterios[8][1] == "Nao"):
            df_filtrado = df_filtrado[df_filtrado["Metro"] == "F"]

    if criterios[9][1] is not None:
        if(criterios[9][1] == "Sim"):
            df_filtrado = df_filtrado[df_filtrado["Mercado"] == "V"]
        elif(criterios[9][1] == "Nao"):
            df_filtrado = df_filtrado[df_filtrado["Mercado"] == "F"]

    if criterios[10][1] is not None:
        if(criterios[10][1] == "Sim"):
            df_filtrado = df_filtrado[df_filtrado["Escola"] == "V"]
        elif(criterios[10][1] == "Nao"):
            df_filtrado = df_filtrado[df_filtrado["Escola"] == "F"]

    # Converter DataFrame em lista para facilitar o processamento
    lista = df_filtrado.values.tolist()

    # Calcular medias ou usar valores definidos nos criterios

    global pesos
    pesos = [1, 1, 1, 1, 1]           #[0]A, [1]P, []

    if criterios[4][1] is None:
        media_area = media_lista(lista, 2)
    else:
        media_area = float(criterios[4][1])
        pesos[0] = 1

    if criterios[3][1] is None:
        media_orca = float(media_lista(lista, 3)) + float(media_lista(lista, 10)) + float(media_lista(lista, 11)/12)
    else:
        media_orca = criterios[3][1]
        pesos[1] = 1

    if criterios[5][1] is None:
        media_quartos = media_lista(lista, 4)
    else:
        media_quartos = float(criterios[5][1])
        pesos[2] = 2

    if criterios[6][1] is None:
        media_banheiros = media_lista(lista, 5)
    else:
        media_banheiros = float(criterios[6][1])
        pesos[3] = 1

    if criterios[7][1] is None:
        media_estacionamento = media_lista(lista, 6)
    else:
        media_estacionamento = float(criterios[7][1])
        pesos[4] = 1

    # Criar o vetor ideal
    ideal.append(float(media_area))            # Tem peso alto     [0] - [2]
    ideal.append(float(media_orca))            # Tem peso alto     [1] -
    ideal.append(float(media_quartos))         # Tem peso medio    [2] -
    ideal.append(float(media_banheiros))       # Tem peso baixo    [3] -
    ideal.append(float(media_estacionamento))  # Tem peso baixo    [4] - [6]

    #print(lista)

    return ideal, lista

def distanciamento_euclidiano():
    menores = filtrada = maximos = minimos = list()                              # Declarei como lista
    global distancias
    distancias = list()

    global base
    base, filtrada = construir_list_base()                          # Preenchi as 2 listas

    if len(filtrada) == 0:
        return menores, filtrada

    maximos, minimos = aux_normaliza(filtrada)

    for c in range(len(filtrada)):
        distancia = 0

        for j in range(5):                                          # Considerar as 5 caracteristicas
            try:
                # Converte ambos os valores para float antes da operacao
                valor_filtro = normaliza_vetor(float(filtrada[c][j+2]), maximos[j], minimos[j]) * pesos[j]             # Converte para float
                valor_base = normaliza_vetor(float(base[j]), maximos[j], minimos[j]) * pesos[j]                       # Converte para float
                #print(f"{valor_filtro} {valor_base}")
                distancia += (valor_filtro - valor_base)**2
            except ValueError:
                continue                                            # Se algum valor nao for numerico, ignora

        distancia = math.sqrt(distancia)
        distancias.append(distancia)
        # Queremos guardar apenas as 3 melhores
        if len(menores) < 5:
            menores.append((c, distancia))                          # Guardar indice e distancia
        else:
            maior_distancia = max(menores, key=lambda x: x[1])
            if distancia < maior_distancia[1]:                      # Verificar se a nova distancia e menor que a maior
                menores.remove(maior_distancia)                     # Remove a maior distancia
                menores.append((c, distancia))                      # Adiciona a nova distancia

        menores.sort(key=lambda x: x[1])

    # Retornar indices dos 3 menores e as distancias
    return menores, filtrada

def mostrar_resultados(menores, filtrada):
    print("\n== Recomendações de apartamentos mais próximos: ==\n")

    # Definir o cabecalho e as larguras de cada coluna
    cabecalho = ["Indice", "Regiao", "Local", "Area", "Preco", "Quartos", "Banheiros", "Estac.",
                 "Metro", "Mercado", "Escola", "Codom.", "IPTU", "Cod", "Site", "Dist."]
    larguras = [8, 10, 25, 6, 8, 8, 10, 7, 7, 7, 9, 8, 6, 12, 12, 8]  # Largura de cada coluna

    # Imprimir cabecalho com as colunas centralizadas
    for col, largura in zip(cabecalho, larguras):
        print(col.center(largura), end=" ")
    print()  # Quebra de linha apos o cabecalho

    print("-" *165)  # Linha separadora

    # Exibicao dos dados formatados
    for (indice, distancia) in menores:
        apartamento = filtrada[indice]  # Acessa o apartamento filtrado pelo indice

        # Exibir o indice
        print(str(indice).center(larguras[0]), end=" ")

        # Iterar sobre os valores do apartamento e ajustar conforme a largura
        for valor, largura in zip(apartamento, larguras[1:-1]):  # Exclui 'Dist.' na iteracao
            print(str(valor).center(largura), end=" ")

        # Adicionar a distancia no final
        print(f"{distancia:.5f}".center(larguras[-1]))  # Ajusta a ultima coluna (Distancia)

def driver():
    while True:
        exibir_menu()
        try:
            op = int(input("\nDigite o numero da opcao desejada: "))
            if op == 0:
                print("\nRealizando pesquisa com os seguintes criterios:")
                for chave, (nome, valor) in criterios.items():
                    nome_formatado = nome.ljust(25)
                    print(f"- {nome_formatado}: {valor if valor else '[-]'}")
                break
            elif op in criterios:
                nome = criterios[op][0]  # Obtem o nome do criterio
                if op in [1, 2]:  # Regiao ou local pretendido
                    if(op == 1):
                        print("\n=== Estados Disponíveis ===  \nSP - São Paulo\nMG - Minas Gerais\nPR - Paraná\nSC - Santa Catarina\nDF - Distrito Federal\n=== === === === === === ===\n")
                        valor = input(f"Digite a sigla da {nome.lower()}: ")
                    else:
                        print("\n=== Cidades Disponíveis ===  \nSP - Sao Paulo, Campinas, Guarulhos, Osasco e Santo Andre\nMG - Uberlandia, Juiz de Fora, Uberaba, Governador Valadares e Belo Horizonte\nPR - Curitiba e Cascavel\nSC - Florianopolis e Biguacu\nDF - Brasilia\n=== === === === === === ===\n")
                        valor = input(f"Digite o nome do {nome.lower()}: ")
                elif op == 3:  # Estimativa de orcamento
                    valor = input("Digite o orcamento estimado (ex: 0-3000): ")
                elif op == 4:  # Area do apartamento
                    valor = input("Digite a area desejada (em m²): ")
                elif op in [5, 6, 7]:  # Numero de quartos ou banheiros
                    valor = input(f"Digite o numero de {nome.lower()}: ")
                elif op in [8, 9, 10]:  # Estacionamento, mercado ou escola
                    valor = input(f"Necessita de {nome.lower()}? (sim/nao): ").lower()
                    valor = "Sim" if valor in ["sim", "s"] else "Nao"
                else:
                    valor = None
                criterios[op][1] = valor  # Atualiza o valor
            else:
                print("Opcao invalida! Tente novamente.")
        except ValueError:
            print("Por favor, insira apenas numeros validos.")

    tres_melhores_indice = lista_melhores = list()
    tres_melhores, lista_melhores = distanciamento_euclidiano()
    if len(lista_melhores) == 0:
        print("Nao ha vaga")
        return

    mostrar_resultados(tres_melhores, lista_melhores)


    colunas = [
    "Regiao", "Local", "Area", "Preco", "Quartos", "Banheiros",
    "Estacionamento", "Metro", "Mercado",
    "Escola", "Condominio", "Imposto",
    "Codigo", "Site"
    ]

    cria_grafico(lista_melhores)

    # Criar o DataFrame
    df_calor = pd.DataFrame(df, columns=colunas)

    # Converter as colunas numéricas para tipo numérico
    colunas_numericas = ["Area", "Preco", "Quartos", "Banheiros",
                         "Estacionamento", "Condominio", "Imposto"]
    for col in colunas_numericas:
        df_calor[col] = pd.to_numeric(df_calor[col], errors='coerce')  # 'coerce' transforma valores inválidos em NaN

    # Filtrar apenas colunas numéricas para correlação
    df_corr = df_calor[colunas_numericas]

    # Remover NaN que podem surgir após a conversão
    df_corr = df_corr.dropna()

    # Criar o heatmap
    sns.heatmap(df_corr.corr(), annot=True, cmap="coolwarm", fmt=".2f")

    print("\n\n\n")

    plt.show()


def cria_pontos(valor, t):
    return [valor * ti for ti in t]

def normaliza_vetor(num, max_, min_):
    if (max_ - min_) == 0:
        return 0
    elif(num == min_):
        return 0.8
    else:
        return (num - min_)/(max_ - min_)

def aux_normaliza(filtrada):
    maximos = [0,0,0,0,0]

    minimos = [filtrada[0][2], (filtrada[0][3] + filtrada[0][10] + filtrada[0][11]/12), filtrada[0][4], filtrada[0][5], filtrada[0][6]]

    for registro in filtrada:
        for i, valor in enumerate(registro[2:7]):  # Índices 2 a 6
            maximos[i] = max(maximos[i], valor)
            minimos[i] = min(minimos[i], valor)

    return maximos, minimos

def exibir_mapa_calor(df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Mapa de Calor - Correlação entre Variáveis")
    plt.show()

def cria_grafico(lista_melhores):
    t = np.arange(0, len(lista_melhores))
    valores_pontos = list()

    cria_reta_ideal = (math.sqrt((base[0])**2 + (base[1])**2 + (base[2])**2 + (base[3])**2 + (base[4])**2)) * np.ones_like(t)
    plt.plot(t, cria_reta_ideal, color='#32CD32')

    for c in range(len(lista_melhores)):
        tmp = math.sqrt((lista_melhores[c][2])**2 + (lista_melhores[c][3] + lista_melhores[c][10] + lista_melhores[c][11]/12)**2 + (lista_melhores[c][4])**2 + (lista_melhores[c][5])**2 + (lista_melhores[c][6])**2)
        if(tmp > math.sqrt((base[0])**2 + (base[1])**2 + (base[2])**2 + (base[3])**2 + (base[4])**2)):
            valores_pontos.append(math.sqrt((base[0])**2 + (base[1])**2 + (base[2])**2 + (base[3])**2 + (base[4])**2) + distancias[c])
        else:
            valores_pontos.append(math.sqrt((base[0])**2 + (base[1])**2 + (base[2])**2 + (base[3])**2 + (base[4])**2) - distancias[c])
    ka = 0
    for valor in valores_pontos:
        plt.plot(ka, valor,'.', color='#708090')
        ka = ka + 1

    plt.title("Gráfico de Pontos para Múltiplos Valores")
    plt.xlabel("Apartamentos")
    plt.ylabel("Indice")

    print("\n\n\n")

    # Mostrar o gráfico
    plt.show()

driver()
