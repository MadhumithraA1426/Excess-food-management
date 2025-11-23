import psycopg
from psycopg.rows import dict_row
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def delete_expired_foods():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM foods WHERE expiry_timestamp < NOW();")


def create_donor(name: str, email: str, password: str):
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO donors (name, email, password)
                VALUES (%s, %s, %s)
                RETURNING id, name, email;
                """,
                (name, email, password),
            )
            donor = cur.fetchone()
    return donor


def get_donor_by_email(email: str):
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM donors WHERE email = %s;", (email,))
            donor = cur.fetchone()
    return donor


def add_food(donor_id: int, food_name: str, quantity: str,
             location: str, contact_phone: str, expiry_timestamp):
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO foods (donor_id, food_name, quantity, location, contact_phone, expiry_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (donor_id, food_name, quantity, location, contact_phone, expiry_timestamp),
            )
            food = cur.fetchone()
    return food


def get_foods_for_donor(donor_id: int):
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM foods
                WHERE donor_id = %s
                ORDER BY expiry_timestamp ASC;
                """,
                (donor_id,),
            )
            foods = cur.fetchall()
    return foods


def get_available_foods():
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT f.id, f.food_name, f.quantity, f.location, f.contact_phone,
                       f.expiry_timestamp, d.name AS donor_name
                FROM foods f
                JOIN donors d ON f.donor_id = d.id
                WHERE f.expiry_timestamp >= NOW()
                ORDER BY f.expiry_timestamp ASC;
                """
            )
            foods = cur.fetchall()
    return foods


def get_available_foods_by_location(location_keyword: str):
    conn = get_connection()
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            query = """
                SELECT f.id, f.food_name, f.quantity, f.location, f.contact_phone,
                       f.expiry_timestamp, d.name AS donor_name
                FROM foods f
                JOIN donors d ON f.donor_id = d.id
                WHERE f.expiry_timestamp >= NOW()
                  AND LOWER(f.location) LIKE %s
                ORDER BY f.expiry_timestamp ASC;
            """
            like_pattern = f"%{location_keyword.lower()}%"
            cur.execute(query, (like_pattern,))
            foods = cur.fetchall()
    return foods


def delete_food_by_id(food_id: int, donor_id: int):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM foods WHERE id = %s AND donor_id = %s RETURNING id;",
                (food_id, donor_id),
            )
            deleted = cur.fetchone()
    return deleted is not None
