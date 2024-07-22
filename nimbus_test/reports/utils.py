import random
import json
from datetime import datetime, timedelta
from fpdf import FPDF

base_data = {
    "analise": [
        {"fenomeno": "chuva", "mensagem": "Registro de chuva moderada ao longo do dia inteiro, com períodos de intensificação em algumas áreas. A chuva começou nas primeiras horas da manhã e se estendeu até a noite, resultando em acumulações significativas. Essa condição pode causar transtornos no trânsito e em áreas vulneráveis a alagamentos."},
        {"fenomeno": "deslizamento", "mensagem": "Deslizamento de terra durante a chuva devido ao encharcamento do solo, que já estava saturado pelas chuvas dos dias anteriores. Esse deslizamento causou bloqueios em estradas locais e danos em algumas propriedades próximas. As autoridades foram acionadas para realizar os devidos reparos e garantir a segurança dos moradores."},
        {"mensagem": "A operação externa foi interrompida durante 3 horas devido à ocorrência de raios. Durante este período, a atividade elétrica foi intensa, representando um risco significativo para as atividades ao ar livre. Todos os funcionários foram instruídos a se abrigarem em locais seguros até que a tempestade passasse e fosse considerado seguro retomar as operações."},
        {"fenomeno": "neve", "mensagem": "Nevou intensamente durante a madrugada, resultando em um acúmulo considerável de neve nas ruas e calçadas. As equipes de limpeza urbana foram mobilizadas para liberar as principais vias de acesso. Houve interrupção no transporte público e algumas escolas suspenderam as aulas devido às condições perigosas das estradas."},
        {"fenomeno": "inundação", "mensagem": "Uma forte chuva causou a rápida elevação dos níveis dos rios, resultando em inundações em diversas áreas baixas. Várias residências foram evacuadas e abrigos temporários foram montados para acolher as famílias afetadas. Equipes de emergência trabalharam durante a noite para resgatar moradores isolados e minimizar os danos."}
    ],
    "previsao": [
        {"fenomeno": "chuva", "mensagem": "No início da tarde haverá chuva forte entre 12h e 13h, com possibilidade de trovoadas. A previsão indica que a intensidade da chuva será suficiente para causar alagamentos temporários em áreas baixas. As atividades a céu aberto não são indicadas durante esse período devido ao risco de raios e inundações rápidas."},
        {"fenomeno": "vento", "mensagem": "Durante a noite, a previsão é de vento forte com rajadas que podem chegar a 50 km/h. Essas condições de vento podem derrubar galhos de árvores e causar dificuldades para o manuseio de equipamentos pesados. As atividades que envolverem uso de guindaste devem ser remanejadas para o período da manhã, quando os ventos estarão mais calmos e seguros para a operação."},
        {"fenomeno": "nevoeiro", "mensagem": "Durante a madrugada haverá a ocorrência de nevoeiro denso, reduzindo a visibilidade a menos de 200 metros em algumas áreas. Esta condição se prolongará até o início da manhã, afetando principalmente a navegação e o tráfego nas estradas. A prática de navegação deverá ser interrompida até que o nevoeiro se dissipe, por volta das 8h da manhã, para evitar acidentes."},
        {"fenomeno": "geada", "mensagem": "No início da manhã haverá formação de geada, principalmente em áreas rurais e baixadas. Esta condição pode afetar negativamente a agricultura, especialmente cultivos sensíveis às baixas temperaturas. Recomenda-se aos agricultores tomarem medidas preventivas para proteger as plantações."},
        {"fenomeno": "chuva", "mensagem": "Previsão de tempestade com raios e ventos fortes, podendo alcançar até 70 km/h. As condições adversas devem durar até o início da noite. É aconselhável que as pessoas evitem áreas abertas e procurem abrigo seguro até que a tempestade passe."},
        {"fenomeno": "onda de calor", "mensagem": "Durante a tarde, espera-se uma onda de calor com temperaturas podendo ultrapassar os 35°C. Essas condições extremas podem representar riscos à saúde, como desidratação e insolação. Recomenda-se evitar exposição prolongada ao sol, manter-se hidratado e procurar locais frescos e sombreados."}
    ]
}

