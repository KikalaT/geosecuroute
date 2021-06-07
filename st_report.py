import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, OSM
from bokeh.transform import factor_cmap
from bokeh.models.tools import WheelZoomTool
from bokeh.models import ColumnDataSource

import streamlit as st

# page configuration
st.set_page_config(
page_title="PySecuRoute v1.0",
layout="wide",
)

# sidebar navigator
st.sidebar.header('PySecuRoute v1.0')
st.sidebar.title('Sommaire')
nav = st.sidebar.radio('',['1. Présentation','2. Exploration','3. Analyse','4. Modélisation','5. Conclusion'])

"""
# PySecuRoute v1.0
### Datascientest - Bootcamp Data Analyst (Avril 2021-Juin 2021)
#### `Pascal INDICE` | `Kikala TRAORÉ` | `Christophe WARDIUS` | `Hervé HOUY`
---
"""

if nav == '1. Présentation':
	"""
	## 1. Présentation
	---
	
	### Présentation du projet
	
	Les accidents corporels sont courants et les répertorier permet de les étudier afin d’identifier
	les différents cas qui ont impliqué des blessures plus ou moins graves. Prédire la gravité
	d’un accident en fonction de ses différentes caractéristiques peut être utile pour proposer
	une solution qui a comme but de réduire la fréquence des accidents graves.

	**Données**

	Plusieurs jeux de données répertorient l’intégralité des accidents corporels de la circulation
	intervenus durant une année précise en France métropolitaine et dans les DOM-TOM. Ces
	jeux de données comprennent des informations de localisation de l’accident ainsi que des
	informations concernant les caractéristiques de l’accident et son lieu, les véhicules impliqués
	et leurs victimes.

	Nous avons choisi d'exploiter les données dont les sources sont téléchargeables au lien suivant :

	[https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/)

	### Organisation et répartition des tâches

	Nous avons choisi ce projet pour la __volumétrie__ et la __variété__ des informations mises à disposition sur un sujet concret qui impacte notre vie au quotidien :

	les déplacements sur les routes françaises et la sécurité routière qui en découle.
	Pourtant, nous ne sommes probablement pas les personnes les plus impactées par le trafic routier.

	Venant de _Caen_, _Le Mans_, _Roanne_ et même _Saint-Denis de La Réunion_, le trafic routier des grandes agglomérations et les accidents récurrents ne sont pas notre lot de désagrément quotidien.

	Mais comme le sujet essentiel de ce projet Data est axé sur la __gravité des blessures corporels__ et la mortalité des accidentés de la route, nous verrons aussi que les spécificités géographiques peuvent donner des informations parlantes et exploitables pour un assureur ou un organisme travaillant dans le large périmètre de la sécurité routière.

	**Répartition des tâches** :

	La répartition des tâches dans l'équipe s'est faite naturellement par affinité sur les sujets et sur les compétences de chacun.

	Notre équipe est composée de profils professionnels aux parcours complètement différents.

	Ces différences de profil et de personnalité ont nourri la richesse des échanges et permis de trouver une vraie complémentarité dans la répartition des tâches :

	__Kikala__: Enseignant, Chercheur, formé au renseignement d'intéret économique, adepte du Zen de Python depuis quelques années, s'est orienté naturellement sur l'exploitation, la mise en forme des données, le data processing.

	Son expérience en Python nous a permis de débuter rapidement le projet et de transmettre ses actuces.

	__Christophe__: Chercheur en Archéologie et Géographie, a pu retrouver facilement ses repères en fouillant la documentation et les hyperparamètres d'un nombre important de modèles de Machine Learning.

	Passionné d'informatique et de programmation web, nous avons pu profiter de ses talents de développeur, de facilitateur de mise à disposition d'environnement cloud pour exécuter les traitements lourds sur un volume important de données.

	__Hervé__: Analyste fonctionnel, Consultant en Assistance en Maitrise d'Ouvrage, a pu continuer de questionner, analyser, détecter les écarts en s'orientant vers la production de graphiques, en requétant et contrôlant l'intégrité des données avant le traitement de Machine Learning.

	__Pascal__ : sa formation en Gestion et Commerce, son attrait pour les tableaux et les statistiques l'ont orienté vers la partie DataVizualiation avec de nombreux graphiques à étudier en liaison avec les résultats du Machine Learning.

	Les parties rédaction, relecture et critique ont été équitablement partagée dans l'équipe.

	### Avancement et suivi du projet

	A l'aide de _Slack_, _codeshare.io_ et des réunions _Zoom_, nous avons pu communiquer régulièrement sur l'avancé du projet et sur nos tâches respectives.

	Nos réunions hebdomadaires avec Maxime de DataScientest, et ses conseils pertinents, ont permis d'aller à l'essentiel et d'éviter de nous égarer facilement vu le vaste sujet étudié, dans le temps restreint rythmé par les certifications hebdomadaires et obligatoires de cette riche formation.

	### Pourquoi PySecuRoute ?
	
	* Pour __Py__thon, langage ubiquitaire en tant que Data Analyst, et plus généralement en Data Science.
	* Notre sensibilité commune sur la __Sécu__rité __Rout__ière
	"""

