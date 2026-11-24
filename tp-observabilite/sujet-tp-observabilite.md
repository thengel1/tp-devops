# TP : Mise en place d'une plateforme d'observabilité avec Prometheus et Grafana

## 1. Objectifs du TP

L'objectif de ce TP est de mettre en place une plateforme de supervision permettant de collecter, stocker, interroger et visualiser des métriques système.

À la fin de ce TP, vous serez capable de :

- Comprendre les principes de l'observabilité.
- Comprendre le fonctionnement de Prometheus.
- Déployer Prometheus et Grafana avec Docker Compose.
- Collecter les métriques d'une machine Linux avec Node Exporter.
- Configurer Prometheus pour récupérer les métriques.
- Connecter Grafana à Prometheus.
- Créer un tableau de bord de supervision.
- Utiliser le langage PromQL pour interroger les métriques.

## 2. Architecture cible

Nous allons utiliser trois composants :

| Composant | Rôle | Port |
|---|---|---|
| Prometheus | Collecte et stockage des métriques | 9090 |
| Grafana | Visualisation des métriques | 3000 |
| Node Exporter | Exposition des métriques système Linux | 9100 |

### Architecture

```text
                 MACHINE LINUX
                      |
                      |
              +---------------+
              |  Node Exporter|
              |    :9100     |
              +---------------+
                      |
                      | Scraping HTTP
                      |
              +---------------+
              |  Prometheus   |
              |    :9090     |
              +---------------+
                      |
                      | PromQL / API
                      |
              +---------------+
              |    Grafana    |
              |     :3000     |
              +---------------+
                      |
                      |
                 Navigateur Web
```

## 3. Prérequis

Avant de commencer, vous devez disposer de :

- Docker installé.
- Docker Compose installé (plugin `docker compose`).
- Un accès Internet pour télécharger les images Docker.
- Un navigateur Web.

Vérifier les installations :

```bash
docker --version
docker compose version
```

Si les commandes fonctionnent, vous pouvez commencer.

## 4. Création du projet

Créer l'arborescence suivante :

```text
tp-observabilite/
│
├── docker-compose.yml
│
└── prometheus/
    └── prometheus.yml
```

## 5. Déploiement avec Docker Compose

Nous allons utiliser directement les images Docker disponibles sur Docker Hub.

Images utilisées :

- `prom/prometheus`
- `grafana/grafana`
- `prom/node-exporter`

Créer le fichier `docker-compose.yml` :

```yaml
services:

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    ports:
      - "9100:9100"
    pid: host
    command:
      - '--path.rootfs=/host'
    volumes:
      - '/:/host:ro,rslave'
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

**Explication :**

- Prometheus collecte les métriques et les conserve dans un volume Docker.
- Grafana permet de visualiser les données collectées.
- Node Exporter expose les métriques système.
- Les trois conteneurs communiquent sur le réseau Docker `monitoring`.
- Les volumes assurent la persistance des données.

**Remarque :** cette configuration Node Exporter est adaptée à un environnement Linux. Elle utilise le système de fichiers de l'hôte pour exposer ses métriques. Sur une machine virtuelle ou un environnement Docker Desktop, certaines métriques peuvent différer.

## 6. Configuration de Prometheus

Créer le fichier :

`prometheus/prometheus.yml`

Ajouter la configuration suivante :

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:

  - job_name: 'prometheus'
    static_configs:
      - targets:
          - 'prometheus:9090'

  - job_name: 'node-exporter'
    static_configs:
      - targets:
          - 'node-exporter:9100'
```

**Explication :**

- `scrape_interval` : fréquence de collecte des métriques.
- `job_name` : nom du service supervisé.
- `targets` : adresse des services à superviser.

Prometheus récupère les métriques toutes les 15 secondes.

## 7. Démarrage de l'environnement

Depuis le répertoire du projet, exécuter :

```bash
docker compose up -d
```

Vérifier que les conteneurs fonctionnent :

```bash
docker compose ps
```

Afficher les logs :

```bash
docker compose logs -f
```

Pour vérifier individuellement un conteneur :

```bash
docker logs prometheus
docker logs grafana
docker logs node-exporter
```

Résultat attendu : les trois conteneurs doivent être démarrés.

## 8. Vérification de Prometheus

Ouvrir un navigateur :

http://localhost:9090

Prometheus doit afficher son interface Web.

### 8.1 Vérifier les targets

Accéder à :

http://localhost:9090/targets

Vous devez retrouver deux targets :

| Target | État attendu |
|---|---|
| prometheus:9090 | UP |
| node-exporter:9100 | UP |

Un état `UP` signifie que Prometheus arrive à récupérer les métriques du service.

Un état `DOWN` indique un problème de communication ou de configuration.

### 8.2 Première requête PromQL

Dans l'interface Prometheus, saisir :

```promql
up
```

Résultat attendu :

- `1` : service disponible.
- `0` : service indisponible.

Tester ensuite :

```promql
node_cpu_seconds_total
```

Cette métrique permet d'observer le temps CPU cumulé.

## 9. Connexion à Grafana

Ouvrir :

http://localhost:3000

Identifiants initiaux :

```text
Utilisateur : admin
Mot de passe : admin
```

Grafana peut demander de modifier le mot de passe lors de la première connexion.

### 9.1 Ajouter Prometheus comme source de données

Dans Grafana :

1. Ouvrir le menu Connections.
2. Sélectionner Data sources.
3. Cliquer sur Add data source.
4. Sélectionner Prometheus.

Renseigner les paramètres suivants :

```text
Name : Prometheus

Prometheus server URL :
http://prometheus:9090
```

