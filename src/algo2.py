import fileinput
import sys



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
        sommet1 = lignes[i].split()[0]
        sommet2 = lignes[i].split()[1]

        aretes.add( (  int(sommet1) , int(sommet2) ) ) 

        graphe.setdefault(sommet1, []).append(sommet2)
        graphe.setdefault(sommet2, []).append(sommet1)


def afficherAretes(A):
    # Supprimer toutes les arêtes du graphe : le graphe résultat est une collection de sommets isolés.
    # Return : Liste d'arêtes
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


#afficherAretes(ajoutTout(nbS,aretes))

"""
for u in graphe:
        for v in graphe[u]:
            print("Arête {%s,%s}" % (u,v))
"""                                    
 

