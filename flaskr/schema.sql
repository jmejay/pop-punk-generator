DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS albums;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE albums (
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

