import pandas as pd
import itertools

DFF = pd.read_csv('Cursos Disponibles FC 2024-1 horas.csv')
ram_df = [[],[]]

def get_horas_cod_sec_tipo(df, curso, seccion, tipo):
    global ram_df
    if (curso, seccion, tipo) in ram_df[0]:
        return ram_df[1][ram_df[0].index((curso, seccion, tipo))]
    ram_df[0].append((curso, seccion, tipo))
    df_c_s_t = df.loc[(df['codigo'] == curso) & (df['seccion'] == seccion) & (df['tipo'] == tipo), 'horas']
    ram_df[1].append(df_c_s_t)
    return df_c_s_t


def get_horas_cod_sec(df, curso, seccion):
    global ram_df
    if (curso, seccion) in ram_df[0]:
        return ram_df[1][ram_df[0].index((curso, seccion))]
    ram_df[0].append((curso, seccion))
    df_c_s_t = df.loc[(df['codigo'] == curso) & (df['seccion'] == seccion), 'horas']
    ram_df[1].append(df_c_s_t)
    return df_c_s_t


def get_cruces_curso_curso(df, curso_i, seccion_i, curso_j, seccion_j):
    # cruces = [cruces[0], cruces[1], cruces[2]] = [teo/teo, teo/pra, pra/pra]
    horas_teo_i = get_horas_cod_sec_tipo(df, curso_i, seccion_i, 'TEORIA')
    horas_pra_i = get_horas_cod_sec_tipo(df, curso_i, seccion_i, 'PRACTICA')
    horas_lab_i = get_horas_cod_sec_tipo(df, curso_i, seccion_i, 'LABORATORIO')
    horas_teo_j = get_horas_cod_sec_tipo(df, curso_j, seccion_j, 'TEORIA')
    horas_pra_j = get_horas_cod_sec_tipo(df, curso_j, seccion_j, 'PRACTICA')
    horas_lab_j = get_horas_cod_sec_tipo(df, curso_j, seccion_j, 'LABORATORIO')

    set_horas_teo_i = set(horas_teo_i)
    set_horas_pra_i = set(horas_pra_i) | set(horas_lab_i)
    set_horas_teo_j = set(horas_teo_j)
    set_horas_pra_j = set(horas_pra_j) | set(horas_lab_j)

    teoria_teoria = len(set_horas_teo_i & set_horas_teo_j)
    practica_practica = len(set_horas_pra_i & set_horas_pra_j)

    cruces_i = (teoria_teoria, len(set_horas_teo_i & set_horas_pra_j), practica_practica)
    cruces_j = (teoria_teoria, len(set_horas_teo_j & set_horas_pra_i), practica_practica)

    num_cruces = teoria_teoria + practica_practica + cruces_i[1] + cruces_j[1]
    return cruces_i, cruces_j, num_cruces


def son_cruces_validos(cruces, condiciones):
    """ (Universidad Nacional de Ingenieria)
    CONDICIONES PARA CONSIDERAR UN CRUCE ENTRE DOS CURSOS COMO VALIDO:
        - Hasta cuatro (04) horas de cruces de horarios de solo teoría con teoría de dos
          asignatura-sección, siendo las horas no necesariamente consecutivas.
        - Hasta dos (02) horas de cruces de horario de teoría con horarios de práctica
          o laboratorios, no necesariamente consecutivas.
        - Hasta dos (02) horas de cruces de horarios de teoría con horarios de práctica
          o laboratorios y hasta dos (02) horas de cruces de horarios de solo teoría con
          teoría, no necesariamente consecutivos.
    """
    # Obtener caracteristicas de cruces
    (teo_teo, teo_pra, pra_pra) = cruces
    if pra_pra > 0 or teo_teo > 4 or teo_pra > 2:
        return False
    es_4tt = (teo_teo <= 4 and teo_pra == 0)
    es_2tp = (teo_teo == 0 and teo_pra <= 2)
    es_2tt2tp = (teo_teo <= 2 and teo_pra <= 2)
    es_valido = es_4tt or es_2tp or es_2tt2tp
    if not es_valido:
        return False
    
    # Verificar condiciones
    (con_cruces_teo_teo, con_cruces_teo_pra) = condiciones[1:]
    if con_cruces_teo_teo and con_cruces_teo_pra:
        return True
    if ((con_cruces_teo_teo and not es_4tt) or
        (con_cruces_teo_pra and not es_2tp)):
        return False
    return True


def es_un_horario_valido(df, cursos, secciones, condiciones):
    num_cruces_horario = 0
    for (curso_i, seccion_i), (curso_j, seccion_j) in itertools.combinations(zip(cursos, secciones), 2):
        cruces_i, cruces_j, num_cruces = get_cruces_curso_curso(df, curso_i, seccion_i, curso_j, seccion_j)
        if not son_cruces_validos(cruces_i, condiciones):
            return False
        if not son_cruces_validos(cruces_j, condiciones):
            return False
        num_cruces_horario += num_cruces
    if condiciones[0] != num_cruces_horario:
        return False
    return True


def caracterizar_y_verificar(df, cursos, condiciones):
        global ram_df
        ram_df = [[],[]]
        lista_horarios = []
        if len(cursos) == 0:
            return lista_horarios
        if condiciones[0]==0 or condiciones[1:]==[False, False] or len(cursos)==1:
        # METODO DE LOS CONJUNTOS
            secciones = cursos.values()
            permutaciones = list(itertools.product(*secciones))
            tam_permutaciones = len(permutaciones)
            ultimos_valores = [valor[-1] for valor in cursos.values()]
            i=0
            while i < tam_permutaciones:
                hay_cruces, horario = False, set()
                lista_cursos = list(cursos.keys())
                for curso, seccion in zip(lista_cursos, permutaciones[i]):
                    horario_test = set(get_horas_cod_sec(df, curso, seccion))
                    if horario & horario_test:
                        i_curso, hay_cruces = lista_cursos.index(curso), True
                        break
                    horario.update(horario_test)
                if not hay_cruces:
                    lista_horarios.append(permutaciones[i])
                else:
                    i_curso+=1
                    permutacion = list(permutaciones[i])
                    permutacion[i_curso:] = ultimos_valores[i_curso:]
                    i = permutaciones.index(tuple(permutacion))
                i+=1
            return lista_horarios
        
        # METODO DE LAS CARACTERISTICAS
        j=0
        for i, permutacion in enumerate(itertools.product(*cursos.values())):
            if es_un_horario_valido(df, cursos.keys(), permutacion, condiciones):
                lista_horarios.append(permutacion)
        return lista_horarios
