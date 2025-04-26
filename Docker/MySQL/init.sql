--既存のデータベースの削除　テスト環境の場合やり直すことがあるため、クリーンな状態から始められるようにする。
DROP DATABASE test;
DROP USER "testuser";

--testuserというユーザーの作成　パスワードをtestと設定
CREATE USER "testuser" IDENTIFIED BY "test";
--testというデータベースの作成
CREATE DATABASE test;
--testデータべースを使用
USE test;
--testデータベース内のすべてのテーブルに対してtestuserにすべての権限を付与する
GRANT ALL PRIVILEGES ON test.* TO "testuser";

--Parent_usersテーブルの作成
CREATE TABLE Parent_users (
--parent_idをint型　AUTO_INCREMENTで連番　主キー
parent_id INT AUTO_INCREMENT PRIMARY KEY,
--parent_user_name VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
parent_user_name VARCHAR(255) UNIQUE NOT NULL,
--mail_adress VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
mail_adress VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR(255)　
password VARCHAR(255) NOT NULL,
--registered_at TIMESTAMP型を利用し登録した日付が入るようにする　CURRENT_TIMESTAMPで現在の日時を返す
registered_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--作成日？registered_atとの違いを知りたい
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--child_usersテーブルの作成
CREATE TABLE Child_users (
--child_id INT型　AUTO_INCREMENTで連番　主キー
child_id INT AUTO_INCREMENT PRIMARY KEY,
--child_user_name VARCHAR型 UNIQUEに設定　NOT NULL
child_user_name VARCHAR(255) UNIQUE NOT NULL,
--mail_adress VARCHAR型　UNIQUEに設定 NOT NULL
mail_adress VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR型　NOT NULL
password VARCHAR(255) NOT NULL,
--user_id VARCHAR型　UNIQUEに設定　NOT NULL
user_id VARCHAR(255) UNIQUE NOT NULL,
--registered_at TIMESTAMP型を利用し登録した日付が入るようにする　CURRENT_TIMESTAMPで現在の日時を返す
registered_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--作成日？registered_atとの違いを知りたい
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--parent_id INT型　NOT NULL 外部キー
parent_id INT NOT NULL,
--idenfication_id INT型でOK？　識別IDの必要性？
idenfication_id INT NOT NULL,
--time_start TIMESTAMP型の指定だけでOK？
time_start TIMESTAMP,
--time_end TIMESTAMP型の指定だけでOK？
time_end TIMESTAMP,
--外部キー ON DELETE CASCADEつける必要あり？親ユーザーが削除された場合に子ユーザーも削除されてしまう？
FOREIGN KEY(parent_id) REFERENCES parent_users(parent_id) ON DELETE CASCADE
);

CREATE Friend_tables (
--unique_id INT型　主キー
unique_id INT AUTO_INCREMENT PRIMARY KEY,
--child_id INT型 NOT NULL 外部キー
child_user_id INT NOT NULL,
--user_id　VARCHAR型 NOT NULL 外部キー
user_id VARCHAR(255) NOT NULL,
FOREIGN KEY (child_user_id) REFERENCES Child_users(child_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES Child_users(user_id) ON DELETE CASCADE,
);

CREATE Channel_tables(
--channel_id INT型　主キー
channel_id INT AUTO_INCREMENT PRIMARY KEY,
--channel_name VARCHAR型　NOT NULL
channel_name VARCHAR(255) NOT NULL,
--created_by INT型 NOT NULL 外部キー
created_by INT NOT NULL,
--create_at TIMESTAMP型
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY(created_by) REFERENCES Child_users(child_id) ON DELETE CASCADE,  
);

CREATE Member_tables(
--child_id INT型 NOT NULL 外部キー DELETE CASCADE必要？
child_id INT NOT NULL,
--channel_id INT型 NOT NULL 外部キー
channel_id INT NOT NULL,
--unique_id INT型　主キー
unique_id INT AUTO_INCREMENT PRIMARY KEY,
--create_at TIMESTAMP型　
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (child_id) REFERENCES Child_users(child_id) ON DELETE CASCADE,
FOREIGN KEY(channel_id) REFERENCES Channel_tables(channel_id) ON DELETE CASCADE,
);

CREATE Messages_tables(
message_id INT AUTO_INCREMENT PRIMARY KEY,
child_id INT NOT NULL,
message_content text NOT NULL,
send_date TIMESTAMP,
channel_id INT NOT NULL,
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY(child_id) REFERENCES Child_users(child_id) ON DELETE CASCADE,
FOREIGN KEY(channel_id) REFERENCES Channel_tables(channel_id) ON DELETE CASCADE,
);







