import streamlit as st
import psycopg2
import os


def connect_db() -> None:
    """
    Function that is used to connect to the Postgres database
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
    )


def create_table() -> None:
    """
    Function that creates a table in the Postgres database
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS messages (
                   message TEXT
                   )
    """
    )
    conn.commit()
    cursor.close()
    conn.close()


def add_message(message) -> None:
    """
    Function that insert a message in the table created in the Postgres database
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
    conn.commit()
    cursor.close()
    conn.close()


def get_messages() -> None:
    """
    Function that get the values/messages from the table created in the Postgres database
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM messages")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return messages


def main():
    st.title("Message Board")
    create_table()

    message = st.text_input("Add a new message: ")
    if st.button("Submit"):
        add_message(message)
        st.success("Message added!")

    st.subheader("Messages")
    messages = get_messages()
    for message in messages:
        st.write(message[0])


if __name__ == "__main__":
    main()
