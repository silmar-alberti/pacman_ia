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

def busca_estrela(problema ,custo,estado,caminho,visitados,fronteira,heuristica):
    if problema.goalTest(estado):
        return 1
    else:
        if estado in visitados:
            return 0
        visitados.add(estado)

        acoes = problema.getActions(estado)


        for acao in acoes:
            estado_filho = problema.getResult(estado,acao)

            if  estado_filho not in visitados :
                custo_filho = custo + problema.getCost(estado,acao)

                heuristica_filho = heuristica(estado_filho,problema)
                fronteira.push((estado_filho, caminho+[acao],custo_filho),custo_filho+heuristica_filho)


        return 0



def estrela(problem,heuristic):

    estado_incial = problem.getStartState()

    fila = util.PriorityQueue()

    fila.push((estado_incial,[],0),0)

    visitados = set()
    # visitados.add(estado_incial)

    while True:
        if not fila.isEmpty():
            (estado ,caminho,custo) = fila.pop()
            resultado = busca_estrela(problem,custo ,estado,caminho,visitados,fila,heuristic)
            if resultado == 1:
                break


    return caminho