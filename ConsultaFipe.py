from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup


class ConsultaFipe:
    """
    Class de Consulta
    """

    def __init__(self) -> None:

        self.datas = None
        self.marcas = None
        self.modelos = None
        self.anos = None

        self.data = None
        self.marca = None
        self.modelo = None
        self.ano = None

        self.options = Options()
        self.options.add_argument('window-size=400,800')
        self.options.add_argument('--headless')

        self.navegador = webdriver.Chrome(options=self.options)
        self.navegador.get('https://veiculos.fipe.org.br/')
        sleep(2)

        self.botao_carro = self.navegador.find_element(
            By.CLASS_NAME, 'ilustra')
        self.botao_carro.click()
        sleep(0.5)

        self.page_content = self.navegador.page_source
        self.site = BeautifulSoup(self.page_content, 'html.parser')

        self.input_select_date = Select(
            self.navegador.find_element(By.ID, 'selectTabelaReferenciacarro'))

        self.input_select_brand = Select(
            self.navegador.find_element(By.ID, 'selectMarcacarro'))

        self.input_select_model = Select(
            self.navegador.find_element(By.ID, 'selectAnoModelocarro'))

        self.input_select_year_fuel = Select(
            self.navegador.find_element(By.ID, 'selectAnocarro'))

        self.botao_pesquisar = self.navegador.find_element(
            By.ID, 'buttonPesquisarcarro')

        self.botao_limpar = None

    def captura_datas(self):
        """
        captura_datas
        """
        return [o.text for o in self.input_select_date.options]

    def select_data(self, data):
        """
        select_data
        """
        self.data = data
        self.input_select_date.select_by_visible_text(data)
        # sleep(0.5)

    def captura_marcas(self):
        """
        captura_marcas
        """
        return [o.text for o in self.input_select_brand.options]

    def select_marca(self, marca):
        """
        select_marca
        """
        self.marca = marca
        self.input_select_brand.select_by_visible_text(marca)
        # sleep(0.5)

    def captura_modelos(self):
        """
        captura_modelo
        """
        return [o.text for o in self.input_select_model.options]

    def select_modelo(self, modelo):
        """
        select_modelo
        """
        self.modelo = modelo
        self.input_select_model.select_by_visible_text(modelo)
        # sleep(0.5)

    def captura_anos(self):
        """
        captura_ano
        """
        return [o.text for o in self.input_select_year_fuel.options]

    def select_ano(self, ano):
        """
        select_ano
        """
        self.ano = ano
        self.input_select_year_fuel.select_by_visible_text(ano)
        # sleep(0.5)

    def consulta(self):
        """
        consulta
        """
        # self.select_data(data)
        # self.select_marca(marca)
        # self.select_modelo(modelo)
        # self.select_ano(ano)
        self.botao_pesquisar.click()
        # sleep(2)
        sleep(0.8)

        # Cod Fipe
        cod_fipe = self.navegador.find_element(
            By.XPATH, '//*[@id="resultadoConsultacarroFiltros"]/table/tbody/tr[2]/td[2]/p').text

        # Cod Autenticacao
        cod_aut = self.navegador.find_element(
            By.XPATH, '//*[@id="resultadoConsultacarroFiltros"]/table/tbody/tr[6]/td[2]/p').text

        # Data Consulta
        data_consulta = self.navegador.find_element(
            By.XPATH, '//*[@id="resultadoConsultacarroFiltros"]/table/tbody/tr[7]/td[2]/p').text

        # Preco Medio
        preco = self.navegador.find_element(
            By.XPATH, '//*[@id="resultadoConsultacarroFiltros"]/table/tbody/tr[8]/td[2]/p').text

        # return {"Mes_Ref": data, "Cod_FIPE": cod_fipe, "Marca": marca, "Modelo": modelo,
        #        "Ano_Modelo": ano, "Autenticacao": cod_aut, "Data_Consulta": data_consulta,
        #        "Preco_Medio": preco}

        return [self.data, cod_fipe, self.marca, self.modelo,
                self.ano, cod_aut, data_consulta, preco]

    def limpa_consulta(self):
        """
        limpa_consulta
        """
        self.botao_limpar = self.navegador.find_element(
            By.XPATH, '//*[@id="buttonLimparPesquisarcarro"]/a')
        self.botao_limpar.click()

        # sleep(0.5)
