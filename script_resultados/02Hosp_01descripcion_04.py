
####
#### Escenciales previos
####
# ruta             = './resultados/02Hospitales/'
# Nombre_archivo   =  '2HOSP_01PAC_02'
# carpeta_script   ='./script_resultados/'
# nombre_script    = '02Hosp_01descripcion_02.py'
# archivo_exportar = ruta + Nombre_archivo  

print(str('Ruta:          ')[:12], ruta)
dum_segs = BD.copy()
dum_segs[DTs] = dum_segs[DTs].applymap(lambda s: s.total_seconds()/60)
dum_segs_a = dum_segs.copy()

for hosp in BD_infohosp.index:
    hosp_en_curso = BD.loc[BD.Establecimiento == infohospitales[hosp]['Nombre']]
    dum_segs = dum_segs_a.loc[dum_segs_a.Establecimiento == infohospitales[hosp]['Nombre']]

    exportar = archivo_exportar + 'texto_' + hosp + '.txt'
    print('', file=open(str(exportar), 'w'))
    print(str('texto_' + hosp + '.txt'))

    #########
    #########   OBJETO 1
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = ' Al realizar los \
    cálculos, se encontraron {} RIC ({} a {}) atenciones al día y  \
    {} RIC ({} a {}) atenciones al mes '.format(
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.day])['Establecimiento'].count().describe()[5],
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.day])['Establecimiento'].count().describe()[4],
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.day])['Establecimiento'].count().describe()[6],
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.month])['Establecimiento'].count().describe()[5],
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.month])['Establecimiento'].count().describe()[4],
            hosp_en_curso.groupby([hosp_en_curso.TS_ingreso.dt.month])['Establecimiento'].count().describe()[6]
            )


    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 1    #######
    dum1 = hosp_en_curso.Triage.value_counts()
    dum2 = hosp_en_curso.Triage.value_counts(dropna=True)


    #########
    #########   OBJETO 2
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'
    a_redondear     =   3 #números a redondear

    texto           = ' La categorizacón de urgencia que recibían los pacientes al ser admitidos a \
    la urgencia fue de {}({}%) para Triage 1, \
    de {}({}%) para Triage 2, \
    de {}({}%) para Triage 3, \
    de {}({}%) para Triage 4, \
    de {}({}%) para Triage 5  . \
    Existen {}({}%) pacientes que no se categorizan'.format(
        dum2['Triage 1'],
        round(float(dum2['Triage 1'])/dum2.sum(), a_redondear)*100,
        dum2['Triage 2'],
        round(float(dum2['Triage 2']/dum2.sum()), a_redondear)*100,
        dum2['Triage 3'],
        round(float(dum2['Triage 3']/dum2.sum()), a_redondear)*100,             
        dum2['Triage 4'],
        round(float(dum2['Triage 4']/dum2.sum()), a_redondear)*100,
        dum2['Triage 5'],
        round(float(dum2['Triage 5']/dum2.sum()), a_redondear)*100,
        dum2.sum() - dum1.sum(),
        round(float((dum2.sum() - dum1.sum())/dum2.sum()), a_redondear)*100,
        )

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))


    #########   FIN OBJETO 2    #######


    ######## IMAGEN y CAPTION ############
    ######################################
    
    nombre_en_clave = 'atenciones_por_hora_y_triage'
    imagen_exportar = archivo_exportar + 'imagen_' + hosp + nombre_en_clave
    hosp_en_curso.groupby(
        [hosp_en_curso.TS_ingreso.dt.hour, 'Triage'])['Establecimiento'].count().unstack().plot(
        figsize = (7,5))
    plt.title('Cantidad de atenciones por hora en el \n '+ infohospitales[hosp]['Nombre'] +
    ' según categorizacón' )
    plt.xlabel('Hora del día')
    plt.savefig(imagen_exportar, dpi=100)
    plt.show()
    plt.clf()

    importar       = imagen_exportar + '.png'
    caption        = 'Distribución de la cantidad de pacientes admitidos según \
        los horarios de admisión según categorización \
        atendidos en el {} entre el {} y el {} '.format(
          infohospitales[hosp]['Nombre'],
          dt.datetime.strftime(tiempo['inicio'], '%d-%m-%Y'),
          dt.datetime.strftime(tiempo['fin'], '%d-%m-%Y'),
          )

    ######    complilación de todo lo trabajado
    imagen_inicio    = '\\begin{figure}[H] \n \
                    \centering \n \
                    \includegraphics[scale=0.55]{'
    imagen_medio     = '}   \n  \caption{ '
    imagen_en_si     = '.' + imagen_exportar
    imagen_caption = caption
    imagen_fin       = '} \n \label{etiqueta_por_definir} \n \
                 \end{figure}  \n'
    imagen_lista     = str(
                            imagen_inicio + imagen_en_si +
                            imagen_medio +
                            imagen_caption + imagen_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(imagen_lista, '\n', file=open(str(exportar), 'a'))

#############################################################
#############################################################
#############################################################
#############################################################

    dom1       = dum_segs[DTs].groupby([dum_segs.TS_ingreso.dt.hour])
    dom2 = dom1.describe(percentiles =[0.25, 0.75]).select(lambda x: x[1] in ['25%', '50%', '75%'], axis=1)
    i = dom2[DTs].copy().columns.levels[0]   # OP's suggestion, for more flexibility!
    nuevas = ['TE Categorización', 'TE Atención médica', 'Atención médica',
                  'TE definición', 'TE Cierre admin', 'TE Total UE']
    rename_dict = dict(zip(i, nuevas))
    dom2 = dom2.rename(columns=rename_dict, level=0)
    dom2.index.names = ['Hora ingreso']
    #dom2
    round(dom2)

    tabla           = round(dom2)
    tabla_caption   = 'Tiempos de espera en {} \
    entre el {} y {}. Los valores están expresados en minutos. TE significa tiempo de espera'.format(
        infohospitales[hosp]['Nombre'],
        BD.TS_ingreso.describe()[4],
        BD.TS_ingreso.describe()[5]
      )

    ######    complilación de todo lo trabajado

    tabla_inicio    = '\\begin{table}[H] \n  \centering \n \\resizebox{\\textwidth}{!}{  \n'
    tabla_medio     = ' } \n\caption{ '         # ojo que acá escalé la tabla
    tabla_fin       = '}   \n \end{table} \n'
    tabla_en_si     = tabla.to_latex(bold_rows=True,
                                     column_format='lccccccccccccccccccccccc')    # no olvidar cantidad de cols
    tabla_lista     = str(
                            tabla_inicio + tabla_en_si +
                            tabla_medio + tabla_caption +
                            tabla_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(tabla_lista, '\n', file=open(str(exportar), 'a'))

#############################################################
#############################################################
#############################################################
#############################################################

    for triage in  ['Triage 2','Triage 3','Triage 4', 'Triage 5' ]:
        dum1 = dum_segs.loc[dum_segs.Triage == triage]
        dom = dum1[DTs].describe()[['DT_EsperaCategorizacion', 'DT_EsperaMD', 'DT_AtencionMD',
               'DT_definicionPAC', 'DT_Espera_CierreAdm', 'DT_Total']].T[['mean','25%','50%','75%'  ]]
        dom.columns = ['Promedio' , 'p25',  'p50' , 'p75']
        dom = dom.T
        dom.columns = ['TE Categorización', 'TE Atención médica', 'Duración Atención médica',
                        'TE definición', 'TE Cierre adminisitrativo', 'TE Total en urgencias']
        dom.T

        tabla           = dom.T
        tabla_caption   = 'Tiempos de espera en unidades de urgencia del {} \
        entre el {} y {} para {}. Los valores están expresados en minutos.'.format(
            infohospitales[hosp]['Nombre'],
            BD.TS_ingreso.describe()[4],
            BD.TS_ingreso.describe()[5],
            triage
          )

        ######    complilación de todo lo trabajado

        tabla_inicio    = '\\begin{table}[H] \n  \centering \n    \n'
        tabla_medio     = '  \n\caption{ '         # ojo que acá escalé la tabla
        tabla_fin       = '}   \n \end{table} \n'
        tabla_en_si     = tabla.to_latex(bold_rows=True,
                                         column_format='lccccc')    # no olvidar cantidad de cols
        tabla_lista     = str(
                                tabla_inicio + tabla_en_si +
                                tabla_medio + tabla_caption +
                                tabla_fin)
        #print(tabla_lista)
        print(tabla_lista, '\n', file=open(str(exportar), 'a'))



#############################################################
#############################################################
#############################################################
#################      IMAGEN        ########################

    # cajas y bigotes #

    nombre_en_clave = 'cajas_y_bigotes_tiempos'
    imagen_exportar = archivo_exportar + 'imagen_' + hosp + nombre_en_clave
    dumA = dum_segs[['DT_EsperaCategorizacion', 'DT_EsperaMD', 'DT_AtencionMD',
           'DT_definicionPAC', 'DT_Espera_CierreAdm', 'DT_Total' , 'Triage']].copy()
    for var in list(DTs):
        q = dumA[var].quantile(0.95)
        dumA[var] = dumA[dumA[var] <q]
        #print(var) 
    
    dumA.columns = ['TE Categorización', 'TE Atención médica', 'Atención médica',
                  'TE definición', 'TE Cierre admin', 'TE Total UE', 'Triage']
    dumA.boxplot(column=['TE Categorización', 'TE Atención médica', 'Atención médica',
                  'TE definición', 'TE Cierre admin', 'TE Total UE'], by=['Triage'],
                 figsize=(9,8))
    plt.suptitle('Gráficos de cajas y bigotes para los distintos tiempos medidos  \n \
    en el {}'.format(
                infohospitales[hosp]['Nombre'],
    ))
    plt.savefig(imagen_exportar, dpi=100)
    plt.show()
    plt.clf()
    caption          = 'Gráfico de cajas y bigotes representando medidas de tendencia \
    central y dispersión de las distintas categorizaciones de urgencia  para tiempo de \
    espera de categorización, tiempo de espera para atención médica, duración de la \
    atención médica, tiempo de espera para definición del paciente (desde su admisión \
    hasta la definición médica, tiempo de espera para el cierre administrativo y \
    tiempo total en la unidad de emergacia'

    ######    complilación de todo lo trabajado
    imagen_inicio    = '\\begin{figure}[H] \n \
                    \centering \n \
                    \includegraphics[scale=0.55]{'
    imagen_medio     = '}   \n  \caption{ '
    imagen_en_si     = '.' + imagen_exportar
    imagen_caption = caption
    imagen_fin       = '} \n \label{etiqueta_por_definir} \n \
                 \end{figure}  \n'
    imagen_lista     = str(
                            imagen_inicio + imagen_en_si +
                            imagen_medio +
                            imagen_caption + imagen_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(imagen_lista, '\n', file=open(str(exportar), 'a'))
    #print(open(str(exportar)).read())

#############################################################
#############################################################
#############################################################
#############################################################


    nombre_en_clave = 'cumplimiento_atencion_tiempos'
    imagen_exportar = archivo_exportar + 'imagen_' + hosp + nombre_en_clave    
    docs = dum_segs
    total ={}
    for x in ['Triage 1', 'Triage 2', 'Triage 3', 'Triage 4', 'Triage 5']:
        doc = docs.loc[docs.Triage == x]
        DT_EsperaMD = {}
        for n in range(5,160,5):
            DT_EsperaMD[str(n)] = (doc.DT_EsperaMD>n).value_counts(normalize=True)[0]*100
        print(x)
        total[x] = DT_EsperaMD

    #total
    cumlimiento = pd.DataFrame.from_dict(total)
    
    dum = cumlimiento.reset_index()#.set_index('index')
    dum['index'] = dum['index'].astype(str).astype(int)
    dum = dum.set_index('index')
    dum.sort_index().plot(figsize= (8,6))
    plt.xlabel('Tiempo en minutos')
    plt.ylabel('% pacientes atendidos')
    plt.title('Porcentaje de pacientes atendidos antes de \n distintos tiempos')
    plt.savefig(imagen_exportar, dpi=100)
    plt.show()
    plt.clf()

    caption          = 'Grafico que muestra la cantidad de pacientes atendidos \
    antes de distintos tiempos en '.format(
        infohospitales[hosp]['Nombre']
        )

    ######    complilación de todo lo trabajado
    imagen_inicio    = '\\begin{figure}[H] \n \
                    \centering \n \
                    \includegraphics[scale=0.55]{'
    imagen_medio     = '}   \n  \caption{ '
    imagen_en_si     = '.' + imagen_exportar
    imagen_caption = caption
    imagen_fin       = '} \n \label{etiqueta_por_definir} \n \
                 \end{figure}  \n'
    imagen_lista     = str(
                            imagen_inicio + imagen_en_si +
                            imagen_medio +
                            imagen_caption + imagen_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(imagen_lista, '\n', file=open(str(exportar), 'a'))

#############################################################
#############################################################
#############################################################
#############################################################

    docs = dum_segs
    total ={}
    for x in ['Triage 1', 'Triage 2', 'Triage 3', 'Triage 4', 'Triage 5']:
        doc = docs.loc[docs.Triage == x]
        DT_EsperaMD = {}
        for n in range(5,160,5):
            DT_EsperaMD[str(n)] = (doc.DT_EsperaMD>n).value_counts(normalize=True)[0]*100
        print(x)
        total[x] = DT_EsperaMD

    #total
    cumlimiento = pd.DataFrame.from_dict(total)
    
    dum = cumlimiento.reset_index()#.set_index('index')
    dum['index'] = dum['index'].astype(str).astype(int)
    dum = dum.set_index('index')

    tabla           = round(dum.sort_index(), 3)
    tabla_caption   = 'Tasa de cumplimiento de atención de pacientes para distintos \
    valores de tiempo según categorizaci de urgencia en el {} entre el {} y el {}.'.format(
        infohospitales[hosp]['Nombre'],
        BD.TS_ingreso.describe()[4],
        BD.TS_ingreso.describe()[5]
      )

    ######    complilación de todo lo trabajado

    tabla_inicio    = '\\begin{table}[H] \n  \centering \n  \n'
    tabla_medio     = '  \n\caption{ '         # ojo que acá escalé la tabla
    tabla_fin       = '}   \n \end{table} \n'
    tabla_en_si     = tabla.to_latex(bold_rows=True,
                                     column_format='lccccccccccccccccccccccc')    # no olvidar cantidad de cols
    tabla_lista     = str(
                            tabla_inicio + tabla_en_si +
                            tabla_medio + tabla_caption +
                            tabla_fin)

    #guardo el objeto (lo apendo a el archivo)
    print(tabla_lista, '\n', file=open(str(exportar), 'a'))