Attention : il faut utiliser `prometheus:9090` et non `localhost:9090`, car Grafana communique avec Prometheus depuis le réseau Docker.

Cliquer sur Save & test.

Résultat attendu :

**Successfully queried the Prometheus API.**

## 10. Création du premier Dashboard

Dans Grafana :

1. Aller dans Dashboards.
2. Cliquer sur New.
3. Sélectionner New Dashboard.
4. Cliquer sur Add visualization.
5. Choisir Prometheus comme source de données.

Nous allons créer plusieurs panneaux de supervision.

### 10.1 Supervision de l'utilisation CPU

Requête PromQL :

```promql
100 * (1 - avg by (instance) (
  rate(node_cpu_seconds_total{mode="idle"}[5m])
))
```

Cette requête permet de calculer le pourcentage d'utilisation CPU.

Configuration du panneau :

```text
Titre : CPU Usage
Type : Time series
Unité : Percent (0-100)
```

### 10.2 Supervision de la mémoire RAM

Requête PromQL :

```promql
100 * (
  1 -
  node_memory_MemAvailable_bytes
  /
  node_memory_MemTotal_bytes
)
```

Configuration :

```text
Titre : RAM Usage
Type : Time series
Unité : Percent (0-100)
```

Cette requête calcule le pourcentage de mémoire utilisée à partir de la mémoire disponible.

### 10.3 Supervision de l'espace disque

Requête PromQL :

```promql
100 * (
  1 -
  node_filesystem_avail_bytes{
    mountpoint="/",
    fstype!="rootfs"
  }
  /
  node_filesystem_size_bytes{
    mountpoint="/",
    fstype!="rootfs"
  }
)
```

Configuration :

```text
Titre : Disk Usage
Type : Gauge
Unité : Percent (0-100)
```

Cette requête permet de surveiller le taux d'occupation du système de fichiers racine.

### 10.4 Supervision du trafic réseau

Trafic entrant :

```promql
rate(node_network_receive_bytes_total{
  device!="lo"
}[5m])
```

Trafic sortant :

```promql
rate(node_network_transmit_bytes_total{
  device!="lo"
}[5m])
```

Configuration :

```text
Titre : Network Traffic
Type : Time series
Unité : bytes/sec
```

### 10.5 Disponibilité des services

Requête :

```promql
up
```

Configuration :

```text
Titre : Services Availability
Type : Stat
```

Cette visualisation permet de surveiller l'état des différents services supervisés.

## 11. Exercices pratiques



### Exercice 5 : Diagnostic

Arrêter volontairement Node Exporter :

```bash
docker stop node-exporter
```

Observer :

1. L'état de la target dans Prometheus.
2. La valeur de la métrique `up`.
3. Les changements dans Grafana.

Redémarrer ensuite le conteneur :

```bash
docker start node-exporter
```

Vérifier le retour à l'état UP.

## 12. Questions de compréhension

1. Quelle est la différence entre Prometheus et Grafana ?
2. Quel est le rôle de Node Exporter ?
3. Que signifie le terme scraping ?
4. À quoi sert le fichier `prometheus.yml` ?
5. Pourquoi Grafana utilise-t-il l'adresse `prometheus:9090` ?
6. À quoi sert PromQL ?
7. Pourquoi utilise-t-on des volumes Docker ?
8. Que se passe-t-il lorsqu'une target passe à l'état DOWN ?
9. Pourquoi est-il important de surveiller les ressources CPU, RAM et disque ?
10. Expliquer la différence entre les états UP et DOWN.
11. Pourquoi utilise-t-on la fonction `rate()` pour calculer l'utilisation CPU ?
12. Pourquoi exclut-on généralement l'interface `lo` ?

## 13. Commandes utiles

### Gestion de l'environnement

Démarrer :

```bash
docker compose up -d
```

Arrêter :

```bash
docker compose stop
```

Redémarrer :

```bash
docker compose restart
```

Supprimer les conteneurs et le réseau :

```bash
docker compose down
```

Supprimer également les volumes :

```bash
docker compose down -v
```

Attention : la dernière commande supprime les données persistées de Prometheus et Grafana.

### Recharger la configuration Prometheus

```bash
curl -X POST http://localhost:9090/-/reload
```

Cette commande fonctionne grâce à l'option `--web.enable-lifecycle` activée dans notre configuration.

## 14. Résultat final attendu

À la fin du TP, vous devez disposer :

- D'un Prometheus fonctionnel.
- D'un Node Exporter qui expose les métriques système.
- D'un Grafana connecté à Prometheus.
- D'un Dashboard contenant au minimum :
  - CPU Usage.
  - RAM Usage.
  - Disk Usage.
  - Network Traffic.
  - Services Availability.

## 15. Pour aller plus loin

Pour approfondir cette plateforme d'observabilité, plusieurs évolutions sont possibles :

- Ajouter cAdvisor pour superviser les conteneurs Docker.
- Ajouter Alertmanager pour gérer les alertes.
- Configurer des alertes Grafana.
- Superviser une application Web.
- Exposer des métriques applicatives avec un client Prometheus.
- Créer des dashboards plus avancés.
- Mettre en place une supervision de plusieurs machines Linux.

### Livrables attendus
- les réponses aux questions
- le lien vers le repo github contenant les fichiers de configuration yml

### Conclusion

Ce TP permet de découvrir les bases d'une plateforme d'observabilité basée sur Prometheus et Grafana.

Prometheus assure la collecte et le stockage des métriques tandis que Grafana permet leur visualisation sous forme de tableaux de bord.

L'association de ces outils constitue une base solide pour construire une plateforme de supervision d'infrastructures et d'applications.
