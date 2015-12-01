from math import floor

import unittest
import random
import os.path

#*********************************************************************************
# Laila Zouaki
# TP5
#*********************************************************************************



class Test(unittest.TestCase):

	def test_fichier_vide(self):
		generer_fichier("test_vide.txt", 0)
		self.assertEqual(processus_complet("test_vide.txt"), [])

	def test_mauvais_format(self):
		self.assertEqual(processus_complet("test_mauvais_format.txt"), [])

	def test_mauvais_path(self):
		self.assertEqual(processus_complet("some_false_path.txt"), [])

	def test_valeurs_aleatoires(self):
		arbre = Arbre()
		liste_aleatoire = [random.randint(1,100) for i in range(1000)]
		arbre.inserer_liste(liste_aleatoire)
		self.assertTrue(verifier_tri(arbre))

	def test_grand_fichier(self):
		generer_fichier("grand_fichier.txt", 10000)
		valeurs_prioritaires = processus_complet("grand_fichier.txt")
		arbre = Arbre()
		arbre.inserer_liste(valeurs_prioritaires)
		self.assertTrue(verifier_tri(arbre))


class Arbre:
	def __init__(self):
		self.tableau = []

	def valeur_max(self):
		return self.tableau[0]

	def fils_gauche(self, indice_parent):
		if 2*indice_parent+1 >= len(self.tableau):
			return None

		return 2*indice_parent+1

	def fils_droit(self, indice_parent):
		if 2*indice_parent+2 >= len(self.tableau):
			return None
			
		return 2*indice_parent+2

	def indice_parent(self, indice_fils):
		return floor((indice_fils-1)/2)

	def inserer_element(self, element):
		self.tableau.append(element)
		indice = len(self.tableau)-1
		while indice != 0 and self.tableau[indice] > self.tableau[self.indice_parent(indice)]:
			self.tableau[indice], self.tableau[self.indice_parent(indice)] = self.tableau[self.indice_parent(indice)], self.tableau[indice]
			indice = self.indice_parent(indice)

	def inserer_liste(self, liste):
		for element in liste:
			self.inserer_element(element)

def ouvrir_fichier(path):
	lignes_fichier = []	
	try:
		with open(path, "r") as fichier:
			for line in fichier:
				lignes_fichier.append(line)

		return lignes_fichier
	except FileNotFoundError:
		return []

def valeurs_prioritaires(lignes_fichier):

	valeurs_priorite = []

	for ligne in lignes_fichier:
		for indice, caractere in enumerate(ligne):
			if caractere == ":":
				valeurs_priorite.append(int(ligne[:indice]))
				break

	return valeurs_priorite


def verifier_tri(arbre):
	for indice, element in enumerate(arbre.tableau):
		if arbre.fils_gauche(indice) != None and element < arbre.tableau[arbre.fils_gauche(indice)]:
			return False

		if arbre.fils_droit(indice) != None and element < arbre.tableau[arbre.fils_droit(indice)]:
			return False

	return True


def queue_prioritaire(valeurs_prioritaires):
	arbre = Arbre()
	for valeur in valeurs_prioritaires:
		arbre.inserer_element(valeur)

	return arbre.tableau	

def processus_complet(path):
	lignes_fichier = ouvrir_fichier(path)
	valeurs_priorite = valeurs_prioritaires(lignes_fichier)
	liste_prioritaire = queue_prioritaire(valeurs_priorite)

	return liste_prioritaire

def generer_fichier(path, nombre_lignes):
	if not os.path.exists(path):
		with open(path, "w") as fichier:
			for i in range(nombre_lignes):
				fichier.write(str(random.randint(1,1000)) + ": random_task\n")

if __name__ == "__main__":

	liste_prioritaire = processus_complet("taches_prioritaires.txt")	
	print(liste_prioritaire)

	unittest.main()


