from audioop import avg
import random
import copy


def chaptersWithPages(fileName):
    f = open(fileName, "r", encoding="utf-8")
    lines = f.readlines()

    chapter = []
    chapterNumber = []

    for line in lines:
        lineList = line.split(":")
        title = lineList[0]
        pages = lineList[1].split(",")
        
        chapterNumber.append(int(pages[1]) - int(pages[0]))
        chapter.append(title)
    return chapterNumber, chapter

chapterNumber, chapterTitle = chaptersWithPages("cap.txt")
numberChapters = len(chapterNumber)
KEYS = 0
PAGES = 1


#Alterado
def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """

    '''fitness = 0
    minGene = min(individual[PAGES])

    for gene in individual[PAGES]:          
        fitness += gene - minGene
    '''

    #Variance
    fitness = 0
    avgGene = sum(individual[PAGES])/len(individual[PAGES])

    for gene in individual[PAGES]:          
        fitness += pow((gene - avgGene), 2)
    return fitness/len(individual[PAGES])

#Ok
def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    best_participant = participants[0]

    for participant in participants:
        if evaluate(participant) < evaluate(best_participant):
            best_participant = participant

    return best_participant


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """

    # interchanging the genes
    for i in range(index, len(parent1)):
        parent1[i], parent2[i] = parent2[i], parent1[i]
    
    return parent1, parent2

#Alterado
def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """

    if random.random() >= m:
        return individual

    for i in range(0, len(individual[KEYS])):
        if not isinstance(individual[KEYS][i], list):
            continue
        
        prob = random.random()
        change = random.random()

        if change < 0.4:
            continue
        
        if prob > 0.5 and i < len(individual[KEYS])-1 and isinstance(individual[KEYS][i], list):
            page = max(individual[KEYS][i])
            individual[KEYS][i].remove(page)
            individual[PAGES][i] -= chapterNumber[page]

            if isinstance(individual[KEYS][i+1], list):
                individual[KEYS][i+1].insert(0, page)
                individual[PAGES][i+1] += chapterNumber[page]
            else:
                individual[KEYS][i+1] = [page, individual[KEYS][i+1]]
                individual[PAGES][i+1] += chapterNumber[page]
        elif i > 0 and isinstance(individual[KEYS][i], list):
            page = min(individual[KEYS][i])
            individual[KEYS][i].remove(page)
            individual[PAGES][i] -= chapterNumber[page]

            if isinstance(individual[KEYS][i-1], list):
                individual[KEYS][i-1].append(page)
                individual[PAGES][i-1] += chapterNumber[page]
            else:
                individual[KEYS][i-1] = [individual[KEYS][i-1], page]
                individual[PAGES][i-1] += chapterNumber[page]
        else:
            continue

        if(len(individual[KEYS][i]) == 1):
            individual[KEYS][i] = individual[KEYS][i][0]

        break

    return individual

#Alterado
def generate_individual(number_of_days):
    keyList = [i for i in range(0, len(chapterNumber))]

    pageList = copy.deepcopy(chapterNumber)

    while(len(keyList) != number_of_days):
        index = random.randint(1, len(keyList)-1)
        keyChap = keyList[index]
        val = pageList[index]

        keyAux =  copy.deepcopy(keyList[index-1])
        keyList[index-1] = []

        if isinstance(keyAux, list):
            for key in keyAux:
                keyList[index-1].append(key)
        else:
            keyList[index-1].append(keyAux)
        
        if isinstance(keyChap, list):
            for key in keyChap:
                keyList[index-1].append(key)
        else:
            keyList[index-1].append(keyChap)

        pageList[index-1] = pageList[index-1] + val

        del keyList[index]
        del pageList[index]
    
    return [keyList, pageList]

#Ok
def top(individuals, n):
    copy_individuals = copy.deepcopy(individuals)
    top_individuals = []

    if(n == 1):
        best = tournament(copy_individuals)
        return best

    best = tournament(copy_individuals)

    for i in range(0, n):
        if len(copy_individuals) == 0:
            top_individuals.append(best)
        else:
            best = tournament(copy_individuals)
            top_individuals.append(best)
            copy_individuals.remove(best)
    
    return top_individuals

#Ok
def selecao(individuals, k):
    part = copy.deepcopy(individuals)

    while(len(part) != k):
        del part[random.randint(0, len(part)-1)]
    
    return top(part, 2)


def run_ga(g, n, k, m, e, number_of_days, graph=False):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """
    max_fit = []
    min_fit = []
    avarage_fit = []
    
    individuals = [generate_individual(number_of_days) for i in range(0, n)]
    new_individuals = []
    cont = 0

    for i in range(0, g):
        new_individuals = []

        if e:
            new_individuals.append(top(individuals, 1))

        while(len(new_individuals) < n):
            p1, p2 = selecao(individuals, k)

            '''o1, o2 = crossover(p1, p2, random.randint(0, 7))
            o1 = mutate(o1, m)
            o2 = mutate(o2, m)'''

            o1 = mutate(p1, m)
            o2 = mutate(p2, m)

            new_individuals.append(o1)
            new_individuals.append(o2)
              
        individuals = new_individuals
        
        min_fit_local = evaluate(new_individuals[0])
        max_fit_local = min_fit_local
        avarage_fit_local = min_fit_local

        cont += 1

        for ind in range(1, len(individuals)):
            fit = evaluate(new_individuals[ind])

            if(fit > max_fit_local):
                max_fit_local = fit

            if(fit < min_fit_local):
                min_fit_local = fit

            avarage_fit_local += fit
        
        max_fit.append(max_fit_local)
        min_fit.append(min_fit_local)
        avarage_fit.append(avarage_fit_local/len(individuals))   

        if min_fit_local == 0:
            break
    
    if graph:
        return top(individuals, 1), [max_fit, min_fit, avarage_fit, cont]
    else:
        return top(individuals, 1)

def the_best(number_of_days):
    best_fit = 10000
    n_bests = 0
    list_bests = []

    times_dont_change = 0

    while(times_dont_change <= 20):
        g, n = random.randint(50,100), random.randint(16,100)
        if n >= 5:
            k = random.randint(2,5)
        else:
            k = random.randint(1,n)
        
        m, e = random.random(), True

        individuals = run_ga(g, n, k, m, e, number_of_days)
        actual = evaluate(individuals)

        if(actual < best_fit):
            list_bests = [g, n, k, m, e]
            n_bests += 1
            best_fit = actual
            times_dont_change = 0
            print("Encontrei:", n_bests, list_bests, best_fit)
        else:
            times_dont_change += 1

    return list_bests, best_fit

'''if __name__ == '__main__':
    number_of_days = 26
    
    parametros, acertos = the_best(number_of_days)

    g, n, k, m, e = parametros

    print("Fui escolhido com ", str(acertos/10)+"% de acertos")
    print(parametros)

    for i in range(0, 3):
        individuals = run_ga(g, n, k, m, e, number_of_days)
        best = evaluate(individuals)
        print(best, individuals)
'''