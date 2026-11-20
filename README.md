# Analyse des cycles économiques au Maroc (2007–2019)

## Présentation

Une analyse empirique des cycles économiques au Maroc,
réalisée à l'aide de Python, du filtre de Hodrick–Prescott
et de tests de corrélation de Pearson.

Le projet examine les fluctuations du PIB réel,
de la consommation, de l'investissement, du commerce extérieur,
des prix et des taux d'intérêt.

## Contexte académique

- Université : Université Mohammed VI Polytechnique
- Faculté : FGSES
- Module : ECO202 — Macroéconomie I
- Enseignant : Pr Faiçal Hossaini
- Année universitaire : 2026–2027

Ce dépôt documente ma contribution individuelle
(questions 6 à 9) à un travail académique collectif.

## Contributeurs

- Saad EL BASSRAOUI — Questions 1 à 5
- Soulaimane ALOUANE — Questions 6 à 9
- Yahya MOUTEI — Questions 10 à 13

Le code et l'analyse présentés ici se concentrent
sur ma contribution, et non sur l'ensemble du travail de groupe.

## Méthodologie

- Données macroéconomiques annuelles : 2007–2019
- Filtre de Hodrick–Prescott (lambda = 100)
- Transformations logarithmiques
- Décomposition tendance-cycle
- Corrélations de Pearson et tests de significativité
- Interprétation historique basée sur les rapports de l'article IV du FMI

## Résultat principal

La composante cyclique de la consommation des ménages
présente une corrélation positive avec le cycle du PIB réel
(r = 0,757, p-value = 0,0027).

Ces résultats ont une portée exploratoire, compte tenu de la
taille réduite de l'échantillon et des limites statistiques
du filtre de Hodrick–Prescott.

## Exécution de l'analyse

Installez les dépendances :

pip install -r requirements.txt

Placez le jeu de données annuel à l'emplacement suivant :

data/macro_annual.csv

Exécutez :

python business_cycle_analysis.py