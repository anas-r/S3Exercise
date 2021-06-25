# S3Exercise

## Description

Un script permettant de synchroniser un dossier local et un bucket distant sur Amazon S3. La comparaison entre les differents fichiers se fait sur la base de leur md5 checksum, en prenant l'hypothèse que l'ETag extrait des objets dans le bucket correspondent bien à des md5 checksum, c'est-à-dire, que les fichiers ont été uploadés en un seul fragment (pas de fractionnement). Voir la doc S3 pour plus d'explications sur ce sujet.

Ce mode de comparaison permet à la fois de traîter tous les cas de l'exercice : upload, delete, update et de les regrouper simplement en upload et delete. Un fichier qui a été mis à jour sur le local sera considéré comme un nouveau fichier (uploadé au bucket), tandis que son la version non mise à jour sur bucket sera considéré comme un fichier "superflu" (supprimé du bucket). 

## Test
Il est impératif de modifier les paramètres globaux de connexion dans le fichier config.py avant de lancer les scripts. Il est aussi conseillé de lancer en premier lieu le script `gen_alea.py` qui permet d'instaurer un scénario de test: 20 fichiers sera créés aléatoirement et uploadés au bucket, ensuite 10 des 20 seront modifiés sur le local, puis 10 nouveaux fichiers seront créés sur le local seulement.

**Exemple de commande:** ``/bin/python3 /home/anasr/Documents/S3Exercise-main/gen_alea.py **NOM_DU_BUCKET**``

Il est ainsi possible de lancer le script `s3_ex_anas_rachyd.py`.

**Exemple de commande:** ``/bin/python3 /home/anasr/Documents/S3Exercise-main/s3_ex_anas_rachyd.py **CHEMIN_COMPLET_VERS_LE_DOSSIER** **NOM_DU_BUCKET**``
Dans le cas courant, ``**CHEMIN_COMPLET_VERS_LE_DOSSIER**`` peut être ``/home/anasr/Documents/S3Exercise-main/random``.
