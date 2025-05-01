from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# ユーザークラス
class User:
   @classmethod
   def create(cls, uid, name, email, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO parents (parent_user_name, email, password) VALUES (%s, %s, %s);"
               cur.execute(sql, (name, email, password,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1062:
               # 重複エラー
               raise ValueError('このメールアドレスは既に登録されています')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def find_by_email(cls, email):
       conn = db_pool.get_conn()
       try:
               with conn.cursor() as cur:
                   sql = "SELECT * FROM parents WHERE email=%s;"
                   cur.execute(sql, (email,))
                   user = cur.fetchone()
               return user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def find_by_id(cls, parent_id):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM parents WHERE parent_id=%s;"
               cur.execute(sql, (parent_id,))
               user = cur.fetchone()
           return user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


# チャンネルクラス
class Channel:
   @classmethod
   def create(cls, uid, new_channel_name, new_channel_description):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);"
               cur.execute(sql, (uid, new_channel_name, new_channel_description,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def get_all(cls):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM channels;"
               cur.execute(sql)
               channels = cur.fetchall()
               return channels
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def find_by_cid(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM channels WHERE id=%s;"
               cur.execute(sql, (cid,))
               channel = cur.fetchone()
               return channel
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def find_by_name(cls, channel_name):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM channels WHERE name=%s;"
               cur.execute(sql, (channel_name,))
               channel = cur.fetchone()
               return channel
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def update(cls, uid, new_channel_name, new_channel_description, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
               cur.execute(sql, (uid, new_channel_name, new_channel_description, cid,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def delete(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "DELETE FROM channels WHERE id=%s;"
               cur.execute(sql, (cid,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


# メッセージクラス
class Message:
   @classmethod
   def create(cls, uid, cid, message):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
               cur.execute(sql, (uid, cid, message,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def get_all(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = """
                   SELECT id, u.uid, user_name, message 
                   FROM messages AS m 
                   INNER JOIN users AS u ON m.uid = u.uid 
                   WHERE cid = %s 
                   ORDER BY id ASC;
               """
               cur.execute(sql, (cid,))
               messages = cur.fetchall()
               return messages
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def delete(cls, message_id):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "DELETE FROM messages WHERE id=%s;"
               cur.execute(sql, (message_id,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


# 子どもクラス
class Child:
    @classmethod
    def create(cls, child_user_name, email, password, friend_child_user_id, parent_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO children (child_user_name, child_email, password, friend_child_user_id, parent_id)
                VALUES (%s, %s, %s, %s, %s);
                """
                cur.execute(sql, (child_user_name, email, password, friend_child_user_id, parent_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1062:
                # 重複エラー
                raise ValueError('このメールアドレスまたはIDは既に登録されています')
            abort(500)
        finally:
            db_pool.release(conn)
    