
import pandas as pd
from models import DadosEntradaTelhado, Telhado
import yaml


"""
Classe geral, contendo lista de telhados
"""
class LayoutPlacas:
    def __init__(self):

        # lê arquivo excel com dados de entrada dos telhados
        excel_data = pd.read_excel('telhados.xlsx', sheet_name='Entrada')
        df = pd.DataFrame(excel_data)
        dados_entrada_telhados = df.to_dict(orient='records')
        dados_entrada_telhados = [DadosEntradaTelhado(**dados_dict) for dados_dict in dados_entrada_telhados]
        self.telhados = [Telhado(dados_entrada_telhado) for dados_entrada_telhado in dados_entrada_telhados]

        # calcula número de placas que cada telhado comporta
        with open('configuracoes.yaml') as file:
            configuracoes = yaml.load(file, Loader=yaml.BaseLoader)
            config_placas = configuracoes['config_placas']
        config_placas = {key: float(valor) for key, valor in config_placas.items()}
        
        for telhado in self.telhados:
            telhado.num_placas_y = 0
            telhado.num_placas_x = 0
            telhado.num_placas_paisagem = 0
            comp_util = telhado.dados_entrada_telhado.comprimento - 2 * config_placas['offset']
            telhado.num_placas_x = int(comp_util / config_placas['larg_placa'])
            # iterativamente, aloca fileiras de placas ao longo da largura do telhado
            larg_restante = telhado.dados_entrada_telhado.largura
            while larg_restante > config_placas['larg_placa']:
                if larg_restante > config_placas['comp_placa']:
                    larg_restante -= config_placas['comp_placa']
                    telhado.num_placas_y += 1
                    if comp_util <  config_placas['larg_placa']:
                        telhado.num_placas_x = 0
                        break                    
                    # verifica se deve descontar a largura do corredor a cada duas fileiras de placas
                    if telhado.num_placas_y % 2 == 0:
                        larg_restante -= config_placas['corredor'] 
                else:  # largura não comporta mais uma fileira de placas em retrato
                    if larg_restante > config_placas['larg_placa']:
                        telhado.num_placas_paisagem = int(comp_util / config_placas['comp_placa'])
                    break
            telhado.totaliza_num_placas(config_placas['kwp_placa'])


    """
    Função que imprime os resultados em arquivo EXCEL
    """
    def imprime_telhados(self):        
        all_data_export = {'nome_telhado': [], 'latitude': [], 'longitude': [], 'azimute': [], 'inclinacao': [], 
            'largura': [], 'comprimento': [], 'num_placas_x': [], 'num_placas_y': [], 'num_placas_paisagem': [], 
            'num_total_placas': [], 'kwp': [], 'mwh_ano': []}
        for telhado in self.telhados:
            for key, value in telhado.dados_entrada_telhado.__dict__.items():
                all_data_export[key].append(value)
            for key, value in telhado.__dict__.items():
                if key == 'dados_entrada_telhado':
                    continue
                all_data_export[key].append(value)      
        df = pd.DataFrame(all_data_export, columns = [nome_coluna for nome_coluna, valor in all_data_export.items()])
        with pd.ExcelWriter('telhados.xlsx', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel (writer, sheet_name='Resultados', index=False, header=True)
