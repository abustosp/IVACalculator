import pandas as pd
import numpy as np
import os
from tkinter.filedialog import askdirectory
#import openpyxl

#leer el archivo Formato.xlsx
Comprobante_C = pd.read_excel('Formato.xlsx', sheet_name='Comprobante_C')
Comprobante_V = pd.read_excel('Formato.xlsx', sheet_name='Comprobante_V')
Alicuota_V = pd.read_excel('Formato.xlsx', sheet_name='Alicuota_V')

#leer todos lor achivos .txt no vacíos de la carpeta Consolidar
path = askdirectory()
Archivos = os.listdir(path)
Archivos_txt = [f for f in Archivos if (os.stat(path + "/" + f).st_size != 0 and f.endswith(".txt"))]
del Archivos

#crear una nueva variable con los Archivos_txt que contengan la palabra 'Alicuota'
Alicuota_txt = [i for i in Archivos_txt if 'Alicuota' in i]
Alicuota_txt_V = [i for i in Alicuota_txt if '- LIV -' in i]
del Alicuota_txt

#crear una nueva variable con los Archivos_txt que no contengan la palabra 'Alicuota'
Comprobante_txt = [i for i in Archivos_txt if 'Alicuota' not in i]
Comprobante_txt_C = [i for i in Comprobante_txt if '- LIC -' in i]
Comprobante_txt_V = [i for i in Comprobante_txt if '- LIV -' in i]

#Eliminar Variables no usadas
del Archivos_txt

#convertir las Columna 'Descripcion' de los dataframes Comprobante
Comprobante_desc_C = Comprobante_C['Descripcion'].tolist()
Comprobante_desc_V = Comprobante_V['Descripcion'].tolist()
Alicuota_desc_V = Alicuota_V['Descripcion'].tolist()

#convertir las Columna 'Ancho' de los dataframes Comprobante
Comprobante_C = Comprobante_C['Ancho'].tolist()
Comprobante_V = Comprobante_V['Ancho'].tolist()
Alicuota_V = Alicuota_V['Ancho'].tolist()

#crear un dataframe vacio para conslidar
Consolidado_CBTE_C = pd.DataFrame()

#crear un loop para leer y consolidar todos los archivos de la variable Comprobante_txt_C de tipo FWF en base a la variable Comprobante
for i in Comprobante_txt_C:
    CBTE = pd.read_fwf(path + '/' + i, widths=Comprobante_C, header=None , encoding=("latin1") , names = Comprobante_desc_C)
    CBTE['Archivo'] = i
    #Dividir la columna 'Archivo' con el separador '-' y crear columnas con los valores obtenidos como 'Fin Cuit', 'CUIT contribuyente', 'LIV/LIC', 'Periodo' y 'Nombre del contribuyente' y eliminar los espacios en blanco al inicio y al final de cada valor
    CBTE['Fin Cuit'] = CBTE['Archivo'].str.split('-').str[0].str.strip()
    CBTE['CUIT contribuyente'] = CBTE['Archivo'].str.split('-').str[1].str.strip()
    #CBTE['LIV/LIC'] = CBTE['Archivo'].str.split('-').str[2].str.strip()
    CBTE['Periodo'] = CBTE['Archivo'].str.split('-').str[3].str.strip()
    CBTE['Nombre del contribuyente'] = CBTE['Archivo'].str.split('-').str[4].str.strip().str.replace(' SOS.txt', '')
    Consolidado_CBTE_C = pd.concat([Consolidado_CBTE_C, CBTE], axis=0)
