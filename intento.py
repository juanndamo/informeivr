import numpy as np
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
from PIL import Image



def transformacion(sql,sql2,conexion, fechainicio, fechafin, combo):
	#CONVERTIR EL MYSQL A UN DATAFRAME
	df = pd.read_sql_query(sql, conexion)


	df2=pd.DataFrame(df)
	if combo=="MP Validacion Productos":

		df2 = df2[~df2['detail'].str.contains('MenuUsuario60Anos', case=False)]
		df2 = df2[~df2['detail'].str.contains('MenuOpcionesNoUsuarioMP3', case=False)]
	    

	#DELIMITAR COLUMNAS POR EL SEPARADOR DE |
	df2['detail'] = df2['detail'].str.split('|')

	#SEPARARLOS POR FILAS
	df2 = df2.explode('detail')

	#REINICIAR EL INDICE
	df2.reset_index(drop=True, inplace=True)
	


	 
	 #LIMPIAR LA DATA, EXTRAE TODO LO QUE ESTE ANTES DE LA , O DE /
	df2['detail'] = df2['detail'].str.split(',|/').str[0]

	if combo=="Coomeva-CAC":

		df464 = pd.read_sql_query(sql2, conexion)
		dfn464=pd.DataFrame(df464)
		#FILTRAR UNICAMIENTE LO QUE TENGA PREOC_1 QUE ES COOMEVA
		dfn464=dfn464[dfn464.detail.str.contains('Opcion1_CAC',case=False)]

		#DELIMITAR COLUMNAS POR EL SEPARADOR DE |
		dfn464['detail'] = dfn464['detail'].str.split('|')

		#SEPARARLOS POR FILAS
		dfn464 = dfn464.explode('detail')

		#REINICIAR EL INDICE
		dfn464.reset_index(drop=True, inplace=True)
		dfn464['detail'] = dfn464['detail'].str.split(',|/').str[0]
		dfn464['detail'] = dfn464['detail'].str.replace('_CAC', '')
		dfn464['detail'] = dfn464['detail'].str.replace('Opcion', 'Opc_')
		df2 = pd.concat([df2, dfn464], ignore_index=True)

		#FILTRAR UNICAMIENTE LOS DATOS QUE NECESITAMOS
		df2 = df2[(df2["detail"] == "") |
		(df2["detail"] == "Menu_Principal") |
		(df2["detail"] == "ColgarAsociadoCoomeva") | 
		(df2["detail"] == "ColgarEnvioExtracto") | 
		(df2["detail"] == "ColgarEstadoCuenta") | 
		(df2["detail"] == "ColgarIVROperativoPiloto") | 
		(df2["detail"] == "Colgar_Lealtad" )| 
		(df2["detail"] == "IAX2") | 
		(df2["detail"] == "IVR_OPERATIVO_PILOTO") | 
		(df2["detail"] == "Opc_1") | 
		(df2["detail"] == "Opc_1_0") | 
		(df2["detail"] == "Opc_1_1" )| 
		(df2["detail"] == "Opc_1_2") | 
		(df2["detail"] == "Opc_1_2_1") | 
		(df2["detail"] == "Opc_1_2_2") | 
		(df2["detail"] == "Opc_1_2_3") | 
		(df2["detail"] == "Opc_1_2_4") | 
		(df2["detail"] == "Opc_1_2_5" )| 
		(df2["detail"] == "Opc_1_2_6") | 
		(df2["detail"] == "Opc_1_3") |
		(df2["detail"] == "Opc_1_4") | 
		(df2["detail"] == "Opc_1_5") | 
		(df2["detail"] == "Opc_1_6") | 
		(df2["detail"] == "Opc_1_6_1") | 
		(df2["detail"] == "Opc_1_6_2") | 
		(df2["detail"] == "Opc_1_6_3" )| 
		(df2["detail"] == "Opc_1_6_4") | 
		(df2["detail"] == "Opc_1_7") |
		( df2["detail"] == "Opc_1_8") |
		(df2["detail"] == "rvGentePila")]

	elif combo=="MP Validacion Productos":
		print("entra")
		df2['detail'] = df2['detail'].str.replace('MI', '')
		df2['detail'] = df2['detail'].str.replace('MISO', '')
		df2['detail'] = df2['detail'].str.replace('SO', '')
		df2['detail'] = df2['detail'].str.replace('Fact', '')

		df2 = df2[(df2["detail"] == "") |
            (df2["detail"] == "ColgarMP3") |
            (df2["detail"] == "IAX2") |
            (df2["detail"] == "IVR_Medicina_Prepagada_V3") |
            (df2["detail"] == "MenuOpcion2MP3") |
            (df2["detail"] == "Opcion3MP3") |
            (df2["detail"] == "Opcion4MP3") |
            (df2["detail"] == "MenuOpcion5MP3") |
            (df2["detail"] == "Opcion6MP3") |
            (df2["detail"] == "ConsultaMedicaMP3") |
            (df2["detail"] == "OrientacionMedicaMP3") |
            (df2["detail"] == "OrientacionClinicaMP3") |
            (df2["detail"] == "MenuAsignarCitaMP") |
            (df2["detail"] == "ConsultarCitaMP") |
            (df2["detail"] == "Opcion5_1MP3") |
            (df2["detail"] == "Opcion5_2MP3") |
            (df2["detail"] == "Opcion5_3MP3") |
            (df2["detail"] == "Opcion5_4MP3") |
            (df2["detail"] == "Opcion1_SubmenuTradicionalMP3") |
            (df2["detail"] == "Opcion2_SubmenuTradicionalMP3") |
            (df2["detail"] == "Opcion3_uracionMP3") |
            (df2["detail"] == "Opcion1_uracionMP3") |
            (df2["detail"] == "GenerarCertificadoAfiliacion") |
            (df2["detail"] == "GenerarCertificadoRetefuente") |
            (df2["detail"] == "MenuOpcion1MP3") |
            (df2["detail"] == "MenuOpcionesMP3") 
            ]

	else:
		df2 = df2[(df2["detail"] == "")|
	    (df2["detail"] == "Menu_Principal_SyS")|
	    (df2["detail"] == "ColgarAsociadoCoomeva")|
	    (df2["detail"] == "ColgarIVROperativoPiloto")|
	    (df2["detail"] == "ColgarSyS")|
	    (df2["detail"] == "IAX2")|
	    (df2["detail"] == "Opcion1_SyS")|
	    (df2["detail"] == "Opcion2_SyS")|
	    (df2["detail"] == "Opcion3_1_SyS")|
	    (df2["detail"] == "Opcion3_2_SyS")|
	    (df2["detail"] == "Opcion4_SyS")|
	    (df2["detail"] == "Opcion6_SyS")|
	    (df2["detail"] == "MenuOpcion3_SyS")]


	#REEMPLAZAR TODO LO QUE SEA COLGAR POR EFECTIVO
	df2['detail'] = df2['detail'].str.replace('Colgar.*', 'Efectvo', regex=True)

	#REEMPLAZAR TODO LO QUE SEA AGENTE POR EFECTIVO
	df2['detail'] = df2['detail'].str.replace('IAX2', 'Efectvo')

	if combo=="Coomeva-CAC":

		df2['detail'] = df2['detail'].str.replace('Menu_Principal', 'IVR_OPERATIVO_PILOTO')


	#REINICIAR EL INDICE
	df2 = df2.reset_index(drop=True)

	#AGREGAR UNA COLUMNA CON EL ELEMENTO DE LA FILA SIGUIENTE DE LA COLUMNA DETAIL
	df2['Destino'] = df2['detail'].shift(-1)

	#REEMPLAZAR EL VACIO POR FIN
	df2['Destino'] = df2['Destino'].replace("", 'Fin')

	#FILTRAR TODO LO QUE EN DETAIL SEA DIFERENTE A ""
	df2 = df2[(df2["detail"] != "")]

	 

	Nuevo="Cuelga"

	#REINICIAR EL INDICE
	df2 = df2.reset_index(drop=True)

	df_sin_duplicados = df2.drop_duplicates(subset='idTracking', keep='last')

	df_sin_duplicados['detail'] = np.where(df_sin_duplicados['detail'] != 'Efectvo', Nuevo, df_sin_duplicados['detail'])

	df2 = df2.merge(df_sin_duplicados, on='idTracking', how='inner')

	columnas = ['idTracking', 'idServer_x', 'uniqueId_x', 'phone_x', 'toService_x', 'start_x', 'end_x', 'detail_x','Destino_x','detail_y']

	df2 = df2[columnas]
	df2["valor"]=1

	def valores_iguales(row):
	    if row['detail_x'] == row['Destino_x']:
	        return True
	    else:
	        return False

	df2['Valores_Iguales'] = df2.apply(valores_iguales, axis=1)


	df2 = df2[(df2["Valores_Iguales"] == False)]


	agrupado = df2.groupby(['detail_x', 'Destino_x',"detail_y"]).size().reset_index(name='Recuento')




	if combo=="Coomeva-CAC":
		xls=pd.ExcelFile('tipologia.xlsx')
		df=pd.read_excel(io=xls, sheet_name="Hoja1")
		df2=pd.DataFrame(df)

	elif combo=="MP Validacion Productos":
		xls=pd.ExcelFile('tipologia.xlsx')
		df=pd.read_excel(io=xls, sheet_name="Hoja3")
		df2=pd.DataFrame(df)

	else:
		xls=pd.ExcelFile('tipologia.xlsx')
		df=pd.read_excel(io=xls, sheet_name="Hoja2")
		df2=pd.DataFrame(df)

	agrupado = pd.merge(agrupado, df2, left_on='detail_x', right_on='Tipo')
	agrupado = pd.merge(agrupado, df2, left_on='Destino_x', right_on='Tipo')

	columnas = ['detail_x', 'Destino_x', 'detail_y', 'Recuento','Numero_x', 'Numero_y']
	agrupado = agrupado[columnas]
	agrupado = agrupado[(agrupado["detail_x"] != "Efectvo")]

	if combo=="Coomeva-CAC":

		agrupado = agrupado[(agrupado['detail_x'] != 'IVR_OPERATIVO_PILOTO') | (agrupado['Destino_x'] != 'IVR_OPERATIVO_PILOTO')]




	figura = grafico(agrupado, fechainicio, fechafin, combo)
	print(figura)
	return figura
