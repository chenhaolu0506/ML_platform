DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS training_status;
CREATE TABLE images (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    path VARCHAR(255),
    is_vehicle BOOLEAN,
    is_confirmed BOOLEAN,
    correct BOOLEAN
);

SELECT * FROM images;

CREATE TABLE training_status (
	id INTEGER KEY,
	is_training BOOLEAN
);

INSERT INTO training_status (id, is_training) VALUES (1, FALSE);
SELECT * FROM training_status;