del Comprobante_desc_C, Comprobante_C, CBTE , Comprobante_txt_C , i
#Dividir las columnas 'Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado' , 'Importe de percepciones o pagos a cuenta de otros impuestos nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones de Impuestos Municipales' , 'Importe de Impuestos Internos' , 'Crédito Fiscal Computable' , 'Otros Tributos' y 'IVA comisión' por 100
Consolidado_CBTE_C['Importe total de la operación'] = Consolidado_CBTE_C['Importe total de la operación']/100
Consolidado_CBTE_C['Importe total de conceptos que no integran el precio neto gravado'] = Consolidado_CBTE_C['Importe total de conceptos que no integran el precio neto gravado']/100
Consolidado_CBTE_C['Importe de operaciones exentas'] = Consolidado_CBTE_C['Importe de operaciones exentas']/100
Consolidado_CBTE_C['Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado'] = Consolidado_CBTE_C['Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado']/100
Consolidado_CBTE_C['Importe de percepciones o pagos a cuenta de otros impuestos nacionales'] = Consolidado_CBTE_C['Importe de percepciones o pagos a cuenta de otros impuestos nacionales']/100
Consolidado_CBTE_C['Importe de percepciones de Ingresos Brutos'] = Consolidado_CBTE_C['Importe de percepciones de Ingresos Brutos']/100
Consolidado_CBTE_C['Importe de percepciones de Impuestos Municipales'] = Consolidado_CBTE_C['Importe de percepciones de Impuestos Municipales']/100
Consolidado_CBTE_C['Importe de Impuestos Internos'] = Consolidado_CBTE_C['Importe de Impuestos Internos']/100
Consolidado_CBTE_C['Crédito Fiscal Computable'] = Consolidado_CBTE_C['Crédito Fiscal Computable']/100
Consolidado_CBTE_C['Otros Tributos'] = Consolidado_CBTE_C['Otros Tributos']/100
Consolidado_CBTE_C['IVA comisión'] = Consolidado_CBTE_C['IVA comisión']/100
#Dividir la columna 'Tipo de cambio' por 1000000
Consolidado_CBTE_C['Tipo de cambio'] = Consolidado_CBTE_C['Tipo de cambio']/1000000
#Si el Tipo de comprobante es igual a ('3' , '8' , '13' , '21' , '38' , '43' , '44' , '48' , '50' , '53' , '70' , '90' , '110' , '112' , '113' , '114' , '119' , '203' , '208' , '213') entonces multiplica el valor de las columnas 'Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado' , 'Importe de percepciones o pagos a cuenta de otros impuestos nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones de Impuestos Municipales' , 'Importe de Impuestos Internos' , 'Crédito Fiscal Computable' , 'Otros Tributos' y 'IVA comisión'
Consolidado_CBTE_C.loc[Consolidado_CBTE_C['Tipo de comprobante'].isin([3 , 8 , 13 , 21 , 38 , 43 , 44 , 48 , 50 , 53 , 70 , 90 , 110 , 112 , 113 , 114 , 119 , 203 , 208 , 213]) , ['Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado' , 'Importe de percepciones o pagos a cuenta de otros impuestos nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones de Impuestos Municipales' , 'Importe de Impuestos Internos' , 'Crédito Fiscal Computable' , 'Otros Tributos' , 'IVA comisión']] *= -1

# #crear un dataframe vacio para conslidar
# Consolidado_CBTE_V = pd.DataFrame()

