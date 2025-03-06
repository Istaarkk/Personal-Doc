
-- quelques joueurs on été chargé via insert_account en python

-- races de base
insert into RACE (RACE_KEY_NAME, RACE_LONG_NAME, RACE_EXP_BY_LEVEL, RACE_HP_INIT_VALUE,
                    RACE_CP_INIT_VALUE, RACE_BONUS_HP_BY_LEVEL, RACE_BONUS_CP_BY_LEVEL) values
    ('ELF', 'elf des forets', 1700, 6, 12, 1.8, 2.5),
    ('GNOME', 'gnome des montagnes du nord', 1500, 1, 15, 1.5, 2.5),
    ('HIELF', 'haut elf du moldor', 2100, 6, 16, 1.8, 3.0),
    ('ORC', 'orc', 2000, 15, 5, 3.1, 1.5),
    ('HORC', 'demi-orc', 1500, 10, 6, 2.8, 2.0),
    ('DWARF', 'nain', 1500, 9, 7, 2.6, 2.8),
    ('HUMAN', 'humain de base', 1500, 8, 8, 2.0, 2.0)
    ;

-- classes de base
insert into CLASS (CLS_KEY_NAME, CLS_LONG_NAME, CLS_EXP_BY_LEVEL, CLS_HP_INIT_VALUE, 
                    CLS_CP_INIT_VALUE, CLS_BONUS_HP_BY_LEVEL, CLS_BONUS_CP_BY_LEVEL) values
    ('THIEF', 'Voleur', 1500, 8, 8, 1.5, 2.0),
    ('NINJA', 'Ninja', 1500, 8, 8, 1.6, 2.2),
    ('WARIO', 'Guerrier', 1500, 10, 6, 3.0, 2.6),
    ('PALDN', 'Paladin', 1500, 10, 6, 2.8, 2.8),
    ('CLERC', 'Pretre', 1500, 6, 10, 2.2, 3.0),
    ('ELEM', 'Elementaliste', 1500, 6, 10, 2.2, 3.1),
    ('WIZ', 'Magicien', 2100, 3, 16, 1.8, 3.5),
    ('BARBN', 'Barbare', 1900, 15, 6, 3.5, 1.8),
    ('AVEN', 'Aventurier standard', 1500, 8, 8, 2.2, 2.2)
    ;

-- quelques restriction
insert into RESTRICTION_CLASS_RACE (CLS_KEY_NAME, RACE_KEY_NAME, RCR_DESC) values
    ('BARBN', 'HIELF', 'trop discipliné'),
    ('BARBN', 'ELF', 'trop discipliné'),
    ('BARBN', 'DWARF', 'ne peut se passer d''armure'),
    ('PALDN', 'ORC', 'trop chaotique'),
    ('PALDN', 'GNOME', 'trop chaotique'),
    ('NINJA', 'DWARF', 'pas assez souple'),
    ('NINJA', 'HORC', 'pas assez souple'),
    ('NINJA', 'ORC', 'pas assez souple'),
    ('ELEM', 'HORC', 'pas assez intelligent'),
    ('ELEM', 'ORC', 'pas assez intelligent'),
    ('WIZ', 'HORC', 'pas assez intelligent'),
    ('WIZ', 'ORC', 'pas assez intelligent')
    ;

-- quelques PJ
insert into AVATAR (AV_NAME, AV_ACTIF, AV_EXP, AV_LEVEL, AV_LAST_HP, AV_LAST_CP,
                    ACC_LOGIN, CLS_KEY_NAME, RACE_KEY_NAME) values
    ('altariel', TRUE, 16400, 4, 19, 30, 'jiji', 'WIZ', 'ELF'), -- av_id = 1
    ('ziguidi', FALSE, 1000, 1, 4, 20, 'theo', 'NINJA', 'GNOME'), -- av_id = 2
    ('alfred de blanche-croix', TRUE, 16000, 5, 32, 32, 'theo', 'PALDN', 'HUMAN'), -- av_id = 3
    ('gros bill', TRUE, 170000, 40, 150, 276, 'hckz', 'WIZ', 'HIELF'), -- av_id = 4
    ('munchkin', TRUE, 170000, 43, 312, 154, 'hckz', 'BARBN', 'ORC'), -- av_id = 5
    ('gunther', FALSE, 22100, 7, 48, 45, 'iopi', 'WARIO', 'DWARF'), -- av_id = 6
    ('grudu', TRUE, 22000, 5, 48, 22, 'iopi', 'BARBN', 'ORC') -- av_id = 7
    ;

