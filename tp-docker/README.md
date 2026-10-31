# tp-docker - réponses aux questions

## Exercice 1

1. **Quel est le rôle du processus principal dans un conteneur ?**

   Il gère l'état du vie du conteneur. Le conteneur passe en exited si le processus principal s'arrête.

2. **Quelle différence existe-t-il entre `docker stop` et `docker kill` ?**

   Docker stop envoie un signal SIGTERM au conteneur, qui permet un arrêt propre en laissant le temps de faire les sauvegardes, etc. docker kill envoie un signal SIGKILL au conteneur qui va le stopper immédiatement.

3. **Pourquoi un conteneur s'arrête-t-il lorsque son processus principal se termine ?**

   Car le conteneur n'a qu'un processus initial. Quand toutes les tâches sont terminées, le processus principal s'arrête.

4. **Quelle différence existe-t-il entre `SIGTERM` et `SIGKILL` ?**

   SIGTERM transmet l'instruction de s'éteindre proprement, alors que SIGKILL est exécuté directement par le système d'exploitation pour un arrêt immédiat.

5. **Pourquoi est-il important qu'une application gère correctement les signaux d'arrêt ?**

   Pour éviter de corrompre des données en cours d'écriture.

## Exercice 2

1. **Quelle différence existe-t-il entre les couches d'une image et la couche inscriptible d'un conteneur ?**

   Les couches de l'image sont en lecture seule et peuvent être partagées entre plusieurs conteneurs, alors que la couche inscriptible est temporaire et seulement pour un conteneur spécifique.

2. **À quoi sert le mécanisme _copy-on-write_ ?**

   Il permet de copier un fichier de l'image vers la couche inscriptible uniquement quand on veut le modifier. Cela permet d'économiser énormément d'espace disque car tout les fichiers non modifié restent dans la courche image.

3. **Pourquoi les modifications effectuées dans un conteneur ne modifient-elles pas directement l'image d'origine ?**

   Car l'image de base est ne dépend pas des conteneurs créés à partir d'elle, elle ne change pas.

