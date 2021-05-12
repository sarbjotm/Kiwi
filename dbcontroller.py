import os, mysql

# TODO: utilize this module whenever the database is being accessed.

def connect_to_db():
    db = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    cur = db.cursor()
    return (db, cur)

def close_db(db, cur):
    cur.close()
    db.close()

def get_balance(cursor, user_id):
    cursor.execute(f"""SELECT money
                FROM dodos
                WHERE id = {user_id}
    """) #BUG: If the user doesn't exist in the db then crashes.
    balance = ''.join(map(str, cursor.fetchall()[0]))
    return balance

def update_money(cursor, db, user_id, money):
    sign = "+" if money >= 0 else "-"
    cursor.execute(f"""UPDATE dodos
        SET money = money {sign} {abs(money)}
        WHERE id = {user_id}
        """)
    db.commit()