elif nav == '2. Exploration':
	"""
		## 2. Exploration des données
		---
	"""
		
	if st.checkbox("Description des données"):
		"""
		### Description des données
		---

		Pour chaque accident corporel (soit un accident survenu sur une voie ouverte à la circulation publique,
		impliquant au moins un véhicule et ayant fait au moins une victime ayant nécessité des soins), des
		saisies d’information décrivant l’accident sont effectuées par l’unité des forces de l’ordre (police,
		gendarmerie, etc.) qui est intervenue sur le lieu de l’accident. Ces saisies sont rassemblées dans
		une fiche intitulée bulletin d’analyse des accidents corporels. L’ensemble de ces fiches constitue le
		fichier national des accidents corporels de la circulation dit « Fichier BAAC » administré par
		l’Observatoire national interministériel de la sécurité routière "ONISR".

		Les bases de données, extraites du fichier BAAC, répertorient l'intégralité des accidents corporels de
		la circulation, intervenus durant une année précise en France métropolitaine, dans les départements
		d’Outre-mer (Guadeloupe, Guyane, Martinique, La Réunion et Mayotte depuis 2012) et dans les autres
		territoires d’outre-mer (Saint-Pierre-et-Miquelon, Saint-Barthélemy, Saint-Martin, Wallis-et-Futuna,
		Polynésie française et Nouvelle-Calédonie ; disponible qu’à partir de 2019 dans l’open data) avec une
		description simplifiée. Cela comprend des informations de localisation de l’accident, telles que
		renseignées ainsi que des informations concernant les caractéristiques de l’accident et son lieu, les
		véhicules impliqués et leurs victimes.

		Par rapport aux bases de données agrégées 2005-2010 et 2006-2011 actuellement disponibles sur le
		site [www.data.gouv.fr](https://www.data.gouv.fr), les bases de données de 2005 à 2019 sont désormais annuelles et composées
		de 4 fichiers (Caractéristiques – Lieux – Véhicules – Usagers) au format csv. 
		
		"""
		
	if st.checkbox("Exploitation des données"):
		"""
		### Exploitation des données
		---
	
		Ayant relevé une incompatibilité entre les datasets antérieurs et postérieurs à 2018, nous avons choisi de fusionner dans un DataFrame l'ensemble des bases de données de 2005 à 2017

		"""
		
	if st.checkbox("Identification des données"):
		"""
		### Identification des données
		---
		
		Afin de faciliter le téléchargement des données, l'ensemble des informations sur les jeux de données est agrégé dans un fichier master JSON :

		* data.json
		"""
		# chargement du 'df_master' des jeu de données
		data = json.load(open('data.json','r'))
		df_master = pd.json_normalize(data['distribution'])
		st.write(df_master.head())
		
	if st.checkbox("Restriction de l'exploration sur les des données sur la période 2005-2017"):
		"""
		### Restriction de l'exploration sur les des données sur la période 2005-2017
		
		
		
		La note de Description des bases de données annuelles des accidents corporels de la circulation routière
		Années de 2005 à 2019 (téléchargeable ici) émet un avertissement :

		Les données sur la qualification de blessé hospitalisé depuis l’année 2018 ne peuvent être comparées aux années précédentes suite à des modifications de process de saisie des forces de l’ordre. L’indicateur « blessé hospitalisé » n’est plus labellisé par l’autorité de la statistique publique depuis 2019.

		Nous avons donc choisi de restreindre une partie de l'exploration des données sur la période 2005-2017, ce qui consitue :

		* 13` années
			
		`4` datasets au format CSV par année :
		* Caractéristiques,
		* Lieux,
		* Véhicules,
		* Usagers.
			
		Soit `52` fichiers CSV à consolider dans un `DataFrame`.

		On remarque qu'une erreur s'est produite avec le fichier `caracteristiques_2009.csv` que l'on traitera donc séparément.
		(Il s'agit en fait d'un fichier _TSV_)
		
		"""
		
	if st.checkbox("Modèle de données"):
		"""
		### Modèle de données
		---
		
		### Descriptifs des fichiers à disposition:
		
		#### Caractéristiques :

		Circonstances générales de l’accident notamment la __date__, les __conditions atmostphériques__ et la __situation géographique__.

		Identifiant(s) du fichier :

		`Num_Acc`: Numéro d'identifiant de l’accident
		
		* LIEUX

		Description du lieu principal de l’accident même si celui-ci s’est déroulé à une intersection

		Identifiant(s) du fichier :

		`Num_Acc`: Numéro d'identifiant de l’accident
		
		* VEHICULES

		Véhicules impliqués dans l'accident avec les caractériques du véhicules

		Identifiant(s) du fichier :

		`Num_Acc` : Numéro d'identifiant de l’accident
		`Num_Veh` : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés)
		
		* USAGERS

		Usagers impliqués dans l'accident avec caractéristiques propres à l'usager et les conséquences de l'accident (gravité)

		Identifiant(s) du fichier :

		`Num_Acc` : Numéro de l’accident
		`Num_Veh` : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés)
		`place` : Permet de situer la place occupée dans le véhicule par l'usager au moment de l'accident

		Chaque ligne correspond à un usager, en terme de données il peut y avoir des "faux" doublons notamment pour les usagers de transport en commun.
		"""
		
	if st.checkbox("Constitution du jeu de données à explorer"):
		
		"""
		### Constitution du jeu de données à explorer
		
		_Principe_:
		Notre étude portant sur la gravité des blessures corporels des usagers, nous devons avoir l'ensembles des données concernant les usagers des accidents sur notre période de 2005 à 2017.

		Pour constituer le jeu de données à explorer, nous prendrons donc le fichier `Usagers` comme fichier "Maitre" et nous ferons toutes les jointures nécessaires avec ce fichier.

		_Pour chaque année de données récupérées_:
		* Création de _4 dataframes_ correspondants aux chargements des _4 fichiers csv_ de l'année.
		* Création d'un _dataframe global_ de l'année résultat des jointures des 4 dataframes de l'année
		* _Concaténation_ de l'ensemble des dataframes globaux pour créer un dataframe final de notre période 2005 à 2017
		
		_Ajout des colonnes 'département' et 'région'_

		Nous avons fait le choix de pouvoir localiser les accidents. Pour cela, nous utiliserons 2 dictionnaires Python téléchargeables [ici](https://gist.github.com/mlorant/b4d7bb6f96c47776c8082cf7af44ad95)

		Ces deux dictionnaires listent les régions et départements français. Dans notre dataframe, le département est renseigné dans la colonne __'dep'__.

		Création des colonnes :
		* 'departement'
		* 'region'
		"""	
	
	if st.checkbox('Data cleaning'):
		"""

		Nous avons effectué un _data cleaning_ des données avec notamment :
		* une gestion des NaN
		* remplacement des NaN par le mode le cas échéant.
		"""
		
		"""
		```
		nan_mode_cols = ['place','secu','lartpc','larrout','env1','infra','situ','vosp','nbv','plan','prof',
						 'surf','circ','actp','locp','etatp','an_nais','obsm','obs','trajet',
						 'manv','choc','senc','atm']

		for col in nan_mode_cols:
			df[col] = df[col].fillna(df[col].mode()[0])

		```
		"""
		"""
		* une conversion de la majorité des colonnes grâce à la fonction pd.to_numeric(...

		Exemple de fonction créée pour le projet et permettant d'afficher la répartition des NaN's :

		"""
		"""
		```
		def show_nan_rep(dataframe):
			missing_count = dataframe.isnull().sum()  the count of missing values
			value_count = dataframe.isnull().count()  the count of all values 
			missing_percentage = round(missing_count / value_count * 100,2)  the percentage of missing values
			missing_df = pd.DataFrame({'nbre': missing_count, '%': missing_percentage})  create a dataframe
			print("Champs vides :")
			print(missing_df.sort_values(by='nbre', ascending=False))
			plt.figure(figsize=(8,8))
			missing_df['%'].sort_values(ascending=False)[:15].plot.pie(autopct="%.1f%%")
			plt.title('Répartition des données manquantes par colonne');
		```
		"""
		"""
		Exemple de fonction créée pour sonder les modalités de chaque colonne :
		"""
		"""
		```
		for i in df.columns[1:]:
			x = df[i].sort_values().unique()
			print('Pour la colonne ',i,', les valeurs sont :',x)
		```
		"""
		"""

		On fait le choix de supprimer les colonnes `v2`, `v1`, `gps`, `pr1`, `pr`, `adr` et `voie` qui de part le caractère erratique de leurs modalités n'apporteront pas de valeur ajoutée à notre étude.

		On conserve les colonnes lat et long pour l'instant.
		"""

	if st.checkbox('Conclusions et export'):
		"""	
		Nous ne proposons pas le code associé dans le présent rapport, vu que le CSV est disponible sur un site internet personnel, à cause de sa grande taille (444Mo) ne pouvant pas être hébergé sur GitHub et la durée potentielle de réalisation.

		[Le lien du CSV global 2005-2017](https://christophe-wardius.fr/projets/pysecuroute/dataset_v3/df_global_v3.csv)

		`df.to_csv('...`
		
		Nous avons fait le choix d'héberger le fichier global 2005-2017 sur le site personnel de Christophe W., car le CSV global a une taille de `444Mo` et GitHub ne permet pas de stocker un tel fichier. 

		En outre, nous avons décidé de proposer un CSV par année pour les besoins de la visualisation de données. Ceux-ci sont disponibles directement sur le GitHub du projet au sein du dossier 'dataset'.
		"""

