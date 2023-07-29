import os
import csv
from time import sleep
import datetime
from ConsultaFipe import ConsultaFipe

arq = os.getcwd() + '/fipe_2023.csv'


def consultas(arquivo):
    """
    consultas
    """

    if not os.path.exists(arquivo):
        with open(arquivo, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            writer.writerow(['Mes_Ref', 'Cod_FIPE', 'Marca', 'Modelo', 'Ano_Modelo', 'Autenticacao',
                            'Data_Consulta', 'Preco_Medio'])
            csvfile.close()

    consulta = ConsultaFipe()
    datas = consulta.captura_datas()

    with open(arquivo, newline='', encoding="utf-8") as csvfile:
        final_line = csvfile.readlines()[-1]
    csvfile.close()

    final_line = final_line.split(';')
    data_final = final_line[0]
    marca_final = final_line[2]
    modelo_final = final_line[3]
    ano_final = final_line[4]

    datas = consulta.captura_datas()
    i_data = datas.index(data_final)
    # print("\n")
    #print(datas, i_data)
    # print("\n")
    consulta.select_data(data_final)
    marcas = consulta.captura_marcas()
    i_marca = marcas.index(marca_final)
    #print(marcas, i_marca)
    consulta.select_marca(marca_final)
    modelos = consulta.captura_modelos()
    i_modelo = modelos.index(modelo_final)
    #print(modelos, i_modelo)
    consulta.select_modelo(modelo_final)
    anos = consulta.captura_anos()
    # print(datas)
    i_ano = anos.index(ano_final)
    #print(anos, i_ano)

    FLAG_MARCAS = False
    FLAG_MODELOS = False
    FLAG_ANOS = False

    # print(i_ano)
    # print(len(anos))

    if i_ano == len(anos) - 1:
        FLAG_ANOS = True
        # print("\n\ni_ano\n\n")
        if i_modelo == len(modelos) - 1:
            FLAG_MODELOS = True
            if i_marca == len(marcas) - 1:
                FLAG_MARCAS = True
                if i_data == len(datas) - 1:
                    print("\nAcabou\n")
                    return True
                else:
                    i_data = i_data - 1
            else:
                i_marca = i_marca + 1
        else:
            i_modelo = i_modelo + 1

    datas = datas[0:i_data+1]
    marcas = marcas[i_marca:len(marcas)]
    modelos = modelos[i_modelo:len(modelos)]
    anos = anos[(i_ano+1):len(anos)]

    with open(arquivo, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        for data in reversed(datas):
            if data != "":
                consulta.select_data(data)
                if FLAG_MARCAS:
                    marcas = consulta.captura_marcas()
                else:
                    FLAG_MARCAS = True
                for marca in marcas:
                    if marca != "":
                        consulta.select_marca(marca)
                        if FLAG_MODELOS:
                            modelos = consulta.captura_modelos()
                        else:
                            FLAG_MODELOS = True
                        for modelo in modelos:
                            if modelo != "":
                                consulta.select_modelo(modelo)
                                if FLAG_ANOS:
                                    anos = consulta.captura_anos()
                                else:
                                    FLAG_ANOS = True
                                for ano in anos:
                                    if ano != "":
                                        consulta.select_ano(ano)
                                        writer.writerow(consulta.consulta())
                                consulta.limpa_consulta()
                                consulta.select_data(data)
                                consulta.select_marca(marca)

        csvfile.close()
    return True


count = 0

while True:
    try:
        consultas(arq)
    except Exception as e:
        print("Erro")
        print(datetime.datetime.now())
        count = count + 1
        sleep(count*60)
        print(datetime.datetime.now())

    finally:
        print(count)
        if count >= 50:
            print("Atingiu 50 erros")
            break
