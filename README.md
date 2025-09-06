# Intégration Hypontech Solar pour Home Assistant

Cette intégration permet de connecter votre onduleur solaire Hypontech à Home Assistant pour surveiller vos panneaux solaires.

## Fonctionnalités
- Récupération automatique des données via l’API cloud Hypontech
- Capteurs d’énergie, puissance, gains, CO2, arbres, etc.
- Configuration 100% via l’interface graphique (aucune ligne dans configuration.yaml)

---

## Installation via HACS

1. **Ajouter le dépôt à HACS**
   - Ouvrez Home Assistant
   - Allez dans **HACS > Intégrations > 3 points (en haut à droite) > Dépôts personnalisés**
   - Ajoutez l’URL du dépôt GitHub :
     ```
     https://github.com/jon7119/hypontech_HA
     ```
   - Type : **Intégration**
   - Cliquez sur **Ajouter**

2. **Installer l’intégration**
   - Dans HACS, recherchez **Hypontech Solar**
   - Cliquez sur **Installer**
   - Redémarrez Home Assistant après l’installation

3. **Configurer l’intégration**
   - Allez dans **Paramètres > Appareils & Services > Ajouter une intégration**
   - Recherchez **Hypontech Solar**
   - Entrez vos identifiants Hypontech Cloud
   - entrez votre plantid genre "https://www.hypon.cloud/plant/2532746207645638656/detail" ou "(ID Système 2532746207645638656)"
   - Validez

---

## Dépannage
- **Aucune ligne `hypontech_ha:` ou `hypontech:` ne doit être ajoutée dans le `configuration.yaml`**
- Si l’intégration n’apparaît pas, vérifiez que le dépôt est bien ajouté dans HACS et que le dossier `custom_components/hypontech_ha/` existe dans votre installation Home Assistant
- Redémarrez Home Assistant après chaque installation ou mise à jour

---

## Liens utiles
- [Documentation Hypontech Cloud](https://hypon.cloud)
- [Dépôt GitHub](https://github.com/jon7119/hypontech_HA)

---


**Développé par jon7119.** 

