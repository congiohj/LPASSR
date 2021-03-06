#!/usr/bin/env python3
# coding: utf-8

####################################################################################################################
## Auteur : Jorane Congio
## Date : 4/12/2016
## Titre : Dichoplay v4
## Consigne : implémenter le jeu du Plus Moins avec une interface graphique. 
##			  L'utilisateur peut choisir :
##			  Le random maximum
##			  Le nombre de tours
##			  Le temps qu'il aura pour trouver (facultatif)
##	Mini bonus : Un menu qui permet d'afficher les regles du jeu
##  Bugs non résolus : * si on clique sur soumettre sans jamais entrer de chiffre
##					     le compteur de tours descends en dessous de 0...
##                     * le programme plante quand on le quitte
## 						 -> a cause de la non utilisation du mainloop de tkinter
####################################################################################################################

from tkinter import *
import random
import time

# Point de départ du jeu : launch_game, appelle par but_begin
class MainWindow:
	def __init__(self, master):
		## Variables non-objet de la classe #######################################################################
		self.secret_number = -1
		self.nb_tour_max = 10
		self.nb_tour_restants = 11
		self.val_max_random = 100
		self.is_game_running = False

		# Le timer est facultatif
		self.start = -1
		self.timer = -1
		self.stop = -1 

		## Parametres de fenetre principale ########################################################################
		self.master = master
		master.title("Dichoplay")
		master.minsize(width=700, height=300)
		
		## Creation du menu
		self.menu = Menu(master)
		self.file_menu = Menu(self.menu, tearoff=0)
		self.file_menu.add_command(label="Règles du jeu", command=self.print_rules)
		self.menu.add_cascade(label="Aide", menu=self.file_menu)
		master.config(menu=self.menu)
		
		## Button
		self.but_retry = Button(master, text = "Rejouer", command = self.restart)
		self.but_retry.pack(side=RIGHT)
		self.but_quit = Button(master, text = 'Quit', command = master.destroy)
		self.but_quit.pack(side=BOTTOM)
		
		## Pannel gauche ###########################################################################################
		self.pan_left = PanedWindow(master, orient=VERTICAL)
		self.pan_left.pack(side=LEFT, expand=Y, fill=BOTH, pady=5, padx=5)

		# Creation des frames (contiennent le texte et l'encadrement)
		self.fra_config = LabelFrame(self.pan_left, borderwidth=2, relief=GROOVE, \
			text="Configuration", padx=20, pady=5)
		self.fra_config.pack(side=TOP, padx=5, pady=5)
		self.txt_interval = Label(self.fra_config, text='Choississez l\'intervalle du nombre à trouver : ')
		self.txt_interval.pack()

		# Definition du contenu des frames
		self.nb_secret_radio = IntVar()
		self.rad_100 = Radiobutton(self.fra_config, text = "0 - 100", variable=self.nb_secret_radio , value=100)
		self.rad_100.select()
		self.rad_100.pack()
		self.rad_500 = Radiobutton(self.fra_config, text = "0 - 500", variable=self.nb_secret_radio , value=500)
		self.rad_500.pack()
		self.rad_1000 = Radiobutton(self.fra_config, text = "0 - 1000", variable=self.nb_secret_radio , value=1000)
		self.rad_1000.pack()
		self.txt_fac_option = Label(self.fra_config, text='Options facultatives').pack()
		self.txt_nb_coups = Label(self.fra_config, text='Nombre de coups : ').pack()
		self.ent_nb_coups = Entry(self.fra_config, bd =3)
		
		self.ent_nb_coups.pack()
		self.txt_time = Label(self.fra_config, text='Temps max en secondes : ').pack()
		self.ent_time = Entry(self.fra_config, bd =3)
		self.ent_time.pack()
		self.txt_max_random = Label(self.fra_config, text='Valeur max du random : ').pack()
		self.ent_max_random = Entry(self.fra_config, bd =3)
		self.ent_max_random.pack()
		self.but_begin = Button(self.fra_config, text='Commencer a jouer', command = self.launch_game)
		self.but_begin.pack()

		## Pannel droit ###########################################################################################
		self.pan_right = PanedWindow(master, orient=VERTICAL)
		self.pan_right.pack(side=LEFT, expand=Y, fill=BOTH, pady=5, padx=5)
		self.fra_game = LabelFrame(self.pan_right, borderwidth=2, relief=GROOVE, \
			text="Jeu", padx=20, pady=5)
		self.fra_game.pack(side=TOP, padx=5, pady=5)
		self.txt_time = Label(self.fra_game, text= "")
		self.txt_time.pack()
		self.txt_game = Label(self.fra_game, text='Saisissez une valeur : ').pack()
		self.ent_game = Entry(self.fra_game, bd=3, state="disable")
		self.ent_game.pack()
		self.but_test_value = Button(self.fra_game, text = "Soumettre", \
			command = self.print_game_status, state="disable")
		self.but_test_value.pack()
		self.txt_indice = Label(self.fra_game, text= " ")
		self.txt_indice.pack()
		self.txt_statut = Label(self.fra_game, text = " ")
		self.txt_statut.pack()

	def restart(self):
		## Fonction sans parametres permettant de relancer une partie
		## Elle reactive la partie configuration de la fenetre 
		## Et remet les champs dans leur etat de base
		self.state_config_items("normal")
		self.state_game_items("disable")
		self.nb_tour_max = 10
		self.nb_tour_restants = 11
		self.is_game_running = False

	def launch_game(self):
		## Fonction sans parametres permettant d'initialiser les parametres de jeu
		## On met le jeu en running et on active la partie game de la fenetre
		self.is_game_running = True
		self.state_config_items("disable")
		self.state_game_items("normal")
		
		## On genere le nombre aleatoire par rapport aux boutons radio
		self.secret_number = random.randint(1, self.nb_secret_radio.get())
		self.val_max_random = self.nb_secret_radio.get()

		## Si l'utilisateur a entre une valeur pour le nombre de coups
		if len(self.ent_nb_coups.get()) > 0:
			try:
				nb_coups = int(self.ent_nb_coups.get())
				if nb_coups > 0:
					self.nb_tour_max = nb_coups
					self.nb_tour_restants = nb_coups + 1
			except ValueError:
				print("Entrez un nombre !")
		## Si l'utilisateur a entre une valeur pour le random max
		if len(self.ent_max_random.get()) > 0:
			try:
				val_random = int(self.ent_max_random.get())
				if val_random > 0:
					self.secret_number = random.randint(1, val_random)
					self.val_max_random = val_random
			except:
				print("Entrez un nombre !")
		
		## Si l'utilisateur a entre un timer
		if len(self.ent_time.get()) > 0:
			try:
				temps = int(self.ent_time.get())
				if temps > 0:
					print("temps")
					self.start = time.time()
					self.timer = temps
					self.stop = self.start + temps

			except:
				print("Entrez un nombre en secondes")

		## Pour faciliter les test on print le nombre a trouver dans le terminal
		print("Le nombre secret est : ", self.secret_number)

	def print_game_status(self):
		## Cette fonction sans parametres affiche le jeu

		self.nb_tour_restants -= 1
		try: ## On verifie si l'utilisateur entre bien un chiffre
			nombre_entre = int(self.ent_game.get())

			## On commence par verifier si il reste des tours a l'utilisateur
			## Les conditions permettent un meilleur feedback
			## Si l'utilisateur gagne ou perd, on met is_game_running a false : la partie est finie
			if self.nb_tour_restants > 1:
				self.txt_statut.config(text="Il vous reste " + str(self.nb_tour_restants -1) + " tours")
				if nombre_entre < self.secret_number:
					self.txt_indice.config(text="Plus grand ! ")
				elif nombre_entre < 0:
					elf.txt_indice.config(text="Le nombre est positif !")
				elif nombre_entre > self.val_max_random:
					self.txt_indice.config(text="Le nombre est plus petit que "+ str(self.val_max_random))
				elif nombre_entre > self.secret_number:
					self.txt_indice.config(text="Plus petit ! ")
				else:
					self.txt_indice.config(text="Bravo !")
					tours = str(self.nb_tour_max - self.nb_tour_restants + 1)
					self.txt_statut.config(text="Vous avez gagné en "+ tours + " tour(s) !")
					self.state_game_items("disable")
					self.is_game_running = False
			## Permet de gerer la victoire au dernier tour
			elif self.nb_tour_restants == 1 and  nombre_entre == self.secret_number:
				self.txt_indice.config(text="Bravo !")
				self.txt_statut.config(text="Vous avez gagné au dernier tour !")
				self.state_game_items("disable")
				self.is_game_running = False
					
			## L'utilisateur a perdu
			else:
				self.txt_indice.config(text="Perdu !")
				self.txt_statut.config(text="Le nombre mystère était " + str(self.secret_number))
				self.state_game_items("disable")
				self.is_game_running = False
					
		except ValueError:
			self.txt_indice.config(text="Entrez un chiffre !")
			self.txt_statut.config(text="Il vous reste " + str(self.nb_tour_restants -1) + " tours")

	def state_config_items(self, state):
		## Fonction sans parametres permettant de rapidement modifier l'etat des widgets
		## du pannel configuration
		self.rad_100.config(state=state)
		self.rad_500.config(state=state)
		self.rad_1000.config(state=state)
		self.ent_nb_coups.config(state=state)
		self.ent_time.config(state=state)
		self.ent_max_random.config(state=state)
		self.but_begin.config(state=state)

	def state_game_items(self, state):
		## Fonction sans parametres permettant de rapidement modifier l'etat des widgets
		## du pannel game
		self.ent_game.config(state=state)
		self.but_test_value.config(state=state)

	def print_rules(self):
		## Fonction sans parametres, appellee quand on clique sur "regles" dans le menu
		RuleWindow = Tk()#Toplevel(master)
		RuleWindow.wm_title("Règles du jeu")
		RuleLabel = Label(RuleWindow, text='\
		Le but du jeu est de trouver en moins \n \
		de coups possibles le nombre choisi   \n \
		par l\'ordinateur                  ').pack()
		ValButton = Button(RuleWindow, text = 'Compris !', command = RuleWindow.destroy).pack()

	def update_time(self):
		## Fonction sans parametres permettant de modifier l'affichage du timer en temps reel
		
		# calcul du temps restant
		self.start = time.time()
		temps_restant = int(self.stop - self.start) + 1
		if temps_restant > 0 and self.is_game_running == True:
			str_temps = "Temps restant : " + str(temps_restant)
			self.txt_time.config(text=str_temps)
		elif temps_restant <= 0:
			self.txt_indice.config(text="Perdu !")
			self.txt_statut.config(text="Le nombre mystère était " + str(self.secret_number))
			self.state_game_items("disable")
			self.state_config_items("normal")

## Programme Principal
if __name__ == '__main__':
	root = Tk()
	my_gio = MainWindow(root) # On crée un instance de la classe MainWindow avec en paramètre une fenêtre Tk

	# L'utilisation d'un while True permet d'ajouter la gestion
	# de l'evenement d'affichage du temps a chaque tour de boucle
	while True:
		root.update_idletasks()
		root.update()
		if my_gio.timer > 0 : # On affiche le timer uniquement si l'utilisateur en a demandé un
			my_gio.update_time()
