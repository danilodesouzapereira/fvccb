

import csv
from layout_placas import LayoutPlacas, Telhado
from math import sqrt


"""
Classe que estima a geração de cada telhado (MWWH/ano)
"""
class PrevisaoGeracao:
    def __init__(self, layout_placas: LayoutPlacas):
        self.layout_placas = layout_placas
        self.banco_mwh = []
        self._le_banco_geracao()
        self._calcula_geracao_por_telhado()

    # lê banco de geração
    def _le_banco_geracao(self):        
        inicial = True
        mwh_por_local = {}
        with open('mwh_por_local_por_azimute.csv', mode='r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                if inicial:
                    inicial = False
                    continue
                lat_lon = f'{row["LATITUDE"]},{row["LONGITUDE"]}'
                if lat_lon in mwh_por_local:
                    mwh_por_local[lat_lon]['mwh_20kwp'].append(float(row["MWH"]))
                else:
                    mwh_por_local[lat_lon] = {'lat': float(row["LATITUDE"]), 'lon': float(row["LONGITUDE"]), 'mwh_20kwp': [float(row["MWH"])]}
        self.banco_mwh = [mwh_local_dict for key, mwh_local_dict in mwh_por_local.items()]


    """
    Método para calcular geração do telhado
    """
    def _calcula_geracao_por_telhado(self):
        for telhado in self.layout_placas.telhados:
            # calcula a geração (MWH) do local mais próximo (para 20KWP)
            dict_geracao = self._determina_dict_geracao_mais_proximo(telhado)
            idx_azimute = int(telhado.dados_entrada_telhado.azimute) % 5
            mwh_20kwp = dict_geracao['mwh_20kwp'][idx_azimute]
            # interpola ou extrapola a geração anual (MWH/ano) para a potência instalada do telhado
            telhado.mwh_ano = round(mwh_20kwp * (telhado.kwp / 20), 2)

    """
    Método para determinar o dicionário de gerações mais próximo
    """
    def _determina_dict_geracao_mais_proximo(self, telhado: Telhado) -> dict:
        lat_ref = telhado.dados_entrada_telhado.latitude
        lon_ref = telhado.dados_entrada_telhado.longitude
        dist_min = 0
        dict_geracao_mais_proximo = None
        for dict_geracao in self.banco_mwh:            
            dist = sqrt(pow((dict_geracao['lat'] - lat_ref), 2) + pow((dict_geracao['lon'] - lon_ref), 2))
            if dict_geracao_mais_proximo is None or dist < dist_min:
                dist_min = dist
                dict_geracao_mais_proximo = dict_geracao
        return dict_geracao_mais_proximo

