# pip install mysql-connector-python
import mysql.connector
from dotenv import load_dotenv
import os
import json

load_dotenv()


conn = mysql.connector.connect(
    host=os.getenv("SQL_HOST"),
    user=os.getenv("SQL_USER"),
    password=os.getenv("SQL_PASSWORD"),
    database=os.getenv("SQL_DATABASE")
)

cursor = conn.cursor()

# Case Accessory
query = "INSERT INTO case_accessory (name, price, type, form_factor) VALUES (%s, %s, %s, %s)"

with open("./pc-part-dataset/data/jsonl/case-accessory.jsonl", "r") as f:
    for line in f:

        data = json.loads(line)
        values = (
            data.get("name"),
            data.get("price"),
            data.get("type"),
            data.get("form_factor")
        )

        cursor.execute(query, values)

conn.commit()
# cursor.execute("select * from case_accessory")

# for row in cursor.fetchall():
#     print(row)


# Case Fan
query = """
INSERT INTO case_fan (
    name, price, size, color, rpm_min, rpm_max,
    airflow_min, airflow_max,
    noise_min, noise_max,
    pwm
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/case-fan.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        airflow_raw = data.get("airflow")
        noise_raw = data.get("noise_level")
        rpm_raw = data.get("rpm")

        def normalize_range(value):
            if isinstance(value, list):
                return (
                    value[0] if len(value) > 0 else None,
                    value[1] if len(value) > 1 else None
                )
            elif isinstance(value, (int, float)):
                return (None, value)
            else:
                return (None, None)

        rpm_min, rpm_max = normalize_range(rpm_raw)
        airflow_min, airflow_max = normalize_range(airflow_raw)
        noise_min, noise_max = normalize_range(noise_raw)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("size"),
            data.get("color"),
            rpm_min,
            rpm_max,
            airflow_min,
            airflow_max,
            noise_min,
            noise_max,
            data.get("pwm")
        )
        # for i, v in enumerate(values):
        #     if isinstance(v, list):
        #         print("LIST FOUND at index", i, "value:", v)
        
        cursor.execute(query, values)

conn.commit()
# cursor.execute("SELECT * FROM case_fan")



# for row in cursor.fetchall():
#     print(row)


# computer case
query = """
INSERT INTO cases (
    name, price, type, color, psu,
    side_panel, external_volume, internal_35_bays
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/case.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("type"),
            data.get("color"),
            data.get("psu"),
            data.get("side_panel"),
            data.get("external_volume"),
            data.get("internal_35_bays")
        )

        cursor.execute(query, values)

conn.commit()
# cursor.execute("SELECT * FROM cases")



# for row in cursor.fetchall():
#     print(row)



# cpu_cooler
query = """
INSERT INTO cpu_coolers (
    name, price,
    rpm_min, rpm_max,
    noise_min, noise_max,
    color, size
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

def normalize_range(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    elif isinstance(value, (int, float)):
        return (None, value)
    return (None, None)

with open("./pc-part-dataset/data/jsonl/cpu-cooler.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        rpm_min, rpm_max = normalize_range(data.get("rpm"))
        noise_min, noise_max = normalize_range(data.get("noise_level"))

        values = (
            data.get("name"),
            data.get("price"),
            rpm_min,
            rpm_max,
            noise_min,
            noise_max,
            data.get("color"),
            data.get("size")
        )

        cursor.execute(query, values)

conn.commit()

# cpus
query = """
INSERT INTO cpus (
    name, price, core_count, core_clock,
    boost_clock, microarchitecture, tdp, graphics
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/cpu.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("core_count"),
            data.get("core_clock"),
            data.get("boost_clock"),
            data.get("microarchitecture"),
            data.get("tdp"),
            data.get("graphics")
        )

        cursor.execute(query, values)

conn.commit()

