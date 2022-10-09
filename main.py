
from layout_placas import LayoutPlacas
from previsao_geracao import PrevisaoGeracao


if __name__ == '__main__':
    # módulo geral, contendo lista de telhados
    layout_placas = LayoutPlacas()
    # módulo que estima a geração de cada telhado (MWWH/ano)
    previsao_geracao_placas = PrevisaoGeracao(layout_placas)
    # imprime resultados em arquivo EXCEL
    layout_placas.imprime_telhados()