-- competences commune
insert into COMPETENCE (COMP_KEY_NAME, COMP_LONG_NAME, COMP_DESC, COMP_INFO_GM) values
    ('SWORD', 'Epee standard', 'competence sur les epees', 'pour utiliser les items correspondant'),
    ('SABER', 'Sabre standard', 'competence sur les sabres', 'pour utiliser les items correspondant'),
    ('DAG', 'Dague standard', 'competence sur les dagues', 'pour utiliser les items correspondant'),
    ('MASS', 'Masse standard', 'competence sur les casses têtes', 'pour utiliser les items correspondant'),
    ('BATON', 'Gourdin/baton standard', 'competence sur les gourdin/batons', 'pour utiliser les items correspondant'),
    ('AXE', 'Hache standard', 'competence sur les haches', 'pour utiliser les items correspondant'),
    ('CUIR', 'Cuir standard', 'competence sur les armures de cuirs', 'pour utiliser les items correspondant'),
    ('CHMAL', 'Côte de maille', 'competence sur les côtes mailles', 'pour utiliser les items correspondant'),
    ('PLATE', 'Plate standard', 'competence sur les armures de plates', 'pour utiliser les items correspondant'),
    ('SHLD', 'Bouclier standard', 'competence sur les boucliers', 'pour utiliser les items correspondant'),
    --
    ('BOW', 'Arc', 'competence sur les arcs', 'pour utiliser les items correspondant'),
    ('XBOW', 'Arbaléte', 'competence sur les arbaletes', 'pour utiliser les items correspondant'),
    ('WAND', 'Baguette Magique', 'competence sur les baguettes', 'pour utiliser les items correspondant'),
    --
    ('HTH', 'Hand-to-Hand', 'combat au corps a corps - pour le frapper un enemi proche', 'compétence générique utiliser par les monstres'),
    ('RANGE', 'Ranged Attack', 'combat a distance - pour le frapper un enemi loin', 'compétence générique utiliser par les monstres'),
    --
    ('STR', 'Force', 'Pour savoir combien on peut porter d''objet', 'utile pour faire plus de dégât'),
    ('MOVE', 'Deplacement', 'Pour les actions necessitant un deplacement', 'quand deplacement sur terrain type terre'),
    ('SWIM', 'Natation', 'Pour les actions necessitant un jet de nage', 'quand deplacement sur terrain type eau'),
    ('FLY', 'Vol', 'Déplacement quand le Z est supérieur à 0', 'quand deplacement sur terrain type air'),
    ('SPELL', 'Lancer un sort', 'pour lancer les sorts', 'pour lancer les sorts')
    ;

