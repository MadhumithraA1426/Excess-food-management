import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def delete_expired_foods():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM foods WHERE expiry_timestamp < NOW();")
    conn.commit()
    cur.close()
    conn.close()


def create_donor(name: str, email: str, password: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        INSERT INTO donors (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, name, email;
        """,
        (name, email, password),
    )
    donor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return donor


def get_donor_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM donors WHERE email = %s;", (email,))
    donor = cur.fetchone()
    cur.close()
    conn.close()
    return donor


def add_food(donor_id: int, food_name: str, quantity: str,
             location: str, contact_phone: str, expiry_timestamp):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        INSERT INTO foods (donor_id, food_name, quantity, location, contact_phone, expiry_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (donor_id, food_name, quantity, location, contact_phone, expiry_timestamp),
    )
    food = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return food


def get_foods_for_donor(donor_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT * FROM foods
        WHERE donor_id = %s
        ORDER BY expiry_timestamp ASC;
        """,
        (donor_id,),
    )
    foods = cur.fetchall()
    cur.close()
    conn.close()
    return foods


def get_available_foods():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
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
    cur.close()
    conn.close()
    return foods


def get_available_foods_by_location(location_keyword: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
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
    cur.close()
    conn.close()
    return foods


def delete_food_by_id(food_id: int, donor_id: int):
    """
    Delete a food by ID only if it belongs to the given donor.
    Returns True on success, False otherwise.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM foods WHERE id = %s AND donor_id = %s RETURNING id;",
        (food_id, donor_id),
    )
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return deleted is not None
