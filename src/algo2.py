import fileinput
import sys
from datetime import datetime
from math import *
import random


graphe = {}
aretes = set()

solution = sys.maxsize


lignes = []
for line in fileinput.input():
    lignes.append(line.rstrip())
lenLignes = len(lignes)

fileinput.close()

for i in range(lenLignes):
    if(lignes[i].split()[0] == 'p'):
        nbS = int( lignes[i].split()[2] )
        nbA = int( lignes[i].split()[3] )
      
    elif(lignes[i].split()[0] == 'c'):
        pass 
        

    else:
        sommet1 = int(lignes[i].split()[0])
        sommet2 = int(lignes[i].split()[1])

        aretes.add( (  sommet1 , sommet2 ) ) 

        graphe.setdefault(sommet1, []).append(sommet2)
        graphe.setdefault(sommet2, []).append(sommet1)


def afficherAretes(A):
    for arete in A:
        print(arete[0],arete[1])


def supprimeTout(A):
    return A



def ajoutTout(S,A):
    At = set()
   
    for i in range(1,S):
        for y in range(i+1,S):
            
            At.add((i,y))
    return At - A




def GRASP(G, Tmax):
    G_etoile = construction(G)
    Tstart = datetime.now()

def construction(G):
    G2 = dict()
    n = len(G)
    CL = list()
    clusters = list()

    for u in G:
        CL.append((u,len(G[u])))

    CL = sorted(CL, key=lambda CL: CL[1])
    Kbest = 0
    
    
    
    while(CL):
        
        Kmin = max(round (Kbest-sqrt(n)) , 1)
        Kmax = min(round (Kbest+ sqrt(n)) , n)
        K = random.randint(Kmin, Kmax)

        for i in range(K):
            try:
                clusters.append([CL.pop()[0]])
            except IndexError:
                break 
        
        lenCL = len(CL)

        try:
            j = CL.pop(random.randint( 0, lenCL-1 ))[0]
        except (IndexError,ValueError):
            break

       
        clusters[maximizes(G, j, clusters)].append(j)

        

    return constructGraphe(clusters)

      
def maximizes(G, j, cl):
    C = list()

    for i in range(len(cl)):
        C.append( (costP(G,j,cl[i]) - costM(G,j,cl[i]), i ) )
    
    return max(C)[1]


def costP(G, j, Ci):
  
    nbV = 0
    
    for u in G[j]:
        if(u in Ci):
            nbV += 1
    return (nbV)

def costM(G, j, Ci):
    nbV = costP(G,j,Ci)
    nbV = len(G[j]) - nbV
    return nbV

def constructGraphe(clust):
    G = dict()

    for u in clust:
        for v in u:

            G.setdefault(v, []).append([int(item) for item in u]) 

    for u in G:
        for i in range (len(G[u])):
             G[u] = G[u][i]
             if (u in G[u]):
                 G[u].remove(u)
             
  
    return G
    
print(construction(graphe))




"""
for u in graphe:
        for v in graphe[u]:
            print("Arête {%s,%s}" % (u,v))
"""                                    


G = {
    1: [2],
    2: [1, 3, 4],
    3: [2, 4],
    4: [2, 3, 5],
    5: [4]
}

F = {
    1: [2, 3, 5],
    2: [1, 4],
    3: [4, 1],
    4: [2, 3, 5],
    5: [4, 1]
}

# (1, 3), (1, 5), (2, 3)


#Fonction qui prend en entrée 2 graphes et qui ressort les arêtes qui différent
def compareGraphes(G, F):
    aretesSolution = set()
    aretesG = set()
    aretesF = set()

    for u in G:
        for v in G[u]:
            if(u > v):
                aretesG.add((u,v))
            else:
                aretesG.add((v, u))
    
    for u in F:
        for v in F[u]:
            if(u > v):
                aretesF.add((u,v))
            else:
                aretesF.add((v, u))

    # S - V : Afficher les éléments présents uniquement dans S
    # S | V : Afficher les éléments présents dans S et dans V               
    aretesSolution = (aretesF - aretesG) | (aretesG - aretesF)

    return aretesSolution


#print(compareGraphes(G, F))
#print(compareGraphes(graphe, construction(graphe)))