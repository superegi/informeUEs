
# ruta             = './resultados/01SS/'
# Nombre_archivo   =  '1SS_01PAC_01'

# carpeta_script   ='./script_resultados/'
# nombre_script    = '01SS_01descripcion_01.py'

# archivo_exportar = ruta + Nombre_archivo               
# ruta_script      = carpeta_script + nombre_script
# ruta_script
# #exec(open(ruta_script).read())

exportar = archivo_exportar + 'texto' + '.txt'
print('', file=open(str(exportar), 'w'))
print(str('texto_' + hosp + '.txt'))

#######
####### objeto
######
texto      = 'Se analizó desde el {} al {}, lo que corresponde {} días.'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5],
  tiempo['diferencia'].days
  )
print(texto, '\n', file=open(str(exportar), 'a'))

####### FIN objeto

#######
####### objeto
######
texto      = 'La población analizada fue la correspondiente al Servicio de Salud Viña \
del Mar Quillota, que según el censo del INE del año 2017 por comuna fue de {} \
personas. La cantidad de atenciones, la población asignada y la cantidad de \
atenciones por 100000 habitantes se encuentra en la tabla adjunta.'.format(
  BD_infohosp.Poblacion.sum()
  )
print(texto, '\n', file=open(str(exportar), 'a'))

####### FIN objeto


dum1 = BD.groupby('Establecimiento')[['TS_ingreso']].count().sort_values('TS_ingreso')
dum2= BD_infohosp[['Nombre','Poblacion']]

dum3 = pd.merge(dum1,dum2, how='right', left_on=['Establecimiento'], right_on=['Nombre'])
dum3['atx100Kh'] = dum3['TS_ingreso']/dum3['Poblacion'] *100.000
dum3.columns = ['Atenciones','Hospital',  'Poblacion', 'Atenciones por 10000 habitantes']
dum3 = dum3.set_index('Hospital')


#########   OBJETO 1
#########
#########    acá creo la tabla que requiero mostrar, 
#########    debe terminar con nombre 'tabla'

tabla           = dum3
tabla_caption   = 'Atenciones en unidades de urgencia de los hospitales del SSVQ \
entre el {} y {}. Se muestra también la población asignada y las atenciones por \
100000 habitantes.'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5]
  )

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





###########
###########
#########

imagen_nombre   = 'atenxsemana'
imagen_exportar = archivo_exportar + 'imagen' + imagen_nombre
BD.groupby([ BD.TS_ingreso.dt.to_period('W'),'Establecimiento'])['TS_ingreso'].count().unstack().plot(figsize=(9,8))

plt.title('Cantidad de atenciones por semana del año' )
plt.xlabel('Semana del año')
plt.savefig(imagen_exportar, dpi=85)
plt.show()
plt.clf()

caption = 'Atenciones en unidades de urgencia de los hospitales del SSVQ entre el {} y {}. Se \
 muestran los hospitales del SSVQ y la distribución a lo largo de las\
 semanas del año'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5])


imagen    = str(
                '\\begin{figure}[H] \n \
                \centering \n \
                \includegraphics[scale=0.55]{' + str('.' + imagen_exportar +'.png') + '} \n \
                \caption{' + caption +'} \n \
                \label{etiqueta_por_definir} \n \
                \end{figure}')
print(imagen, '\n', file=open(str(exportar), 'a'))

#########################
########################

imagen_nombre = 'atenxhora'
imagen_exportar = archivo_exportar + 'imagen' + imagen_nombre
BD.groupby([ BD.TS_ingreso.dt.hour, 'Establecimiento'])['TS_ingreso'].count().unstack().plot(figsize=(9,8))

plt.title('Cantidad de atenciones por hora del día' )
plt.xlabel('Hora del día')
plt.savefig(imagen_exportar, dpi=85)
plt.show()
plt.clf()
caption = 'Atenciones en unidades de urgencia de los hospitales del SSVQ entre el {} y {}. Se \
 muestran los hospitales del SSVQ y la distribución a lo largo de las\
 horas del día'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5])


imagen    = str(
                '\\begin{figure}[H] \n \
                \centering \n \
                \includegraphics[scale=0.55]{' + str('.' + imagen_exportar +'.png') + '} \n \
                \caption{' + caption +'} \n \
                \label{etiqueta_por_definir} \n \
                \end{figure}')
print(imagen, '\n', file=open(str(exportar), 'a'))


# #########################
# ########################

imagen_nombre = 'atensemanal'
imagen_exportar = archivo_exportar + 'imagen' + imagen_nombre

dia_semana = pd.Categorical(BD.TS_ingreso.dt.weekday_name, ordered=True)
dia_semana = dia_semana.reorder_categories(['Monday','Tuesday', 'Wednesday',
  'Thursday','Friday', 'Saturday' ,'Sunday' ])