# #crear un loop para leer y consolidar todos los archivos de la variable Comprobante_txt_V de tipo FWF en base a la variable Comprobante
# for i in Comprobante_txt_V:
#     CBTE = pd.read_fwf(path + '/' + i, widths=Comprobante_V, header=None , encoding=("latin1") , names = Comprobante_desc_V)
#     CBTE['Archivo'] = i
#     CBTE['Fin Cuit'] = CBTE['Archivo'].str.split('-').str[0].str.strip()
#     CBTE['CUIT contribuyente'] = CBTE['Archivo'].str.split('-').str[1].str.strip()
#     #CBTE['LIV/LIC'] = CBTE['Archivo'].str.split('-').str[2].str.strip()
#     CBTE['Periodo'] = CBTE['Archivo'].str.split('-').str[3].str.strip()
#     CBTE['Nombre del contribuyente'] = CBTE['Archivo'].str.split('-').str[4].str.strip().str.replace(' SOS.txt' , '')
#     Consolidado_CBTE_V = pd.concat([Consolidado_CBTE_V, CBTE], axis=0)
#del Comprobante_desc_V, Comprobante_V, CBTE , Comprobante_txt_V , i
del Comprobante_desc_V, Comprobante_V , Comprobante_txt_V
# #Dividir las columnas 'Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Percepción a no categorizados' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta de impuestos Nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones impuestos Municipales' , 'Importe impuestos internos' , 'Otros Tributos' por 100
# Consolidado_CBTE_V['Importe total de la operación'] = Consolidado_CBTE_V['Importe total de la operación']/100
# Consolidado_CBTE_V['Importe total de conceptos que no integran el precio neto gravado'] = Consolidado_CBTE_V['Importe total de conceptos que no integran el precio neto gravado']/100
# Consolidado_CBTE_V['Percepción a no categorizados'] = Consolidado_CBTE_V['Percepción a no categorizados']/100
# Consolidado_CBTE_V['Importe de operaciones exentas'] = Consolidado_CBTE_V['Importe de operaciones exentas']/100
# Consolidado_CBTE_V['Importe de percepciones o pagos a cuenta de impuestos Nacionales'] = Consolidado_CBTE_V['Importe de percepciones o pagos a cuenta de impuestos Nacionales']/100
# Consolidado_CBTE_V['Importe de percepciones de Ingresos Brutos'] = Consolidado_CBTE_V['Importe de percepciones de Ingresos Brutos']/100
# Consolidado_CBTE_V['Importe de percepciones impuestos Municipales'] = Consolidado_CBTE_V['Importe de percepciones impuestos Municipales']/100
# Consolidado_CBTE_V['Importe impuestos internos'] = Consolidado_CBTE_V['Importe impuestos internos']/100
# Consolidado_CBTE_V['Otros Tributos'] = Consolidado_CBTE_V['Otros Tributos']/100
# #Dividir la columna 'Tipo de cambio' por 1000000 
# Consolidado_CBTE_V['Tipo de cambio'] = Consolidado_CBTE_V['Tipo de cambio']/1000000
# #Si el Tipo de comprobante es igual a (3 , 8 , 13 , 21 , 38 , 43 , 44 , 48 , 50 , 53 , 70 , 90 , 110 , 112 , 113 , 114 , 119 , 203 , 208 , 213) entonces multiplica el valor de las columnas 'Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Percepción a no categorizados' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta de impuestos Nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones impuestos Municipales' , 'Importe impuestos internos' , 'Otros Tributos' por -1
# Consolidado_CBTE_V.loc[Consolidado_CBTE_V['Tipo de comprobante'].isin([3 , 8 , 13 , 21 , 38 , 43 , 44 , 48 , 50 , 53 , 70 , 90 , 110 , 112 , 113 , 114 , 119 , 203 , 208 , 213]) , ['Importe total de la operación' , 'Importe total de conceptos que no integran el precio neto gravado' , 'Percepción a no categorizados' , 'Importe de operaciones exentas' , 'Importe de percepciones o pagos a cuenta de impuestos Nacionales' , 'Importe de percepciones de Ingresos Brutos' , 'Importe de percepciones impuestos Municipales' , 'Importe impuestos internos' , 'Otros Tributos']] *= -1

#crear un dataframe vacio para conslidar
Consolidado_ALIC_V = pd.DataFrame()

#crear un loop para leer y consolidar todos los archivos de la variable Alicuota_txt_V de tipo FWF en base a la variable Alicuota
for i in Alicuota_txt_V:
    ALIC = pd.read_fwf(path + '/' + i, widths=Alicuota_V, header=None , encoding=("latin1") , names = Alicuota_desc_V)
    ALIC['Archivo'] = i
    ALIC['Fin Cuit'] = ALIC['Archivo'].str.split('-').str[0].str.strip()
    ALIC['CUIT contribuyente'] = ALIC['Archivo'].str.split('-').str[1].str.strip()
    #ALIC['LIV/LIC'] = ALIC['Archivo'].str.split('-').str[2].str.strip()
    ALIC['Periodo'] = ALIC['Archivo'].str.split('-').str[3].str.strip()
    ALIC['Nombre del contribuyente'] = ALIC['Archivo'].str.split('-').str[4].str.strip().str.replace(' Alicuota SOS.txt' , '')
    Consolidado_ALIC_V = pd.concat([Consolidado_ALIC_V, ALIC], axis=0)
