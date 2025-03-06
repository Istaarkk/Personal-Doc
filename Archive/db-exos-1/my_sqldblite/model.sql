/*
 comment
 */

PRAGMA foreign_keys=ON;

-- table account pour enregistrer les joueurs
drop table if exists ACCOUNT;
create table ACCOUNT (
        ACC_ID              integer,
        ACC_LOGIN           char(15) NOT NULL,
        ACC_NAME            char(32) NOT NULL,
        ACC_SURNAME         varchar(25) NOT NULL,
        ACC_PWD             varchar(40) NOT NULL,
        ACC_MAIL            text NOT NULL,
        CONSTRAINT          "An account have a primary key" primary key(ACC_LOGIN)
);
-- un avatar est d'une certaine race
--      * un nom long
--      * l'expérience (EXP) nécessaire pour prendre un niveau
--      * valeur initiale de point de vie (HP .. Hit Point)
--      * valeur initiale de point de compétence (CP)
--      * bonus à chaque gain de niveau et est à ajouter aux HP
--      * bonus à chaque gain de niveau et est à ajouter aux CP
drop table if exists RACE;
create table RACE (
        RACE_KEY_NAME           char(5) NOT NULL,
        RACE_LONG_NAME          char(32) NOT NULL,
        RACE_EXP_BY_LEVEL       integer NOT NULL,
        RACE_HP_INIT_VALUE      integer NOT NULL,
        RACE_CP_INIT_VALUE      integer NOT NULL,
        RACE_BONUS_HP_BY_LEVEL  float NOT NULL,
        RACE_BONUS_CP_BY_LEVEL  float NOT NULL,
        CONSTRAINT              "A race have a primary key" primary key(RACE_KEY_NAME)
);

-- un avatar est d'une certaine classe
--      * un nom long
--      * l'expérience (EXP) nécessaire pour prendre un niveau
--      * valeur initiale de point de vie (HP .. Hit Point)
--      * valeur initiale de point de compétence (CP)
--      * bonus à chaque gain de niveau et est à ajouter aux HP initiaux
--      * bonus à chaque gain de niveau et est à ajouter aux CP initiaux
drop table if exists CLASS;
create table CLASS (
        CLS_KEY_NAME            char(5) NOT NULL,
        CLS_LONG_NAME           char(32) NOT NULL,
        CLS_EXP_BY_LEVEL        integer NOT NULL,
        CLS_HP_INIT_VALUE       integer NOT NULL,
        CLS_CP_INIT_VALUE       integer NOT NULL,
        CLS_BONUS_HP_BY_LEVEL   float NOT NULL,
        CLS_BONUS_CP_BY_LEVEL   float NOT NULL,
        CONSTRAINT              "A class have a primary key" primary key(CLS_KEY_NAME)
);

-- il existe des restrictions de classe/race
-- on ne peut pas créer d'avatar ayant une combinaison CLASSE/RACE présente dans cette table
drop table if exists RESTRICTION_CLASS_RACE;
create table RESTRICTION_CLASS_RACE (
        RCR_DESC                text NOT NULL,
        CLS_KEY_NAME            char(5) NOT NULL,
        RACE_KEY_NAME           char(5) NOT NULL
);

-- un user incarne plusieurs avatars avec :
--      * nombre de pièce d'or PO de l'avatar
--      * expérience de l'avatar
--      * level de l'avatar
--      * HP à la dernière connexion de l'avatar
--      * Compétence Point à la dernière connexion
drop table if exists AVATAR;
create table AVATAR (
        AV_ID               integer primary key,
        AV_NAME             char(32) NOT NULL,
        AV_ACTIF            boolean DEFAULT FALSE,
        AV_CURRENT_PO       integer,
        AV_EXP              integer NOT NULL,
        AV_LEVEL            integer NOT NULL,
        AV_LAST_HP          integer NOT NULL,
        AV_LAST_CP          integer NOT NULL,
        ACC_LOGIN           char(15) NOT NULL,
        RACE_KEY_NAME       char(5) NOT NULL,
        CLS_KEY_NAME        char(5) NOT NULL
);

-- compétence générique
--      * nom long
--      * description de la compétence
--      * information pour le Game Master concernant les régles associées à cette compétence
drop table if exists COMPETENCE;
create table COMPETENCE (
        COMP_KEY_NAME           char(5) NOT NULL,
        COMP_LONG_NAME          char(32) NOT NULL,
        COMP_DESC               text,
        COMP_INFO_GM            text,
        CONSTRAINT              "A competence have a primary key" primary key(COMP_KEY_NAME)
);

