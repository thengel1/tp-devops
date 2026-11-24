# TP Observabilité

## Réponses aux questions

1. **Quelle est la différence entre Prometheus et Grafana ?**

   Prometheus collecte les métriques de Node Exporter et les stocke dans une base de données. Grafana interroge Prometheus uniquement pour pouvoir visualiser les métriques en créant des tableaux de bord détaillés.

2. **Quel est le rôle de Node Exporter ?**

   Son rôle est de collecter les métriques brutes du système d'une machine Linux (CPU, RAM, disque, réseau, etc). Il les met en forme et les expose par HTTP pour que Prometheus puisse les récupérer.

3. **Que signifie le terme scraping ?**

   Le scraping est le fait d'interroger automatiquement et régulièrement des pages web par HTTP. Ici c'est Prometheus qui interroge régulierement Node Exporter.

4. **À quoi sert le fichier `prometheus.yml` ?**

   C'est le fichier de configuration principal de Prometheus. On y définit la fréquence de scraping et la liste des services à scraper.

5. **Pourquoi Grafana utilise-t-il l'adresse `prometheus:9090` ?**

   Car rafana et Prometheus tournent dans des conteneurs séparés mais dans le même réseau docker, et `prometheus` est l'adresse répertoriée dans le DNS de ce réseau.

6. **À quoi sert PromQL ?**

   C'est le langage de requête utilisé par Prometheus. Il sert à créer des requêtes pour filtrer les métriques stockées ou calculer des statistiques.

7. **Pourquoi utilise-t-on des volumes Docker ?**

   Pour avoir des données persistantes. Sans volume, tout le contenu d'un conteneur docker est supprimé quand il est détruit. Avec volumes, les données sont sauvegardées dans un répertoire en dehors du conteneur.

8. **Que se passe-t-il lorsqu'une target passe à l'état DOWN ?**

   Prometheus ne peut plus collecter ses métriques. La valeur de la métrique up passe à 0 et les graphiques dans Grafana qui utilisent ces métriques ne peuvent plus être mis à jour.

9. **Pourquoi est-il important de surveiller les ressources CPU, RAM et disque ?**

   Pour détecter les anomalies et anticiper les pannes de serveurs.

10. **Expliquer la différence entre les états UP et DOWN.**

    UP indique que Prometheus arrive bien à atteindre sa cible et collecter les métriques. DOWN indique le contraire, c'est à dire quand la cible est innaccessible.

11. **Pourquoi utilise-t-on la fonction `rate()` pour calculer l'utilisation CPU ?**

    Car la métrique CPU est un compteur qui se cummule depuis le démarrage de la machine. La fonction rate() permet de calculer le taux d'évolution par seconde pour connaître le taux d'utilisation au moment présent.

12. **Pourquoi exclut-on généralement l'interface `lo` ?**

    L'interface lo correspond au réseau interne de la machine vers elle-même. On l'exclut pour mesurer uniquement les échanges avec l'extérieur.