-- competence de RACE
insert into FX_RACE (RACE_KEY_NAME, COMP_KEY_NAME, CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE) values
    -- l'humain est le standard de reference
    ('HUMAN', 'STR', 0, 11, 0.5, 1),
    ('HUMAN', 'MOVE', 0, 12, 0.5, 1),
    ('HUMAN', 'SWIM', 3, 13, 0.5, 2),
    ('HUMAN', 'BATON', 5, 5, 0.5, 1),
    ('HUMAN', 'BOW', 8, 4, 0.5, 4),
    -- un elf c'est pas super costaud
    ('ELF', 'STR', 0, 8, 0.5, 2),
    -- par contre ca galope
    ('ELF', 'MOVE', 0, 12, 1.5, 1),
    -- et ca nage pas trop mal
    ('ELF', 'SWIM', 0, 11, 1, 1),
    -- de plus tous les elfs utilisent des arcs
    ('ELF', 'BOW', 0, 10, 1.5, 1),
    -- un haut elf, c'est comme un elf en mieux
    ('HIELF', 'STR', 0, 8, 1.5, 2),
    ('HIELF', 'MOVE', 0, 12, 1.5, 1),
    ('HIELF', 'SWIM', 0, 11, 1, 1),
    ('HIELF', 'BOW', 0, 11, 1.7, 1),
    ('HIELF', 'WAND', 4, 8, 1, 2),
    -- un gnome c'est tout petit
    ('GNOME', 'STR', 0, 5, 0.5, 3),
    -- mais ca galope tres vite
    ('GNOME', 'MOVE', 0, 12, 2.5, 0.5),
    -- c plus dur de nager
    ('GNOME', 'SWIM', 6, 9, 0.5, 3),
    -- ca utilise une dague
    ('GNOME', 'DAG', 3, 5, 0.5, 1),
    -- un orc c'est bourrin
    ('ORC', 'STR', 0, 15, 2, 0.5),
    -- ca cours bien
    ('ORC', 'MOVE', 0, 11, 1.5, 1.5),
    -- mais ca nage comme un caillou
    ('ORC', 'SWIM', 6, 6, 0.5, 5),
    -- ca utilise la peau de ses enemis pour se vétir
    ('ORC', 'CUIR', 0, 5, 0.5, 3),
    -- un demi-orc c'est presque un orc
    ('HORC', 'STR', 0, 13, 1.5, 1),
    ('HORC', 'MOVE', 0, 11, 1, 2),
    ('HORC', 'SWIM', 5, 8, 0.5, 4),
    ('HORC', 'CUIR', 1, 5, 0.5, 1),
    -- un nain c'est solide
    ('DWARF', 'STR', 0, 14, 1.5, 1),
    -- c'est pas un bolide
    ('DWARF', 'MOVE', 0, 8, 0.5, 2),
    -- nage comme un caillou avec son pote l'orc...non pas son pote
    ('DWARF', 'SWIM', 6, 6, 0.5, 5),
    -- tous les nains savent utiliser une hache
    ('DWARF', 'AXE', 0, 5, 0.5, 1)
    ;
---- competences specifiques à une classe
insert into FX_CLS (COMP_KEY_NAME, CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE, CLS_KEY_NAME) values
    -- epee
    ('SWORD', 1, 10, 1.5, 1,  'WARIO'),
    ('SWORD', 1, 8, 0.8, 1, 'PALDN'),
    ('SWORD', 1, 6, 1.3, 1, 'BARBN'),
    ('SWORD', 1, 5, 0.5, 2, 'AVEN'),
    ('SWORD', 2, 8, 1.2, 2, 'NINJA'),
    ('SWORD', 2, 8, 0.6, 2, 'THIEF'),
    ('SWORD', 2, 5, 0.5, 3, 'ELEM'),
    ('SWORD', 3, 4, 0.4, 3, 'CLERC'),
    -- sabre
    ('SABER', 1, 12, 1.6, 2, 'NINJA'),
    ('SABER', 1, 10, 1.5, 2, 'WARIO'),
    ('SABER', 6, 10, 0.5, 2, 'AVEN'),
    -- dague
    ('DAG', 1, 10, 1.5, 1, 'THIEF'),
    ('DAG', 1, 10, 1.6, 1, 'NINJA'),
    ('DAG', 1, 8, 0.6, 2, 'WIZ'),
    ('DAG', 1, 8, 0.5, 2, 'ELEM'),
    ('DAG', 1, 8, 0.9, 2, 'BARBN'),
    ('DAG', 1, 8, 1.1, 2, 'WARIO'),
    ('DAG', 2, 8, 0.6, 2, 'AVEN'),
    -- masse
    ('MASS', 1, 10, 1.3, 1,  'CLERC'),
    ('MASS', 1, 8, 1.2, 1, 'PALDN'),
    ('MASS', 1, 8, 1.1, 2, 'WARIO'),
    ('MASS', 3, 4, 0.8, 2, 'AVEN'),
    -- gourdin/baton
    ('BATON', 1, 10, 1.5, 1, 'THIEF'),
    ('BATON', 1, 10, 1.6, 1, 'NINJA'),
    ('BATON', 1, 9, 0.5, 1, 'AVEN'),
    ('BATON', 1, 8, 0.4, 1, 'WIZ'),
    ('BATON', 1, 8, 0.5, 1, 'ELEM'),
    -- hache
    ('AXE', 1, 12, 1.8, 1, 'BARBN'),
    ('AXE', 1, 12, 1.3, 1, 'WARIO'),
    ('AXE', 4, 10, 0.8, 2, 'AVEN'),
    -- armure de cuir
    ('CUIR', 1, 10, 0.8, 1, 'BARBN'),
    ('CUIR', 1, 10, 1.5, 1, 'THIEF'),
    ('CUIR', 2, 8, 0.2, 2, 'AVEN'),
    -- maille
    ('CHMAL', 1, 10, 1, 1, 'WARIO'),
    ('CHMAL', 2, 10, 1, 1, 'PALDN'),
    ('CHMAL', 3, 10, 1, 1, 'CLERC'),
    ('CHMAL', 3, 10, 1.4, 2, 'AVEN'),
    -- armure de plate
    ('PLATE', 1, 12, 1.6, 1, 'WARIO'),
    ('PLATE', 3, 10, 1.4, 2, 'PALDN'),
    ('PLATE', 6, 10, 1.4, 2, 'AVEN'),
    -- bouclier
    ('SHLD', 1, 12, 1.8, 1, 'WARIO'),
    ('SHLD', 1, 10, 1.4, 2, 'PALDN'),
    ('SHLD', 5, 10, 1.4, 3, 'AVEN'),
    -- arc
    ('BOW', 1, 11, 1.2, 1, 'THIEF'),
    ('BOW', 1, 11, 1.3, 1, 'NINJA'),
    ('BOW', 1, 10, 1, 2, 'WARIO'),
    ('BOW', 1, 11, 1.1, 2, 'BARBN'),
    ('BOW', 2, 9, 1.2, 1, 'AVEN'),
    -- arbalete
    ('XBOW', 1, 11, 1.2, 1, 'THIEF'),
    ('XBOW', 1, 12, 1.5, 1, 'WARIO'),
    ('XBOW', 1, 10, 1.2, 2, 'AVEN'),
    -- baguette magique
    ('WAND', 2, 10, 1.2, 2, 'ELEM'),
    ('WAND', 1, 12, 1.4, 1, 'WIZ'),
    ('WAND', 5, 6, 0.1, 4, 'AVEN'),
    -- sort
    ('SPELL', 1, 10, 1.2, 1.2, 'CLERC'),
    ('SPELL', 4, 8, 1, 2, 'PALDN'),
    ('SPELL', 0, 12, 1.8, 1, 'WIZ'),
    ('SPELL', 2, 10, 1.5, 1, 'ELEM')
    ;

