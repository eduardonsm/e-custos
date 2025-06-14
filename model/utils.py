def transformar_para_escala_1_3(valor):
    """
    Transforma um valor [0-100] em uma escala de 1 a 3.
    Se o valor for None, retorna None.
    """
    if valor is None:
        return None

    if valor <= 33:
        return 1
    elif valor <= 66:
        return 2
    else:  
        return 3
def transformar_para_escala_1_5(valor):
    """
    Transforma um valor [0-100] em uma escala de 1 a 5.
    Se o valor for None, retorna None.
    """
    if valor is None:
        return None

    if valor <= 20:
        return 1
    elif valor <= 40:
        return 2
    elif valor <= 60:
        return 3
    elif valor <= 80:
        return 4
    else:  
        return 5