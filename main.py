
from layout_placas import LayoutPlacas
from previsao_geracao import PrevisaoGeracao
from generate_report import generate_pdf_from_dict


if __name__ == '__main__':
    # módulo geral, contendo lista de telhados
    layout_placas = LayoutPlacas()
    # módulo que estima a geração de cada telhado (MWWH/ano)
    previsao_geracao_placas = PrevisaoGeracao(layout_placas)
    # imprime resultados em arquivo EXCEL
    lines_table_telhados = layout_placas.imprime_telhados()
    # generate pdf file
    generate_pdf_from_dict(lines_table_telhados)
