import itertools
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None

    # Alla pressione del bottone “Crea Grafo”, occorre creare un grafo completo, non ordinato, pesato,
    # in cui i vertici siano le squadre di cui al punto precedente
    # e gli archi colleghino tutte le coppie distinte di squadre
    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        #for u in self._grafo.nodes:
            #for v in self._grafo.nodes:
                #if u!=v:
                    #self._grafo.add_edge(u, v)

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)
        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]]
            sal2 = mapSalary[e[1]]
            peso = sal1 + sal2
            self._grafo[e[0]][e[1]]["weight"] = sal1 + sal2

            # self._grafo[e[0]][e[1]]["weight"] = mapSalary[e[0]] + mapSalary[e[1]]

    # Stampare per tale squadra l’elenco delle squadre adiacenti, ed
    # il peso degli archi corrispondenti, in ordine decrescente di peso
    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        return viciniTuples

    # Richiama il metodo del DAO
    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams =  DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID : t for t in self._teams}

        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)



