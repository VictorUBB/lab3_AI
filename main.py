import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# read the network details
def readNet(fileName):
    f = open(fileName, "r")
    net = {}
    n = int(f.readline())
    net['noNodes'] = n
    mat = []
    for i in range(n):
        mat.append([])
        line = f.readline()
        elems = line.split(" ")
        for j in range(n):
            mat[-1].append(int(elems[j]))
    net["mat"] = mat
    degrees = []
    noEdges = 0
    for i in range(n):
        d = 0
        for j in range(n):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    net["noEdges"] = noEdges
    net["degrees"] = degrees
    f.close()
    return net

def modularity(communities, param):
    noNodes = param['noNodes']
    mat = param['mat']
    degrees = param['degrees']
    noEdges = param['noEdges']
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if (communities[i] == communities[j]):
               Q += (mat[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M

def modularityGML(G,communities):
    noNodes =nx.number_of_nodes(G)
    mat = nx.to_numpy_array(G)
    degrees =[val for (node, val) in nx.degree(G)]
    noEdges = nx.number_of_edges(G)
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if (communities[i] == communities[j]):
               Q += (mat[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M
def initialize(nrOfNodes,nrOfChromosomes):
    """
    model de reprezentare luat din lucrarea: https://arxiv.org/ftp/cond-mat/papers/0604/0604419.pdf
    reprezentare cromozom : crom=[comunity ID1 ,community ID2... ,community IDNrOfNOdes ],
    astfel cromozomul reprezinta o forma de impartirii a retelei pe comunitati
    :param nrOfNodes: nr de noduri din grag
    :param nrOfChromosomes:  numarul de cromozoni ce dorim sa i creeam
    :return: o matrice cu cromozomoi
    """
    chromosomes=np.random.randint(nrOfNodes,size=(nrOfChromosomes,nrOfNodes))
    # for i in range(nrOfChromosomes):
    #     #creeam un cromozom random
    return chromosomes

def cross_over(chromosome_x,chromosome_y):
    """
    functie ce se ocupa de incrucisarea cromozomilor
    se alege aleator o comunitate din chromosome_x
    si toate pozitile pe care apare in chromosone x sunt transferate in chromosome_y i
    :param chromosome_x:source cromosome
    :param chromosome_y:destination chromosome
    :return:child chromosome
    """
    community_to_excange=np.random.choice(chromosome_x)
    for poz,community in enumerate(chromosome_x):
        if community==community_to_excange:
            chromosome_y[poz]=community
    return chromosome_y

def mutation(chromosome):
    """
    functia ce se ocupa de mutatiea unui cromozom
    un nod este plasat intr-o comunitatea aleatoare
    :param chromosome: chromosomul ce trebuie mutat
    :return: chromosomul modificat
    """
    community=np.random.choice(chromosome)
    node=np.random.choice(range(len(chromosome)))
    chromosome[node]=community
    return chromosome

def selction(chromosomes_lst):
    """
    functie ce alege chromosomii cu cea mai mare valuare a functii de fitness(modularitate)
    :param chromosomes: lista de cromozomii
    :return: chromosomii cu cea mai mare valuare a modularitati
    """
    chromosomes_lst.sort(reverse=True, key=lambda x:x[0])
    return chromosomes_lst[0],chromosomes_lst[1]

def create_tuple(chromosomes,G):
    chroms_with_value=[]
    for chromosome in chromosomes:
        chroms_with_value.append((modularityGML(G,chromosome),chromosome))
    return chroms_with_value

def ga_algorithm(path,nr_of_generations):
    G = nx.read_gml(path, label='id', destringizer=int)
    chromos=initialize(G.number_of_nodes(),40)
    chromosomes=create_tuple(chromos,G)
    for i in range(nr_of_generations):
        for j in range(int(nr_of_generations/2)):
            ch_x,ch_y=selction(chromosomes)
            child=cross_over(ch_x[1],ch_y[1])
            p_of_mutation=np.random.random(10)
            if(p_of_mutation<2,5):
                mutation(child)
            chromosomes.append((modularityGML(G,child),child))
        chromosomes.sort(reverse=True,key=lambda x:x[0])
        chromosomes=chromosomes[:int(nr_of_generations/2)]
    return chromosomes[0]

def plotNetwork1(network, communities):
    np.random.seed(123)  # to freeze the graph's view (networks uses a random view)
    #    A=np.matrix(network["mat"])
    G = nx.read_gml(network, label='id', destringizer=int)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(4, 4))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=100, cmap=plt.cm.RdYlBu, node_color=communities)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()
# chromosomes=initialize(5,8)
# print(chromosomes)
# ch_x=np.random.choice(range(len(chromosomes)))
# ch_y=np.random.choice(range(len(chromosomes)))
# print("ch_x:",chromosomes[ch_x])
# print("ch_y",chromosomes[ch_y])
# print(cross_over(chromosomes[ch_x],chromosomes[ch_y]))
# print(mutation(chromosomes[ch_x]))
# G = nx.read_gml('data/real-networks/real/karate/karate.gml', label='id', destringizer=int)
# chromosomes=initialize(G.number_of_nodes(),10)
# #print(modularityGML(G,chromosomes[1]))
# lst=create_tuple(chromosomes,G)
# for el in lst:
#     print(el[0],el[1])
path='data/real-networks/real/krebs/krebs.gml'
comms=ga_algorithm(path,125)
plotNetwork1(path,comms[1])