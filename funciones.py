def base_imponible(data_total_fra, data_tipo_iva):
    base_imponible= data_total_fra/(1.00+(data_tipo_iva/100.00))

    return redondear(base_imponible)

def iva(data_total_fra, data_tipo_iva):
    base = base_imponible(data_total_fra, data_tipo_iva)
    iva = base*(data_tipo_iva/100.00)
    return redondear(iva)

contador = 0
def contar_pulsos():
    #Da valor al idd y cuenta los asientos
    global contador
    contador += 1
    return contador

def redondear(numero):
    #Redondea a dos decimales
    return round(numero, 2)






