
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
    print('', file=open(str(exportar), 'w'))
    print(str('texto_' + hosp + '.txt'))

    dum = tab_frec(hosp_en_curso.ClasificacionConsulta)


    #########
    #########   OBJETO 1
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = 'Los pacientes que consultaron, acudían al servicio de urgencia por \
    atención médica en {} ({}%) casos, por atención ginecológica en {} ({}%) casos y por \
    atención por matrona en {} ({}%) casos.'.format(
        dum['n']['ATENCION MEDICA NIÑO Y ADULTO'],
        round(dum['%']['ATENCION MEDICA NIÑO Y ADULTO'], 4),
        dum['n']['ATENCION MEDICA GINECO-OBSTETRA'],
        round(dum['%']['ATENCION MEDICA GINECO-OBSTETRA'], 4),
        dum['n']['ATENCION POR MATRONA'],
        round(dum['%']['ATENCION POR MATRONA'], 4)
        )

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 1    #######

    dum = tab_frec(hosp_en_curso.Arribo_paciente)

    #########
    #########   OBJETO 2
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = 'De los pacientes anlizados, {} ({}%) llegaron a la unidad de \
    emergencias por sus medios, {} ({}%) traidos por una ambulancia, {} ({}%) por \
    personal policial.'.format(
        dum['n']['Espontáneo'],
        round(dum['%']['Espontáneo'], 4),
        dum['n']['Ambulancia'],
        round(dum['%']['Ambulancia'], 4),
        dum['n']['Policia'],
        round(dum['%']['Policia'], 4)
        )

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 2    #######

    dum = tab_frec(hosp_en_curso.LlegadaSAMU)

    #########
    #########   OBJETO 3
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = 'Cuando los pacientes llegaron en ambulancia pública , \
    {} ({}%) de ellos lo hicieron en una básica, {} ({}%)  en una avanzada. \
    '.format(
        dum['n']['SAMU Básica M1'],
        round(dum['%']['SAMU Básica M1'], 4),
        dum['n']['SAMU Avanzada M2'],
        round(dum['%']['SAMU Avanzada M2'], 4)
        )
        

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 3    #######

    dum = tab_frec(hosp_en_curso.Origen_paciente)

    #########
    #########   OBJETO 4
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = 'El origen desde donde consultan los pacientes fue desde \
    su domicilio en {} ({}%) casos, referido de un centro público en {} ({}%) \
    casos.'.format(
        dum['n']['Origen Espontáneo'],
        round(dum['%']['Origen Espontáneo'], 4),
        dum['n']['Referido centro público'],
        round(dum['%']['Referido centro público'], 4),
        dum['n']['Otro origen'],
        round(dum['%']['Otro origen'], 4)
        )
        

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 4    #######

    dum = tab_frec(hosp_en_curso.AtInterrumpidaPor)
    dum1 = hosp_en_curso.AtInterrumpidaPor.value_counts(dropna=False)
    num = list(hosp_en_curso.AtInterrumpidaPor.value_counts(dropna=False)[[0]])[0]
    num


    #########
    #########   OBJETO 4
    #########
    #########    acá creo la tabla que requiero mostrar, 
    #########    debe terminar con nombre 'tabla'

    texto           = 'De los pacientes admitidos en la unidad de emergencia, \
    {} ({}%) completaron su proceso de atención correctamente. Aquellos pacientes \
    que no completaron su atención, fueron clasificados en {} ({}%) casos \
    por Administrativo y/o fuga del paciente, \
    en {} ({}%) casos por Paciente se Retira Bajo su Propio Riesgo.'.format(
        float(dum1[[0]]),
        round( float(
            dum1[[0]]) /  float(dum1.sum()
                               ), 3)*100,
        dum['n']['Administrativo y/o fuga del paciente'],
        round(dum['%']['Administrativo y/o fuga del paciente'], 4),
        dum['n']['Paciente se Retira Bajo su Propio Riesgo'],
        round(dum['%']['Paciente se Retira Bajo su Propio Riesgo'], 4)
        )

    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 4    #######

    #########
    #########   OBJETO 5
    #########

    texto           = 'Hubo {} ({}%) pancientes que fallecieron en la unidad de \
    emergencias. '.format(
        hosp_en_curso.CondicionAlCierre.value_counts()[1],
        round(hosp_en_curso.CondicionAlCierre.value_counts()[1]/
        hosp_en_curso.CondicionAlCierre.value_counts().sum(),4)
)


    #guardo el objeto (lo apendo a el archivo)
    print(texto, '\n', file=open(str(exportar), 'a'))

    #########   FIN OBJETO 5    #######
