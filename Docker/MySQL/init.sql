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

--Parentsテーブルの作成
CREATE TABLE Parents (
--parent_idをint型　AUTO_INCREMENTで連番　主キー
parent_id INT AUTO_INCREMENT PRIMARY KEY,
--parent_user_name VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
parent_user_name VARCHAR(255) UNIQUE NOT NULL,
--email VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
email VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR(255)　
password VARCHAR(255) NOT NULL,
--作成日
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--childrenテーブルの作成
CREATE TABLE Children (
--child_id INT型　AUTO_INCREMENTで連番　主キー
child_id INT AUTO_INCREMENT PRIMARY KEY,
--child_user_name VARCHAR型 UNIQUEに設定　NOT NULL
child_user_name VARCHAR(255) UNIQUE NOT NULL,
--child_email VARCHAR型　UNIQUEに設定 NOT NULL
child_email VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR型　NOT NULL
password VARCHAR(255) NOT NULL,
--friend_child_user_id VARCHAR型　UNIQUEに設定　NOT NULL
friend_child_user_id VARCHAR(255) UNIQUE NOT NULL,
--作成日
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--parent_id INT型　NOT NULL 外部キー
parent_id INT NOT NULL,
--child_status 0と1で使用可能と禁止のステータス変更　CHECKで0と1以外の値が入らないようにする。DEFAULT句で最初の値を0とする。
child_status INT DEFAULT 0 CHECK(child_status IN (0, 1)),
--外部キー ON DELETE CASCADEつける必要あり？親ユーザーが削除された場合に子ユーザーも削除されてしまう？
FOREIGN KEY(parent_id) REFERENCES parent_users(parent_id) ON DELETE CASCADE
);

CREATE TABLE Friends (
--unique_id INT型　主キー
friend_id INT AUTO_INCREMENT PRIMARY KEY,
--child_id INT型 NOT NULL 外部キー
child_id INT NOT NULL,
--user_id　VARCHAR型 NOT NULL 外部キー
friend_child_user_id VARCHAR(255) NOT NULL,
FOREIGN KEY (child_id) REFERENCES Children(child_id) ON DELETE CASCADE,
FOREIGN KEY (friend_child_user_id) REFERENCES Children(friend_child_user_id) ON DELETE CASCADE
);

CREATE Channels(
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

CREATE Messages(
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







