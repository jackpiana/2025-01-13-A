import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.bestPt = 0
        self.bestPath = []

    def build_graph(self, loc):
        self.grafo.clear()

        nodesMap = DAO.getter_nodesMap(loc)
        nodes = nodesMap.values()
        self.grafo.add_nodes_from(nodes)

        potentialEdges = DAO.getter_potentialEdges()

        for nid1 in nodesMap.keys():
            for nid2 in nodesMap.keys():
                if nid1 == nid2:
                    continue
                if (nid1, nid2) in potentialEdges and (nid1, nid2) not in list(self.grafo.edges):
                    n1 = nodesMap[nid1]
                    n2 = nodesMap[nid2]
                    if n1.ch == n2.ch:
                        w = n1.ch
                    else:
                        w = n1.ch + n2.ch
                    self.grafo.add_edge(n1, n2, weight=w)

        print(self.grafo)


    def get_analisi(self):
        ccs = nx.connected_components(self.grafo)
        res = []
        for cc in ccs:
            if len(cc) > 1:
                res.append(list(cc))
        sorted_res = sorted(res, key=lambda x: len(x), reverse=True)
        return sorted_res

    def calcola_bestpath(self):
        self.bestPt = 0
        self.bestPath = []
        for nodoStart in list(self.grafo.nodes()):
            if nodoStart.ess != "?":
                self.ricorsione([nodoStart])

    def ricorsione(self, parziale):
        rimanenti = self.calcola_rimanenti(parziale)
        if rimanenti == []:
            self.calcolaPunteggio(parziale)
        else:
            rimanenti = rimanenti.copy()
            for n in rimanenti:
                parziale.append(n)
                parziale = parziale.copy()
                self.ricorsione(parziale)
                parziale.pop()

    def calcola_rimanenti(self, parziale):
        rimanenti = []
        nodoStart = parziale[-1]
        vicini = list(self.grafo.neighbors(nodoStart))
        for v in vicini:
            if nodoStart.ess != v.ess:
                continue
            if v.gid > nodoStart.gid:
                rimanenti.append(v)
        return rimanenti

    def calcolaPunteggio(self, parziale):
        pt = len(parziale)
        if pt > self.bestPt:
            self.bestPt = pt
            self.bestPath = parziale
        if pt == self.bestPt:
            sottografoNew = (self.grafo.subgraph(parziale))
            sottografoOld = (self.grafo.subgraph(self.bestPath))
            newScore = nx.number_connected_components(sottografoNew)
            oldScore = nx.number_connected_components(sottografoOld)
            if newScore < oldScore:
                self.bestPath = parziale
                print('porcacciodio')
            else:
                print('qui')


if __name__ == "__main__":
    m = Model()
    m.build_graph('nucleus')
    m.get_analisi()
    m.calcola_bestpath()
    print(m.bestPath)


#nid2 > nid1 and
