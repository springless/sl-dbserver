BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> c0593ad90703

CREATE TABLE "user" (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    email VARCHAR, 
    CONSTRAINT pk_user PRIMARY KEY (id), 
    CONSTRAINT uq_user_email UNIQUE (email)
);

CREATE TABLE post (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    body VARCHAR NOT NULL, 
    CONSTRAINT pk_post PRIMARY KEY (id), 
    CONSTRAINT fk_post_user_id_user FOREIGN KEY(user_id) REFERENCES "user" (id)
);

INSERT INTO alembic_version (version_num) VALUES ('c0593ad90703') RETURNING alembic_version.version_num;

COMMIT;

