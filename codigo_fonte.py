# =============================================================================
# SIGIC – Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia
# Colônia: Aurora Siger
# =============================================================================
#
# Equipe:
# Eduardo Alves da Silva - RM568601  
# Gabrielly Drosda da Silva - RM 571793       
# Lisandra Jacinto de Araujo -	RM 574055    
# Nathan Caio da Silva - RM 568750      
#
# Execução: python codigo_fonte.py
# Requisito: Python 3.x - sem nenhuma biblioteca externa
# =============================================================================


# =============================================================================
# PARTE 1 — ESTRUTURA & DADOS
# Responsável: Eduardo Alves da Silva 
# =============================================================================
#
# Aqui fica a base de tudo. Definimos os módulos da colônia e organizamos
# os dados usando as quatro estruturas exigidas pelo enunciado. A escolha
# de cada estrutura foi feita pensando em legibilidade e em facilitar o
# trabalho das partes 2 e 3.
#
# Por que cada estrutura foi escolhida:
#
#   TUPLA (INFO_FIXA):
#     Usada para guardar informações que jamais mudam durante a execução,
#     como o nome da colônia e a versão do sistema. A tupla é imutável por
#     natureza, então ela protege esses dados de qualquer alteração acidental.
#
#   DICIONÁRIO (modulos):
#     É a estrutura principal dos dados. Cada módulo tem vários atributos
#     com nomes diferentes, e o dicionário permite acessar qualquer um deles
#     pelo nome: modulos["Habitação"]["status"] é muito mais claro do que
#     tentar lembrar que o status estava no índice 4 de uma lista.
#
#   LISTA (lista_modulos, lista_arestas):
#     Usada onde precisamos de uma sequência ordenada. A lista_modulos define
#     a ordem dos índices na matriz de adjacência. A lista_arestas facilita
#     a iteração sobre todas as conexões nos algoritmos.
#
#   MATRIZ (lista de listas — matriz_adjacencia):
#     Representa o grafo da rede. A posição [i][j] guarda a distância em
#     metros entre o módulo i e o módulo j. Zero significa sem conexão direta.
#     É a forma mais natural de implementar um grafo em Python puro.
# =============================================================================


# Tupla com os metadados fixos da colônia — imutável por design
INFO_FIXA = (
    "Aurora Siger",            # nome oficial da colônia
    "SIGIC v1.0",              # versão do sistema
    "2031-03-15",              # data de fundação
    "Marte – Planície Elísio"  # localização geográfica
)

# Lista com os nomes dos módulos na ordem canônica.
# Essa ordem define os índices usados na matriz de adjacência abaixo,
# então ela não pode ser alterada depois de criada sem reconstruir a matriz.
lista_modulos = [
    "Habitação",                # índice 0
    "Centro de Controle",       # índice 1
    "Armazenamento de Energia", # índice 2
    "Agricultura",              # índice 3
    "Laboratório Científico",   # índice 4
    "Comunicação",              # índice 5
    "Suporte Médico",           # índice 6
    "Produção de Oxigênio",     # índice 7
]

