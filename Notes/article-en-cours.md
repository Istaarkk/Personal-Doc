# Article (En cours)

***

### **Introduction Générale**

L'architecture informatique de bas niveau est une discipline fondamentale pour tout ingénieur en informatique. Elle permet de comprendre les interactions entre les composants matériels et logiciels d'un système et leur fonctionnement à un niveau élémentaire. Ce livre aborde les concepts essentiels pour comprendre l'architecture informatique moderne, avec un accent particulier sur le **kernel** du système d'exploitation et la manière dont les logiciels malveillants (maldev) exploitent cette architecture pour pénétrer les systèmes. L'objectif est d'équiper les lecteurs non seulement d'une compréhension théorique approfondie mais aussi de compétences pratiques pour sécuriser un système.

Le livre est structuré en sept chapitres :

1. **L'architecture matérielle et logicielle d'un système**
2. **Le jeu d'instructions et l'exécution des programmes**
3. **Le rôle et l'architecture du système d'exploitation**
4. **Le kernel : structure et fonctionnement**
5. **La gestion des ressources par le kernel**
6. **Le développement de logiciels malveillants : introduction et techniques**
7. **Exploitation avancée et contre-mesures en sécurité**

***

***

### **Chapitre 1 : Introduction à l'Architecture Informatique**

#### **1.1. L’Architecture Informatique : Définition et Histoire**

L'architecture informatique désigne l'organisation et la structure des composants d'un ordinateur. Elle comprend à la fois les éléments matériels et logiciels qui interagissent pour exécuter des programmes.

Historiquement, l'architecture de Von Neumann a servi de base à la conception des ordinateurs modernes. Proposée par John von Neumann en 1945, cette architecture repose sur une mémoire partagée pour les instructions et les données. Si cette conception a permis d’obtenir une flexibilité sans précédent, elle entraîne également un **goulot d'étranglement** : les instructions et les données doivent emprunter le même chemin pour accéder à la mémoire, ce qui peut ralentir le processus.

En revanche, l'architecture **Harvard** permet de séparer les mémoires d’instructions et de données, offrant ainsi des performances améliorées. Cependant, elle est plus complexe à implémenter.

#### **1.2. Composants Matériels d’un Système**

Les principaux composants matériels d'un système informatique sont :

1. **Le processeur (CPU)** : L’unité centrale de traitement exécute les instructions des programmes. Il est constitué de plusieurs unités, dont l'**unité arithmétique et logique (ALU)** et l'**unité de contrôle (CU)**.
2. **La mémoire (RAM)** : La mémoire vive sert à stocker temporairement les données et les instructions en cours d'exécution. Elle est volatile, c’est-à-dire que son contenu est perdu lorsque le système est éteint.
3. **Les périphériques d'entrée et de sortie (I/O)** : Ils permettent à l’ordinateur de communiquer avec le monde extérieur (clavier, souris, écran, imprimante, etc.).
4. **Les bus** : Ils sont responsables de la communication entre le processeur, la mémoire et les périphériques.

#### **1.3. Composants Logiciels d’un Système**

Les composants logiciels permettent de tirer parti du matériel pour exécuter des tâches utiles. Parmi ceux-ci, on trouve :

1. **Le système d’exploitation (OS)** : C’est le logiciel qui gère le matériel et les ressources logicielles d'un ordinateur. Il fournit une interface entre l’utilisateur et le matériel.
2. **Les applications** : Ce sont des programmes qui permettent à l'utilisateur d'effectuer des tâches spécifiques (traitement de texte, navigation internet, etc.).
3. **Le firmware** : Logiciel intégré dans le matériel pour initier et contrôler ses opérations de base.

#### **Résumé du Chapitre 1**

Dans ce chapitre, nous avons couvert les bases de l'architecture informatique. Nous avons exploré les composants matériels et logiciels d'un système et les principes fondamentaux de l'architecture Von Neumann et Harvard. Ces concepts serviront de fondation pour comprendre les mécanismes de bas niveau des systèmes informatiques.

***

***

### **Chapitre 2 : Le Jeu d’Instructions et l'Interaction Matériel/Logiciel**

#### **2.1. Le Jeu d’Instructions (ISA)**

Le **jeu d'instructions** (Instruction Set Architecture, ISA) est l'ensemble des instructions que le processeur peut comprendre et exécuter. L'ISA définit la manière dont un programme s'exécute sur une architecture donnée. Les principaux types d'ISA sont :

