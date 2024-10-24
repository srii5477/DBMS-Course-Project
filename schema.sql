DROP TABLE IF EXISTS disaster_types;

CREATE TABLE disaster_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dname TEXT NOT NULL,
    descrip TEXT NOT NULL,
    official_bureau TEXT NOT NULL,
    monitoring_status TEXT NOT NULL,
    protocol TEXT NOT NULL
);