4. **À quoi sert la commande `docker diff` ?**

   Elle liste toutes les differences de fichiers entre le conteneur et son image (tous les fichiers crées dans le conteneur et tous les fichiers copiés et modifié de l'image à la couche insciptible).

5. **Pourquoi les modifications apportées à la couche inscriptible sont-elles perdues lorsqu'on supprime le conteneur ?**

   Car la couche inscriptible fait entièrement partie du conteneur.

## Exercice 3

1. **Pourquoi utiliser plusieurs instructions `FROM` ?**

   cela permet de diviser le travail : une étape pour compiler le code avec toutes les dépendances nécessaires, puis une autre qui ne contient que l'application compilée à faire tourner.

2. **Quelle différence existe-t-il entre l'étape `builder` et l'étape finale ?**

   Le builder contient toutes les bibliothèques et le compilateur. L'étape finale contient seulement les fichiers nécessaire pour exécuter le programme.

3. **Pourquoi l'image finale ne contient-elle pas le compilateur Go ?**

   Parce qu'une fois que l'exécutable est créé, le compilateur ne sert plus à rien. Cela permet de gagner de l'espace.

4. **Quels sont les avantages d'une image finale minimale ?**

   Elle prend moins d'espace et se déploie beaucoup plus vite sur les serveurs.

5. **Quelles précautions faut-il prendre avant d'utiliser une image `scratch` en production ?**

   Il faut s'assurer que le programme compilé embarque toutes ses dépendances.

## Exercice 4

1. **Pourquoi est-il préférable d'exécuter une application avec un utilisateur non privilégié ?**

   En cas d'intrusion dans le conteneur, l'attaquant aura des droits qui l'empêcheront de modifier le système.

2. **Que sont les capacités Linux ?**

   Ce sont des privilèges de root que l'on peut activer / désactiver un à un. Cela permet de donner au programme uniquement les droits nécessaire pour faire tourner le programme.

3. **Quelle différence existe-t-il entre `--read-only` et `--tmpfs` ?**

   --read-only interdit strictement toute écriture sur le disque dur, et --tmpfs permet d'écrire des fichiers temporaires en RAM utiles au déroulement du programme.

4. **Pourquoi un conteneur peut-il avoir besoin de zones inscriptibles malgré un système de fichiers racine en lecture seule ?**

   Car toutes les applications ont besoins de créer des fichier temporaires (cache, logs, etc.)

5. **Ces options suffisent-elles à garantir une isolation parfaite ? Justifiez votre réponse.**

   Non car le conteneur partage le noyau de la machine hôte et le risque 0 n'existe pas.

## Exercice 5

1. **Quelle différence existe-t-il entre un conteneur arrêté et un conteneur supprimé ?**

   Un conteneur arrêté est en pause et peut être relancé, les données ne sont pas supprimées. Un conteneur supprimé n'existe plus du tout.

2. **Que signifie un code de sortie différent de zéro ?**

   Cela signifie que le programme ne s'est pas terminé normalement.

3. **Quelle différence existe-t-il entre les sorties standard et d'erreur ?**

   La sortie standard affiche le fonctionnement normal du programme, et la sortie d'erreur est spécifique aux alertes d'erreurs.

4. **Pourquoi les journaux sont-ils utiles lorsqu'un conteneur se termine trop rapidement ?**

   Car ils permettent de comprendre pourquoi il s'est terminé trop vite, et remonter la trace de l'erreur.

5. **Pourquoi faut-il examiner le code de sortie au lieu de se fier uniquement au message d'erreur ?**

   Car le code de sortie indique clairement de quelle manière le programme c'est terminé, et parce que le message d'erreur peut potentiellement être aussi trompeur ou imcomplet par exemple.

## Exercice 6

1. **Pourquoi des journaux trop volumineux peuvent-ils poser problème ?**

Car ils peuvent envahir l'espace de stockage et potentiellement faire planter d'autres programmes.

2. **À quoi sert un pilote de journaux Docker ?**

   Le pilote de journaux permet de choisir le format et la destination des logs (les garder localement ou les envoyer sur un serveur distant).

3. **Quelle différence existe-t-il entre la consultation des journaux avec `docker logs` et leur stockage sur le long terme ?**

   docker logs permets de lire les fichiers de logs temporaires du conteneur, alors qu'un stockage à long terme permets d'archiver les logs en dehors du conteneur.

4. **Pourquoi la rotation des journaux est-elle importante sur un serveur ?**

   La roatation des journaux est importante pour respecté l'espace de stockage alloué aux logs, en supprimant les plus anciens pour insérer les nouveaux.

5. **Pourquoi faut-il choisir une stratégie de journalisation adaptée à l'environnement de production ?**

   Car chaque production a des contraintes de performances et de sécurité différentes, qui implique de tracer les erreurs efficacement en évitant de stocker trop de données.

## Exercice 7

1. **Quelle différence existe-t-il entre `docker exec` et `docker run` ?**

   run crée et démarre un nouveau conteneur, et exec permet de rentrer dans un conteneur en cours pour lancer de nouvelles commandes.

2. **À quoi sert `docker top` ?**

   Cela sert à lister tout les processus qui tournent dans le conteneur.

3. **Pourquoi `docker diff` peut-il être utile pendant un diagnostic ?**

   Car cela permet de vérifier rapidement si un fichier à été crée ou modifié anormalement.

4. **Quelles informations fournit `docker stats` ?**

   docker stats fourni la consommation CPU, RAM et réseau en temps réel du conteneur.

5. **Pourquoi faut-il éviter de modifier manuellement un conteneur en production sans documenter les changements ?**

   Car dans un conteneur en cours, ces changements sont éphèmères, et seraient perdus si le conteneur est recréé.

## Conclusion sur les améliorations apportées à l'image et à la sécurité du conteneur.

Au niveau de l'image, un Dockerfile multi-stage permet de garder uniquement les fichiers nécessaire au fonctionnement du programme, en se passant du compilateur par exemple, ce qui réduit la taille de l'image.

Au niveau de la sécurité, les risques peuvent être limités en utilisant un utilisateur autre que root pour garder uniquement les privilèges basiques, en utilisant un système de fichiers en lecture seule, et en utilisant un configuration propre des logs pour bien tracer les erreurs sans envahir l'espace de stockage.
