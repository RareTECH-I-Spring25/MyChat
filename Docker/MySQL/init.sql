DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser'@'%';

CREATE DATABASE IF NOT EXISTS chatapp DEFAULT CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'testuser'@'%' IDENTIFIED BY 'testuser';
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'%';
FLUSH PRIVILEGES;

<<<<<<< HEAD
--Parentsテーブルの作成
CREATE TABLE parents (
--parent_idをint型　AUTO_INCREMENTで連番　主キー
parent_id INT AUTO_INCREMENT PRIMARY KEY,
--parent_user_name VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
parent_user_name VARCHAR(255)  NOT NULL,
--parent_email VARCHAR(255)　ユニークキーとして設定し他のユーザーと被らないように　NOT NULLでNULLができないように
parent_email VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR(255)　
parent_password VARCHAR(255) NOT NULL,
--作成日
create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
--update_at ON UPDATEで新しく取得した現在の日時を返す
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--childrenテーブルの作成
CREATE TABLE children (
--child_id INT型　AUTO_INCREMENTで連番　主キー
child_id INT AUTO_INCREMENT PRIMARY KEY,
--child_user_name VARCHAR型 UNIQUEに設定　NOT NULL
child_user_name VARCHAR(255) NOT NULL,
--child_email VARCHAR型　UNIQUEに設定 NOT NULL
child_email VARCHAR(255) UNIQUE NOT NULL,
--password VARCHAR型　NOT NULL
child_password VARCHAR(255) NOT NULL,
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

CREATE TABLE friends (
--unique_id INT型　主キー
friend_id INT AUTO_INCREMENT PRIMARY KEY,
--child_id INT型 NOT NULL 外部キー
child_id INT NOT NULL,
--user_id　VARCHAR型 NOT NULL 外部キー
friend_child_user_id VARCHAR(255) NOT NULL,
FOREIGN KEY (child_id) REFERENCES Children(child_id) ON DELETE CASCADE,
FOREIGN KEY (friend_child_user_id) REFERENCES Children(friend_child_user_id) ON DELETE CASCADE
);

CREATE channels(
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

CREATE messages(
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







=======
USE chatapp;

-- parentsテーブルの作成
CREATE TABLE parents (
  parent_id INT AUTO_INCREMENT PRIMARY KEY,
  parent_user_name VARCHAR(255)  NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- childrenテーブルの作成
CREATE TABLE children (
  child_id INT AUTO_INCREMENT PRIMARY KEY,
  child_user_name VARCHAR(255)  NOT NULL,
  child_email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  friend_child_user_id VARCHAR(255) UNIQUE NOT NULL,
  create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  parent_id INT NOT NULL,
  child_status INT DEFAULT 1 CHECK(child_status IN (0, 1)),
  FOREIGN KEY(parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE
);

CREATE TABLE friends (
  friend_id INT AUTO_INCREMENT PRIMARY KEY,
  child_id INT NOT NULL,
  friend_child_user_id VARCHAR(255) NOT NULL,
  channel_id INT,
  FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE,
  FOREIGN KEY (friend_child_user_id) REFERENCES children(friend_child_user_id) ON DELETE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);

CREATE TABLE channels (
  channel_id INT AUTO_INCREMENT PRIMARY KEY,
  channel_name VARCHAR(255) NOT NULL,
  created_by INT NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY(created_by) REFERENCES children(child_id) ON DELETE CASCADE
);

CREATE TABLE messages (
  message_id INT AUTO_INCREMENT PRIMARY KEY,
  child_id INT NOT NULL,
  message_content text NOT NULL,
  send_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  channel_id INT NOT NULL,
  create_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY(child_id) REFERENCES children(child_id) ON DELETE CASCADE,
  FOREIGN KEY(channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);
>>>>>>> develop