def generate_random_weather_data():
    def random_date():
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() + timedelta(days=30)
        return start_date + (end_date - start_date) * random.random()

    dynamic_data = {"analise": [], "previsao": []}

    num_analise = random.randint(1, len(base_data["analise"]))
    analyses = random.sample(base_data["analise"], num_analise)
    for analysis in analyses:
        entry = {
            "data": random_date().strftime('%Y-%m-%dT%H:%M'),
            "mensagem": analysis["mensagem"]
        }
        if random.choice([True, False]):
            entry["fenomeno"] = analysis.get("fenomeno", "Outros")
        dynamic_data["analise"].append(entry)

    num_previsao = random.randint(1, len(base_data["previsao"]))
    previsoes = random.sample(base_data["previsao"], num_previsao)
    for previsao in previsoes:
        entry = {
            "data": random_date().strftime('%Y-%m-%dT%H:%M'),
            "mensagem": previsao["mensagem"]
        }
        if random.choice([True, False]):
            entry["fenomeno"] = previsao.get("fenomeno", "Outros")
        dynamic_data["previsao"].append(entry)

    return dynamic_data

class PDF(FPDF):
    def __init__(self, client_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_name = client_name
        self.current_section = ''

    def header(self):
        old_left_margin, old_top_margin, old_right_margin = self.l_margin, self.t_margin, self.r_margin
        self.set_margins(0, 0, 0)
        self.set_fill_color(25, 25, 112)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 20)
        self.set_x(0)
        self.set_y(0)
        self.cell(0, 15, 'Relatório Meteorológico', 0, 1, 'C', fill=True)
        self.set_fill_color(218, 165, 32)
        self.cell(0, 3, '', 0, 1, 'C', fill=True)
        self.set_text_color(0, 0, 0)
        self.set_margins(old_left_margin, old_top_margin, old_right_margin)
        self.set_header_info()

    def set_header_info(self):
        self.set_y(30)
        self.set_font('Arial', 'B', 10)

        self.cell(0, 10, f'Cliente: {self.client_name}', 0, 0, 'L')

        data_str = f'Data: {datetime.now().strftime("%d/%m/%Y")}'
        data_width = self.get_string_width(data_str) + 2
        self.set_x(self.w - self.r_margin - data_width)

        self.cell(data_width, 10, data_str, 0, 1, 'R')

    def chapter_title(self, title, fill_color=None):
        self.set_font('Arial', 'B', 12)
        if fill_color:
            self.set_fill_color(*fill_color)
            self.set_text_color(255, 255, 255)
            self.cell(50, 10, title, 0, 1, 'L', fill=True)
            self.set_text_color(0, 0, 0)
        else:
            self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 8)
        self.multi_cell(0, 10, body)
        self.ln()

    def colored_text(self, text):
        self.set_font('Arial', '', 8)
        self.multi_cell(0, 10, text)
        self.ln()

def generate_pdf_report(data, output_path, client_name):
    pdf = PDF(client_name)

    analises_agrupadas = {}
    for analysis in data["analise"]:
        fenomeno = analysis.get("fenomeno", "Outros")
        if fenomeno not in analises_agrupadas:
            analises_agrupadas[fenomeno] = []
        analises_agrupadas[fenomeno].append(analysis)

    pdf.add_page()
    pdf.current_section = 'Análises'
    pdf.set_header_info()
    pdf.chapter_title('Análises')

    for fenomeno, analises in analises_agrupadas.items():
        tem_forte = any("forte" in analysis["mensagem"] for analysis in analises)
        if tem_forte:
            fill_color = (255, 0, 0)
        else:
            fill_color = (169, 169, 169)
        pdf.chapter_title(fenomeno, fill_color)
        for analysis in analises:
            body = f'Data: {analysis["data"]}\n{analysis["mensagem"]}'
            pdf.colored_text(body)

    previsoes_agrupadas = {}
    for forecast in data["previsao"]:
        fenomeno = forecast.get("fenomeno", "Outros")
        if fenomeno not in previsoes_agrupadas:
            previsoes_agrupadas[fenomeno] = []
        previsoes_agrupadas[fenomeno].append(forecast)

    pdf.add_page()
    pdf.current_section = 'Previsões'
    pdf.set_header_info()
    pdf.chapter_title('Previsões')

    for fenomeno, forecasts in previsoes_agrupadas.items():
        tem_forte = any("forte" in forecast["mensagem"] for forecast in forecasts)
        if tem_forte:
            fill_color = (255, 0, 0)
        else:
            fill_color = (169, 169, 169)
        pdf.chapter_title(fenomeno, fill_color)
        for forecast in forecasts:
            body = f'Data: {forecast["data"]}\n{forecast["mensagem"]}'
            pdf.colored_text(body)

    pdf.output(output_path)