def grafico(agrupado, fechainicio, fechafin, combo):

	if combo=="Coomeva-CAC":



		coomeva = (agrupado['Numero_y'] == 2) & (agrupado['Numero_x'] == 1)
		coomeva1 = (agrupado['Numero_y'] == 24) & (agrupado['Numero_x'] == 1)
		coomeva2 = (agrupado['Numero_y'] == 23) & (agrupado['Numero_x'] == 1)
		coomeva3 = (agrupado['Numero_y'] == 1) & (agrupado['Numero_x'] == 2)

		coomeva464 = (agrupado['Numero_y'] == 2) & (agrupado['Numero_x'] == 0)
		coomeva1464 = (agrupado['Numero_y'] == 24) & (agrupado['Numero_x'] == 0)
		coomeva2464 = (agrupado['Numero_y'] == 23) & (agrupado['Numero_x'] == 0)
		coomeva3464 = (agrupado['Numero_y'] == 0) & (agrupado['Numero_x'] == 2)


		efectivo = agrupado['Numero_y'] == 23
		abandona = agrupado['Numero_y'] == 24
		opc111 = agrupado['Numero_y'] == 2
		devuelvoivr=(agrupado['Numero_y'] == 1) & (agrupado['Numero_x'] == 12)


		d10=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 3)
		d11=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 4)
		d12=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 5)
		d13=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 6)
		d14=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 7)
		d15=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 8)
		d16=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 9)
		d17=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 10)
		d18=(agrupado['Numero_x'] == 2) &(agrupado['Numero_y'] == 11)

		d61=(agrupado['Numero_x'] == 9) &(agrupado['Numero_y'] == 2)
		d21=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 2)
		d51=(agrupado['Numero_x'] == 8) &(agrupado['Numero_y'] == 2)

		
		d6_1=(agrupado['Numero_x'] == 9) &(agrupado['Numero_y'] == 18)
		d6_2=(agrupado['Numero_x'] == 9) &(agrupado['Numero_y'] == 19)
		d6_3=(agrupado['Numero_x'] == 9) &(agrupado['Numero_y'] == 20)
		d6_4=(agrupado['Numero_x'] == 9) &(agrupado['Numero_y'] == 21)
		
		d2_1=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 12)
		d2_2=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 13)
		d2_3=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 14)
		d2_4=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 15)
		d2_5=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 16)
		d2_6=(agrupado['Numero_x'] == 5) &(agrupado['Numero_y'] == 17)

		d5_gp=(agrupado['Numero_x'] == 8) &(agrupado['Numero_y'] == 22)



		total464 = agrupado.loc[coomeva464, 'Recuento'].sum()+agrupado.loc[coomeva1464, 'Recuento'].sum()+agrupado.loc[coomeva2464, 'Recuento'].sum()-agrupado.loc[coomeva3464, 'Recuento'].sum()
		total = agrupado.loc[coomeva, 'Recuento'].sum()+agrupado.loc[coomeva1, 'Recuento'].sum()+agrupado.loc[coomeva2, 'Recuento'].sum()-agrupado.loc[coomeva3, 'Recuento'].sum()
		totalefe = agrupado.loc[efectivo, 'Recuento'].sum()
		totalaba = agrupado.loc[abandona, 'Recuento'].sum()
		totalopc1 = agrupado.loc[opc111, 'Recuento'].sum()

		totalcoomeva=total464+total

		print(totalcoomeva)
		print(total464)
		print(total)
		print(totalopc1)

		totalopc1_1=agrupado.loc[d11, 'Recuento'].sum()
		totalopc1_2=agrupado.loc[d12, 'Recuento'].sum()
		totalopc1_3=agrupado.loc[d13, 'Recuento'].sum()
		totalopc1_4=agrupado.loc[d14, 'Recuento'].sum()
		totalopc1_5=agrupado.loc[d15, 'Recuento'].sum()
		totalopc1_6=agrupado.loc[d16, 'Recuento'].sum()
		totalopc1_7=agrupado.loc[d17, 'Recuento'].sum()
		totalopc1_8=agrupado.loc[d18, 'Recuento'].sum()
		totalopc1_0=agrupado.loc[d10, 'Recuento'].sum()
		total1i=agrupado.loc[coomeva3, 'Recuento'].sum()
		print(totalopc1_8)

		totalopc1_6_d=agrupado.loc[d16, 'Recuento'].sum()-agrupado.loc[d61, 'Recuento'].sum()
		totalopc1_2_d=agrupado.loc[d12,'Recuento'].sum()-agrupado.loc[d21, 'Recuento'].sum()
		totalopc1_5_d=agrupado.loc[d15,'Recuento'].sum()-agrupado.loc[d51, 'Recuento'].sum()


		totalopc6_1=agrupado.loc[d6_1, 'Recuento'].sum()
		totalopc6_2=agrupado.loc[d6_2, 'Recuento'].sum()
		totalopc6_3=agrupado.loc[d6_3, 'Recuento'].sum()
		totalopc6_4=agrupado.loc[d6_4, 'Recuento'].sum()

		totalopc2_1=agrupado.loc[d2_1, 'Recuento'].sum()
		totalopc2_2=agrupado.loc[d2_2, 'Recuento'].sum()
		totalopc2_3=agrupado.loc[d2_3, 'Recuento'].sum()
		totalopc2_4=agrupado.loc[d2_4, 'Recuento'].sum()
		totalopc2_5=agrupado.loc[d2_5, 'Recuento'].sum()
		totalopc2_6=agrupado.loc[d2_6, 'Recuento'].sum()

		totalopc5_gp=agrupado.loc[d5_gp, 'Recuento'].sum()

		label  =  ["",
			"Llamadas Ingresadas",
			f"Coomeva 100%",
			f"Asesor de servicios {round((totalopc1_0/totalopc1)*100,2)}%",
			f"Asociarse y referidos {round((totalopc1_1/totalopc1)*100,2)}%",
			f"Recaudo y facturacion {round((totalopc1_2/totalopc1)*100,2)}%",
			f"Educacion y gente pila {round((totalopc1_3/totalopc1)*100,2)}%",
			f"Vivienda {round((totalopc1_4/totalopc1)*100,2)}%",
			f"Revalorizacion {round((totalopc1_5/totalopc1)*100,2)}%",
			f"Otros productos {round((totalopc1_6/totalopc1)*100,2)}%",
			f"PQR's {round((totalopc1_7/totalopc1)*100,2)}%",
			f"Retirarse {round((totalopc1_8/totalopc1)*100,2)}%",
			f"Informacion general {round((totalopc2_1/totalopc1_2_d)*100,2)}%",
			f"Envio de factura {round((totalopc2_2/totalopc1_2_d)*100,2)}%",
			f"Pago con tarjeta de credito {round((totalopc2_3/totalopc1_2_d)*100,2)}%",
			f"info medios de pago {round((totalopc2_4/totalopc1_2_d)*100,2)}%",
			f"Recaudo {round((totalopc2_5/totalopc1_2_d)*100,2)}%",
			f"Reactivacion {round((totalopc2_6/totalopc1_2_d)*100,2)}%",
			f"Informacion Lealtad {round((totalopc6_1/totalopc1_6_d)*100,2)}%",
			f"Tarjeta coomeva {round((totalopc6_2/totalopc1_6_d)*100,2)}%",
			f"Credimutual {round((totalopc6_3/totalopc1_6_d)*100,2)}%",
			f"Vida plenitud {round((totalopc6_4/totalopc1_6_d)*100,2)}%",
			f"rvGentePila",
			f"Efectivo",
			f"Abandona",
			]

		tipografico="IVR COOMEVA-CAC"

		node_x_positions = [0.001,0.2,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,1,1]
		node_y_positions = [0.5,0.5,0.9,0.1,0.2,0.35,0.45,0.5,0.55,0.7,0.8,0.1,0.15,0.2,0.25,0.3,0.35,0.5,0.55,0.6,0.65,0.4,0.75,0.25]

		bar_data = go.Bar(
		    x=[0, 1, 2.4, 3.7, 5.4 ,6],
		    y=[20, 20, 20, 20, 20, 0],
		    width=0.18,
		    
		    marker=dict(color=["white","#dcdcdc","#dcdcdc","#dcdcdc","white","white"],
		    	line=dict(color="white", width=0.5))
		)

	elif combo=="MP Validacion Productos":

		mp = (agrupado['Numero_y'] == 1) & (agrupado['Numero_x'] == 0)
		mp1 = (agrupado['Numero_y'] == 23) & (agrupado['Numero_x'] == 0)
		mp2 = (agrupado['Numero_y'] == 24) & (agrupado['Numero_x'] == 0)
		mp3 = (agrupado['Numero_y'] == 23) & (agrupado['Numero_x'] == 1)
		mp4 = (agrupado['Numero_y'] == 24) & (agrupado['Numero_x'] == 1)



		mpmenuprincipal = agrupado['Numero_y'] == 1

		mpopc1 = agrupado['Numero_y'] == 2
		mpopc2 = agrupado['Numero_y'] == 3
		mpopc3 = agrupado['Numero_y'] == 4
		mpopc4 = agrupado['Numero_y'] == 5
		mpopc5 = agrupado['Numero_y'] == 6
		mpopc6 = agrupado['Numero_y'] == 7

		mpopc21 = agrupado['Numero_y'] == 8
		mpopc22 = agrupado['Numero_y'] == 9
		mpopc23 = agrupado['Numero_y'] == 10
		mpopc31 = agrupado['Numero_y'] == 11
		mpopc32 = agrupado['Numero_y'] == 12
		mpopc51 = agrupado['Numero_y'] == 13
		mpopc52 = agrupado['Numero_y'] == 14
		mpopc53 = agrupado['Numero_y'] == 15
		mpopc54 = agrupado['Numero_y'] == 16
		mpopc61 = agrupado['Numero_y'] == 17
		mpopc62 = agrupado['Numero_y'] == 18

		mpopc521 = agrupado['Numero_y'] == 19
		mpopc522 = agrupado['Numero_y'] == 20
		mpopc531 = agrupado['Numero_y'] == 21
		mpopc532 = agrupado['Numero_y'] == 22

		efectivomp = agrupado['Numero_y'] == 23
		abandonamp = agrupado['Numero_y'] == 24

		abandonoopc1=agrupado.loc[mp3, 'Recuento'].sum()
		efeopc1=agrupado.loc[mp4, 'Recuento'].sum()


		totalmp=agrupado.loc[mp, 'Recuento'].sum()+agrupado.loc[mp1, 'Recuento'].sum()+agrupado.loc[mp2, 'Recuento'].sum()
		totalmpmenuprincipal=agrupado.loc[mpmenuprincipal, 'Recuento'].sum()

		totalmpopc1=agrupado.loc[mpopc1, 'Recuento'].sum()
		totalmpopc2=agrupado.loc[mpopc2, 'Recuento'].sum()
		totalmpopc3=agrupado.loc[mpopc3, 'Recuento'].sum()
		totalmpopc4=agrupado.loc[mpopc4, 'Recuento'].sum()
		totalmpopc5=agrupado.loc[mpopc5, 'Recuento'].sum()
		totalmpopc6=agrupado.loc[mpopc6, 'Recuento'].sum()

		mpopc21=agrupado.loc[mpopc21, 'Recuento'].sum()
		mpopc22=agrupado.loc[mpopc22, 'Recuento'].sum()
		mpopc23=agrupado.loc[mpopc23, 'Recuento'].sum()
		mpopc31=agrupado.loc[mpopc31, 'Recuento'].sum()
		mpopc32=agrupado.loc[mpopc32, 'Recuento'].sum()
		mpopc51=agrupado.loc[mpopc51, 'Recuento'].sum()
		mpopc52=agrupado.loc[mpopc52, 'Recuento'].sum()
		mpopc53=agrupado.loc[mpopc53, 'Recuento'].sum()
		mpopc54=agrupado.loc[mpopc54, 'Recuento'].sum()
		mpopc61=agrupado.loc[mpopc61, 'Recuento'].sum()
		mpopc62=agrupado.loc[mpopc62, 'Recuento'].sum()

		mpopc521=agrupado.loc[mpopc521, 'Recuento'].sum()
		mpopc522=agrupado.loc[mpopc522, 'Recuento'].sum()
		mpopc531=agrupado.loc[mpopc531, 'Recuento'].sum()
		mpopc532=agrupado.loc[mpopc532, 'Recuento'].sum()


		totalabandonamp=agrupado.loc[abandonamp, 'Recuento'].sum()
		totalefectivomp=agrupado.loc[efectivomp, 'Recuento'].sum()

		totalmenu1=totalmpopc1+totalmpopc2+totalmpopc3+totalmpopc4+totalmpopc5+totalmpopc6

		total1=abandonoopc1
		total2=efeopc1

		total3=totalmpmenuprincipal

		print(totalmenu1)
		print(total1)
		print(total2)
		print(total3)


		label = [
		    "IVR_Medicina_Prepagada_V3",
		    "MenuOpciones 100%",
		    f"1. Declaracion Renta {round((totalmpopc1/totalmpmenuprincipal)*100,1)}%",
		    f"2. Orientación médica {round((totalmpopc2/totalmpmenuprincipal)*100,1)}%",
		    f"3. Citas C.M.C.M.P. {round((totalmpopc3/totalmpmenuprincipal)*100,1)}%",
		    f"4. Autorizaciones médicas. {round((totalmpopc4/totalmpmenuprincipal)*100,1)}%",
		    f"5. F.,D.M.,T.ADMON. {round((totalmpopc5/totalmpmenuprincipal)*100,1)}%",
		    f"6. Agente servicio. {round((totalmpopc6/totalmpmenuprincipal)*100,1)}%",
		    f"consulta medica virtual {round((mpopc21/totalmpopc2)*100,1)}%",
		    f"orientacion medica telefonica {round((mpopc22/totalmpopc2)*100,1)}%",
		    f"nutricion y psicologia {round((mpopc23/totalmpopc2)*100,1)}%",
		    f"Asignar citas {round((mpopc31/totalmpopc3)*100,1)}%",
		    f"Consultar o cancelar citas {round((mpopc32/totalmpopc3)*100,1)}%",
		    f"enviar diractorio medico {round((mpopc51/totalmpopc5)*100,1)}%",
		    f"Facturacion {round((mpopc52/totalmpopc5)*100,1)}%",
		    f"generar certificados {round((mpopc53/totalmpopc5)*100,1)}%",
		    f"agente servicio {round((mpopc54/totalmpopc5)*100,1)}%",
		    f"Citas centros medicos {round((mpopc61/totalmpopc6)*100,1)}%",
		    f"facturacion servicio al cliente {round((mpopc62/totalmpopc6)*100,1)}%",
		    f"pagos {round((mpopc521/mpopc52)*100,1)}%",
		    f"agente servicios {round((mpopc522/mpopc52)*100,1)}%",
		    f"afiliacion {round((mpopc531/mpopc53)*100,1)}%",
		    f"retefuentes {round((mpopc532/mpopc53)*100,1)}%",
		    f"Efectivo %",
		    f"Abandona %"
		]

		tipografico="IVR MP (Productos)"

		bar_data = go.Bar(
            x=[0, 0.9, 2.3, 3.7, 5.1 ,6],
            y=[20, 20, 20, 20, 20, 0],
            width=0.18,
            
            marker=dict(color=["white","#dcdcdc","#dcdcdc","#dcdcdc","#dcdcdc","white"],
                line=dict(color="white", width=0.5)))

	else:
		coomevasys = (agrupado['Numero_y'] == 1) & (agrupado['Numero_x'] == 0)
		coomevasys1 = (agrupado['Numero_y'] == 2) & (agrupado['Numero_x'] == 0)
		coomevasys2 = (agrupado['Numero_y'] == 3) & (agrupado['Numero_x'] == 0)
		coomevasys3 = (agrupado['Numero_y'] == 4) & (agrupado['Numero_x'] == 0)
		coomevasys4 = (agrupado['Numero_y'] == 5) & (agrupado['Numero_x'] == 0)

		totalprincipalsys=(agrupado['Numero_x'] == 0)

		totalsysefectivo = (agrupado['Numero_y'] == 8)
		totalsysabandona = (agrupado['Numero_y'] == 9) 

		devuelve3principal = (agrupado['Numero_y'] == 0) & (agrupado['Numero_x'] == 3)



		totalsys=agrupado.loc[totalprincipalsys,'Recuento'].sum()-agrupado.loc[devuelve3principal,'Recuento'].sum()

		totalsysabandona=agrupado.loc[totalsysabandona,'Recuento'].sum()

		totalsysefectivo=agrupado.loc[totalsysefectivo,'Recuento'].sum()



		tipografico="IVR COOMEVA-SyS"

		label  =  ["Menu Princial",
    "Informacion y solicitud de productos",
    "Asistencias integrales",
    "Cancelacion de polizas de seguros",
    "Pago de contado",
    "Asesor de servicios",
    "Cancelacion de autos, rc medica y hogar",
    "Cancelacion de tarjetas, pensiones y mascotas",
    "Efectivo",
    "Abandona",

    ]
		bar_data = go.Bar(
            x=[0, 2.05, 4.1, 4.7, 5.4 ,6],
            y=[20, 20, 20, 20, 20, 0],
            width=0.18,
            
            marker=dict(color=["white","#dcdcdc","#dcdcdc","white","white","white"],
                line=dict(color="white", width=0.5)))



	source_data = list(agrupado["Numero_x"])
	target_data = list(agrupado["Numero_y"])
	value_data = list(agrupado["Recuento"])
	col=list(agrupado["detail_y"])
	colors=[]
	for i in range(len(source_data)):
	    if col[i]=="Efectvo":
	        colors.append('#24E62D')
	    else:
	        colors.append('#E5282E')

	 
	pyLogo = Image.open("Logo.png")

	# Convertir la imagen a formato Plotly
	pyLogo_plotly = go.layout.Image(source=pyLogo)
	if combo=="Coomeva-CAC" :
		fig = go.Figure(go.Sankey(
		    arrangement = "snap",
		    node=dict(
		        pad=20,
		        thickness=20,

	            y= node_y_positions,
	            x=node_x_positions,
		        line=dict(color="black", width=1),
		        label=label,


		    ),
		    link=dict(
		        source=source_data,
		        target=target_data,
		        value=value_data,
		        color=colors
		    )
		))

	else :
		fig = go.Figure(go.Sankey(
		    arrangement = "snap",
		    node=dict(
		        pad=40,
		        thickness=20,
		        line=dict(color="black", width=1),
		        label=label,


		    ),
		    link=dict(
		        source=source_data,
		        target=target_data,
		        value=value_data,
		        color=colors
		    )
		))
		
	# Agregar el gráfico de barras a la figura
	fig.add_trace(bar_data)
	fig.update_xaxes(showline=False, zeroline=False,showgrid=False, showticklabels=False)
	fig.update_yaxes(showline=False, zeroline=False,showgrid=False, showticklabels=False)

	# Personalizar el diseño del diagrama
	if combo=="Coomeva-CAC":
		fig.update_layout(
		    xaxis=dict(tickmode='array', tick0=2, dtick=2),
		    title_text=f"{tipografico}      %ABANDONO:  {round((totalaba/(total+total464))*100,2)}%           %EFECTIVAS:  {round((totalefe/(total+total464))*100,2)}%           {fechainicio} - {fechafin}",
		    hovermode="y unified",
		    font=dict(size=15,family="Arial Black")
		)

	elif combo=="MP Validacion Productos":
		fig.update_layout(
		    xaxis=dict(tickmode='array', tick0=2, dtick=2),
		    title_text=f"{tipografico}      %ABANDONO:   {round((totalabandonamp/(totalmp))*100,2)}%          %EFECTIVAS:  {round((totalefectivomp/(totalmp))*100,2)}%           {fechainicio} - {fechafin}",
		    hovermode="y unified",
		    font=dict(size=15,family="Arial Black")
		)

	else:
		fig.update_layout(
		    xaxis=dict(tickmode='array', tick0=2, dtick=2),
		    title_text=f"{tipografico}      %ABANDONO:   {round((totalsysabandona/totalsys)*100,2)}%          %EFECTIVAS:   {round((totalsysefectivo/totalsys)*100,2)}%        {fechainicio} - {fechafin}",
		    hovermode="y unified",
		    font=dict(size=15,family="Arial Black")
		)

	fig.update_layout(
    plot_bgcolor='white',  # Cambia el color de fondo del gráfico
    paper_bgcolor='white'  # Cambia el color de fondo del papel (área alrededor del gráfico)
    )

	

	fig.add_layout_image(
	    pyLogo_plotly,
	    x=0,
	    y=4,
	    xref="x",
	    yref="y",
	    sizex=1,
	    sizey=4,
	    opacity=1,
	    layer="above"
	)

	if combo=="MP Validacion Productos":

		fig.add_annotation(
		    text="Menu 1",  # Texto que deseas mostrar
		    x=0.9,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black") # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 2",  # Texto que deseas mostrar
		    x=2.3,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 3",  # Texto que deseas mostrar
		    x=3.7,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 4",  # Texto que deseas mostrar
		    x=5.1,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)

	elif combo=="Coomeva-CAC":

		fig.add_annotation(
		    text="Menu 1",  # Texto que deseas mostrar
		    x=1,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black") # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 2",  # Texto que deseas mostrar
		    x=2.4,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 3",  # Texto que deseas mostrar
		    x=3.7,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)

	else:
		fig.add_annotation(
		    text="Menu 1",  # Texto que deseas mostrar
		    x=2.1,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)
		fig.add_annotation(
		    text="Menu 2",  # Texto que deseas mostrar
		    x=4.1,  # Coordenada x de la etiqueta
		    y=0,  # Coordenada y de la etiqueta
		    showarrow=False,  # Opcional: para mostrar o no una flecha
		    font=dict(family="Arial Black",size=25, color="black")  # Cambiar el color del texto a rojo
		)



	fig.write_html("mi_grafico_sankey.html")
	figura = fig
	figura.show()
	return figura
