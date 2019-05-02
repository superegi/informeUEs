
for hosp in BD_infohosp.index:
    print(hosp)
    hosp_en_curso = BD.loc[BD.Establecimiento == infohospitales[hosp]['Nombre']]

    
    edad = hosp_en_curso[data_paciente]['Edad']
    sexo = hosp_en_curso[data_paciente]['Sexo_x']#.value_counts()
    prevision = hosp_en_curso[data_paciente]['Prevision']
    atencionesanteriores = hosp_en_curso[data_paciente]['NumeroAtencionesAnteriores']

    tab_edad = pd.cut(edad,
                      [0, 5,15, 35, 65, 10000],
                      labels = ['0-4.', '5-14.', '15-34.', '35-64.', '>65'], 
                      right = False
                     ).value_counts(sort=False)
    tab_atencionesanteriores = pd.cut(atencionesanteriores,
           [0, 1,2,5,10, 10000],
          labels = ['1', '2', '3-5', '6-10', '>11'],
          ).value_counts(sort=False)
    
    
    #edad.describe()[5]
    #edad.describe()
    #sexo.value_counts()
    #prevision.value_counts().head()
    #atencionesanteriores.describe()
    
    #tab_atencionesanteriores.plot(kind='bar')
    #atencionesanteriores.hist()
    
    edad.hist()
    plt.title(
        str('Histograma de edad de los pacientes atendidos \n en el '+ infohospitales[hosp]['Nombre']
           ) )
    plt.xlabel('Edad')
    plt.ylabel('Cantidad de atenciones')
    plt.savefig(
        str(archivo_exportar+'imagen_'+hosp)
        , dpi=140) 
    plt.clf()
    
    #print( '---------------------------------- \n-----------------------------------')
    print('Se registraron {} atenciones en el periodo estudiado.'.format(
      hosp_en_curso.Nombre.count()
      ),
      'Dentro de las atenciones analizadas para el {}, hubo {} pacientes con su primera consulta, \
     {} en su segunda consulta, {} de 3 a 5 consultas, {} de 6 a 10 consultas y {} \
      mayor a 11 consultas.'.format(
        infohospitales[hosp]['Nombre'],
        str(str(tab_atencionesanteriores['1']) +               # 1ra atencion
            ' (' +
            str(round((tab_atencionesanteriores['1'])/tab_atencionesanteriores.sum(), 4)*100) +
           '%)'),
        str(str(tab_atencionesanteriores['2']) +               # 2da atencion
            ' (' +
            str(round((tab_atencionesanteriores['2'])/tab_atencionesanteriores.sum(), 4)*100) +
           '%)'),
        str(str(tab_atencionesanteriores['3-5']) +               # 3-5 atencion
            ' (' +
            str(round((tab_atencionesanteriores['3-5'])/tab_atencionesanteriores.sum(), 4)*100) +
           '%)'),
        str(str(tab_atencionesanteriores['6-10']) +               # 6-10 atencion
            ' (' +
            str(round((tab_atencionesanteriores['6-10'])/tab_atencionesanteriores.sum(), 4)*100) +
           '%)'),
        str(str(tab_atencionesanteriores['>11']) +               # >11 atencion
            ' (' +
            str(round((tab_atencionesanteriores['>11'])/tab_atencionesanteriores.sum(), 4)*100) +
           '%)'),
        ),
          '\n'*2,
          'Los pacientes con 3 o más atenciones fueron {} mujeres con una mediana de {} años y RIC \
           de {} a {}.'.format(
              str(
                  str(
                      hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Sexo_x.value_counts()['Mujer']) +     # mujeres >2 consultas
                  ' (' +
                  str(
                      round(
                          (hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Sexo_x.value_counts()['Mujer']
                          )/hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Sexo_x.value_counts().sum(), 2)*100) +
                  '%)'),
              hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Edad.describe()[5],
              hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Edad.describe()[4],
              hosp_en_curso.loc[hosp_en_curso['NumeroAtencionesAnteriores']>2
                                       ].Edad.describe()[6]
          ),

          '\n'*2,
          
          'Dentro de los pacientes analizados, el {} presentó una mediana de edad de {} años con un \
          RIC de {} a {}. Las atenciones menores a 15 años fueron {} , las mayores a 15 años {}. \
          La distribución por edad se puede ver en el gráfico adjunto.'.format(
        infohospitales[hosp]['Nombre'],
        edad.describe()[5],
        edad.describe()[4],
        edad.describe()[6],
        str(str(tab_edad['0-4.'] + tab_edad['5-14.']) +               # atenciones MENORES a 15a
            ' (' +
            str(round((tab_edad['0-4.'] +tab_edad['5-14.'])/tab_edad.sum(), 2)*100) +
           '%)'),
        str(str(tab_edad[['15-34.', '35-64.', '>65']].sum()) +               # atenciones MAYORES a 15a
            ' (' +
            str(round((tab_edad[['15-34.', '35-64.', '>65']].sum())/tab_edad.sum(), 2)*100) +
           '%)')
          ),
          
          '\n'*2,
          
          'Se encontró {} mujeres y {} hombres. '.format(
              str(str(sexo.value_counts()['Mujer']) +               # mujeres
                  ' (' +
                  str(round((sexo.value_counts()['Mujer'])/sexo.value_counts().sum(), 2)*100) +
                  '%)'),
              str(str(sexo.value_counts()['Hombre']) +               # hombres
                  ' (' +
                  str(round((sexo.value_counts()['Hombre'])/sexo.value_counts().sum(), 2)*100) +
                  '%)'),
              
          ),
          '\n'*2
         , file = open(str(archivo_exportar + 'texto_'+ hosp + '.txt'), 'w'), sep=''
         )
    #print( '---------------------------------- \n------------------------------------\n')
    
    print('Histograma de edad de los pacientes atendidos en el {} entre el {} y el {}'.format(
          infohospitales[hosp]['Nombre'],
          dt.datetime.strftime(tiempo['inicio'], '%d-%m-%Y'),
          dt.datetime.strftime(tiempo['fin'], '%d-%m-%Y'),
          ),
      file = open(str(archivo_exportar + 'ima_caption_'+ hosp + '.caption'), 'w'),
      sep='')
print('-------------------------- \n   \
  ARCHIVOS:  ')

print(str(archivo_exportar + 'texto_'+ hosp + '.txt'))
print(str(archivo_exportar + 'ima_caption_'+ hosp + '.caption'))
print('Resultado: (por hospital): \n', 
  'grafico con histograma de edad \n \
  analisis del n de consultas con n y %\n \
  metricas de edad y división >y< a 15a\n \
  distribución por sexo')