# external hard drive
query = """
INSERT INTO external_hard_drives (
    name, price, type, interface,
    capacity_gb, price_per_gb, color
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/external-hard-drive.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("type"),
            data.get("interface"),
            data.get("capacity"),
            data.get("price_per_gb"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# fan controller
query = """
INSERT INTO fan_controllers (
    name, price, channels, channel_wattage,
    pwm, form_factor_min, form_factor_max, color
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

def normalize_range(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    elif isinstance(value, (int, float)):
        return (None, value)
    return (None, None)

with open("./pc-part-dataset/data/jsonl/fan-controller.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        ff_min, ff_max = normalize_range(data.get("form_factor"))

        values = (
            data.get("name"),
            data.get("price"),
            data.get("channels"),
            data.get("channel_wattage"),
            data.get("pwm"),
            ff_min,
            ff_max,
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# headphones
query = """
INSERT INTO headphones (
    name, price, type,
    freq_min, freq_max,
    microphone, wireless,
    enclosure_type, color
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def normalize_range(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    elif isinstance(value, (int, float)):
        return (None, value)
    return (None, None)

with open("./pc-part-dataset/data/jsonl/headphones.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        freq_min, freq_max = normalize_range(data.get("frequency_response"))

        values = (
            data.get("name"),
            data.get("price"),
            data.get("type"),
            freq_min,
            freq_max,
            data.get("microphone"),
            data.get("wireless"),
            data.get("enclosure_type"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# internal hard drive
query = """
INSERT INTO internal_hard_drives (
    name, price, capacity_gb, price_per_gb,
    type, cache, form_factor, interface
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/internal-hard-drive.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("capacity"),
            data.get("price_per_gb"),
            data.get("type"),
            data.get("cache"),
            data.get("form_factor"),
            data.get("interface")
        )

        cursor.execute(query, values)

conn.commit()

# keyboard
query = """
INSERT INTO keyboards (
    name, price, style, switches,
    backlit, tenkeyless,
    connection_type, color
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/keyboard.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("style"),
            data.get("switches"),
            data.get("backlit"),
            data.get("tenkeyless"),
            data.get("connection_type"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# memory
query = """
INSERT INTO memory (
    name, price,
    speed_min, speed_max,
    modules_count, module_size_gb,
    price_per_gb, color,
    first_word_latency, cas_latency
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def normalize_range(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    elif isinstance(value, (int, float)):
        return (None, value)
    return (None, None)

def normalize_modules(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    return (None, None)

with open("./pc-part-dataset/data/jsonl/memory.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        speed_min, speed_max = normalize_range(data.get("speed"))
        modules_count, module_size = normalize_modules(data.get("modules"))

        values = (
            data.get("name"),
            data.get("price"),
            speed_min,
            speed_max,
            modules_count,
            module_size,
            data.get("price_per_gb"),
            data.get("color"),
            data.get("first_word_latency"),
            data.get("cas_latency")
        )

        cursor.execute(query, values)

conn.commit()

# monitors
query = """
INSERT INTO monitors (
    name, price, screen_size,
    resolution_width, resolution_height,
    refresh_rate, response_time,
    panel_type, aspect_ratio
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def normalize_pair(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    return (None, None)

with open("./pc-part-dataset/data/jsonl/monitor.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        res_w, res_h = normalize_pair(data.get("resolution"))

        values = (
            data.get("name"),
            data.get("price"),
            data.get("screen_size"),
            res_w,
            res_h,
            data.get("refresh_rate"),
            data.get("response_time"),
            data.get("panel_type"),
            data.get("aspect_ratio")
        )

        cursor.execute(query, values)

conn.commit()

# motherboard
query = """
INSERT INTO motherboards (
    name, price, socket, form_factor,
    max_memory, memory_slots, color
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/motherboard.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("socket"),
            data.get("form_factor"),
            data.get("max_memory"),
            data.get("memory_slots"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# mice
query = """
INSERT INTO mice (
    name, price, tracking_method,
    connection_type, max_dpi,
    hand_orientation, color
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/mouse.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("tracking_method"),
            data.get("connection_type"),
            data.get("max_dpi"),
            data.get("hand_orientation"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# optical drives
query = """
INSERT INTO optical_drives (
    name, price,
    bd_read, dvd_read, cd_read,
    bd_write, dvd_write, cd_write
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/optical-drive.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("bd"),
            data.get("dvd"),
            data.get("cd"),
            data.get("bd_write"),
            data.get("dvd_write"),
            data.get("cd_write")
        )

        cursor.execute(query, values)

conn.commit()

# os
query = """
INSERT INTO operating_systems (
    name, price,
    supports_32bit, supports_64bit,
    max_memory_gb
) VALUES (%s, %s, %s, %s, %s)
"""

def parse_modes(modes):
    supports_32 = False
    supports_64 = False

    if isinstance(modes, list):
        supports_32 = 32 in modes
        supports_64 = 64 in modes

    return supports_32, supports_64

with open("./pc-part-dataset/data/jsonl/os.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        supports_32, supports_64 = parse_modes(data.get("mode"))

        values = (
            data.get("name"),
            data.get("price"),
            supports_32,
            supports_64,
            data.get("max_memory")
        )

        cursor.execute(query, values)

conn.commit()

# power supply
query = """
INSERT INTO power_supplies (
    name, price, type, efficiency,
    wattage, modular, color
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

def normalize_modular(value):
    if isinstance(value, str):
        return value  # "Full", "Semi", etc.
    elif value is False:
        return "None"
    elif value is True:
        return "Full"  # fallback assumption
    return None

with open("./pc-part-dataset/data/jsonl/power-supply.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("type"),
            data.get("efficiency"),
            data.get("wattage"),
            normalize_modular(data.get("modular")),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# sound card
query = """
INSERT INTO sound_cards (
    name, price, channels, digital_audio,
    snr, sample_rate, chipset, interface
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/sound-card.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("channels"),
            data.get("digital_audio"),
            data.get("snr"),
            data.get("sample_rate"),
            data.get("chipset"),
            data.get("interface")
        )

        cursor.execute(query, values)

conn.commit()

# speakers
query = """
INSERT INTO speakers (
    name, price, configuration,
    wattage, freq_min, freq_max, color
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

def normalize_range(value):
    if isinstance(value, list):
        return (
            value[0] if len(value) > 0 else None,
            value[1] if len(value) > 1 else None
        )
    elif isinstance(value, (int, float)):
        return (None, value)
    return (None, None)

with open("./pc-part-dataset/data/jsonl/speakers.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        freq_min, freq_max = normalize_range(data.get("frequency_response"))

        values = (
            data.get("name"),
            data.get("price"),
            data.get("configuration"),
            data.get("wattage"),
            freq_min,
            freq_max,
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# thermal paste
query = """
INSERT INTO thermal_paste (
    name, price, amount
) VALUES (%s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/thermal-paste.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("amount")
        )

        cursor.execute(query, values)

conn.commit()


# ups
query = """
INSERT INTO ups (
    name, price, capacity_watt, capacity_va
) VALUES (%s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/ups.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("capacity_w"),
            data.get("capacity_va")
        )

        cursor.execute(query, values)

conn.commit()


# video cards
query = """
INSERT INTO video_cards (
    name, price, chipset, memory, core_clock,
    boost_clock, color, length
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/video-card.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("chipset"),
            data.get("memory"),
            data.get("core_clock"),
            data.get("boost_clock"),
            data.get("color"),
            data.get("length")
        )

        cursor.execute(query, values)

conn.commit()

# webcams
query = """
INSERT INTO webcams (
    name, price, resolutions, connection, focus_type,
    os, fov
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

def array_to_string(array):
    if isinstance(array, list):
        return ",".join(array)
    return ""

with open("./pc-part-dataset/data/jsonl/webcam.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        resolutions = array_to_string(data.get("resolutions"))
        os_supported = array_to_string(data.get("os"))

        values = (
            data.get("name"),
            data.get("price"),
            resolutions,
            data.get("connection"),
            data.get("focus_type"),
            os_supported,
            data.get("fov")
        )

        cursor.execute(query, values)

conn.commit()

# wired network cards
query = """
INSERT INTO wired_network_cards (
    name, price, interface, color
) VALUES (%s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/wired-network-card.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("interface"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# wireless network cards
query = """
INSERT INTO wireless_network_cards (
    name, price, protocol, interface, color
) VALUES (%s, %s, %s, %s, %s)
"""

with open("./pc-part-dataset/data/jsonl/wireless-network-card.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)

        values = (
            data.get("name"),
            data.get("price"),
            data.get("protocol"),
            data.get("interface"),
            data.get("color")
        )

        cursor.execute(query, values)

conn.commit()

# cursor.execute("SELECT * FROM wireless_network_cards")



# for row in cursor.fetchall():
#     print(row)

cursor.close()
conn.close()