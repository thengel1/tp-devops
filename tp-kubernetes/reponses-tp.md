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

   Le readiness probe indique si un pod est prêt à recevoir les requêtes extérieures, et la liveness indique si le pod est bien en vie ou si il a besoin d'être redémarré.

5. **Que peut-il se passer si une limite mémoire est trop basse ?**

   Si l'application consomme plus de mémoire que le quota attribué, le processus de l'application et arrêté de force et son conteneur est détruit avant d'être recréé. Un limite mémoire trop basse provoquera trop souvent cela.

## Partie 3 — Résilience et auto-rétablissement (40 min)

1. **Pourquoi le Pod supprimé est-il remplacé ?**
2. **Quelle différence existe-t-il entre la suppression d’un Pod et l’arrêt d’un processus dans un conteneur ?**
3. **Pourquoi un redémarrage de conteneur ne signifie-t-il pas nécessairement que le cluster entier est en panne ?**
4. **Que se passerait-il si le nœud unique de Minikube devenait indisponible ?**
5. **Pourquoi un cluster local à un seul nœud ne permet-il pas de démontrer la tolérance à la panne d’un nœud physique ?**