-- effet des compétences
--      * niveau minimum requis pour utiliser la compétence
--      * valeur minimum de la compétence
--      * valeur à multiplier par le niveau réel et à ajouter à la valeur initiale de la compétence
--      * point de compétence utilisé à chaque utilisation
drop table if exists COMPETENCE_FX;
create table COMPETENCE_FX (
        CFX_ID                  integer primary key,
        CFX_MIN_LEVEL_REQ       integer NOT NULL,
        CFX_INIT_VALUE          integer NOT NULL,
        CFX_BONUS_BY_LEVEL      float NOT NULL,
        CFX_CP_BY_USE           integer NOT NULL,
        COMP_KEY_NAME           char(5) NOT NULL --,
);

-- il y a des compétences de race
drop table if exists COMPETENCE_RACE;
create table COMPETENCE_RACE (
        CFX_ID                  integer NOT NULL,
        RACE_KEY_NAME           char(5) NOT NULL,
        CONSTRAINT              "A competence of race have a primary key" primary key(CFX_ID, RACE_KEY_NAME)
);

-- il y a des effets de competence de race
drop view if exists FX_RACE;
create view FX_RACE as select * from COMPETENCE_FX natural inner join COMPETENCE_RACE;
create trigger FX_RACE_INS INSTEAD OF INSERT ON FX_RACE
BEGIN
    insert into COMPETENCE_FX (CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE, COMP_KEY_NAME)
    values (new.CFX_MIN_LEVEL_REQ, new.CFX_INIT_VALUE, new.CFX_BONUS_BY_LEVEL, new.CFX_CP_BY_USE, new.COMP_KEY_NAME);
    insert into COMPETENCE_RACE (CFX_ID, RACE_KEY_NAME)
    values (last_insert_rowid(), new.RACE_KEY_NAME);
END;
create trigger FX_RACE_UPD INSTEAD OF UPDATE ON FX_RACE
BEGIN
    UPDATE COMPETENCE_FX SET CFX_MIN_LEVEL_REQ = new.CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE = new.CFX_INIT_VALUE,
        CFX_BONUS_BY_LEVEL = new.CFX_BONUS_BY_LEVEL,
        CFX_CP_BY_USE = new.CFX_CP_BY_USE,
        COMP_KEY_NAME = new.COMP_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
    UPDATE COMPETENCE_RACE SET RACE_KEY_NAME = new.RACE_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
END;
create trigger FX_RACE_DEL INSTEAD OF DELETE ON FX_RACE
BEGIN
    DELETE FROM COMPETENCE_FX WHERE CFX_ID=old.CFX_ID;
    DELETE FROM COMPETENCE_RACE WHERE CFX_ID=old.CFX_ID;
END;

-- il y a des compétences de classe
drop table if exists COMPETENCE_CLS;
create table COMPETENCE_CLS (
        CFX_ID                  integer NOT NULL,
        CLS_KEY_NAME            char(5) NOT NULL,
        CONSTRAINT              "A competence of class have a primary key" primary key(CFX_ID, CLS_KEY_NAME)
);

-- il y a des effets de competence de classe
drop view if exists FX_CLS;
create view FX_CLS as select * from COMPETENCE_FX natural inner join COMPETENCE_CLS;
create trigger FX_CLS_INS INSTEAD OF INSERT ON FX_CLS
BEGIN
    insert into COMPETENCE_FX (CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE, COMP_KEY_NAME)
    values (new.CFX_MIN_LEVEL_REQ, new.CFX_INIT_VALUE, new.CFX_BONUS_BY_LEVEL, new.CFX_CP_BY_USE, new.COMP_KEY_NAME);
    insert into COMPETENCE_CLS (CFX_ID, CLS_KEY_NAME)
    values (last_insert_rowid(), new.CLS_KEY_NAME);
END;
create trigger FX_CLS_UPD INSTEAD OF UPDATE ON FX_CLS
BEGIN
    UPDATE COMPETENCE_FX SET CFX_MIN_LEVEL_REQ = new.CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE = new.CFX_INIT_VALUE,
        CFX_BONUS_BY_LEVEL = new.CFX_BONUS_BY_LEVEL,
        CFX_CP_BY_USE = new.CFX_CP_BY_USE,
        COMP_KEY_NAME = new.COMP_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
    UPDATE COMPETENCE_CLS SET CLS_KEY_NAME = new.CLS_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
END;
create trigger FX_CLS_DEL INSTEAD OF DELETE ON FX_CLS
BEGIN
    DELETE FROM COMPETENCE_FX WHERE CFX_ID=old.CFX_ID;
    DELETE FROM COMPETENCE_CLS WHERE CFX_ID=old.CFX_ID;
END;

-- terrain de jeu, le comment on passe d'une carte a une autre est hors propos (portes, téléporteur etc...)
drop table if exists MAP;
create table MAP (
    MAP_ID                      integer,
    MAP_WIDTH                   integer NOT NULL,
    MAP_HEIGHT                  integer NOT NULL,
    MAP_DESC                    text NOT NULL,
    CONSTRAINT                  "A Map have a primary key" primary key(MAP_ID)
);

