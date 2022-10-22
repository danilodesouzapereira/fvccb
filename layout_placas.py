
import pandas as pd
from models import DadosEntradaTelhado, Telhado
import yaml


"""
Classe geral, contendo lista de telhados
"""
class LayoutPlacas:
    def __init__(self):

        # lê arquivo excel com dados de entrada dos telhados
        excel_data = pd.read_excel('..\\entrada.xlsx', sheet_name='Entrada')
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
            comp_util = telhado.dados_entrada_telhado.comprimento - 2 * config_placas['offset']
            num_placas_x = int(comp_util / config_placas['larg_placa'])
            # iterativamente, aloca fileiras de placas ao longo da largura do telhado
            larg_restante = telhado.dados_entrada_telhado.largura
            while larg_restante > config_placas['larg_placa']:
                if larg_restante > config_placas['comp_placa']:
                    if comp_util <  config_placas['larg_placa']:
                        break                    
                    larg_restante -= config_placas['comp_placa']
                    telhado.layout['retrato'].append(num_placas_x)
                    # verifica se deve descontar a largura do corredor a cada duas fileiras de placas
                    if len(telhado.layout['retrato']) % 2 == 0:
                        larg_restante -= config_placas['corredor'] 
                else:  # largura não comporta mais uma fileira de placas em retrato
                    if larg_restante > config_placas['larg_placa']:
                        telhado.layout['paisagem'] = int(comp_util / config_placas['comp_placa'])
                    break

            # calcula o número total de placas
            telhado.totaliza_num_placas(config_placas['kwp_placa'])
            # remove placas, em função da porcentagem de utilização do telhado
            num_placas_remover = round((1 - (telhado.dados_entrada_telhado.utilizacao_porc / 100)) * telhado.num_total_placas)
            if num_placas_remover > 0:
                if num_placas_remover < telhado.layout['paisagem']:
                    telhado.layout['paisagem'] -= num_placas_remover
                else:
                    num_placas_remover -= telhado.layout['paisagem']
                    telhado.layout['paisagem'] = 0
                    while num_placas_remover > 0:
                        if num_placas_remover < telhado.layout['retrato'][-1]:
                            telhado.layout['retrato'][-1] -= num_placas_remover
                            num_placas_remover = 0
                        else:
                            num_placas_remover -= telhado.layout['retrato'][-1]
                            telhado.layout['retrato'].pop()
                # recalcula o número total de placas
                telhado.totaliza_num_placas(config_placas['kwp_placa'])
            


    """
    Função que imprime os resultados em arquivo EXCEL
    """
    def imprime_telhados(self) -> list:        
        all_data_export = {'nome_telhado': [], 'latitude': [], 'longitude': [], 'azimute': [], 'inclinacao': [], 
            'largura': [], 'comprimento': [], 'utilizacao_porc': [], 'layout_retrato': [], 'layout_paisagem': [], 
            'num_total_placas': [], 'kwp': [], 'mwh_ano': []}
        for telhado in self.telhados:        
            for key, value in telhado.__dict__.items():
                if key == 'dados_entrada_telhado':
                    for key2, value2 in value.__dict__.items():
                        all_data_export[key2].append(value2)
                elif key == 'layout':
                    layout_retrato = ''
                    for num_placas_retrato in value['retrato']:
                        layout_retrato += str(num_placas_retrato) + ' , '
                    if len(layout_retrato) > 0:
                        layout_retrato = layout_retrato[0:-3]
                    all_data_export['layout_retrato'].append(layout_retrato)      
                    all_data_export['layout_paisagem'].append(value['paisagem'])     
                else:
                    all_data_export[key].append(value)      

        # nomes_colunas = [nome_coluna for nome_coluna, valor in all_data_export.items()]
        # df = pd.DataFrame(all_data_export, columns = nomes_colunas)
        # with pd.ExcelWriter('..\\saida.xlsx', mode='a', if_sheet_exists='replace') as writer:
        #     df.to_excel (writer, sheet_name='Resultados', index=False, header=True)
       

        with open('..\\saida.txt', 'w') as file:
            for nome_telhado in all_data_export['nome_telhado']:
                idx = all_data_export['nome_telhado'].index(nome_telhado)
                file.write(f'Telhado: {nome_telhado}\n')
                for key, value in all_data_export.items():
                    if key == 'nome_telhado':
                        continue
                    file.write(f'{key}: {value[idx]}\n')
                file.write('------------------------\n')

        lines_table_telhados = []
        for nome_telhado in all_data_export['nome_telhado']:
            lines_table = []
            lines_table_telhados.append(lines_table)
            idx = all_data_export['nome_telhado'].index(nome_telhado)
            for key, value in all_data_export.items():
                if key == 'nome_telhado':
                    continue
                lines_table.append({'Telhado': key, nome_telhado: str(value[idx])})
        
        return lines_table_telhados