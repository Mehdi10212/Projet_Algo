import fileinput
import sys
import time
import random
import signal
from math import sqrt


class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True

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

for i in range(1,nbS+1):
    if i not in graphe:
        graphe.setdefault(i, [])

def sommets():
    sommetsL = set()
    for i in range(1,nbS):
        sommetsL.add(i)

    return sommetsL


def afficherAretes(A):
    for arete in A:
        print(arete[0],arete[1])

# Heuristique : Supprimer toutes les arêtes du graphe : le graphe résultat est une collection de sommets isolés.
# Fonctionne en moins de 10 min pour tous les JDD
def supprimeTout(A):
    return A


# Heuristique : Ajouter toutes les arêtes manquantes du graphe : le graphe résultat est une clique.
# Fonctionne en moins de 10 min pour tous les JDD
def ajoutTout(S,A):
    At = set()
   
    for i in range(1,S):
        for y in range(i+1,S):
            
            At.add((i,y))
    return At - A


# Heuristique : GRASP fonctionne en moins de 10 min pour les JDD où il a moins de 10 000 sommets environs 
def GRASP(G, Tmax):

    killer = Killer()
    G_etoile = constructGraphe(construction(G))
    start_time = time.time()  
    tempsMoyen = 0
    tempsTotal = 0 
    tempsRestant =  Tmax - start_time
    nbIteration = 0

    while(tempsRestant > 2*tempsMoyen):

        tempsA = time.time()

        if killer.exit_now:
            return G_etoile
        G_prim = construction(G)
        G_prim = constructGraphe(localSearch(G_prim))
        
        if (len(compareGraphes(G, G_prim)) < len(compareGraphes(G, G_etoile))):
            G_etoile = G_prim

        tempsIteration = time.time() - tempsA 
        tempsTotal += tempsIteration
        
        nbIteration += 1
        
        tempsMoyen =  tempsTotal / nbIteration
        tempsRestant -= tempsIteration

    return G_etoile


def relativeNeighborhood(G):
    n = nbS
    CL = list()
    clusters = list()

    for u in G:
        CL.append((u,len(G[u])))

    CL = sorted(CL, key=lambda CL: CL[1])
    Kbest = 0
        
    
    while(CL):
        
        Kmin = max(round (Kbest-sqrt(n)) , 1)
        Kmax = min(round (Kbest+ sqrt(n)) , n)
        K = random.randint(Kmin, Kmax) #K comprit entre 1 et n 

        for _ in range(K):
            try:
                clusters.append([CL.pop()[0]])
            except IndexError:
                break 
        
        
        lenCL = len(CL)

        try:
            j = CL.pop(random.randint( 0, lenCL-1 ))[0]
            
        except (IndexError,ValueError):
            break

      
        clusters[maximizes(G[j], j, clusters)].append(j)
        Kbest = len(clusters)
        
      
        
    
    return clusters

      
    
    

    
def maximizes(Gj, j, cl):
    C = list()

    for i in range(len(cl)):
        C.append( (costP(Gj,cl[i]) - costM(Gj,cl[i]), i ) )

    
    return max(C)[1]


def costP(Gj, Ci):

    nbV = 0
    for u in Gj:
        if(u in Ci):
            nbV += 1

    return (nbV)

def costM(Gj, Ci):
    
    return len(Ci) - costP(Gj,Ci)

def constructGraphe(clust):

    G = dict()
    for u in clust:
        for i in u:
            G[i] = u.copy()
            if (i in G[i] ):
                 G[i].remove(i)
             
  
    return G


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

def maximumCost(clusters):
    costM = 0
    cost = 0 

    for c in clusters:
        sc = sommets() - set(c) 
        for i in c:
             cost += costP(graphe[i],sc )
        
        if (cost>= costM):
            costM = cost
            cl = c.copy()

        cost = 0 
    return cl


def clusterSplit(clusters):
    

    costM = 0
    cost = 0 

    
    cl = maximumCost(clusters)

    for i in cl:
        cost = costP(graphe[i],cl )
     
        if (cost>=costM):
            
            costM = cost
            I = i
    
    costM = 0 
    clj = cl.copy()
    clj.remove(I)
    J = 0 
    for j in clj:
        cost = costP(graphe[j],clj)
        if (cost>=costM and (j not in graphe[i])):
            costM = cost
            J = j

    if (I == J or J == 0):
        return clusters 

    clusters.remove(cl)

    clI = [I]
    clJ = [J]

    for v in cl:
        if( costP(graphe[v], [I]) >= costP(graphe[v], [J]) ):
            clI.append(v)
        else:
            clJ.append(v)

    clusters.append(clI)
    clusters.append(clJ)
    
    return clusters 


def emptyCluster(clusters):
    
    if (len(clusters)==1):
        return clusters
    cl = maximumCost(clusters)
    costM = 0
    clusters.remove(cl)

    for i in cl:
        for c in range(len(clusters)):
            cost = costP(graphe[i],clusters[c])
            if (cost >= costM):
                costM = cost 
                k = c 
        clusters[k].append(i)

    return clusters


def vertexAgglomeration(G):
    n = nbS
    CL = list()
    clusters = list()

    for u in G:
        CL.append((u,len(G[u])))

    CL = sorted(CL, key=lambda CL: CL[1])

    K = random.randint(1, n) #K comprit entre 1 et n 

    for _ in range(K):
        try:
            clusters.append([CL.pop()[0]])
        except IndexError:
            break 
        

    for j in CL: 
        try:
            clusters[maximizes(G[j[0]], j[0], clusters)].append(j[0])
            
        except (IndexError,ValueError):
            break
    
    return clusters

def construction(G):
    if(random.randint(0, 1) == 1):
        
        return relativeNeighborhood(G)
    else:
        
        return vertexAgglomeration(G)

def localSearch(clusters):
    if(random.randint(0, 1) == 1):
       
        return emptyCluster(clusters)
    else:
        
        return clusterSplit(clusters)


timeout = time.time() + 3

if (nbS > 30000):
    supprimeTout(supprimeTout)

else:
    afficherAretes(compareGraphes(GRASP(graphe,timeout),graphe))

