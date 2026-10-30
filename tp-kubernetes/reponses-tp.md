## Partie 1 — Explorer l’architecture Kubernetes

### Questions

1. **Quel est le rôle du control plane ?**

   Son rôle est d'administrer le cluster. Il reçoit les commandes kubectl et applique les changements a autres noeuds.

2. **Quelle différence existe-t-il entre un nœud Kubernetes et un Pod ?**

   Un noeud Kubernetes est la machine virtuelle qui fournit les coeurs CPU et la RAM. Un pod est un élèment hebergé sur le noeud et qui contient un ou plusieurs conteneurs.

3. **Quel contrôleur maintient le nombre de réplicas demandé par un Deployment ?**

   C'est le ReplicaSet qui vérifie rérgulièrement que le nombre de réplicas correspond au nombre demandé par le Deployment.

4. **Quelle différence existe-t-il entre un conteneur et un Pod ?**

   Un conteneur contient une application et ses dépendances. Un pod est un élèment qui heberge un ou plusieurs de ces conteneurs.

5. **Quelles limites présente un cluster local à un seul nœud par rapport à un cluster de production ?**

   Dans un cluster à un noeud, les applications ne fonctionneront plus si le noeud tomba en panne. Les ressources / performances de calculs sont aussi limités par ce qui est alloué au noeud.

### Réalisez un schéma simple du cluster local et expliquez le rôle des composants que vous avez identifiés.

```
Machine hôte
    |
    |---Noeud Kubernetes
              |
              |----Control Pane :
              |          Reçoit les commandes kubectl
              |          et administre les pods
              |
              |----Worker Node
                        |
                        |----Pod 1
                        |       |-----Conteneur 1
                        |       |         |-----Application
                        |       |
                        |       |-----Conteneur 2
                        |       |          |....
                        |       |...
                        |
                        |----Pod 2
                        |       | .....
                        |
                        |....
```

## Partie 2 — Déployer une application web

### Créer un namespace

**Question 2.** **Quel intérêt présente un namespace dans un environnement partagé entre plusieurs équipes ?**

Un namespace permets aux équipe de créer des application qui porte le même nom, et permets de mettre des quotas de RAM / CPU.

### Créer une page web avec une ConfigMap

**Question 3.** **Pourquoi utiliser une ConfigMap plutôt que d’intégrer directement la page dans le manifeste du Deployment ?**

Pour pouvoir modifier le contenu de la page sans avoir à reconstruire l'image.

### Questions

1. **Quel est le rôle du Deployment par rapport au ReplicaSet ?**

   Le ReplicaSet vérifie le bon fonctionnement des pods, et le Deployment gère les mises à jours.

2. **Pourquoi ne pas accéder directement aux adresses IP des Pods ?**

   Car les pods sont éphémères, et leur adresse IP change quand ils sont recréés.

3. **Quelle différence existe-t-il entre `ClusterIP`, `NodePort` et `LoadBalancer` ?**

   ClusterIs rend l'application visible uniquement depuis l'intérieur du cluster, NodePort ouvre un port sur la machine hôte pour accéder à l'application depuis l'extérieur, et LoadBalancer utilise un cloud pour exposer l'application sur internet.

4. **Quelle différence existe-t-il entre une readiness probe et une liveness probe ?**

   Le readiness probe indique si un pod est prêt à recevoir les requêtes extérieures, et la liveness indique si le pod est bien en vie ou si il a besoin d'être recréé.

5. **Que peut-il se passer si une limite mémoire est trop basse ?**

   Si l'application consomme plus de mémoire que le quota attribué, le processus de l'application et arrêté de force et son conteneur est détruit avant d'être recréé. Un limite mémoire trop basse provoquera trop souvent cela.

## Partie 3 — Résilience et auto-rétablissement (40 min)

1. **Pourquoi le Pod supprimé est-il remplacé ?**

   Car le ReplicaSet surveille en permanence qu'il y a bien le nombre de pods demandés en vie. Si un pod est supprimé, il enclenche la création d'un nouveau immédiatement.

2. **Quelle différence existe-t-il entre la suppression d’un Pod et l’arrêt d’un processus dans un conteneur ?**

   Supprimer un pod détruit tout l'élèment et ses propriété, comme son adresse IP. Arrêter un pod ne le détruit pas et il conserve toutes les données au redémarrage.

3. **Pourquoi un redémarrage de conteneur ne signifie-t-il pas nécessairement que le cluster entier est en panne ?**

   Car un conteneur peut redémarrer à cause d'un bug venant de l'application qu'il héberge, indépendant des autres conteneurs.

4. **Que se passerait-il si le nœud unique de Minikube devenait indisponible ?**

   Plus aucun pods ne serait accessible car il n'y a pas de relais pour le noeud de Minikube.