-- Les catégories de monstre
drop table if exists MONSTER;
create table MONSTER (
    MON_KEY_NAME                char(10) NOT NULL,
    MON_EXP_DEAD                integer,
    MON_HP_MIN                  integer,
    MON_HP_MAX                  integer,
    MON_CP_MIN                  integer,
    MON_CP_MAX                  integer,
    CONSTRAINT                  "A Monster have a primary key" primary key(MON_KEY_NAME)
);

-- il y a des competences de monstre
drop table if exists COMPETENCE_MONSTER;
create table COMPETENCE_MONSTER (
        CFX_ID                  integer NOT NULL,
        MON_KEY_NAME           char(10) NOT NULL,
        CONSTRAINT              "A competence of MONSTER have a primary key" primary key(CFX_ID, MON_KEY_NAME)
);

-- il y a les effets des compétences de monstre
drop view if exists FX_MONSTER;
create view FX_MONSTER as select * from COMPETENCE_FX natural inner join COMPETENCE_MONSTER;
create trigger FX_MONSTER_INS INSTEAD OF INSERT ON FX_MONSTER
BEGIN
    insert into COMPETENCE_FX (CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE, CFX_BONUS_BY_LEVEL, CFX_CP_BY_USE, COMP_KEY_NAME)
    values (new.CFX_MIN_LEVEL_REQ, new.CFX_INIT_VALUE, new.CFX_BONUS_BY_LEVEL, new.CFX_CP_BY_USE, new.COMP_KEY_NAME);
    insert into COMPETENCE_MONSTER (CFX_ID, MON_KEY_NAME)
    values (last_insert_rowid(), new.MON_KEY_NAME);
END;
create trigger FX_MONSTER_UPD INSTEAD OF UPDATE ON FX_MONSTER
BEGIN
    UPDATE COMPETENCE_FX SET CFX_MIN_LEVEL_REQ = new.CFX_MIN_LEVEL_REQ, CFX_INIT_VALUE = new.CFX_INIT_VALUE,
        CFX_BONUS_BY_LEVEL = new.CFX_BONUS_BY_LEVEL,
        CFX_CP_BY_USE = new.CFX_CP_BY_USE,
        COMP_KEY_NAME = new.COMP_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
    UPDATE COMPETENCE_MONSTER SET MON_KEY_NAME = new.MON_KEY_NAME
    WHERE CFX_ID = old.CFX_ID;
END;
create trigger FX_MONSTER_DEL INSTEAD OF DELETE ON FX_MONSTER
BEGIN
    DELETE FROM COMPETENCE_FX WHERE CFX_ID=old.CFX_ID;
    DELETE FROM COMPETENCE_MONSTER WHERE CFX_ID=old.CFX_ID;
END;

-- Mobile Object (un avatar ou un monstre instancié)
--      * position X du Mob
--      * position Y du Mob
--      * point d'endurance pour le déplacement
--      * valeur d'incrément sur la position X au prochain tour
--      * valeur d'incrément sur la position Y au prochain tour
--      * valeur courante des Hit Points HP
--      * valeur courante des Compétences Points CP
drop table if exists MOB;
create table MOB (
        MOB_ID                      integer primary key,
        MOB_POS_X                   integer NOT NULL,
        MOB_POS_Y                   integer NOT NULL,
        MOB_FUEL                    integer NOT NULL,
        MOB_NEXT_X                  integer NOT NULL,
        MOB_NEXT_Y                  integer NOT NULL,
        MOB_CURRENT_HP              integer NOT NULL,
        MOB_CURRENT_CP              integer NOT NULL,
        MAP_ID                      integer NOT NULL
);

-- trésor présent sur le terrain de jeu ou porté par un monstre
--      * valeur d'expérience du trésor
--      * valeur en piéce d'or du trésor
--      * position X du trésor
--      * position Y du trésor
drop table if exists TREASURE;
create table TREASURE (
        TRS_ID                      integer primary key,
        TRS_EXP                     integer,
        TRS_PO                      integer,
        TRS_POS_X                   integer,
        TRS_POS_Y                   integer,
        MAP_ID                      integer NOT NULL,
        MOB_ID                      integer DEFAULT NULL
);

-- Les joueurs sur la carte
drop table if exists PLAYINGAVATAR;
create table PLAYINGAVATAR (
    MOB_ID                      integer NOT NULL,
    AV_ID                       integer NOT NULL,
    CONSTRAINT                  "A PlayingAvatar have a primary key" primary key(MOB_ID, AV_ID)
);

-- Les monstres sur la carte
drop table if exists PLAYINGMONSTER;
create table PLAYINGMONSTER (
    MOB_ID                      integer NOT NULL,
    MON_KEY_NAME                char(10) NOT NULL,
    CONSTRAINT                  "A PlayingMonster have a primary key" primary key(MOB_ID, MON_KEY_NAME)
);
