SET search_path TO public;

INSERT INTO "user" (id, name, email) VALUES
  (1, 'user1', 'user1@email.com')
  ,(2, 'user2', 'user2@email.com')
;

INSERT INTO post (id, user_id, timestamp, body) VALUES
  (1, 1, timestamp '2022-02-07 01:02:03.000', 'This is a post')
;

COMMIT;
