def listbox_to_cursos(seleccionados):
    cursos = {}
    for elemento in seleccionados:
        codigo, seccion, nombre = elemento.split(" ", 2)
        if codigo not in cursos:
            cursos[codigo] = set()  # Usamos un conjunto para evitar secciones duplicadas
        cursos[codigo].add(seccion)
    
    for codigo, secciones in cursos.items():
        cursos[codigo] = sorted(secciones)
    return cursos


def secciones_to_horario(cursor, cursos, secciones):    
    days = ["LU", "MA", "MI", "JU", "VI", "SA"]
    dict_days = {day:"" for day in days}
    hours = ["07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15",
                 "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22"]
    horario = {horax: dict_days.copy() for horax in hours}

    for curso, seccion in zip(cursos, secciones):
        cursor.execute("SELECT horas, tipo FROM horarios_2024_1 WHERE codigo = ? AND seccion = ?", (curso, seccion,))
        for (hora, tipo) in cursor.fetchall():
            hora_int = int(hora) - 7
            dia, horadea = days[hora_int // 15], hours[hora_int % 15]
            if tipo == "TEORIA":
                descripcion = f'{curso} {seccion} T'
            else:
                descripcion = f'{curso} {seccion} ' + ('P' if tipo == "PRACTICA" else 'L')
            horario[horadea][dia] += descripcion if horario[horadea][dia] == "" else (' | ' + descripcion)
    return horario
