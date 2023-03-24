# IVACalculator


Es una Mini APP desarrolada en FLASK, que en base a los archivos descargados desde el servicio 'Mis Comprobantes' y 'Mis Retenciones' en AFIP y un archivo Excel donde se indican los saldos a favor de periodos anteriores (si es que tienen), calcula el saldo de IVA a pagar o a favor del contribuyente.

Los archivos si o si tienen que tener el siguiente formato. Nro terminacion CUIT - MCR o MCE (depende si es emitidos o recibidos) - Periodo - Nombre Contribuyente (Ejemplo: 5 - MCR - 022023 - 20183536665 - Bonura Marcelo.xlsx)

# Como usarla

Hay que indicar en el input la direccion de la carpeta donde se encuentran descargados los archivos excel de comprobantes emitidos, recibidos y retenciones con el formato anteriormente especificado.

También hay que seleccionar el archivo Excel con saldos a favor periodos anteriores.