# Dicionário principal com todos os atributos de cada módulo.
# Os campos seguem exatamente o que a seção 1.1 do enunciado pede:
#   consumo_energetico  → kW necessários para operação contínua
#   prioridade          → 1 (crítico) até 5 (baixa prioridade)
#   capacidade_armazena → capacidade de armazenamento do módulo
#   distancias          → dicionário {módulo_vizinho: distância_em_metros}
#   necessidade_comunic → frequência de troca de dados com outros módulos
#   status              → "ativo" | "em manutenção" | "em alerta"
modulos = {
    "Habitação": {
        "consumo_energetico": 120,
        "prioridade": 1,              # crítico — é onde a tripulação mora e sobrevive
        "capacidade_armazena": 500,   # litros de água e suprimentos básicos
        "distancias": {
            "Centro de Controle": 50,
            "Suporte Médico": 40,
            "Produção de Oxigênio": 60,
        },
        "necessidade_comunic": "Alta",
        "status": "ativo",
    },
    "Centro de Controle": {
        "consumo_energetico": 85,
        "prioridade": 1,              # crítico — de lá saem todas as decisões da colônia
        "capacidade_armazena": 200,   # GB de dados operacionais armazenados
        "distancias": {
            "Habitação": 50,
            "Armazenamento de Energia": 30,
            "Comunicação": 45,
            "Laboratório Científico": 70,
        },
        "necessidade_comunic": "Alta",
        "status": "ativo",
    },
    "Armazenamento de Energia": {
        "consumo_energetico": 15,     # apenas o consumo do próprio sistema de gestão
        "prioridade": 1,              # crítico — alimenta todos os outros módulos
        "capacidade_armazena": 10000, # kWh que o módulo consegue guardar
        "distancias": {
            "Centro de Controle": 30,
            "Agricultura": 55,
            "Suporte Médico": 65,
            "Produção de Oxigênio": 40,
            "Habitação": 80,
        },
        "necessidade_comunic": "Média",
        "status": "ativo",
    },
    "Agricultura": {
        "consumo_energetico": 95,     # iluminação artificial e sistema de irrigação
        "prioridade": 2,              # alta — sem comida a colônia não sobrevive a longo prazo
        "capacidade_armazena": 3000,  # kg de alimentos que consegue estocar
        "distancias": {
            "Armazenamento de Energia": 55,
            "Laboratório Científico": 35,
        },
        "necessidade_comunic": "Baixa",
        "status": "ativo",
    },
    "Laboratório Científico": {
        "consumo_energetico": 110,
        "prioridade": 3,              # média — pesquisa é importante, mas não emergencial
        "capacidade_armazena": 150,   # kg de amostras e materiais de análise
        "distancias": {
            "Centro de Controle": 70,
            "Agricultura": 35,
            "Comunicação": 50,
        },
        "necessidade_comunic": "Média",
        "status": "ativo",
    },
    "Comunicação": {
        "consumo_energetico": 60,
        "prioridade": 2,              # alta — coordenação interna e contato com a Terra
        "capacidade_armazena": 500,   # GB de buffer para mensagens em trânsito
        "distancias": {
            "Centro de Controle": 45,
            "Laboratório Científico": 50,
        },
        "necessidade_comunic": "Alta",
        "status": "ativo",
    },
    "Suporte Médico": {
        "consumo_energetico": 75,
        "prioridade": 1,              # crítico — saúde da tripulação não pode esperar
        "capacidade_armazena": 300,   # unidades de suprimentos médicos
        "distancias": {
            "Habitação": 40,
            "Armazenamento de Energia": 65,
            "Produção de Oxigênio": 30,
        },
        "necessidade_comunic": "Alta",
        "status": "ativo",
    },
    "Produção de Oxigênio": {
        "consumo_energetico": 140,    # processo de eletrólise é o que mais consome
        "prioridade": 1,              # crítico — sem oxigênio não há nada mais a fazer
        "capacidade_armazena": 800,   # m³ de O₂ armazenado em reservatórios
        "distancias": {
            "Habitação": 60,
            "Armazenamento de Energia": 40,
            "Suporte Médico": 30,
        },
        "necessidade_comunic": "Média",
        "status": "ativo",
    },
}

# Número de módulos — definido uma vez e reutilizado em todo o código
N = len(lista_modulos)

# Mapeamento nome - índice para acessar a matriz sem ficar procurando na lista
indice_modulo = {nome: i for i, nome in enumerate(lista_modulos)}

# Matriz de adjacência N×N.
# Posição [i][j] contém a distância em metros entre módulo i e módulo j.
# O grafo é não-dirigido: se A conecta a B com X metros, B conecta a A também.
# Começa toda zerada e é preenchida automaticamente a partir dos dicionários acima.
matriz_adjacencia = [[0] * N for _ in range(N)]

for nome_origem, dados in modulos.items():
    i = indice_modulo[nome_origem]
    for nome_destino, peso in dados["distancias"].items():
        j = indice_modulo[nome_destino]
        matriz_adjacencia[i][j] = peso
        matriz_adjacencia[j][i] = peso  # garante que a matriz é simétrica

# Lista de arestas no formato (origem, destino, peso).
# Evita duplicatas, pois só inclui pares onde o índice de origem é menor que o de destino.
# Os algoritmos da Parte 2 vão usar essa lista para percorrer conexões.
lista_arestas = []
for i in range(N):
    for j in range(i + 1, N):
        if matriz_adjacencia[i][j] > 0:
            lista_arestas.append(
                (lista_modulos[i], lista_modulos[j], matriz_adjacencia[i][j])
            )


