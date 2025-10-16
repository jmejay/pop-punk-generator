BEGIN

UPDATE ratings
SET spotify_id = albums.album_id
FROM albums
WHERE ratings.album_id = albums.id

COMMIT;