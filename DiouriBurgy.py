# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:34:36 2024

@author: isdio
"""

from tkinter import *
from random import randint
from tkinter import colorchooser

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Forme:
    def __init__(self, canevas, x, y):
        self.__canevas = canevas
        self.__item = None
        self.x = x
        self.y = y
    
    def effacer(self):
        self.__canevas.delete(self.__item)
    
    def deplacement(self, dx, dy):
        self.__canevas.move(self.__item, dx, dy)
        self.x += dx
        self.y += dy
        
    def get_cavenas(self):
        return self.__canevas
    
    def set_item(self,item):
        self.__item = item
    
    def get_item(self):
        return self.__item

    def set_state(self, s):
        self.__canevas.itemconfig(self.__item, state=s)

class Rectangle(Forme):
    def __init__(self, canevas, x, y, l, h, couleur):
        Forme.__init__(self, canevas, x, y)
        item = canevas.create_rectangle(x, y, x+l, y+h, fill=couleur, state="hidden")
        self.set_item(item)
        self.__l = l
        self.__h = h
    
    def __str__(self):
        return f"Rectangle d'origine {self.x},{self.y} et de dimensions {self.__l}x{self.__h}"

    def get_dim(self):
        return self.__l, self.__h

    def set_dim(self, l, h):
        self.__l = l
        self.__h = h

    def contient_point(self, x, y):
        return self.x <= x <= self.x + self.__l and \
               self.y <= y <= self.y + self.__h

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x   = min(x0, x1)
        self.y   = min(y0, y1)
        self.__l = abs(x0 - x1)
        self.__h = abs(y0 - y1)

class Ellipse(Forme):
    def __init__(self, canevas, x, y, rx, ry, couleur):
        Forme.__init__(self, canevas, x, y)
        item = canevas.create_oval(x-rx, y-ry, x+rx, y+ry, fill=couleur, state="hidden")
        self.set_item(item)
        self.__rx = rx
        self.__ry = ry

    def __str__(self):
        return f"Ellipse de centre {self.x},{self.y} et de rayons {self.__rx}x{self.__ry}"

    def get_dim(self):
        return self.__rx, self.__ry

    def set_dim(self, rx, ry):
        self.__rx = rx
        self.__ry = ry

    def contient_point(self, x, y):
        return ((x - self.x) / self.__rx) ** 2 + ((y - self.y) / self.__ry) ** 2 <= 1

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x = (x0 + x1) // 2
        self.y = (y0 + y1) // 2
        self.__rx = abs(x0 - x1) / 2
        self.__ry = abs(y0 - y1) / 2

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ZoneAffichage(Canvas):
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, master=parent, width=w, height=h, bg=c)
        self.__couleurFond = c

        # Listes des formes du pendu, dans l'ordre du dessin
        self.__listeShape = []

        # Dessin des différentes parties du pendu (base, poteau, traverse, corde, etc.)
        self.__listeShape.append(Rectangle(self, 50, 270, 200, 26, "brown"))
        self.__listeShape.append(Rectangle(self, 87, 83, 26, 200, "brown"))
        self.__listeShape.append(Rectangle(self, 87, 70, 150, 26, "brown"))
        self.__listeShape.append(Rectangle(self, 183, 67, 10, 40, "brown"))
        self.__listeShape.append(Ellipse(self, 188, 120, 20, 20, "black"))
        self.__listeShape.append(Rectangle(self, 175, 143, 26, 60, "black"))
        self.__listeShape.append(Rectangle(self, 133, 150, 40, 10, "black"))
        self.__listeShape.append(Rectangle(self, 203, 150, 40, 10, "black"))
        self.__listeShape.append(Rectangle(self, 175, 205, 10, 40, "black"))
        self.__listeShape.append(Rectangle(self, 191, 205, 10, 40, "black"))

    def cachePendu(self):
        # Cache toutes les parties du pendu (les rend invisibles)
        for f in self.__listeShape:
            f.set_state("hidden")

    def dessinePiecePendu(self, i):
        # Affiche une partie du pendu en fonction du nombre de tentatives manquées
        if i <= len(self.__listeShape):
            self.__listeShape[i - 1].set_state("normal")

class MonBoutonLettre(Button):
    def __init__(self, parent, fen, t):
        # Initialisation des boutons représentant les lettres du clavier
        Button.__init__(self, master=parent, text=t, state=DISABLED)
        self.__fen = fen
        self.__lettre = t

    def cliquer(self):
        # Gère l'événement de clic sur une lettre
        self.config(state=DISABLED)
        self.__fen.traitement(self.__lettre)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

class FenPrincipale(Tk):
    def __init__(self):
        # Initialisation de la fenêtre principale
        Tk.__init__(self)
        self.title('Jeu du pendu')
        self.configure(bg="#2687bc")  # Couleur de fond par défaut

        # Création de la barre de menu
        self.menuBar = Menu(self)
        self.config(menu=self.menuBar)
        # Création du menu "Options d'affichage" pour traiter les couleurs de l'interface
        optionsMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Options d'affichage", menu=optionsMenu)
        
        # Options pour changer les couleurs de la fenêtre et de la zone d'affichage
        optionsMenu.add_command(label="Changer couleur extérieure", command=self.choix_couleur_exterieure)
        optionsMenu.add_command(label="Changer couleur zone pendu", command=self.choix_couleur_zone_affichage)
        optionsMenu.add_command(label="Changer couleur du texte", command=self.choix_couleur_texte)

        # La barre d'outils
        barreOutils = Frame(self)
        barreOutils.pack(side=TOP, padx=5, pady=5)
        newGameButton = Button(barreOutils, text='Nouvelle partie', width=13)
        newGameButton.pack(side=LEFT, padx=5, pady=5)
        quitButton = Button(barreOutils, text='Quitter', width=13)
        quitButton.pack(side=LEFT, padx=5, pady=5)

        # Bouton Annuler pour l'Undo
        self.undoButton = Button(barreOutils, text='Annuler', width=13, command=self.annulerDernierCoup, state=DISABLED)
        self.undoButton.pack(side=LEFT, padx=5, pady=5)
        # Le canvas pour le dessin du pendu
        self.__zoneAffichage = ZoneAffichage(self, 320, 320, "#ec4062")
        self.__zoneAffichage.pack(side=TOP, padx=5, pady=5)
        # Le mot à deviner
        self.__lmot = Label(self, text='Mot :', bg="#2687bc", fg="white")
        self.__lmot.pack(side=TOP)
        
        # Le clavier
        clavier = Frame(self)
        clavier.pack(side=TOP, padx=5, pady=5)
        self.__boutons = []
        for i in range(26):
            t = chr(ord('A') + i)
            self.__boutons.append(MonBoutonLettre(clavier, self, t))
        # Placement des boutons du clavier
        for i in range(3):
            for j in range(7):
                self.__boutons[i * 7 + j].grid(row=i, column=j)
        for j in range(5):
            self.__boutons[21 + j].grid(row=3, column=j + 1)
            
        # Commandes associées aux boutons
        quitButton.config(command=self.destroy)
        newGameButton.config(command=self.nouvellePartie)
        for i in range(26):
            self.__boutons[i].config(command=self.__boutons[i].cliquer)
            
        # Commandes associées aux boutons

        self.__mot = ""
        self.__motAffiche = ""
        self.__mots = []
        self.__nbManques = 0
        self.__historique = []  # Historique pour la fonctionnalité Undo
        
        # Chargement du fichier de mots
        self.chargeMots()
        # On commence une nouvelle partie
        self.nouvellePartie()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Methode pour le changement de couleur de l'interface:
    
    def choix_couleur_exterieure(self):
        c = colorchooser.askcolor(title='Choix de la couleur extérieure')
        if c[1]:
            self.configure(bg=c[1])
            self.__lmot.config(bg=c[1])

    def choix_couleur_zone_affichage(self):
        c = colorchooser.askcolor(title='Choix de la couleur de la zone d\'affichage')
        if c[1]:
            self.__zoneAffichage.config(bg=c[1])

    def choix_couleur_texte(self):
        c = colorchooser.askcolor(title='Choix de la couleur du texte')
        if c[1]:
            self.__lmot.config(fg=c[1])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def chargeMots(self):
        # Charge la liste de mots à partir d'un fichier
        with open('mots.txt', 'r') as f:
            self.__mots = f.read().split('\n')

    def nouvellePartie(self):
        # Prépare une nouvelle partie en réinitialisant les éléments
        for i in range(26):
            self.__boutons[i].config(state=NORMAL)
            
         # Choisit un nouveau mot au hasard
        self.__mot = self.__mots[randint(0, len(self.__mots) - 1)]
        self.__motAffiche = len(self.__mot) * '*'
        self.__lmot.config(text='Mot : ' + self.__motAffiche)
        
        # Réinitialise le nombre de tentatives et efface le dessin précédent
        self.__nbManques = 0
        self.__zoneAffichage.cachePendu()
        self.__historique = []  # Réinitialiser l'historique
        self.undoButton.config(state=DISABLED)  # Désactiver le bouton Undo

    def traitement(self, lettre):
        # Gère la logique de traitement d'une lettre devinée
        cpt = 0
        lettres = list(self.__motAffiche)
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettre:
                cpt += 1
                lettres[i] = lettre

        self.__motAffiche = ''.join(lettres)
        self.__historique.append((lettre, self.__motAffiche, self.__nbManques))  # Ajouter à l'historique

        if cpt == 0:
            self.__nbManques += 1
            self.__zoneAffichage.dessinePiecePendu(self.__nbManques)
            if self.__nbManques >= 10:
                self.finPartie(False)
        else:
            self.__lmot.config(text='Mot : ' + self.__motAffiche)
            if self.__mot == self.__motAffiche:
                self.finPartie(True)

        self.undoButton.config(state=NORMAL)  # Activer le bouton Undo

    def annulerDernierCoup(self):
        if not self.__historique:
            return
        
        # Retirer la dernière tentative de l'historique
        lettre, motAffiche, nbManques = self.__historique.pop()
        self.__motAffiche = motAffiche
        self.__nbManques = nbManques

        self.__lmot.config(text='Mot : ' + self.__motAffiche)
        self.__boutons[ord(lettre) - ord('A')].config(state=NORMAL)  # Réactiver le bouton de la lettre
        self.__zoneAffichage.cachePendu()  # Cache toutes les parties du pendu

        for i in range(1, self.__nbManques + 1):
            self.__zoneAffichage.dessinePiecePendu(i)  # Redessiner les pièces du pendu

        # Désactiver le bouton Undo si plus de coups à annuler
        if not self.__historique:
            self.undoButton.config(state=DISABLED)

    def finPartie(self, gagne):
        for b in self.__boutons:
            b.config(state=DISABLED)
        self.undoButton.config(state=DISABLED)  # Désactiver le bouton Undo à la fin de la partie

        if gagne:
            self.__lmot.config(text=self.__mot + ' - Bravo, vous avez gagné')
        else:
            self.__lmot.config(text='Vous avez perdu, le mot était : ' + self.__mot)

if __name__ == '__main__':
    fen = FenPrincipale()
    fen.mainloop()