# --- Funções auxiliares de dados (Parte 1) -----------------------------------

def exibir_modulo(nome):
    # Mostra os detalhes completos de um módulo específico de forma legível
    if nome not in modulos:
        print(f"\n  [ERRO] Módulo '{nome}' não existe.")
        return
    m = modulos[nome]
    print(f"\n{'='*54}")
    print(f"  MÓDULO: {nome}")
    print(f"{'='*54}")
    print(f"  Consumo energético    : {m['consumo_energetico']} kW")
    print(f"  Prioridade            : {m['prioridade']}  (1 = mais crítico)")
    print(f"  Capacidade armazenada : {m['capacidade_armazena']}")
    print(f"  Comunicação           : {m['necessidade_comunic']}")
    print(f"  Status atual          : {m['status'].upper()}")
    vizinhos_str = ", ".join(
        f"{v} ({p}m)" for v, p in m["distancias"].items()
    ) or "nenhum"
    print(f"  Vizinhos diretos      : {vizinhos_str}")
    print(f"{'='*54}\n")


def listar_modulos():
    # Exibe todos os módulos em formato de tabela com status e prioridade
    print(f"\n{'='*64}")
    print(f"  MÓDULOS DA COLÔNIA {INFO_FIXA[0]}")
    print(f"{'='*64}")
    print(f"  {'#':<4} {'Módulo':<28} {'Prior.':<8} {'Status'}")
    print(f"  {'-'*60}")
    for i, nome in enumerate(lista_modulos):
        m = modulos[nome]
        print(f"  {i:<4} {nome:<28} {m['prioridade']:<8} {m['status']}")
    print(f"{'='*64}\n")


def atualizar_status(nome, novo_status):
    # Muda o status operacional de um módulo, com validação do valor informado
    validos = {"ativo", "em manutenção", "em alerta"}
    if nome not in modulos:
        print(f"  [ERRO] Módulo '{nome}' não encontrado.")
        return
    if novo_status not in validos:
        print(f"  [ERRO] Status inválido. Use: {validos}")
        return
    modulos[nome]["status"] = novo_status
    print(f"  [OK] '{nome}' → status atualizado para '{novo_status}'.")


def consumo_total():
    # Soma o consumo de todos os módulos que estão ativos no momento
    return sum(
        m["consumo_energetico"]
        for m in modulos.values()
        if m["status"] == "ativo"
    )


def modulos_por_prioridade():
    # Retorna os módulos em ordem do mais crítico (1) para o menos crítico
    return sorted(lista_modulos, key=lambda n: modulos[n]["prioridade"])


def exibir_matriz():
    # Imprime a matriz de adjacência com abreviações nos cabeçalhos
    # para caber num terminal de largura razoável
    abrev = ["HAB", "CC ", "AE ", "AGR", "LAB", "COM", "MED", "O2 "]
    print(f"\n{'='*54}")
    print("  MATRIZ DE ADJACÊNCIA  (distâncias em metros, 0 = sem conexão)")
    print(f"{'='*54}")
    cabecalho = "       " + "  ".join(f"{a:>4}" for a in abrev)
    print(cabecalho)
    for i in range(N):
        linha = f"  {abrev[i]} " + "  ".join(
            f"{matriz_adjacencia[i][j]:>4}" for j in range(N)
        )
        print(linha)
    print(f"{'='*54}\n")


def exibir_rede_texto():
    # Mostra todas as conexões da rede como lista, mais fácil de ler que a matriz
    print(f"\n{'='*54}")
    print("  CONEXÕES DA REDE – Aurora Siger")
    print(f"{'='*54}")
    for origem, destino, peso in lista_arestas:
        print(f"  {origem}  ──({peso}m)──  {destino}")
    print(f"\n  Total de arestas: {len(lista_arestas)}")
    print(f"  Total de módulos: {N}")
    print(f"{'='*54}\n")