* **CISC (Complex Instruction Set Computing)** : Chaque instruction peut effectuer plusieurs opérations.
* **RISC (Reduced Instruction Set Computing)** : Les instructions sont simples et rapides, mais nécessitent plus d'instructions pour effectuer des tâches complexes.

Les ISA les plus populaires incluent **x86** (utilisé dans les ordinateurs de bureau et serveurs) et **ARM** (dominant dans les appareils mobiles).

#### **2.2. Le Cycle d’Exécution d’une Instruction**

Le processeur exécute les instructions en suivant un cycle en quatre étapes :

1. **Fetch** : L'instruction est lue depuis la mémoire.
2. **Decode** : L'instruction est décodée par l'unité de contrôle pour déterminer l'opération à réaliser.
3. **Execute** : L'ALU exécute l'opération.
4. **Writeback** : Le résultat de l'opération est écrit dans un registre ou en mémoire.

Ce cycle se répète pour chaque instruction du programme, et ce processus est extrêmement rapide.

#### **2.3. Interaction Logiciel-Matériel**

L'interaction entre le logiciel et le matériel se fait principalement à travers des **appels système (syscalls)**. Ces appels permettent aux programmes utilisateurs de demander des services du système d'exploitation (accès au réseau, gestion des fichiers, etc.).

Les **drivers de périphériques** jouent également un rôle clé en permettant au système d'exploitation de communiquer avec le matériel, comme les disques durs ou les cartes graphiques.

#### **Résumé du Chapitre 2**

Ce chapitre a expliqué le fonctionnement du processeur et du jeu d'instructions. Nous avons exploré le cycle d'exécution d'une instruction et l'importance des appels système et des drivers pour faire interagir le logiciel et le matériel.

***

***

### **Chapitre 3 : Architecture du Système d’Exploitation**

#### **3.1. Rôle du Système d’Exploitation**

Le **système d'exploitation (OS)** est responsable de la gestion des ressources matérielles, de l’exécution des programmes, et de la gestion de la communication entre le matériel et les utilisateurs. L'OS agit comme une couche d'abstraction entre le matériel et les applications.

#### **3.2. Couches du Système d’Exploitation**

1. **Le Kernel** : C’est la partie centrale de l’OS, responsable de la gestion des ressources matérielles.
2. **Les utilitaires et services** : Fournissent des fonctions supplémentaires telles que la gestion des fichiers, des processus, et la sécurité.
3. **Les interfaces utilisateur** : Offrent des moyens d’interaction avec l'ordinateur (CLI ou GUI).

#### **3.3. Types d’Architecture d’OS**

* **Monolithique** : Le kernel contrôle toutes les fonctions du système, comme dans **Linux**.
* **Microkernel** : Le microkernel ne gère que les fonctions essentielles, comme dans **Minix**.
* **Hybride** : Une combinaison des deux, comme dans **Windows**.

#### **Résumé du Chapitre 3**

Ce chapitre a détaillé les composants d'un système d’exploitation, avec une explication du rôle du kernel et des différences entre les types d'architectures d'OS.

***

***

### **Chapitre 4 : Le Kernel : Structure et Fonctionnement**

#### **4.1. Le Rôle du Kernel**

Le **kernel** est responsable de la gestion de la mémoire, des processus, des périphériques, et de la communication entre le matériel et le logiciel. Il fonctionne en mode noyau (kernel mode), un mode privilégié qui lui permet d’avoir un accès complet au matériel.

#### **4.2. Structure du Kernel**

1. **Gestion des Processus** : Le kernel crée, planifie et termine les processus en fonction de leur priorité et de leur état.
2. **Gestion de la Mémoire** : Le kernel alloue et libère de la mémoire pour les processus et utilise des techniques telles que la **pagination** pour gérer la mémoire virtuelle.
3. **Gestion des Interruptions** : Le kernel répond aux interruptions matérielles (par exemple, une demande d’entrée/sortie) en suspendant les processus en cours et en prenant les mesures nécessaires.
4. **Gestion des Périphériques** : Le kernel utilise des **drivers** pour gérer les périphériques et les rendre accessibles aux applications.

#### **Résumé du Chapitre 4**

Ce chapitre a fourni une vue d'ensemble du kernel, de ses rôles essentiels et des mécanismes qu'il utilise pour gérer les ressources du système.

***

### **Chapitre 5 : La Gestion des Ressources par le Kernel**

#### **5.1. Gestion de la Mémoire**

Le **kernel** utilise des techniques avancées pour gérer la mémoire. Parmi celles-ci :