del Alicuota_desc_V, Alicuota_V, ALIC , Alicuota_txt_V , i
#Dividir las columnas 'Importe neto gravado' y 'Impuesto liquidado' por 100
Consolidado_ALIC_V['Importe neto gravado'] = Consolidado_ALIC_V['Importe neto gravado']/100
Consolidado_ALIC_V['Impuesto liquidado'] = Consolidado_ALIC_V['Impuesto liquidado']/100
#Si el Tipo de comprobante es igual a (3 , 8 , 13 , 21 , 38 , 43 , 44 , 48 , 50 , 53 , 70 , 90 , 110 , 112 , 113 , 114 , 119 , 203 , 208 , 213) entonces multiplica el valor de las columnas 'Importe neto gravado' y 'Impuesto liquidado' por -1
Consolidado_ALIC_V.loc[Consolidado_ALIC_V['Tipo de comprobante'].isin([3 , 8 , 13 , 21 , 38 , 43 , 44 , 48 , 50 , 53 , 70 , 90 , 110 , 112 , 113 , 114 , 119 , 203 , 208 , 213]) , ['Importe neto gravado' , 'Impuesto liquidado']] *= -1

#crear Tablas dinamicas para todos los dataframe en base a la columnas 'Archivo' y 'Tipo de comprobante' 'Alícuota de IVA' y eliminar las columnas que no se necesitan

Consolidado_CBTE_CP = Consolidado_CBTE_C.pivot_table(index=['Fin Cuit', 'CUIT contribuyente', 'Periodo' , 'Nombre del contribuyente'], aggfunc='sum')
# Dejar solamente la columna 'Crédito Fiscal Computable'
Consolidado_CBTE_CP = Consolidado_CBTE_CP[['Crédito Fiscal Computable']]
del Consolidado_CBTE_C

# Consolidado_CBTE_VP = Consolidado_CBTE_V.pivot_table(index=['Fin Cuit', 'CUIT contribuyente', 'Periodo' , 'Nombre del contribuyente'], aggfunc='sum')
# #Eliminar columnas 'Cantidad de alícuotas de IVA' , 'Código de documento del comprador' , 'Fecha de Vencimiento o Pago' , 'Fecha de comprobante' , 'Número de comprobante' , 'Número de comprobante hasta' , 'Punto de venta' , 'Tipo de cambio'
# Consolidado_CBTE_VP = Consolidado_CBTE_VP.drop(['Cantidad de alícuotas de IVA', 'Código de documento del comprador', 'Fecha de Vencimiento o Pago', 'Fecha de comprobante', 'Número de comprobante', 'Número de comprobante hasta', 'Punto de venta', 'Tipo de cambio'], axis=1)
# del Consolidado_CBTE_V

Consolidado_ALIC_VP = Consolidado_ALIC_V.pivot_table(index=['Fin Cuit', 'CUIT contribuyente', 'Periodo' , 'Nombre del contribuyente'], aggfunc='sum')
# Dejar solamente la columna 'Impuesto liquidado'
Consolidado_ALIC_VP = Consolidado_ALIC_VP[['Impuesto liquidado']]
del Consolidado_ALIC_V

# Consolidar los dataframes Consolidado_CBTE_CP y Consolidado_ALIC_VP en base a la columna 'index' en un nuevo dataframe llamado 'Saldo'
Saldo = pd.merge(Consolidado_CBTE_CP, Consolidado_ALIC_VP, on=['Fin Cuit', 'CUIT contribuyente', 'Periodo' , 'Nombre del contribuyente'], how='outer')
# Reemplazar los valores nulos por 0
Saldo = Saldo.fillna(0)
#Crear la columna de 'Saldo Técnico' como la resta de las columnas 'Impuesto liquidado' y 'Crédito Fiscal Computable'
Saldo['Saldo Técnico'] = Saldo['Impuesto liquidado'] - Saldo['Crédito Fiscal Computable']


#Exportar los dataframes consolidados a un archivo excel
# Archivo_final = pd.ExcelWriter('Consolidado.xlsx', engine='openpyxl')
# Consolidado_CBTE_C.to_excel(Archivo_final, sheet_name='CBTE_C' , index=False)
# Consolidado_CBTE_CP.to_excel(Archivo_final, sheet_name='CBTE_C TD')
# Consolidado_CBTE_V.to_excel(Archivo_final, sheet_name='CBTE_V' , index=False)
# Consolidado_CBTE_VP.to_excel(Archivo_final, sheet_name='CBTE_V TD')
# Archivo_final.save()
