create table Users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(64),
    password VARCHAR(64),
    first_name VARCHAR(64),
    last_name VARCHAR(64)
);
create table Tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(64),
    description VARCHAR(255),
    created_at DATETIME,
    due_date DATETIME,
    completed_at DATETIME,
    user_id INTEGER
);