* **Mémoire virtuelle** : Permet d’abstraire l’espace mémoire et de donner l’impression à chaque processus qu’il possède toute la mémoire.
* **Pagination** et **segmentation** : Divisent la mémoire en blocs pour un accès plus efficace et sécurisé.

#### **5.2. Planification des Processus**

Le **planificateur de processus** du kernel décide quel processus sera exécuté à chaque instant. Il utilise des **algorithmes de planification** pour allouer le temps CPU entre les différents processus.

#### **Résumé du Chapitre 5**

Dans ce chapitre, nous avons détaillé la gestion de la mémoire et des processus par le kernel, et comment ces mécanismes assurent une gestion efficace des ressources du système.

***

### **Chapitre 6 : Le Développement de Logiciels Malveillants : Introduction et Techniques**

#### **6.1. Qu’est-ce qu’un Logiciel Malveillant ?**

Un **logiciel malveillant** (maldev) est un programme conçu pour endommager, perturber ou exploiter un système informatique. Cela inclut des **virus**, **vers**, **chevaux de Troie**, **ransomwares**, et bien d’autres types d'attaques.

#### **6.2. Techniques de Développement de Maldev**

Les logiciels malveillants exploitent souvent des failles dans le kernel, les drivers ou des vulnérabilités dans les applications. Parmi les techniques utilisées :

* **Exploitation de buffers overflow** : Permet à un attaquant d’écrire du code malveillant dans des zones mémoires non protégées.
* **Injection de code** : Injecte du code malveillant dans des processus légitimes.
* **Exploitation des vulnérabilités d’un OS** : Par exemple, des failles dans la gestion de la mémoire.

#### **Résumé du Chapitre 6**

Ce chapitre a présenté les bases du maldev, expliquant les différents types de logiciels malveillants et les techniques employées pour infecter les systèmes.

***

#### **7.1. Techniques d’Exploitation Avancées : Les Rootkits**

Les **rootkits** sont des outils malveillants conçus pour dissimuler des processus, des fichiers ou des modifications dans un système afin de permettre à un attaquant de maintenir un accès non détecté et persistant. Ils sont souvent utilisés pour cacher d'autres formes de malwares, comme des chevaux de Troie ou des keyloggers, et peuvent s'infiltrer profondément dans le système d'exploitation ou même dans le firmware, rendant leur détection et leur suppression particulièrement difficiles.

**1. Fonctionnement d’un Rootkit**

Les rootkits exploitent principalement des vulnérabilités dans le noyau du système d'exploitation ou dans des composants critiques tels que les pilotes de périphériques, afin d’acquérir des privilèges élevés. Une fois installés, ils effectuent plusieurs actions pour masquer leur présence :

* **Modification du noyau** : Les rootkits au niveau noyau interceptent et modifient les appels système, ce qui permet de cacher les processus malveillants, les fichiers ou les connexions réseau. Par exemple, un rootkit pourrait modifier les fonctions qui renvoient la liste des processus en cours pour qu'elles ne montrent pas celui qu’il a installé.
* **Filtrage des entrées et sorties** : Ils peuvent également intercepter les commandes du système pour filtrer toute information suspecte. Par exemple, un attaquant pourrait exécuter des commandes de recherche pour détecter un rootkit, mais le rootkit pourrait répondre avec des résultats altérés pour masquer sa propre existence.
* **Installation persistante** : Les rootkits visent également à garantir que, même après un redémarrage ou une tentative de nettoyage, ils resteront actifs. Certains rootkits modifient le **bootloader** du système pour charger des versions malveillantes du noyau avant que l’OS légitime ne soit chargé. D’autres peuvent s'installer dans le **firmware** de composants matériels, comme les cartes réseau ou les périphériques de stockage.

**2. Types de Rootkits**

Il existe plusieurs types de rootkits, chacun ayant des objectifs et des méthodes d'infiltration différents. Voici les principaux :

