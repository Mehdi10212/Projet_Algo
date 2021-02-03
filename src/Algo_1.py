import fileinput
import sys

def AfficherAretes(G):
    for u in G:
        for v in G[u]:
            print("Arête {%s,%s}" % (u,v))

def AfficherSommet(G):
    for u in G:
        print("Sommet {%s}" % (u))


def lireFichier():
    graphe = dict()
    aretes = list()
    #solution = sys.maxsize
    
    lignes = []
    #for line in fileinput.input():
    for line in open("test.txt", "r"):
        lignes.append(line.rstrip())
    lenLignes = len(lignes)


    for i in range(lenLignes):
        if(lignes[i].split()[0] == 'p'):
            nbS = int( lignes[i].split()[2] )
            nbA = int( lignes[i].split()[3] )
        
        elif(lignes[i].split()[0] == 'c'):
            pass
            """ 
            for word in lignes[i].split():
                if(word == "optimal"):
                    try:
                        if(type(int(word)) == int):
                            solution = int(word)
                    except ValueError:
                        pass
        """
        else:
            aretes.append(lignes[i])
    
    #print(aretes)
    #print("La solution est en",solution,"étapes")
    #print("Nombre de sommet :",nbS)
    #print("Nombre d'aretes :", nbA)
    #for u in aretes:
    #    print(u)    
    return aretes           


def SupprimerAretes():
    # Supprimer toutes les arêtes du graphe : le graphe résultat est une collection de sommets isolés.
    # Return : Liste d'arêtes
    listeAretes = lireFichier()

    #print("Liste des arêtes supprimer : ")
    for u in listeAretes:
        print(u)
    
def ceerGraphe():
    listeAretes = lireFichier()

    



if __name__ == "__main__":

    """
    G = {
        "a": ["b"],
        "b": ["a", "c", "d"],
        "c": ["b", "d"],
        "d": ["b", "c", "e"],
        "e": ["d"]
    }
    """
    #AfficherAretes(G)
    SupprimerAretes()
    #AfficherAretes(G)
    #lireFichier()

