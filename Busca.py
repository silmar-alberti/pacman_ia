import util

def busca_largura(problema ,profundidade,estado,caminho,visitados,fronteira):
    if estado not in visitados:
        visitados.add(estado)
        if not fronteira.is_empty():
            fronteira.remove(estado)

    if problema.goalTest(estado) :
        return 1
    elif profundidade == 0:
        fronteira.add(estado,caminho)
        return 0
    else:
        corte = False
        acoes = problema.getActions(estado)

        for acao in acoes:
            filho = problema.getResult(estado,acao)
            if filho not  in visitados:
                caminho_filho = caminho+[acao]
                resultado = busca_largura(problema,profundidade-1,filho,caminho_filho,visitados,fronteira)
                if resultado == 0:
                    corte = True
                elif resultado != None:
                    caminho+=[acao]
                    return 1


        if corte:
            return 0
        else:
            return None

def largura(problem):

    estado_incial = problem.getStartState()
    caminho = []

    fronteira = util.Fronteira()

    fronteira.add(estado_incial,[])

    limite = 1
    visitados = set()
    while True:
        if not fronteira.is_empty():
            estado, caminho = fronteira.pop()
            resultado = busca_largura(problem,limite ,estado,caminho,visitados,fronteira)
            if resultado == 1:
                break

    return caminho

def busca_estrela(problema ,estado,caminho,visitados,fronteira,heuristica):
    if estado not in visitados:
        visitados.add(estado)

    if problema.goalTest(estado):
        return 1
    else:
        acoes = problema.getActions(estado)
        for acao in acoes:
            estado_filho = problema.getResult(estado,acao)
            custo = problema.getCost(estado,acao)
            custo += heuristica(estado,acao)
            fronteira.push((estado_filho, caminho+[acao]),custo)
        return 0



def estrela(problem,heuristic):

    estado_incial = problem.getStartState()
    caminho = []

    fila = util.PriorityQueue()

    fila.push((estado_incial,[]),0)

    custo = 0
    visitados = set()
    while True:
        if not fila.isEmpty():
            (estado ,caminho) = fila.pop()
            resultado = busca_estrela(problem ,estado,caminho,visitados,fila,heuristic)
            if resultado == 1:
                break
            custo += 1

    return caminho