import pandas as pd
import numpy as np
import os
import openpyxl
import xlrd

#ruta_archivos = input('Ingrese la ubicación donde estan guardados los archivos')
#archivo_saldos = input('Seleccione el archivo de Saldos a favor periodos anteriores')


def liquidacion(ruta_archivos, archivo_saldos):
    # Define la dirección donde se encuentran los archivos Excel
    path = ruta_archivos

    # Define una lista vacía donde almacenarás los archivos Excel que contengan 'MCE' en el nombre
    lista_ventas = []
    ventas_list = []

    # Itera sobre los archivos en el directorio y agrega los que cumplan con el criterio a la lista
    for venta in os.listdir(path):
        if venta.endswith('.xlsx') and 'MCE' in venta:
            lista_ventas.append(venta)

    # Iterar sobre cada archivo dentro de la lista de ventas
    for venta in lista_ventas:
        # Leer cada archivo dentro de la ruta de archivos de ventas
        MCE = pd.read_excel(os.path.join(path, venta),
                            skiprows=1)
        # Extraer el cuit del nombre del archivo
        cuit_ventas = venta.split("-")[3].strip()
        # Extraer el nombre de contribuyente del nombre del archivo
        contribuyente = venta.split("-")[4].strip().replace('.xlsx', '')
        # Multiplicar el IVA por el Tipo de Cambio
        MCE['IVA'] = MCE['IVA'] * MCE['Tipo Cambio']
        # Si contiene nota de credito que reste
        MCE.loc[MCE["Tipo"].str.contains("Nota de Crédito", na=False), ['IVA']] *= -1
        # Sumar la columna del IVA debito
        iva_debito = MCE['IVA'].sum()
        # Crear DataFrame con la info
        ventas = pd.DataFrame({'CUIT': cuit_ventas, 'Contribuyente': contribuyente, 'IVA debito': iva_debito},
                              index=[0])
        # Concateno los resultados en una lista
        ventas_list.append(ventas)

    # Concateno los resultados al data frame de ventas definitivo
    ventas = pd.concat(ventas_list, ignore_index=True)

    # Dar formato a los numeros
    pd.options.display.float_format = '{:.2f}'.format

    # Define una lista vacía donde almacenarás los archivos Excel que contengan 'MCE' en el nombre
    archivos_compras = []
    compras_list = []

    # Itera sobre los archivos en el directorio y agrega los que cumplan con el criterio a la lista
    for compra in os.listdir(path):
        if compra.endswith('.xlsx') and 'MCR' in compra:
            archivos_compras.append(compra)

    # Iterar sobre cada archivo dentro de la lista de ventas
    for compra in archivos_compras:
        # Leer cada archivo dentro de la ruta de archivos de ventas
        MCR = pd.read_excel(os.path.join(path, compra),
                            skiprows=1)
        # Extraer el cuit del nombre del archivo
        cuit_compra = compra.split("-")[3].strip()
        # Extraer el nombre de contribuyente del nombre del archivo
        contribuyente = compra.split("-")[4].strip().replace('.xlsx', '')
        # Multiplicar el IVA por el Tipo de Cambio
        MCR['IVA'] = MCR['IVA'] * MCR['Tipo Cambio']
        # Si contiene nota de credito que reste
        MCR.loc[MCR["Tipo"].str.contains("Nota de Crédito", na=False), ['IVA']] *= -1
        # Sumar la columna del IVA debito
        iva_credito = MCR['IVA'].sum()
        # Crear DataFrame con la info
        compras = pd.DataFrame({'CUIT': cuit_compra, 'Contribuyente': contribuyente, 'IVA credito': iva_credito},
                               index=[0])
        # Concateno los resultados en una lista
        compras_list.append(compras)

    # Concateno los resultados al data frame de ventas definitivo
    compras = pd.concat(compras_list, ignore_index=True)

    saldos_anteriores = pd.read_excel(archivo_saldos)

    archivos_retenciones = []
    retenciones_list = []

    # Itera sobre los archivos en el directorio y agrega los que cumplan con el criterio a la lista
    for retencion in os.listdir(path):
        if retencion.endswith('.xls') and 'Mis Retenciones' in retencion:
            archivos_retenciones.append(retencion)

    print(archivos_retenciones)

    # Iterar sobre cada archivo dentro de la lista de ventas
    for retencion in archivos_retenciones:

        # Leer cada archivo dentro de la ruta de archivos de ventas
        MisRet = pd.read_excel(os.path.join(path, retencion))

        # Extraer el cuit del nombre del archivo
        cuit_ret = retencion.split("-")[3].strip()

        # Extraer el nombre de contribuyente del nombre del archivo
        contribuyente = retencion.split("-")[4].strip().replace('.xls', '')

        total_ret = MisRet['Importe Ret./Perc.'].sum()

        # Crear DataFrame con la info
        retenciones = pd.DataFrame({'CUIT': cuit_ret, 'Contribuyente': contribuyente, 'Total Ret': total_ret},
                                   index=[0])

        # Concateno los resultados en una lista
        retenciones_list.append(retenciones)

    # Concateno los resultados al data frame de ventas definitivo
    retenciones = pd.concat(retenciones_list,
                            ignore_index=True)

    # Creamos el dataframe de resultados
    resultados = pd.merge(ventas,
                          compras[['CUIT', 'IVA credito']],
                          on='CUIT',
                          how='left')

    resultados['CUIT'] = resultados['CUIT'].astype(np.int64)

    resultados = pd.merge(resultados,
                          saldos_anteriores[['CUIT', 'Saldo 1er P']],
                          on='CUIT',
                          how='left')

    # Llenamos los NaN con ceros
    resultados['Saldo 1er P'] = resultados['Saldo 1er P'].fillna(0)

    # Calcular columna de saldos
    resultados['Saldo'] = resultados['IVA debito'] - resultados['IVA credito'] - resultados['Saldo 1er P']

    # Definimos una función lambda que evalúa la condición y devuelve el valor correspondiente
    condicion = lambda x: "A favor contribuyente" if x < 0 else "A favor AFIP"

    # Utilizamos apply para aplicar la función a cada fila de la columna evaluada y crear la nueva columna
    resultados["Resultado 1er P"] = resultados["Saldo"].apply(condicion)

    resultados = pd.merge(resultados,
                          saldos_anteriores[['CUIT', 'Saldo 2do P']],
                          on='CUIT',
                          how='left')
    resultados['Saldo 2do P'] = resultados['Saldo 2do P'].fillna(0)

    # Concateno df de retenciones con resultados
    retenciones['CUIT'] = retenciones['CUIT'].astype(np.int64)

    resultados = pd.merge(resultados,
                          retenciones[['CUIT', 'Total Ret']],
                          on='CUIT',
                          how='left')

    resultados['Total Ret'] = resultados['Total Ret'].fillna(0)

    resultados['Saldo 2P'] = resultados['Total Ret'] + resultados['Saldo 2do P']

    # Verifica si la columna "Resultado 1er P" contiene "A favor contribuyente"
    mask = resultados['Resultado 1er P'] == 'A favor AFIP'

    # Aplica el cálculo solo para los casos que cumplen con la condición
    resultados.loc[mask, 'Iva a pagar'] = resultados['Saldo'] - resultados['Saldo 2P']
    resultados['Iva a pagar'] = resultados['Iva a pagar'].fillna(0)

    # Cambiar nombre de columnas
    resultados.rename(columns={'Saldo 1er P': 'Saldo tecnico PA',
                               'Saldo': 'Saldo tecnico del periodo',
                               'Saldo 2do P': 'SLD PA',
                               'Saldo 2P': 'SLD del periodo'},
                      inplace=True)
    pd.options.display.max_columns = None
    pd.set_option('display.width', 250)

    return resultados


