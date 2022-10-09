from dataclasses import dataclass


@dataclass
class DadosEntradaTelhado:
    nome_telhado: str
    latitude: float
    longitude: float
    azimute: float
    inclinacao: float
    largura: float
    comprimento: float


class Telhado:
    def __init__(self, dados_entrada_telhado: DadosEntradaTelhado):
        self.dados_entrada_telhado = dados_entrada_telhado
        self.num_placas_x: int = 0
        self.num_placas_y: int = 0
        self.num_placas_paisagem: int = 0
        self.num_total_placas: int = 0
        self.kwp: float = 0.0
        self.mwh_ano: float = 0.0
    
    def totaliza_num_placas(self, kwp_placa: float):
        self.num_total_placas = self.num_placas_x * self.num_placas_y
        self.num_total_placas += self.num_placas_paisagem
        self.kwp = self.num_total_placas * kwp_placa