elif nav == '3. Analyse':
	"""
		## 3. Analyse et Visualisation des données
	"""
	
	"""
	###### Afin d'optimiser le temps de chargement et l'affichage, nous avons fait le choix de __filtrer__ les données de visualisation __par année__.
	---	
	"""
	"""
	##### Sélectionnez une année d'étude (de 2005 à 2017)
	"""
	annee = st.selectbox("", np.arange(2005,2018,1))

	@st.cache(suppress_st_warning=True,allow_output_mutation=True,max_entries=None,ttl=60*3)
	def preprocess():
		
		# chargement des df par année
		df = {}
		
		#chargement des données depuis le cloud
		df[annee] = pd.read_csv('https://www.jazzreal.org/static/df_'+str(annee)+'_v3.csv')
		
		# sampling du df à 10%
		df[annee] = df[annee].sample(frac=0.10, replace=False, random_state=1234)
		
		# gestion des dates
		df[annee].an=df[annee].an+2000
		df[annee]['date']=pd.to_datetime((df[annee].an*10000+df[annee].mois*100+df[annee].jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
		df[annee]['day']= df[annee].date.dt.weekday
		
		# conversion de la longitude en 'float64'
		df[annee]['long'] = pd.to_numeric(df[annee]['long'], errors='coerce')
		
		# conversion du CRS en mercator
		k = 6378137
		df[annee]["x"] = (df[annee]['long'] / 100000)* (k * np.pi / 180.0)
		df[annee]["y"] = np.log(np.tan((90 + df[annee]['lat']/100000) * np.pi / 360.0)) * k
		
		# data cleaning
		df[annee].dropna()
		
		print('(done) loading csv file for '+str(annee))

		return df[annee]
	
	# chargement des dataframes
	df = preprocess()
	
	df['date']= pd.to_datetime((df.an*10000+df.mois*100+df.jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
	df['day']= df.date.dt.day_name()
	df['day']= pd.Categorical(df['day'],['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],ordered=True)
	df['age']= df.an-df.an_nais
	
	df_non_indemnes = df[df['grav']!=1]
	df_tues = df[df['grav']==2]
	
	print('(done) : preprocessing completed.')
	
	# ajout année sur le sidebar	 
	st.sidebar.markdown("### Analyses sur l'année : "+str(annee))
	
	# recherche par mot-clés
	"""
	##### Recherche de visualisations par mot-clés (en minuscule, séparé par des espaces)
	"""
	search = st.text_input('')
	"""
	###### exemples de mot-clés : `carte` `région` `département` `gravité` `mois` `jour` `heure` `véhicule` `route` `collision` `sexe`
	"""

	# graphiques

	
	## tableau des régions avec le plus d'accidentés pour comparé avec le plus de blessés
	def Tableau_Des_Régions_Avec_Le_Plus_D_accidentés_Pour_Comparé_Avec_Le_Plus_De_Blessés():
		x1 = pd.crosstab(df.grav, df.region, rownames=['gravite'], colnames=['region'])
		st.write(x1)


	## tableau des régions avec le plus de tués pour comparé avec le plus de blessés
	def Tableau_Des_Régions_Avec_Le_Plus_De_Tués_Pour_Comparé_Avec_Le_Plus_De_Blessés():
		x2 = pd.crosstab(df_tues.grav, df_tues.region, rownames=['nombre de Tués'], colnames=['region'])
		st.write(x2)

	## tableau des départements avec le plus de tués
	def Tableau_Des_Départements_Avec_Le_Plus_De_Tués():
		x3 = pd.crosstab(df_tues.grav, df_tues.departement, rownames=['nombre de Tués'], colnames=['departement'])
		st.write(x3)

	## tableau des régions avec le plus de blessés pour comparaison
	def Tableau_Des_Régions_Avec_Le_Plus_De_Blessés_Pour_Comparaison():
		x4 = pd.crosstab(df.grav, df.region, rownames=['gravite'], colnames=['region'])
		st.write(x4)

	## distribution des accidentés par région/département
	def Distribution_Des_Accidentés_Par_Régiondépartement():
		x5 = pd.pivot_table(df, index=['region', 'departement'], values='grav', aggfunc='count')
		st.write(x5)

	## tableau des nombre de tués par région et département
	def Tableau_Des_Nombre_De_Tués_Par_Région_Et_Département():
		pd.set_option("max_rows", None)
		x6 = pd.pivot_table(df_tues, index=['region', 'departement'], values='grav', aggfunc='count')
		st.write(x6)


	## palmarès des régions avec le plus et le moins d'accidentés
	def Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_Daccidentés():
		max_col = df['region'].value_counts().head(5)
		min_col = df['region'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.set_ylabel('nombre')
		ax1.title.set_text("5 régions avec le plus d'accidents corporels")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 regions avec le moins d'accidents corporels")
		ax2.set_ylabel('nombre')
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## palmarès des régions avec le plus et le moins de tués
	def Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_De_Tués():
		max_col = df_tues['region'].value_counts().head(5)
		min_col = df_tues['region'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.title.set_text("5 régions avec le plus d'accidents mortels")
		labels = ax1.get_xticklabels()
		ax1.set_ylabel('nombre')
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 régions avec le moins d'accidents mortels")
		ax2.set_ylabel('nombre')
		plt.xticks(rotation=45);
		st.pyplot(fig)
	
	## palmarès des départements avec le plus d'accidents corporels
	def Palmarès_Des_Départements_Avec_Le_Plus_Daccidents_Corporels():
		max_col = df['departement'].value_counts().head(5)
		min_col = df['departement'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.title.set_text("5 départements avec le plus d'accidents corporels")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 départements avec le moins d'accidents corporels")
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## palmarès des Départements avec le plus et le moins de Tués
	def Palmarès_Des_Départements_Avec_Le_Plus_Et_Le_Moins_De_Tués():
		max_col_tues = df_tues['departement'].value_counts().head(5)
		min_col_tues = df_tues['departement'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col_tues.index, y=max_col_tues, order=max_col_tues.index, ax=ax1)
		ax1.title.set_text("5 départements avec le plus de Tués")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col_tues.index, y=min_col_tues, order=min_col_tues.index, ax=ax2)
		ax2.title.set_text("5 départements avec le moins de Tués")
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## distribution des accidenté(e)s par gravité de blessure
	def Distribution_Des_Accidentées_Par_Gravité_De_Blessure():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav",data=df)
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures");
		st.pyplot(fig)
	
	##BOKEH##
	## carte intéractive des accidentés par gravité
	def Carte_Intéractive_Des_Accidentés_Par_Gravité():
		df_geo = df[['lat','long','grav','an']]
		df_geo['lat'] = pd.to_numeric(df_geo['lat'], errors='coerce')
		df_geo['long'] = pd.to_numeric(df_geo['long'], errors='coerce')
		df_geo['lat'] = df_geo['lat'] / 100000
		df_geo['long'] = df_geo['long'] / 100000
		k = 6378137
		df_geo["x"] = (df_geo['long'])* (k * np.pi / 180.0)
		df_geo["y"] = np.log(np.tan((90 + df_geo['lat']) * np.pi / 360.0)) * k
		tile_provider = get_provider(OSM)
		tools = "pan,wheel_zoom,reset"
		p = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
				   x_axis_type="mercator", y_axis_type="mercator",
				   tools=tools,
				   plot_width=800,
				   plot_height=600,
				   title='Accidents de la route par gravité ('+str(annee)+')'
				   )
		p.add_tile(tile_provider)
		geo_source_1 = ColumnDataSource(data=df_geo[df_geo['grav'] == 1])
		geo_source_2 = ColumnDataSource(data=df_geo[df_geo['grav'] == 2])
		geo_source_3 = ColumnDataSource(data=df_geo[df_geo['grav'] == 3])
		geo_source_4 = ColumnDataSource(data=df_geo[df_geo['grav'] == 4])
		p1 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_1, color='green', legend_label='Indemne')
		p2 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_4, color='yellow', legend_label='Blessé léger')
		p3 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_3, color='orange', legend_label='Blessé hospitalisé')
		p4 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_2, color='red', legend_label='Tué')
		p.xgrid.grid_line_color = None
		p.ygrid.grid_line_color = None
		p.xaxis.major_label_text_color = None
		p.yaxis.major_label_text_color = None
		p.xaxis.major_tick_line_color = None  
		p.xaxis.minor_tick_line_color = None  
		p.yaxis.major_tick_line_color = None  
		p.yaxis.minor_tick_line_color = None  
		p.yaxis.axis_line_color = None
		p.xaxis.axis_line_color = None
		p.legend.click_policy = "hide"
		st.bokeh_chart(p)
	
	## distribution des accidentés par mois
	def Distribution_Des_Accidentés_Par_Mois():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="mois", data=df);
		plt.legend(labels=['Janvier',
						   'Février',
						   'Mars',
						   'Avril',
						   'Mai',
						   'Juin',
						   'Juillet',
						   'Août',
						   'Septembre',
						   'Octobre',
						   'Novembre',
						   'Décembre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des mois de l'année");
		st.pyplot(fig)
	
	## distribution des accidentés par jour de la semaine
	def Distribution_Des_Accidentés_Par_Jour_De_La_Semaine():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="day", data=df);
		plt.legend(labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des jours de la semaine");
		st.pyplot(fig)
	
	## distribution par heure / minutes
	def Distribution_Par_Heure_Minutes():
		fig, ax = plt.subplots(figsize=(11,5))
		sns.kdeplot(x='hrmn',hue='grav',multiple="stack",data=df)
		plt.legend(labels=['Blessé léger','Blessé hospitalisé','Tué','Indemne'])
		plt.xticks([0,500,1000,1500,2000],['0:00','5:00','10:00','15:00','20:00'])
		plt.xlim(right=2500)
		plt.xlabel('Heures')
		plt.ylabel('Densité')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'heure");
		st.pyplot(fig)
		
	## graphique par catégorie de véhicule
	def Graphique_Par_Catégorie_De_Véhicule():
		fig, ax = plt.subplots(figsize=(15,15))
		sns.countplot(x="grav", hue="catv", data=df);
		plt.legend(labels=['01 - Bicyclette',
						   '02 - Cyclomoteur <50cm3',
						   '03 - Voiturette (Quadricycle à moteur carrossé)',
						   '04 - scooter immatriculé',
						   '05 - motocyclette',
						   '06 - side-car',
						   '07 - VL seul',
						   '08 - VL + caravane',
						   '09 - VL + remorque',
						   '10 - VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque',
						   '11 - VU (10) + caravane',
						   '12 - VU (10) + remorque',
						   '13 - PL seul 3,5T <PTCA <= 7,5T',
						   '14 - PL seul > 7,5T',
						   '15 - PL > 3,5T + remorque',
						   '16 - Tracteur routier seul',
						   '17 - Tracteur routier + semi-remorque',
						   '18 - transport en commun',
						   '19 - tramway',
						   '20 - Engin spécial',
						   '21 - Tracteur agricole',
						   '30 - Scooter < 50 cm3',
						   '31 - Motocyclette > 50 cm3 et <= 125 cm3',
						   '32 - Scooter > 50 cm3 et <= 125 cm3',
						   '33 - Motocyclette > 125 cm3',
						   '34 - Scooter > 125 cm3',
						   '35 - Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)',
						   '36 - Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)',
						   '37 - Autobus',
						   '38 - Autocar',
						   '39 - Train',
						   '40 - Tramway',
						   '99 - Autre véhicule'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de véhicule');
		st.pyplot(fig)
	
	## graphique par catégorie de route
	def Graphique_Par_Catégorie_De_Route():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catr", data=df);
		plt.legend(labels=['1 - Autoroute',
						   '2 - Route nationale',
						   '3 - Route Départementale',
						   '4 - Voie Communale',
						   '5 - Hors réseau public',
						   '6 - Parc de stationnement ouvert à la circulation publique',
						   '9 - autre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de route');
		st.pyplot(fig)
	
	## graphique par type de collision
	def Graphique_Par_Type_De_Collision():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="col", data=df);
		plt.legend(labels=['Deux véhicules - frontale',
						   'Deux véhicules - par l’arrière',
						   'Deux véhicules - par le coté',
						   'Trois véhicules et plus – en chaîne',
						   'Trois véhicules et plus - collisions multiples',
						   'Autre collision',
						   'Sans collision'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction du type de collision");
		st.pyplot(fig)

	## proportion masculin / féminin (accidentés)
	def Proportion_Masculin_Féminin_accidentés():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="sexe",data=df)
		plt.xticks([0,1],['M','F'])
		plt.xlabel("Sexe de l'accidenté(e)")
		plt.ylabel("nombre Usagers")
		plt.title('Distribution des accidentés par sexe');
		st.pyplot(fig)

	## proportion masculin/féminin ( tués )
	def Proportion_Masculinféminin_Tués_():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="sexe",data=df_tues)
		plt.xticks([0,1],['M','F'])
		plt.xlabel("Sexe de l'accidenté(e)")
		plt.ylabel("nombre de Tués")
		plt.title("Distribution des Tué(e)s par sexe");
		st.pyplot(fig)

	## proportion masculin/féminin ( tués par âge )
	def Proportion_Masculinféminin_Tués_Par_Age_():
		g = sns.FacetGrid(df_tues, col='sexe')
		g.map(plt.hist, 'age');
		st.pyplot(g)

	## graphique par sexe
	def Graphique_Par_Sexe():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="sexe", data=df);
		plt.legend(labels=['M','F'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du sexe');
		st.pyplot(fig)
	
	## distribution des accidenté(e)s par gravité des blessures en fonction de l'âge
	def Distribution_Des_Accidentées_Par_Gravité_Des_Blessures_En_Fonction_De_Lâge():
		fig, ax = plt.subplots(figsize=(11,5))
		sns.kdeplot(x='age',hue='grav',multiple="stack",data=df)
		plt.legend(labels=['Blessé léger','Blessé hospitalisé','Tué','Indemne'])
		plt.xlim(right=110)
		plt.xlabel('Age')
		plt.ylabel('Densité')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'âge");
		st.pyplot(fig)
	
	## graphique par catégorie d'usager
	def Graphique_Par_Catégorie_Dusager():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catu", data=df);
		plt.legend(labels=['1 - Conducteur',
						   '2 - Passager',
						   '3 - Piéton',
						   '4 - Pieton Roller/Trotinette'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories d'usagers");
		st.pyplot(fig)
	
	## graphique par type de trajet
	def Graphique_Par_Type_De_Trajet():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="trajet", data=df);
		plt.legend(labels=['Non renseigné',
						   'Domicile – travail',
						   'Domicile – école',
						   'Courses – achats',
						   'Utilisation professionnelle',
						   'Promenade – loisirs',
						   'Autre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du type de trajet');	
		st.pyplot(fig)
	
	# FIN VISUALISATIONS #
	######################
	
	graphs = {
	"tableau des régions avec le plus d'accidentés pour comparé avec le plus de blessés":Tableau_Des_Régions_Avec_Le_Plus_D_accidentés_Pour_Comparé_Avec_Le_Plus_De_Blessés,
	"tableau des régions avec le plus de tués pour comparé avec le plus de blessés":Tableau_Des_Régions_Avec_Le_Plus_De_Tués_Pour_Comparé_Avec_Le_Plus_De_Blessés,
	"tableau des départements avec le plus de tués":Tableau_Des_Départements_Avec_Le_Plus_De_Tués,
	"tableau des régions avec le plus de blessés pour comparaison":Tableau_Des_Régions_Avec_Le_Plus_De_Blessés_Pour_Comparaison,
	"distribution des accidentés par région/département":Distribution_Des_Accidentés_Par_Régiondépartement,
	"tableau des nombre de tués par région et département":Tableau_Des_Nombre_De_Tués_Par_Région_Et_Département,
	"palmarès des régions avec le plus et le moins d'accidentés":Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_Daccidentés,
	"palmarès des régions avec le plus et le moins de tués":Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_De_Tués,
	"palmarès des départements avec le plus d'accidents corporels":Palmarès_Des_Départements_Avec_Le_Plus_Daccidents_Corporels,
	"palmarès des Départements avec le plus et le moins de Tués":Palmarès_Des_Départements_Avec_Le_Plus_Et_Le_Moins_De_Tués,
	"distribution des accidenté(e)s par gravité de blessure":Distribution_Des_Accidentées_Par_Gravité_De_Blessure,
	"carte intéractive des accidentés par gravité":Carte_Intéractive_Des_Accidentés_Par_Gravité,
	"distribution des accidentés par mois":Distribution_Des_Accidentés_Par_Mois,
	"distribution des accidentés par jour de la semaine":Distribution_Des_Accidentés_Par_Jour_De_La_Semaine,
	"distribution par heure / minutes":Distribution_Par_Heure_Minutes,
	"graphique par catégorie de véhicule":Graphique_Par_Catégorie_De_Véhicule,
	"graphique par catégorie de route":Graphique_Par_Catégorie_De_Route,
	"graphique par type de collision":Graphique_Par_Type_De_Collision,
	"proportion masculin / féminin (accidentés)":Proportion_Masculin_Féminin_accidentés,
	"proportion masculin/féminin ( tués )":Proportion_Masculinféminin_Tués_,
	"proportion masculin/féminin ( tués par âge )":Proportion_Masculinféminin_Tués_Par_Age_,
	"graphique par sexe":Graphique_Par_Sexe,
	"distribution des accidenté(e)s par gravité des blessures en fonction de l'âge":Distribution_Des_Accidentées_Par_Gravité_Des_Blessures_En_Fonction_De_Lâge,
	"graphique par catégorie d'usager":Graphique_Par_Catégorie_Dusager,
	"graphique par type de trajet":Graphique_Par_Type_De_Trajet,
	}

	
	# sélection et affichage des graphiques par mot-clés
	for key,value in graphs.items():
		for word in search.split():
			if word in key:
				if st.checkbox(key):
					value()

elif nav == '4. Modélisation':
	"""
	TODO
	"""

elif nav == '5. Conclusion':
	"""
	TODO
	"""
