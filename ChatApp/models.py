from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# Userクラス
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


# Channelクラス
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


# Chhildクラス
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

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM children WHERE child_email=%s;"
                cur.execute(sql, (email,))
                child = cur.fetchone()
            return child
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, child_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM children WHERE child_id=%s;"
                cur.execute(sql, (child_id,))
                child = cur.fetchone()
            return child
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update_status(cls, child_id, status):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE children SET child_status=%s WHERE child_id=%s;"
                cur.execute(sql, (status, child_id))
                conn.commit()
        except Exception as e:
            print(f"エラー: {e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_parent_id(cls, parent_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM children WHERE parent_id=%s;"
                cur.execute(sql, (parent_id,))
                children = cur.fetchall()
            return children
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, child_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM children WHERE child_id=%s;"
                cur.execute(sql, (child_id,))
                conn.commit()
        except Exception as e:
            print(f"エラー: {e}")
            abort(500)
        finally:
            db_pool.release(conn)


# Friendsクラス
class Friends:
    @classmethod
    def find_by_friend_child_user_id(cls, friend_child_user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT child_id, child_user_name, friend_child_user_id 
                FROM children 
                WHERE friend_child_user_id = %s;
                """
                cur.execute(sql, (friend_child_user_id,))
                return cur.fetchone()
        except Exception as e:
            print(f'エラーが発生しました：{e}')
            return None
        finally:
            db_pool.release(conn)

    @classmethod
    def is_friend_exists(cls, child_id, friend_child_user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT f.* 
                FROM friends f
                JOIN children c ON f.friend_child_user_id = c.friend_child_user_id
                WHERE f.child_id = %s AND c.friend_child_user_id = %s;
                """
                cur.execute(sql, (child_id, friend_child_user_id))
                return cur.fetchone() is not None
        except Exception as e:
            print(f'エラーが発生しました：{e}')
            return False
        finally:
            db_pool.release(conn)

    @classmethod
    def create_with_channel(cls, child_id, friend_child_user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # トランザクション開始
                conn.begin()
                
                # チャンネル作成
                sql_channel = "INSERT INTO channels () VALUES ();"
                cur.execute(sql_channel)
                channel_id = cur.lastrowid

                # 自分の情報を取得
                sql_get_self = "SELECT friend_child_user_id FROM children WHERE child_id = %s;"
                cur.execute(sql_get_self, (child_id,))
                self_info = cur.fetchone()

                # 友達の情報を取得
                sql_get_friend = "SELECT child_id FROM children WHERE friend_child_user_id = %s;"
                cur.execute(sql_get_friend, (friend_child_user_id,))
                friend_info = cur.fetchone()

                if not self_info or not friend_info:
                    raise Exception("ユーザー情報が見つかりません")

                # 双方向の友達関係を作成
                sql_friend1 = """
                INSERT INTO friends (child_id, friend_child_user_id, channel_id) 
                VALUES (%s, %s, %s);
                """
                cur.execute(sql_friend1, (child_id, friend_child_user_id, channel_id))

                sql_friend2 = """
                INSERT INTO friends (child_id, friend_child_user_id, channel_id) 
                VALUES (%s, %s, %s);
                """
                cur.execute(sql_friend2, (friend_info['child_id'], self_info['friend_child_user_id'], channel_id))
                
                # トランザクションコミット
                conn.commit()
                return channel_id
        except Exception as e:
            # エラー時はロールバック
            conn.rollback()
            print(f'エラーが発生しました：{e}')
            return None
        finally:
            db_pool.release(conn)

    @classmethod
    def get_friends(cls, child_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT f.friend_id, c.child_user_name, f.channel_id 
                FROM friends f 
                JOIN children c ON f.friend_child_user_id = c.friend_child_user_id 
                WHERE f.child_id = %s;
                """
                cur.execute(sql, (child_id,))
                return cur.fetchall()
        except Exception as e:
            print(f'エラーが発生しました：{e}')
            return []
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, friend_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # トランザクション開始
                conn.begin()
                
                # チャンネルIDを取得
                sql_get_channel = "SELECT channel_id FROM friends WHERE friend_id = %s;"
                cur.execute(sql_get_channel, (friend_id,))
                result = cur.fetchone()
                if result:
                    channel_id = result['channel_id']
                    
                    # メッセージを削除
                    sql_delete_messages = "DELETE FROM messages WHERE channel_id = %s;"
                    cur.execute(sql_delete_messages, (channel_id,))
                    
                    # 友達関係を削除（双方向）
                    sql_delete_friends = "DELETE FROM friends WHERE channel_id = %s;"
                    cur.execute(sql_delete_friends, (channel_id,))
                    
                    # チャンネルを削除
                    sql_delete_channel = "DELETE FROM channels WHERE channel_id = %s;"
                    cur.execute(sql_delete_channel, (channel_id,))
                
                # トランザクションコミット
                conn.commit()
        except Exception as e:
            # エラー時はロールバック
            conn.rollback()
            print(f'エラーが発生しました：{e}')
        finally:
            db_pool.release(conn)



    