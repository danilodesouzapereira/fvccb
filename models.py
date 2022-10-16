from dataclasses import dataclass


@dataclass
class DadosEntradaTelhado:
    nome_telhado: str
    latitude: float         # latitude [graus]
    longitude: float        # longitude [graus]
    azimute: float          # orientação azimutal do telhado [graus]
    inclinacao: float       # inclinação do telhado [graus]
    largura: float          # largura do telhado [m]
    comprimento: float      # comprimento do telhado [m]
    utilizacao_porc: float  # porcentagem de utilização do telhado [%]


class Telhado:
    def __init__(self, dados_entrada_telhado: DadosEntradaTelhado):
        self.dados_entrada_telhado = dados_entrada_telhado
        self.layout: dict = {'retrato': [], 'paisagem': 0}
        self.num_total_placas: int = 0
        self.kwp: float = 0.0
        self.mwh_ano: float = 0.0
    
    def totaliza_num_placas(self, kwp_placa: float):
        self.num_total_placas = 0
        for num_placas_x in self.layout['retrato']:
            self.num_total_placas += num_placas_x
        self.num_total_placas += self.layout['paisagem']
        self.kwp = self.num_total_placas * kwp_placa
