import pdfkit
import pandas as pd


# function to convert dicts to html table
def _dict2htmltable(data):
    html = ''.join('<th>' + x + '</th>' for x in data[0].keys())
    for d in data:
        html += '<tr>' + ''.join('<td>' + x + '</td>' for x in d.values()) + '</tr>'
    return '<table border=1 class="stocktable" id="table1">' + html + '</table>'

# function to generate PDF from DICT
def generate_pdf_from_dict(all_report_data: list):
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    path_to_file = 'report_html.html'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    cont = 1
    for report_data_list in all_report_data:
        # convert dicts to html
        lines_html = _dict2htmltable(report_data_list)
        with open(f'report_html.html', 'w') as file_html:
            file_html.write(lines_html)
        # convert html into pdf
        pdfkit.from_file(path_to_file, output_path=f'report_pdf_{cont}.pdf', configuration=config)
        cont += 1


"""
# get data as a list of dicts
data = [{'symbol': 'AAPL', 'price': '154.73', 'change_dol': '-3.79', 'change_pct': '(-2.39%)'},
        {'symbol': 'GOOGL', 'price': '2,597.41', 'change_dol': '-51.18', 'change_pct': '(-1.93%)'},
        {'symbol': 'ABBV', 'price': '149.06', 'change_dol': '-0.11', 'change_pct': '(-0.07%)'},
        {'symbol': 'XOM', 'price': '84.92', 'change_dol': '-0.44', 'change_pct': '(-0.52%)'}]

# convert dicts to html table
def dict2htmltable(data):
    html = ''.join('<th>' + x + '</th>' for x in data[0].keys())
    for d in data:
        html += '<tr>' + ''.join('<td>' + x + '</td>' for x in d.values()) + '</tr>'
    return '<table border=1 class="stocktable" id="table1">' + html + '</table>'

# generate html file
lines_html = dict2htmltable(data)
with open(f'report_html.html', 'w') as file_html:
    file_html.write(lines_html)

# convert html into pdf
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
path_to_file = 'report_html.html'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
pdfkit.from_file(path_to_file, output_path='report_pdf.pdf', configuration=config)"""

