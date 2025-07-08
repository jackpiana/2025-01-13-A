import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.locdd = None

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()

        self._model.build_graph(self.locdd)

        self._view.txt_result.controls.append(ft.Text(self._model.grafo))

        edges = list(self._model.grafo.edges(data= True))
        sorted_edges = sorted(edges, key = lambda e: e[2]['weight'])
        for e in sorted_edges:
            self._view.txt_result.controls.append(ft.Text(f"{e[0].gid} <-> {e[1].gid}   peso: {e[2]['weight']}"))

        self._view.update_page()

    def analyze_graph(self, e):
        ccs = self._model.get_analisi()
        for cc in ccs:
            self._view.txt_result.controls.append(ft.Text(f"componente connessa lunga: {len(cc)}"))
            for node in cc:
                self._view.txt_result.controls.append(ft.Text(f"{node.gid}"))
            self._view.txt_result.controls.append(ft.Text(f"\n"))

        self._view.update_page()



    def handle_path(self, e):
        self._view.txt_result.controls.clear()
        self._model.calcola_bestpath()
        bestPath = self._model.bestPath
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n.gid}"))
        self._view.update_page()



#DROPDOWN
    def fill_dropdown(self):
        lista_opzioni = DAO.getter_localizations()
        for o in lista_opzioni:
            self._view.dd_localization.options.append(ft.dropdown.Option(key= o,
                                                                  text=o,
                                                                  data= o,
                                                                  on_click=self.read_dropdown))
    def read_dropdown(self, e):
        self.locdd = e.control.data
        print(f"valore letto: {self.locdd} - {type(self.locdd)}")
