--DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS post;
--DROP TABLE IF EXISTS albums;


CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS albums (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  album_name TEXT NOT NULL,
  album_id TEXT NOT NULL,
  release_date TIMESTAMP,
  total_tracks INTEGER,
  spotify_album_link TEXT,
  spotify_album_image_url TEXT,
  band_name TEXT,
  band_id TEXT,
  band_popularity INTEGER,
  band_spotify_url TEXT
);

CREATE TABLE IF NOT EXISTS generations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  album_id INTEGER,
  generated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (album_id) REFERENCES album (id)
);

CREATE TABLE IF NOT EXISTS ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  album_id INTEGER,
  generation_id INTEGER,
  rated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  rating INTEGER,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (album_id) REFERENCES album (id),
  FOREIGN KEY (generation_id) REFERENCES generations (id)
);
