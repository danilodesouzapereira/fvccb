import pdfkit
import pandas as pd


# function to convert dicts to html table
def _dict2htmltable(data, nome_telhado):

    # insert CSS style
    css_lines = ''
    with open('report_css_style.css', 'r') as file_css:
        for line in file_css.readlines():
            css_lines += line
    html_style = f'<style>{css_lines}</style>'   

    html_header = f'<h1>CNS - FOTOVOLTAICO</h1><h4>Resultado de dimensionamento - {nome_telhado}</h4>'
    html = ''.join('<th>' + x + '</th>' for x in data[0].keys())
    for d in data:
        html += '<tr>' + ''.join('<td>' + x + '</td>' for x in d.values()) + '</tr>'
    return html_style + html_header + '<table class="content-table">' + html + '</table>'    


# function to generate PDF from DICT
def generate_pdf_from_dict(all_report_data: list):
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    path_to_file = 'report_html.html'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    for report_data_list in all_report_data:
        nome_telhado = list(report_data_list[0].keys())[-1]
        # convert dicts to html
        lines_html = _dict2htmltable(report_data_list, nome_telhado)
        with open(f'report_html.html', 'w') as file_html:
            file_html.write(lines_html)
        # convert html into pdf
        pdfkit.from_file(path_to_file, output_path=fr'..\Resultado - {nome_telhado}.pdf', configuration=config)