5. **Pourquoi un cluster local à un seul nœud ne permet-il pas de démontrer la tolérance à la panne d’un nœud physique ?**

   Car si le noeud devient indisponible / tombe en panne, alors tous les pods deviennent inaccessible. L'intérêt de Kubernetes est d'avoir plusieurs noeuds pour transférer les pods d'un noeud qui tombe en panne vers un noeud sain.

## Partie 4 — Mise à l’échelle et découverte de services

1. **Quelle différence existe-t-il entre la mise à l’échelle manuelle et l’autoscaling ?**

   La mise à l'échelle manuelle nécessite qu'un humain tape la commande pour changer le nombre de pods, alors que l'autoscaling change le nombre de pods automatiquement en fonction du traffic de requêtes et de la consomation CPU.

2. **Quel est le rôle d’un Horizontal Pod Autoscaler (HPA) ?**

   Il observe les performances et augmente / diminue automatiquement le nombre de pods.

3. **Pourquoi un HPA basé sur le CPU nécessite-t-il des métriques et des ressources correctement configurées ?**

   Car le HPA prend ses décisions en se basant sur le pourcentage de consomation CPU par rapport à la limite fixé. Si il n'y a pas de limites, le HPA ne déclenchera pas d'autoscaling.

4. **Pourquoi quatre réplicas sur un seul nœud ne garantissent-ils pas la disponibilité en cas de panne de ce nœud ?**

   Car si le noeud tombe en panne, tout les pods qu'il contient deviennent indisponible.

## Partie 5 — Mise à jour et retour arrière

1. **Que signifie la stratégie `RollingUpdate` ?**

   C'est une stratégie de mise à jour des pods où pour chaque pod (un à la fois), un nouveau pod mis à jour est démarré puis seulement quand ce nouveau pod est prêt, supprimer l'ancien pod. Cela permets de garder le service disponible, plutôt que de couper et mettre à jour tous les pods en même temps, qui mettrais en pause le service.

2. **Pourquoi une mise à jour progressive ne garantit-elle pas, à elle seule, une disponibilité parfaite ?**

   Le risque est que la nouvelle version de l'application contiennent un bug. Car Kubernetes supprime les anciens pods avant de savoir si les nouveaux fonctionnent correctement.

3. **Dans quelles conditions `rollout undo` fonctionne-t-il ?**

   Il ne fonctionne que pour annuler des modifications faites sur le Deployment, pas pour des modifications sur une ancienne ConfigMap pas exemple.

4. **Pourquoi faut-il versionner les configurations et planifier les migrations de base de données séparément ?**

   Car la base de données peut changer de schéma entre plusieurs versions. Si les pods et la base sont mis à jour, après un undo l'application reviendra en arrière mais pas le schéma de la base, et l'application ne pourras plus lire la base correctement.

## Partie 6 — Diagnostic et dépannage

Pour chaque incident, suivez une démarche structurée : **symptôme → hypothèse → diagnostic → correction → vérification**.

### Incident A — Image introuvable

- **Quel état observez-vous ?**

  Un nouveau pod a été créé, d'abors avec le status ImagePullBackOff puis ErrImagePull.

- **Quel événement indique la cause probable ?**

  Dans la liste des events : "failed to pull and unpack image docker.io/library/unexistingimage:latest [...]"

- **Comment corriger le manifeste et vérifier le retour à la normale ?**

  Il faut réappliquer la bonne config : `kubectl apply -f k8s/03-deployment.yaml`, puis vérifier que les pods sont bien en état running.

### Incident B — Service inaccessible

- **Pourquoi le Service n’a-t-il plus de destination exploitable ?**

  Car le service identifie les pods grâce à son selector. Si l'étiquette d'un pod change mais que le selector n'est pas mis à jour, alors le service ne trouvera plus le pod.

- **Pourquoi les Pods peuvent-ils être opérationnels alors que l’application est inaccessible via le Service ?**

  L'application peut très bien tourner à l'intérieurs des pods, même si la communication entre les pods et le service est coupées, mais alors plus aucun traffic réseau ne leur est envoyé.

- **Quelle correction permet de rétablir le routage ?**

  Il faut remettre le selector du service pour qu'il corresponde bien à la sections labels dans le Deployment -> labels.

### Incident C — Sonde de santé incorrecte

- **Quel est l’effet d’une readiness probe en échec ?**

  L'état du pod est bien Running mais READY n'est pas activé (0/1). Le service coupe alors la connextion avec lui.

- **En quoi son effet diffère-t-il de celui d’une liveness probe en échec ?**

  Si une readiness échoue, cela isole le pod du réseau sans détruire de conteneur, alors que si une liveness échoue, le conteneur est détruit et recréé.

- **Pourquoi une sonde mal configurée peut-elle provoquer une indisponibilité ?**

  Car une erreur d'URL au niveau de la sonde fera passer le conteneur comme en panne alors que l'application peut très bien tourner. Si cela arrive dans tout les pods, cela va provoquer une panne générale.
