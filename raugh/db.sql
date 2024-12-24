CREATE TABLE User (
    id INT PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('Student', 'Admin') NOT NULL, 
    email TEXT,
    phone VARCHAR(15)
);

CREATE TABLE Teacher (
    id INT PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization TEXT NOT NULL, 
    email TEXT,
    phone VARCHAR(15)
);

CREATE TABLE Department (
    id INT PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(20) NOT NULL,
    year INT NOT NULL CHECK(year BETWEEN 1 AND 4), 
    major_subjects_id INT, 
    minor_subjects_id INT, 
    FOREIGN KEY(major_subjects_id) REFERENCES SubjectGroup(id),
    FOREIGN KEY(minor_subjects_id) REFERENCES SubjectGroup(id)
);

CREATE TABLE Subject (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    type ENUM('Major', 'Minor') NOT NULL, 
    teacher_id INT,
    FOREIGN KEY(teacher_id) REFERENCES Teacher(id)
);

CREATE TABLE SubjectGroup (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL 
);

CREATE TABLE SubjectGroupMapping (
    group_id INT,
    subject_id INT,
    PRIMARY KEY(group_id, subject_id),
    FOREIGN KEY(group_id) REFERENCES SubjectGroup(id),
    FOREIGN KEY(subject_id) REFERENCES Subject(id)
);

CREATE TABLE Days (
    id INT PRIMARY KEY AUTOINCREMENT,
    day_name VARCHAR(20) NOT NULL 
);

CREATE TABLE TimeSlot (
    id INT PRIMARY KEY AUTOINCREMENT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE Break (
    id INT PRIMARY KEY AUTOINCREMENT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    day_id INT,
    dept_id INT,
    FOREIGN KEY(day_id) REFERENCES Days(id),
    FOREIGN KEY(dept_id) REFERENCES Department(id)
);

CREATE TABLE Schedule (
    id INT PRIMARY KEY AUTOINCREMENT,
    day_id INT,
    time_slot_id INT,
    subject_id INT,
    dept_id INT,
    teacher_id INT,
    room_number VARCHAR(20), 
    FOREIGN KEY(day_id) REFERENCES Days(id),
    FOREIGN KEY(time_slot_id) REFERENCES TimeSlot(id),
    FOREIGN KEY(subject_id) REFERENCES Subject(id),
    FOREIGN KEY(dept_id) REFERENCES Department(id),
    FOREIGN KEY(teacher_id) REFERENCES Teacher(id)
);

ALTER TABLE Schedule
ADD CONSTRAINT teacher_time_conflict UNIQUE (day_id, time_slot_id, teacher_id);

ALTER TABLE Schedule
ADD CONSTRAINT dept_time_conflict UNIQUE (day_id, time_slot_id, dept_id);