# =============================================================================
# PARTE 2 — ALGORITMOS DE REDES
# Responsável: Gabrielly Drosda da Silva 
# =============================================================================
#
# Implementamos BFS, DFS e Dijkstra do zero, sem usar nenhuma biblioteca
# externa. Cada algoritmo tem um papel diferente na análise da rede:
#
#   BFS  - explora a rede camada por camada; ideal para descobrir quais
#           módulos são alcançáveis e em quantos saltos a partir de um ponto.
#
#   DFS  -  mergulha fundo antes de voltar; usamos ele junto com o algoritmo
#           de Tarjan para detectar pontes — conexões cuja remoção quebraria
#           a rede em partes isoladas.
#
#   Dijkstra -  encontra o caminho de menor custo entre dois módulos, o que
#              na prática significa a rota que desperdiça menos energia ao
#              distribuir carga entre os módulos da colônia.
# =============================================================================

def _vizinhos(nome):
    # Retorna lista de (vizinho, peso) para um módulo, lendo da matriz.
    # Função interna usada pelos três algoritmos abaixo.
    i = indice_modulo[nome]
    return [
        (lista_modulos[j], matriz_adjacencia[i][j])
        for j in range(N)
        if matriz_adjacencia[i][j] > 0
    ]


def bfs(origem):
    # BFS – Busca em Largura
    #
    # Começa no módulo de origem e vai visitando os vizinhos em camadas.
    # Usamos uma fila simples (lista com pop(0)) em vez de deque porque o
    # número de módulos é pequeno e não precisamos otimizar esse ponto.
    # No final, identificamos módulos que não são alcançáveis da origem.
    if origem not in modulos:
        print(f"\n  [ERRO] Módulo '{origem}' não existe.")
        return []

    visitados = []
    fila = [origem]
    vistos = {origem}

    print(f"\n{'='*54}")
    print(f"  BFS – Exploração a partir de: {origem}")
    print(f"{'='*54}")

    while fila:
        atual = fila.pop(0)        # retira o primeiro (FIFO)
        visitados.append(atual)

        # Ordena os vizinhos pelo nome para que a saída seja sempre a mesma
        for vizinho, _ in sorted(_vizinhos(atual), key=lambda x: x[0]):
            if vizinho not in vistos:
                vistos.add(vizinho)
                fila.append(vizinho)

    print(f"  Ordem de visita ({len(visitados)} módulos):")
    for i, nome in enumerate(visitados, 1):
        print(f"    {i}. {nome}")

    desconectados = [m for m in lista_modulos if m not in vistos]
    if desconectados:
        print(f"\n  ⚠  Módulos não alcançáveis a partir de '{origem}':")
        for d in desconectados:
            print(f"     - {d}")
    else:
        print(f"\n  ✓  Todos os módulos são alcançáveis a partir de '{origem}'.")

    print(f"{'='*54}\n")
    return visitados


def dfs(origem):
    # DFS – Busca em Profundidade
    #
    # usa uma pilha (lista com pop()) para ir o mais fundo possível antes
    # de voltar. Após a varredura, chama a detecção de pontes para identificar
    # conexões críticas — aquelas que, se removidas, fragmentariam a rede.
    if origem not in modulos:
        print(f"\n  [ERRO] Módulo '{origem}' não existe.")
        return []

    visitados = []
    pilha = [origem]
    vistos = set()

    print(f"\n{'='*54}")
    print(f"  DFS – Exploração a partir de: {origem}")
    print(f"{'='*54}")

    while pilha:
        atual = pilha.pop()        # retira o topo (LIFO)
        if atual in vistos:
            continue
        vistos.add(atual)
        visitados.append(atual)

        # Empilha em ordem reversa para que a visita siga a ordem alfabética
        for vizinho, _ in sorted(_vizinhos(atual), key=lambda x: x[0], reverse=True):
            if vizinho not in vistos:
                pilha.append(vizinho)

    print(f"  Ordem de visita ({len(visitados)} módulos):")
    for i, nome in enumerate(visitados, 1):
        print(f"    {i}. {nome}")

    print("\n  Verificando conexões críticas (pontes)...")
    pontes = _detectar_pontes()
    if pontes:
        print(f"  ⚠  {len(pontes)} conexão(ões) crítica(s) encontrada(s):")
        for u, v in pontes:
            print(f"     - {u}  ↔  {v}")
            print(f"       (remover essa ligação isolaria parte da rede)")
    else:
        print("  ✓  Nenhuma conexão crítica — a rede tem redundância suficiente.")

    print(f"{'='*54}\n")
    return visitados