dia_semana = dia_semana.rename_categories(
    ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernres', 'Sábado', 'Domingo'])


BD.groupby([dia_semana, 'Establecimiento'])['TS_ingreso'].count().unstack().plot(
  #kind = 'barh',
  figsize=(9,6))
plt.title('Cantidad de atenciones por día de la semana' )
plt.xlabel('Día de la semana')
plt.xticks(np.arange(7),dia_semana.categories.values)
plt.savefig(imagen_exportar, dpi=85)
plt.show()
plt.clf()

caption = 'Atenciones en unidades de urgencia de los hospitales del SSVQ entre el {} y {}. Se \
 muestran los hospitales del SSVQ y la distribución a lo largo de los \
 días de la semana'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5])


imagen    = str(
                '\\begin{figure}[H] \n \
                \centering \n \
                \includegraphics[scale=0.55]{' + str('.' + imagen_exportar +'.png') + '} \n \
                \caption{' + caption +'} \n \
                \label{etiqueta_por_definir} \n \
                \end{figure}')
print(imagen, '\n', file=open(str(exportar), 'a'))


# #########################
# ########################

imagen_nombre = 'atenxtriagexmes'
imagen_exportar = archivo_exportar + 'imagen' + imagen_nombre
mes = pd.Categorical(BD['TS_ingreso'].dt.strftime('%b'), ordered=True)#, dtype="category")
mes = mes.reorder_categories(['ene', 'feb', 'mar', 'abr', 'may', 
                       'jun', 'jul', 'ago', 'sep', 'oct',
                       'nov', 'dic'])
mensual = BD.groupby([mes, 'Triage']).Triage.count()
mensual.unstack().plot(kind='bar', figsize= (10,5), width=1)
plt.ylabel('Cantidad de atenciones')
plt.title('Cantidad de pacientes atendidos según su categorización \n \
por mes')
plt.savefig(imagen_exportar, dpi=85)
plt.show()
plt.clf()

caption = 'Atenciones en unidades de urgencia de los hospitales del SSVQ entre el {} y {}. Se \
 muestra la cantidad de atenciones, meses del año y categorización de urgencia'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5])


imagen    = str(
                '\\begin{figure}[H] \n \
                \centering \n \
                \includegraphics[scale=0.55]{' + str('.' + imagen_exportar +'.png') + '} \n \
                \caption{' + caption +'} \n \
                \label{etiqueta_por_definir} \n \
                \end{figure}')
print(imagen, '\n', file=open(str(exportar), 'a'))





#########   OBJETO 1
#########
#########    acá creo la tabla que requiero mostrar, 
#########    debe terminar con nombre 'tabla'

dum = BD.copy()
dum[DTs]   = dum[DTs].applymap(lambda s: s.total_seconds()/60)
dom = dum[DTs].describe()[['DT_EsperaCategorizacion', 'DT_EsperaMD', 'DT_AtencionMD',
       'DT_definicionPAC', 'DT_Espera_CierreAdm', 'DT_Total']].T[['mean','25%','50%','75%'  ]]
dom.columns = ['Promedio' , 'p25',  'p50' , 'p75']
dom = dom.T
dom.index.names = ['Hora ingreso']
dom.columns = ['TE Categorización', 'TE Atención médica', 'Duración Atención médica',
                'TE definición', 'TE Cierre adminisitrativo', 'TE Total en urgencias']

tabla           = dom.T
tabla_caption   = 'Tiempos de espera en unidades de urgencia de los hospitales del SSVQ \
entre el {} y {}. Los valores están expresados en minutos.'.format(
  BD.TS_ingreso.describe()[4],
  BD.TS_ingreso.describe()[5]
  )

######    complilación de todo lo trabajado

tabla_inicio    = '\\begin{table}[H] \n  \centering \n'
tabla_medio     = '\caption{ '
tabla_fin       = '}   \n \end{table} \n'
tabla_en_si     = tabla.to_latex(bold_rows=True,
                                 column_format='lcccc')    # no olvidar cantidad de cols
tabla_lista     = str(
                        tabla_inicio + tabla_en_si +
                        tabla_medio + tabla_caption +
                        tabla_fin)

#guardo el objeto (lo apendo a el archivo)
print(tabla_lista, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 1    #######


###############################
############ SUPER TABLA CON METRICAS DE TIEMPOS
###########################

# dum        = BD.copy()
# dum[DTs]   = dum[DTs].applymap(lambda s: s.total_seconds()/60)

dom1       = dum[DTs].groupby([dum.TS_ingreso.dt.hour])
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
tabla_caption   = 'Tiempos de espera en el SS \
entre el {} y {}. Los valores están expresados en minutos.'.format(
    BD.TS_ingreso.describe()[4],
    BD.TS_ingreso.describe()[5]
  )

######    complilación de todo lo trabajado

tabla_inicio    = '\\begin{table}[H] \n  \centering \n \\resizebox{\\textwidth}{!}{'
tabla_medio     = '} \caption{ '
tabla_fin       = '}   \n \end{table} \n'
tabla_en_si     = tabla.to_latex(bold_rows=True,
                                 column_format='lcccccccccccccccccccccc')    # no olvidar cantidad de cols
tabla_lista     = str(
                        tabla_inicio + tabla_en_si +
                        tabla_medio + tabla_caption +
                        tabla_fin)

#guardo el objeto (lo apendo a el archivo)
print(tabla_lista, '\n', file=open(str(exportar), 'a'))