* **Rootkits de niveau utilisateur** : Ce type de rootkit fonctionne au-dessus du noyau, dans l'espace d’utilisateur. Ils sont généralement moins difficiles à détecter que les rootkits de niveau noyau, mais peuvent toujours masquer des processus et manipuler des fichiers pour passer inaperçus.
* **Rootkits de niveau noyau (Kernel-level rootkits)** : Ces rootkits agissent directement sur le noyau du système d’exploitation et ont un accès complet aux ressources système. Ils peuvent interférer avec la gestion de la mémoire, intercepter des appels système, ou encore manipuler les droits d’accès aux fichiers. Ce type est plus puissant et plus difficile à détecter que les rootkits de niveau utilisateur.
* **Rootkits de firmware** : Ces rootkits s'installent dans le firmware de périphériques matériels (par exemple, cartes réseau, UEFI, BIOS). Étant plus persistants et invisibles à l’OS, ils peuvent rester actifs même si le système d'exploitation est réinstallé ou que le disque dur est formaté. Cela permet aux attaquants de maintenir un accès persistant à un appareil, malgré les tentatives de nettoyage.
* **Rootkits de type "bootkit"** : Un bootkit modifie le processus de démarrage de l'ordinateur. Il s’installe dans le **MBR** (Master Boot Record) ou le **UEFI**, ce qui lui permet de charger des logiciels malveillants avant que le système d’exploitation ne soit chargé. Cela lui permet d'éviter les antivirus et d'autres outils de sécurité qui s’exécutent au démarrage du système.

**3. Techniques de Détection des Rootkits**

Détecter un rootkit est un défi majeur, car ces logiciels sont conçus pour être invisibles aux outils de sécurité classiques. Voici quelques méthodes pour détecter un rootkit :

* **Analyse comportementale** : Plutôt que de se concentrer uniquement sur les fichiers ou processus suspects, certains outils de détection analysent les comportements du système, comme les appels système anormaux, les tentatives de modification des fichiers système critiques, ou les tentatives de communication avec des serveurs de commande et de contrôle (C\&C).
* **Analyse d’intégrité** : Certains outils comparent des instantanés du système à des versions saines de ces fichiers ou processus. Si des modifications non autorisées sont détectées, cela peut indiquer la présence d'un rootkit.
* **Contrôles de mémoire et de noyau** : Des outils plus avancés, comme **chkrootkit** ou **rkhunter**, scrutent la mémoire et les processus du noyau à la recherche de signes d'injection malveillante.
* **Analyse des signatures** : Certaines solutions antivirus utilisent des signatures spécifiques pour détecter des rootkits connus. Cependant, en raison de leur nature polymorphe, les rootkits peuvent souvent échapper à ces systèmes.

**4. Contre-Mesures et Protection Contre les Rootkits**

Il existe plusieurs stratégies pour se protéger contre les rootkits :

* **Mise à jour régulière des logiciels** : Les rootkits exploitent souvent des vulnérabilités connues dans des logiciels obsolètes. Assurez-vous que tous les systèmes, applications et firmwares sont régulièrement mis à jour pour combler ces failles.
* **Utilisation de solutions antivirus et antimalware** : Bien qu’elles ne soient pas infaillibles contre les rootkits les plus sophistiqués, des solutions antivirus et antimalware modernes offrent une première ligne de défense. Certaines solutions spécialisées sont capables de détecter des comportements suspects ou des modifications inattendues des fichiers système.
* **Verrouillage du noyau et de l’UEFI** : Configurer les paramètres de sécurité du noyau et de l’UEFI pour empêcher le démarrage de logiciels non autorisés est essentiel. Par exemple, l'activation du **Secure Boot** dans l’UEFI empêche l'exécution de tout code non signé avant le démarrage du système d’exploitation.
* **Utilisation de systèmes d’intégrité du code** : Des outils comme **AppArmor** ou **SELinux** peuvent restreindre les actions des applications et processus, limitant ainsi les possibilités d’actions malveillantes dans le système.
* **Réinstallation complète du système** : Si un rootkit est détecté et qu'il n'est pas possible de le nettoyer, une réinstallation complète du système d’exploitation, suivie d'un formatage des disques et de la réinstallation des applications à partir de sources sûres, peut être nécessaire pour éliminer toute trace de l'infection.

**5. Conclusion**

### Les rootkits représentent une menace persistante et sophistiquée pour la sécurité des systèmes informatiques modernes. Leur capacité à masquer leur présence et à assurer un accès prolongé rend leur détection difficile. Pour se protéger efficacement, les utilisateurs et les administrateurs doivent adopter une approche proactive, en combinant des mises à jour régulières, l’utilisation de logiciels de sécurité avancés, et des pratiques de durcissement des systèmes pour minimiser les risques d’infection par un rootkit.

#### **Conclusion Générale**

Ce livre a fourni un aperçu approfondi de l’architecture informatique de bas niveau, en particulier du kernel et de son rôle essentiel dans la gestion des ressources d’un système. Nous avons également exploré les fondements du maldev et les techniques de sécurité pour se défendre contre ces attaques. Cette compréhension est indispensable pour toute personne souhaitant se spécialiser en sécurité informatique et en gestion des systèmes.
