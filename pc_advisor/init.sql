-- Copy and paste this into mysql terminal
CREATE DATABASE pcbuilder;

CREATE TABLE case_accessory (
    id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(255),
    price DECIMAL(10, 2),
    type varchar(255),
    form_factor float
);

CREATE TABLE case_fan (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2),
    size INTEGER,                 -- mm
    color TEXT,
    rpm_min INTEGER,
    rpm_max INTEGER,
    airflow_min NUMERIC(6,2),     -- from array[0]
    airflow_max NUMERIC(6,2),     -- from array[1]
    noise_min NUMERIC(5,2),       -- from array[0]
    noise_max NUMERIC(5,2),       -- from array[1]
    pwm BOOLEAN
);

CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2),
    type TEXT,
    color TEXT,
    psu TEXT,
    side_panel TEXT,
    external_volume NUMERIC(6,2),
    internal_35_bays INT
);

CREATE TABLE cpu_coolers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    rpm_min INT,
    rpm_max INT,
    noise_min DECIMAL(4,1),
    noise_max DECIMAL(4,1),
    color TEXT,
    size INT
);

CREATE TABLE cpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    core_count INT,
    core_clock DECIMAL(4,2),
    boost_clock DECIMAL(4,2),
    microarchitecture TEXT,
    tdp INT,
    graphics TEXT
);

CREATE TABLE external_hard_drives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    type TEXT,
    interface TEXT,
    capacity_gb INT,
    price_per_gb DECIMAL(6,3),
    color TEXT
);

CREATE TABLE fan_controllers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    channels INT,
    channel_wattage INT,
    pwm BOOLEAN,
    form_factor_min DECIMAL(4,2),
    form_factor_max DECIMAL(4,2),
    color TEXT
);

CREATE TABLE headphones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    type TEXT,
    freq_min INT,
    freq_max INT,
    microphone BOOLEAN,
    wireless BOOLEAN,
    enclosure_type TEXT,
    color TEXT
);

CREATE TABLE internal_hard_drives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    capacity_gb INT,
    price_per_gb DECIMAL(6,3),
    type TEXT,
    cache INT,
    form_factor TEXT,
    interface TEXT
);

CREATE TABLE keyboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    style TEXT,
    switches TEXT,
    backlit TEXT,
    tenkeyless BOOLEAN,
    connection_type TEXT,
    color TEXT
);

CREATE TABLE memory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),

    speed_min INT,
    speed_max INT,

    modules_count INT,
    module_size_gb INT,

    price_per_gb DECIMAL(6,3),
    color TEXT,
    first_word_latency INT,
    cas_latency INT
);

CREATE TABLE monitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    screen_size DECIMAL(4,1),
    resolution_width INT,
    resolution_height INT,
    refresh_rate INT,
    response_time DECIMAL(5,2),
    panel_type TEXT,
    aspect_ratio TEXT
);

CREATE TABLE motherboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    socket TEXT,
    form_factor TEXT,
    max_memory INT,
    memory_slots INT,
    color TEXT
);

CREATE TABLE mice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    tracking_method TEXT,
    connection_type TEXT,
    max_dpi INT,
    hand_orientation TEXT,
    color TEXT
);

CREATE TABLE optical_drives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),

    bd_read INT,
    dvd_read INT,
    cd_read INT,

    bd_write TEXT,
    dvd_write TEXT,
    cd_write TEXT
);

CREATE TABLE operating_systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),

    supports_32bit BOOLEAN,
    supports_64bit BOOLEAN,

    max_memory_gb INT
);

CREATE TABLE power_supplies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    type TEXT,
    efficiency TEXT,
    wattage INT,
    modular TEXT,
    color TEXT
);

CREATE TABLE sound_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    channels DECIMAL(3,1),
    digital_audio INT,
    snr INT,
    sample_rate INT,
    chipset TEXT,
    interface TEXT
);

CREATE TABLE speakers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    configuration DECIMAL(2,1),
    wattage DECIMAL(6,2),
    freq_min INT,
    freq_max INT,
    color TEXT
);

CREATE TABLE thermal_paste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    amount INT
);

CREATE TABLE ups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    capacity_watt INT,
    capacity_va INT
);

CREATE TABLE video_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    chipset TEXT,
    memory INT,
    core_clock DECIMAL(10,2),
    boost_clock DECIMAL(10,2),
    color TEXT,
    length INT
);

CREATE TABLE webcams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    resolutions TEXT,
    connection TEXT,
    focus_type TEXT,
    os TEXT,
    fov DECIMAL(5,2)
);

CREATE TABLE wired_network_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    interface TEXT,
    color TEXT
);

CREATE TABLE wireless_network_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    protocol TEXT,
    interface TEXT,
    color TEXT
);