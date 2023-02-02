CREATE TABLE IF NOT EXISTS nte_episode (
    id SERIAL NOT NULL PRIMARY KEY,
    flagged BOOLEAN DEFAULT false,
    flagged_reason VARCHAR(1024),
    title VARCHAR(256),
    production_code VARCHAR(16),
    star_date VARCHAR(32),
    air_date DATE,
    description VARCHAR(10240),
    season VARCHAR(16),
    episode VARCHAR(16),
    samples JSON NOT NULL
)
INSERT INTO nte_episode (title, season, episode, samples) VALUES (%s, %s, %s, %s)
