from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import torch
sections = pd.read_csv("parcelles/01-reseau-neurones/donnees/sections_2025.csv")

print(sections.head())
print(len(sections), 'sections')

colonnes_entree = ["djma", "djme", "djmh"]
colonne_sortie = "trentieme_heure"

entrees = torch.tensor(sections[colonnes_entree].values, dtype=torch.float32)
# Doubles crochets : la sortie reste une colonne (3680, 1), comme ce que le réseau va produire.
sortie = torch.tensor(sections[[colonne_sortie]].values, dtype=torch.float32)

print(entrees.shape, sortie.shape)

# Graine fixe : même mélange et mêmes poids de départ à chaque lancement, donc mêmes résultats.
torch.manual_seed(0)
ordre_melange = torch.randperm(len(entrees))
nombre_entrainement = int(0.8*len(entrees))

# Le « : » coupe la liste mélangée en deux morceaux qui ne se chevauchent pas :
#   [7, 2, 9, 0, 4, 8, 1, 6 | 3, 5]   →   [:8] = entraînement (80 %)   [8:] = test (20 %)
indices_entrainement = ordre_melange[:nombre_entrainement]
indices_test = ordre_melange[nombre_entrainement:]

# Mêmes indices pour les entrées et la sortie : le DJMA d'une section reste collé à SA 30e heure.
entrees_entrainement, sortie_entrainement = entrees[indices_entrainement], sortie[indices_entrainement]
entrees_test, sortie_test = entrees[indices_test], sortie[indices_test]

'''
étape . normalisation des données
'''
# Moyenne et écart-type calculés sur l'entraînement SEULEMENT, puis appliqués au test : sinon le test fuit.
# C'est un changement d'unités pour le réseau ; il garde les proportions (une autoroute reste énorme).
moyenne_entrees = entrees_entrainement.mean(dim=0)
ecart_type_entrees = entrees_entrainement.std(dim=0)
entrees_entrainement = (entrees_entrainement - moyenne_entrees) / ecart_type_entrees
entrees_test = (entrees_test - moyenne_entrees) / ecart_type_entrees

moyenne_sortie = sortie_entrainement.mean()
ecart_type_sortie = sortie_entrainement.std()
sortie_entrainement = (sortie_entrainement - moyenne_sortie) / ecart_type_sortie
sortie_test = (sortie_test - moyenne_sortie) / ecart_type_sortie

print(entrees_entrainement.mean(dim=0), entrees_entrainement.std(dim=0))

# Le 2e nombre d'une couche = le 1er de la suivante : 3 → 32 → 16 → 1.
reseau = torch.nn.Sequential(
    torch.nn.Linear(len(colonnes_entree), 32),
    torch.nn.ReLU(),
    torch.nn.Linear(32,16),
    torch.nn.ReLU(),
    # Pas de ReLU à la fin : la sortie mise à l'échelle peut être négative, ReLU la bloquerait à 0.
    torch.nn.Linear(16,1)
)

print(sum(parametre.numel() for parametre in reseau.parameters()), 'paramètres')



'''
étape . entraînement du réseau
'''
fonction_cout = torch.nn.MSELoss()
optimiseur = torch.optim.SGD(reseau.parameters(), lr=0.01)


'''
étape . boucle d'entraînement
'''
taille_mini_lot = 100
nombre_epoques = 100

courbe_apprentissage = []  # ajouté par Claude : garde les coûts pour le graphique de la page

for epoque in range(nombre_epoques):
    ordre_mini_lots = torch.randperm(len(entrees_entrainement))

    # Mesuré AVANT l'apprentissage de l'époque : l'époque 0 montre le réseau pas encore entraîné.
    if epoque % 10 == 0 or epoque == nombre_epoques - 1:
        with torch.no_grad():
            cout_entrainement = fonction_cout(reseau(entrees_entrainement), sortie_entrainement)
            cout_test = fonction_cout(reseau(entrees_test), sortie_test)
        print(f"époque {epoque} : coût entraînement {cout_entrainement.item():.4f}, coût test {cout_test.item():.4f}")
        courbe_apprentissage.append((epoque, round(cout_entrainement.item(), 4), round(cout_test.item(), 4)))  # ajouté par Claude

    # range(0, 2944, 100) donne 0, 100, …, 2900 : 30 débuts de lots ; le dernier lot n'a que 44 sections.
    for debut in range(0,len (entrees_entrainement), taille_mini_lot):
        indices_lot = ordre_mini_lots[debut:debut + taille_mini_lot]
        prediction = reseau(entrees_entrainement[indices_lot])
        cout = fonction_cout(prediction, sortie_entrainement[indices_lot])
        optimiseur.zero_grad()  # sinon PyTorch ADDITIONNE les gradients d'un lot à l'autre
        cout.backward()         # rétropropagation : calcule les 673 coups de pouce (vidéo 3)
        optimiseur.step()       # un pas vers le bas avec ces coups de pouce (vidéo 2)

'''
étape . évaluation du réseau et comparaison avec d'autres modèles
'''
# `sortie` (en véhicules), pas `sortie_test` (mise à l'échelle) : la note se donne en véhicules.
vraie_30e_heure_test = sortie[indices_test]

resultats = []  # ajouté par Claude : garde les notes pour le tableau de la page


def afficher_erreur(nom_modele, prediction):
    ecart = (prediction - vraie_30e_heure_test).abs()
    erreur_relative = (ecart / vraie_30e_heure_test).mean()
    print(f"{nom_modele} : erreur moyenne de {ecart.mean().item():.0f} véhicules, soit {100 * erreur_relative.item():.1f} %")
    resultats.append((nom_modele, round(ecart.mean().item()), round(100 * erreur_relative.item(), 1)))  # ajouté par Claude


with torch.no_grad():
    # On défait la mise à l'échelle : × écart-type + moyenne, pour revenir en véhicules.
    prediction_reseau = reseau(entrees_test) * ecart_type_sortie + moyenne_sortie
afficher_erreur("Réseau", prediction_reseau)

djma = torch.tensor(sections[["djma"]].values, dtype=torch.float32)
# Le ratio vient de l'entraînement seulement, comme la mise à l'échelle.
ratio_median = (sortie[indices_entrainement] / djma[indices_entrainement]).median()
prediction_regle = ratio_median * djma[indices_test]
afficher_erreur(f"Règle {ratio_median.item():.3f} × DJMA", prediction_regle)


# La forêt prend `entrees` brutes : un arbre pose des questions (« DJMA > 5000 ? »), l'échelle ne change rien.
# .ravel() : (2944, 1) → (2944,) pour scikit-learn ; .unsqueeze(1) : (736,) → (736, 1) pour comparer.
foret = RandomForestRegressor(random_state=0)
foret.fit(entrees[indices_entrainement], sortie[indices_entrainement].ravel())
prediction_foret = torch.tensor(foret.predict(entrees[indices_test]), dtype=torch.float32).unsqueeze(1)
afficher_erreur("Forêt aléatoire", prediction_foret)


# Ajouté par Claude : les petits CSV de résultats qui alimentent la page de la station.
pd.DataFrame(resultats, columns=["modele", "erreur_vehicules", "erreur_pourcentage"]).to_csv(
    "parcelles/01-reseau-neurones/resultats.csv", index=False)
pd.DataFrame(courbe_apprentissage, columns=["epoque", "cout_entrainement", "cout_test"]).to_csv(
    "parcelles/01-reseau-neurones/courbe_apprentissage.csv", index=False)
