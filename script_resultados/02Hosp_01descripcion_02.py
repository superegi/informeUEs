
####
#### Escenciales previos
####
# ruta             = './resultados/02Hospitales/'
# Nombre_archivo   =  '2HOSP_01PAC_02'
# carpeta_script   ='./script_resultados/'
# nombre_script    = '02Hosp_01descripcion_02.py'
# archivo_exportar = ruta + Nombre_archivo  

print(str('Ruta:          ')[:12], ruta)
for hosp in BD_infohosp.index:
    hosp_en_curso = BD.loc[BD.Establecimiento == infohospitales[hosp]['Nombre']]
    exportar = archivo_exportar + 'texto_' + hosp + '.txt'
    print(' ', file=open(str(exportar), 'w'))
    print(str('texto_' + hosp + '.txt'))

    #########
    #########   OBJETO 1
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    tabla           = tab_frec(hosp_en_curso.Prevision).head(7)
    tabla_caption   = 'Previsión  de los pacientes que consultaron en \
    el hospital de {} entre el {} y el {}. '.format(
          infohospitales[hosp]['Nombre'],
          dt.datetime.strftime(tiempo['inicio'], '%d-%m-%Y'),
          dt.datetime.strftime(tiempo['fin'], '%d-%m-%Y'),)

    ######    complilación de todo lo trabajado
    
    tabla_inicio    = '\\begin{table}[H] \n  \centering \n'
    tabla_medio     = '\caption{ '
    tabla_fin       = '}   \n \end{table} \n'
    tabla_en_si     = tabla.to_latex(bold_rows=True,
                                     column_format='lccc')    # no olvidar cantidad de cols
    tabla_lista     = str(
                            tabla_inicio + tabla_en_si +
                            tabla_medio + tabla_caption +
                            tabla_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(tabla_lista, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 1    #######

    #########
    #########   OBJETO 2
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    tabla           = tab_frec(hosp_en_curso.Comuna).head(7)
    tabla_caption   = 'Comunas de origen de los pacientes que consultaron en \
    el hospital de {} entre el {} y el {}. '.format(
          infohospitales[hosp]['Nombre'],
          dt.datetime.strftime(tiempo['inicio'], '%d-%m-%Y'),
          dt.datetime.strftime(tiempo['fin'], '%d-%m-%Y'),
          )

    ######
    ######    complilación de todo lo trabajado
    ######

    tabla_inicio    = '\\begin{table}[H] \n  \centering \n'
    tabla_medio     = '\caption{ '
    tabla_fin       = '}   \n \end{table} \n'

    tabla_en_si     = tabla.to_latex(bold_rows=True,
                                     column_format='lccc')    # no olvidar cantidad de cols
    tabla_lista     = str(
                            tabla_inicio + tabla_en_si +
                            tabla_medio + tabla_caption +
                            tabla_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(tabla_lista, '\n', file=open(str(exportar), 'a'))
    #########   FIN OBJETO 2    #######