def _detectar_pontes():
    # Algoritmo de Tarjan para encontrar pontes em grafos não-dirigidos.
    #
    # A ideia é manter dois valores para cada nó durante a DFS:
    #   disc[u] → momento em que o nó u foi descoberto
    #   low[u]  → menor disc acessível a partir da subárvore enraizada em u
    #
    # Se low[v] > disc[u] para uma aresta (u, v), então essa aresta é uma
    # ponte — não existe caminho alternativo de v para u sem passar por ela.
    visitado = [False] * N
    disc = [-1] * N
    low  = [-1] * N
    pai  = [-1] * N
    timer = [0]
    pontes = []

    def _dfs_tarjan(u):
        visitado[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v in range(N):
            if matriz_adjacencia[u][v] == 0:
                continue
            if not visitado[v]:
                pai[v] = u
                _dfs_tarjan(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    pontes.append((lista_modulos[u], lista_modulos[v]))
            elif v != pai[u]:
                low[u] = min(low[u], disc[v])

    for i in range(N):
        if not visitado[i]:
            _dfs_tarjan(i)

    return pontes


def dijkstra(origem, destino):
    # Algoritmo de Dijkstra para caminho de menor custo.
    #
    # Partimos com distância zero na origem e infinito em todo o resto.
    # A cada passo, escolhemos o nó não-visitado mais barato, relaxamos
    # suas arestas e seguimos. Ao final, reconstruímos o caminho usando
    # o dicionário "anterior" que rastreia quem veio antes de quem.
    #
    # Não usamos heapq. para 8 módulos, o min() simples é suficiente.
    if origem not in modulos or destino not in modulos:
        print("\n  [ERRO] Um dos módulos informados não existe.")
        return None, None

    INFINITO = float("inf")
    dist = {nome: INFINITO for nome in lista_modulos}
    dist[origem] = 0
    anterior = {nome: None for nome in lista_modulos}
    nao_visitados = list(lista_modulos)

    while nao_visitados:
        # Pega o nó mais barato que ainda não foi processado
        atual = min(nao_visitados, key=lambda n: dist[n])

        if dist[atual] == INFINITO:
            break   # nenhum nó restante é alcançável

        if atual == destino:
            break   # chegamos onde queríamos

        nao_visitados.remove(atual)

        for vizinho, peso in _vizinhos(atual):
            if vizinho not in nao_visitados:
                continue
            nova_dist = dist[atual] + peso
            if nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                anterior[vizinho] = atual

    # Reconstrói o caminho percorrendo o dicionário "anterior" de trás pra frente
    caminho = []
    passo = destino
    while passo is not None:
        caminho.append(passo)
        passo = anterior[passo]
    caminho.reverse()

    custo = dist[destino]

    print(f"\n{'='*54}")
    print(f"  DIJKSTRA – Caminho mínimo")
    print(f"  De    : {origem}")
    print(f"  Para  : {destino}")
    print(f"{'='*54}")

    if custo == INFINITO:
        print("  ✗  Não existe caminho entre os módulos informados.")
        print(f"{'='*54}\n")
        return [], INFINITO

    print(f"  Rota encontrada ({len(caminho) - 1} salto(s)):")
    print(f"    {' → '.join(caminho)}")
    print(f"  Custo total: {custo} metros")
    print("\n  Detalhamento do trajeto:")
    for k in range(len(caminho) - 1):
        i = indice_modulo[caminho[k]]
        j = indice_modulo[caminho[k + 1]]
        trecho = matriz_adjacencia[i][j]
        print(f"    {caminho[k]}  →  {caminho[k + 1]}: {trecho} m")

    print(f"{'='*54}\n")
    return caminho, custo


def analisar_eficiencia():
    # Avalia a rede olhando para o grau de cada nó (quantas conexões tem),
    # aponta possíveis gargalos e lista o consumo dos módulos críticos.
    print(f"\n{'='*54}")
    print("  ANÁLISE DE EFICIÊNCIA OPERACIONAL")
    print(f"{'='*54}")

    graus = {}
    for i, nome in enumerate(lista_modulos):
        graus[nome] = sum(1 for j in range(N) if matriz_adjacencia[i][j] > 0)

    print("\n  Grau de conectividade por módulo:")
    for nome, grau in sorted(graus.items(), key=lambda x: -x[1]):
        barra = "█" * grau
        print(f"    {nome:<28} {grau} conexão(ões)  {barra}")

    media = sum(graus.values()) / N
    print(f"\n  Média de conexões por módulo: {media:.1f}")

    gargalos = [n for n, g in graus.items() if g <= 1]
    if gargalos:
        print("\n  ⚠  Módulos com conectividade baixa (possíveis gargalos):")
        for g in gargalos:
            print(f"     - {g}")
    else:
        print("\n  ✓  Nenhum gargalo de conectividade identificado.")

    print("\n  Módulos de prioridade 1 e seu consumo energético:")
    for nome in lista_modulos:
        m = modulos[nome]
        if m["prioridade"] == 1:
            print(f"    {nome:<28} {m['consumo_energetico']} kW")

    print(f"\n  Consumo total (módulos ativos): {consumo_total()} kW")
    print(f"{'='*54}\n")


# =============================================================================
# PARTE 3 — MODELAGEM MATEMÁTICA & SUSTENTABILIDADE ESG
# Responsável: Lisandra Jacinto de Araujo 
# =============================================================================
#
# Modelamos o crescimento do consumo energético usando uma função exponencial.
# A escolha faz sentido porque uma colônia em expansão não cresce de forma
# linear: cada módulo novo aumenta não só o consumo próprio, mas também
# a demanda por distribuição, comunicação e suporte entre todos os existentes.
#
# Fórmula: C(t) = C0 × e^(r × t)
#
#   C(t) → consumo energético total estimado no tempo t (em kW)
#   C0   → consumo atual da colônia (calculado em tempo de execução)
#   r    → taxa de crescimento por período — adotamos 8% ao ano (r = 0.08)
#   t    → anos desde a fundação da colônia
#   e    → constante de Euler (~2.718), base do crescimento natural
#
# Análise qualitativa:
#   A função é crescente e acelerada. Quanto maior o t, mais rápido o
#   consumo sobe em termos absolutos. O ponto crítico para a Aurora Siger
#   é quando C(t) se aproxima da capacidade máxima de armazenamento de
#   energia — esse é o sinal de que novos geradores ou painéis são necessários.
#
# Relação com a colônia:
#   Com essa projeção conseguimos planejar com antecedência quando expandir
#   a infraestrutura de geração e armazenamento, orientando as decisões de
#   governança antes que a demanda supere a oferta.
# =============================================================================

def _exp_taylor(x, termos=25):
    # Calcula e^x usando a série de Taylor, sem usar math.exp.
    # Isso evita qualquer dependência de biblioteca externa.
    # Série: e^x = 1 + x + x²/2! + x³/3! + ...
    resultado = 0.0
    fat = 1
    pot = 1.0
    for n in range(termos):
        if n > 0:
            fat *= n
            pot *= x
        resultado += pot / fat
    return resultado


def modelagem_consumo():
    # Projeta o crescimento do consumo energético nos próximos 10 anos
    # usando o modelo exponencial C(t) = C0 * e^(r*t)
    C0 = consumo_total()
    r  = 0.08   # 8% de crescimento anual — estimativa conservadora para Marte
    cap_max = modulos["Armazenamento de Energia"]["capacidade_armazena"]

    print(f"\n{'='*54}")
    print("  MODELAGEM MATEMÁTICA – Crescimento Energético")
    print(f"{'='*54}")
    print(f"  Fórmula : C(t) = C0 × e^(r × t)")
    print(f"  C0      = {C0} kW  (consumo base dos módulos ativos)")
    print(f"  r       = {r}  (taxa de crescimento anual de 8%)")
    print(f"  Limite  = {cap_max} kWh  (capacidade de armazenamento atual)")
    print(f"\n  {'Ano':<6} {'C(t) em kW':<16} {'Variação'}  {'Alerta'}")
    print(f"  {'-'*50}")

    for t in range(0, 11):
        ct = C0 * _exp_taylor(r * t)
        variacao = ct / C0
        alerta = "⚠ PRÓXIMO DO LIMITE" if ct > cap_max * 0.75 else ""
        print(f"  {t:<6} {ct:<16.1f} {variacao:.2f}x    {alerta}")

    print(f"\n  Quando C(t) ultrapassa {cap_max * 0.75:.0f} kW (75% do limite)")
    print("  é hora de iniciar a expansão da capacidade de geração.")
    print(f"{'='*54}\n")


def relatorio_esg():
    # Relatório de Sustentabilidade e Governança cobrindo os 5 pilares
    # exigidos pela seção 1.6 do enunciado
    print(f"\n{'='*62}")
    print("  RELATÓRIO ESG – Sustentabilidade e Governança")
    print(f"  Colônia {INFO_FIXA[0]}")
    print(f"{'='*62}")

    total = consumo_total()

    # 1. Uso sustentável de energia
    print("\n  1. USO SUSTENTÁVEL DE ENERGIA")
    print(f"  Consumo total atual: {total} kW")
    print("  Estratégias de redução:")
    print("    • Em períodos de baixa geração solar, desligar módulos de")
    print("      prioridade 3 ou superior (ex.: Laboratório em modo econômico)")
    eco = modulos["Laboratório Científico"]["consumo_energetico"] * 0.30
    print(f"    • Modo econômico no Laboratório: economia de ~{eco:.0f} kW "
          f"({eco/total*100:.1f}% do total)")
    print("    • Redistribuir carga nos horários de pico de geração solar")

    # 2. Expansão organizada
    print("\n  2. EXPANSÃO ORGANIZADA DA COLÔNIA")
    print("  Critérios para adicionar novos módulos:")
    print("    • Cada novo módulo deve ter pelo menos 2 conexões na rede")
    print("    • Priorizar ligação com Armazenamento de Energia para")
    print("      garantir distribuição direta sem intermediários")
    print("    • Reexecutar Dijkstra após toda expansão para atualizar")
    print("      as rotas de distribuição energética")

    # 3. Priorização de sistemas críticos
    print("\n  3. PRIORIZAÇÃO DE SISTEMAS CRÍTICOS")
    print("  Módulos de prioridade 1 — não podem ser desligados:")
    for nome in modulos_por_prioridade():
        if modulos[nome]["prioridade"] == 1:
            print(f"    • {nome}  ({modulos[nome]['consumo_energetico']} kW)")
    print("  Em crise energética: módulos prioridade 3+ entram em modo")
    print("  econômico antes de qualquer corte nos módulos críticos.")

    # 4. Governança tecnológica
    print("\n  4. GOVERNANÇA TECNOLÓGICA")
    print("  Diretrizes para decisões computacionais responsáveis:")
    print("    • Todo roteamento de energia é validado pelo Dijkstra —")
    print("      nenhuma decisão de distribuição feita manualmente")
    print("    • Alertas automáticos quando consumo supera 80% da capacidade")
    print("    • Toda mudança de status de módulo deve ser registrada")
    print("    • Módulos críticos devem sempre ter ao menos uma rota alternativa")

    # 5. Redução de desperdícios
    print("\n  5. REDUÇÃO DE DESPERDÍCIOS")
    print("  Usando Dijkstra para encontrar a rota mais eficiente")
    print("  do Armazenamento de Energia até o Suporte Médico:\n")
    caminho, custo = dijkstra("Armazenamento de Energia", "Suporte Médico")
    if caminho and custo != float("inf"):
        print(f"  Rota ótima encontrada com {custo}m — minimiza a perda")
        print("  energética por resistência nos cabos de distribuição.")
    print("  Rotas mais longas desperdiçam mais energia em transmissão;")
    print("  o uso consistente do Dijkstra garante a rota de menor perda.")

    print(f"\n{'='*62}\n")


# =============================================================================
# PARTE 4 — MENU & INTEGRAÇÃO
# Responsável: Nathan Caio da Silva
# =============================================================================
#
# Menu principal do sistema. Reúne todas as funções das partes anteriores
# e as apresenta ao usuário de forma clara e navegável pelo terminal.
# O loop só encerra quando o usuário digitar 0.
# =============================================================================

def _selecionar_modulo(mensagem="Escolha um módulo"):
    # Exibe a lista numerada e pede que o usuário escolha um módulo pelo índice.
    # Retorna o nome do módulo escolhido ou None se a entrada for inválida.
    print(f"\n  {mensagem}:")
    for i, nome in enumerate(lista_modulos):
        print(f"    {i} – {nome}")
    try:
        escolha = int(input("\n  Digite o número: "))
        if 0 <= escolha < N:
            return lista_modulos[escolha]
        print("  [ERRO] Número fora do intervalo.")
        return None
    except ValueError:
        print("  [ERRO] Entrada inválida. Digite um número inteiro.")
        return None


def _simular_situacao():
    # Permite ao usuário mudar o status de um módulo para simular uma falha,
    # uma manutenção programada ou um retorno à operação normal.
    # Depois da mudança, exibe o novo consumo total para mostrar o impacto.
    print("\n  SIMULAÇÃO DE SITUAÇÃO OPERACIONAL")
    print("  Altere o status de um módulo para testar um cenário.\n")
    nome = _selecionar_modulo("Escolha o módulo a simular")
    if not nome:
        return
    print("\n  Novo status:")
    print("    0 – ativo")
    print("    1 – em manutenção")
    print("    2 – em alerta")
    opcoes = ["ativo", "em manutenção", "em alerta"]
    try:
        idx = int(input("\n  Digite o número: "))
        if 0 <= idx <= 2:
            atualizar_status(nome, opcoes[idx])
            print(f"\n  Consumo total atualizado: {consumo_total()} kW")
        else:
            print("  [ERRO] Opção inválida.")
    except ValueError:
        print("  [ERRO] Entrada inválida.")


def _cabecalho():
    # Exibe o cabeçalho do sistema na inicialização
    print("\n" + "=" * 62)
    print("        SIGIC – Sistema Inteligente de Gerenciamento")
    print(f"        Colônia {INFO_FIXA[0]}  |  {INFO_FIXA[1]}")
    print(f"        {INFO_FIXA[3]}")
    print(f"        Fundação: {INFO_FIXA[2]}")
    print("=" * 62 + "\n")


def menu():
    # Loop principal — exibe as opções e chama a função correta conforme
    # a escolha do usuário. Cada opção leva a uma funcionalidade diferente
    # implementada nas partes anteriores.
    _cabecalho()

    while True:
        print("\n" + "─" * 50)
        print("  MENU PRINCIPAL")
        print("─" * 50)
        print("  [ 1]  Listar todos os módulos")
        print("  [ 2]  Consultar módulo específico")
        print("  [ 3]  Visualizar rede (conexões)")
        print("  [ 4]  Exibir matriz de adjacência")
        print("  [ 5]  BFS – Explorar conectividade da rede")
        print("  [ 6]  DFS – Detectar conexões críticas")
        print("  [ 7]  Dijkstra – Encontrar caminho mínimo")
        print("  [ 8]  Análise de eficiência operacional")
        print("  [ 9]  Projeção de consumo energético (modelagem)")
        print("  [10]  Relatório de sustentabilidade e governança (ESG)")
        print("  [11]  Simular situação operacional")
        print("  [ 0]  Sair")
        print("─" * 50)

        escolha = input("\n  Opção: ").strip()

        if escolha == "0":
            print("\n  Encerrando o SIGIC. Até logo!\n")
            break

        elif escolha == "1":
            listar_modulos()

        elif escolha == "2":
            nome = _selecionar_modulo()
            if nome:
                exibir_modulo(nome)

        elif escolha == "3":
            exibir_rede_texto()

        elif escolha == "4":
            exibir_matriz()

        elif escolha == "5":
            nome = _selecionar_modulo("Módulo de origem para o BFS")
            if nome:
                bfs(nome)

        elif escolha == "6":
            nome = _selecionar_modulo("Módulo de origem para o DFS")
            if nome:
                dfs(nome)

        elif escolha == "7":
            print("\n  DIJKSTRA – defina origem e destino:\n")
            origem = _selecionar_modulo("Módulo de ORIGEM")
            if origem:
                destino = _selecionar_modulo("Módulo de DESTINO")
                if destino:
                    dijkstra(origem, destino)

        elif escolha == "8":
            analisar_eficiencia()

        elif escolha == "9":
            modelagem_consumo()

        elif escolha == "10":
            relatorio_esg()

        elif escolha == "11":
            _simular_situacao()

        else:
            print("\n  [ERRO] Opção inválida. Digite um número do menu.")

        input("\n  Pressione Enter para continuar...")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    menu()
