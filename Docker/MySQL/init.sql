-- parentsテーブルの作成
CREATE TABLE parents (
  parent_id INT AUTO_INCREMENT PRIMARY KEY,
  parent_user_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- childrenテーブルの作成
CREATE TABLE children (
  child_id INT AUTO_INCREMENT PRIMARY KEY,
  child_user_name VARCHAR(255) NOT NULL,
  child_email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  friend_child_user_id VARCHAR(255) UNIQUE NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  parent_id INT NOT NULL,
  child_status INT DEFAULT 0 CHECK(child_status IN (0, 1)),
  FOREIGN KEY(parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE
);

-- channelsテーブルの作成
CREATE TABLE channels (
  channel_id INT AUTO_INCREMENT PRIMARY KEY,
  channel_name VARCHAR(255) NOT NULL,
  created_by INT NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY(created_by) REFERENCES children(child_id) ON DELETE CASCADE
);

-- friendsテーブルの作成
CREATE TABLE friends (
  friend_id INT AUTO_INCREMENT PRIMARY KEY,
  child_id INT NOT NULL,
  friend_child_user_id VARCHAR(255) NOT NULL,
  channel_id INT NOT NULL,
  FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE,
  FOREIGN KEY (friend_child_user_id) REFERENCES children(friend_child_user_id) ON DELETE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);

-- messagesテーブルの作成
CREATE TABLE messages (
  message_id INT AUTO_INCREMENT PRIMARY KEY,
  child_id INT NOT NULL,
  message_content text NOT NULL,
  send_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  channel_id INT NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY(child_id) REFERENCES children(child_id) ON DELETE CASCADE,
  FOREIGN KEY(channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);