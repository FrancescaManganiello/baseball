import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        self._model.creaGrafo(self._view._ddAnno.value)
        n, m = self._model.getGraphDetails()        # numero nodi e numero archi
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. Il grafo è costituito di {n} nodi e {m} archi"))

        self._view.update_page()

    def handleDettagli(self, e):

        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un team dal menu.", color="red"))
            self._view.update_page()
            return

        viciniTuple = self._model.getVicini(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il nodo {self._choiceTeam} ha {len(viciniTuple)} vicini", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Di seguito una lista ordinata dei vicini", color="green"))
        for v in viciniTuple:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} - peso {v[1]}", color = "green"))

        self._view.update_page()

    def handlePercorso(self, e):
        pass

    # METODO PER RIEMPIRE IL DROPDOWN
    def _fillDDYears(self):
        years = self._model.getAllYears()

        """ I metodo
        yearsDD = []
        for y in years:
            yearsDD.append(ft.dropdown.Option(y))
        """

        yearsDD = list(map(lambda x:ft.dropdown.Option(x), years))
        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    # Metodo chiamato quando qualcuno ha selezionato un anno, deve recuperare tutti i team che hanno
    # giocato in quell'anno e stamparli nel textfield e anche riempire il dropdown sotto
    def handleYearSelection(self, e):

        if self._view._ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("Selezionare un anno dal menù a tendina"))

        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)

        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per il {self._view._ddAnno.value} sono iscritte al "
                                                          f"campionato {len(teams)} squadre"))

        # Nello stesso momento occorre aggiornare il contenuto della tendina “Squadre”
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data = t,
                                                                    text = t.name,
                                                                    on_click = self.readDDTeams))
            self._view.update_page()

        self._view.update_page()

    # Legge dall'evento qual'è l'oggetto dal menù selezionato
    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team {self._choiceTeam}")




