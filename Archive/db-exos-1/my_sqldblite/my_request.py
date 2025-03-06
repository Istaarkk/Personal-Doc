def load_v_avatar(model):
    with model.con as cursor:
        cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS v_avatar AS
        SELECT 
            a.ACC_LOGIN,
            acc.ACC_NAME,
            acc.ACC_SURNAME,
            a.AV_NAME,
            a.AV_EXP,
            a.AV_LEVEL
        FROM AVATAR a
        JOIN ACCOUNT acc ON a.ACC_LOGIN = acc.ACC_LOGIN
        WHERE a.AV_ACTIF = TRUE
        ORDER BY a.ACC_LOGIN, a.AV_NAME ASC
        """)

def load_v_ingame(model):
    with model.con as cursor:
        cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS v_ingame AS
        SELECT 
            a.ACC_LOGIN,
            a.AV_NAME,
            m.MOB_POS_X as av_pos_x,
            m.MOB_POS_Y as av_pos_y
        FROM AVATAR a
        JOIN PLAYINGAVATAR pa ON a.AV_ID = pa.AV_ID
        JOIN MOB m ON pa.MOB_ID = m.MOB_ID
        ORDER BY a.ACC_LOGIN DESC, a.AV_NAME DESC
        """)

def load_v_race_class(model):
    with model.con as cursor:
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_race_class AS
        SELECT 
            r.RACE_KEY_NAME,
            r.RACE_LONG_NAME,
            c.CLS_KEY_NAME,
            c.CLS_LONG_NAME,
            (r.RACE_EXP_BY_LEVEL + c.CLS_EXP_BY_LEVEL) AS required_exp_by_level,
            (r.RACE_BONUS_HP_BY_LEVEL + c.CLS_BONUS_HP_BY_LEVEL) AS bonus_hp_by_level,
            (r.RACE_BONUS_CP_BY_LEVEL + c.CLS_BONUS_CP_BY_LEVEL) AS bonus_cp_by_level
        FROM RACE r
        CROSS JOIN CLASS c
        WHERE NOT EXISTS (
            SELECT 1 FROM RESTRICTION_CLASS_RACE rcr
            WHERE rcr.RACE_KEY_NAME = r.RACE_KEY_NAME
            AND rcr.CLS_KEY_NAME = c.CLS_KEY_NAME
        )
        ORDER BY required_exp_by_level DESC,
                bonus_hp_by_level DESC,
                bonus_cp_by_level DESC
        """)

def f_account_actif(model, acc_login):
    with model.con as cursor:
        result = cursor.execute("""
        SELECT COUNT(*)
        FROM AVATAR
        WHERE ACC_LOGIN = ? AND AV_ACTIF = TRUE
        """, (acc_login,)).fetchone()
        return result[0] == 1

def f_progression(model, race, cls, lvlmin, lvlmax):
    with model.con as cursor:
        return cursor.execute("""
        WITH RECURSIVE levels(level) AS (
            SELECT ? UNION ALL
            SELECT level + 1 FROM levels WHERE level < ?
        )
        SELECT
            l.level,
            (l.level - 1) * (r.RACE_EXP_BY_LEVEL + c.CLS_EXP_BY_LEVEL) AS xp,
    CAST((r.RACE_HP_INIT_VALUE + c.CLS_HP_INIT_VALUE) +
        (l.level - 1) * (r.RACE_BONUS_HP_BY_LEVEL + c.CLS_BONUS_HP_BY_LEVEL) AS INTEGER) AS hp,
    CAST((r.RACE_CP_INIT_VALUE + c.CLS_CP_INIT_VALUE) +
        (l.level - 1) * (r.RACE_BONUS_CP_BY_LEVEL + c.CLS_BONUS_CP_BY_LEVEL) AS INTEGER) AS cp

        FROM levels l
        CROSS JOIN RACE r
        CROSS JOIN CLASS c
        WHERE r.RACE_KEY_NAME = ? AND c.CLS_KEY_NAME = ?
        ORDER BY l.level ASC
        """, (lvlmin, lvlmax, race, cls)).fetchall()
        