insert into MAP (MAP_WIDTH, MAP_HEIGHT, MAP_DESC) values
    (100, 100, 'zone de debut'),
    (1000, 1500, 'monde 1'),
    (1200, 1600, 'monde 2')
    ;

insert into MOB (MAP_ID, MOB_POS_X, MOB_POS_Y, MOB_NEXT_X, MOB_NEXT_Y, MOB_FUEL, MOB_CURRENT_HP, MOB_CURRENT_CP) values
    (1, 50, 50, 1, 1, 5, 10, 10), -- mob_id = 1
    (1, 50, 70, 1, 1, 5, 10, 10), -- mob_id = 2
    (1, 5, 25, 1, 1, 5, 10, 10), -- mob_id = 3
    (2, 500, 450, 1, 1, 5, 10, 10), -- mob_id = 4
    (3, 150, 250, 1, 1, 5, 10, 10), -- mob_id = 5
    (3, 50, 450, 1, 1, 5, 10, 10) -- mob_id = 6
    ;

insert into PLAYINGAVATAR values
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 6),
    (6, 7)
    ;

insert into MONSTER values
    ('SKELETON', 100, 10, 15, 0, 0),
    ('BAT', 50, 5, 8, 0, 0),
    ('UNDEAD', 500, 50, 80, 0, 0)
    ;

insert into FX_MONSTER (CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE, COMP_KEY_NAME, MON_KEY_NAME) values
    (0, 10, 0, 0, 'MOVE', 'SKELETON'),
    (0, 30, 0, 0, 'HTH', 'SKELETON'),
    (0, 15, 0, 0, 'PLATE', 'SKELETON'),
    --
    (0, 10, 0, 0, 'MOVE', 'BAT'),
    (0, 30, 0, 0, 'HTH', 'BAT'),
    (0, 5, 0, 0, 'CUIR', 'BAT'),
    --
    (0, 10, 0, 0, 'MOVE', 'UNDEAD'),
    (0, 30, 0, 0, 'HTH', 'UNDEAD'),
    (0, 5, 0, 0, 'CUIR', 'UNDEAD')
    ;
