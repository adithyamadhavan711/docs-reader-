import sqlite3

conn = sqlite3.connect("docs.db")
c = conn.cursor()


def create_table():

    c.execute("""
        CREATE TABLE IF NOT EXISTS Documents (
            DocumentID TEXT PRIMARY KEY,
            Title TEXT,
            Content TEXT,
            Modified_time TEXT
        )
    """)

    conn.commit()


def create_fts_table():

    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS Doc_FTS
        USING fts5(
            DocumentID,
            Title,
            Content
        )
    """)

    conn.commit()


def insert(DocumentID, Title, Content, Modified_time):

    c.execute(
        """
        INSERT INTO Documents
        (DocumentID, Title, Content, Modified_time)
        VALUES (?, ?, ?, ?)
        """,
        (DocumentID, Title, Content, Modified_time),
    )

    conn.commit()

    c.execute(
        """
        INSERT INTO Doc_FTS
        (DocumentID, Title, Content)
        VALUES (?, ?, ?)
    """,
        (DocumentID, Title, Content),
    )

    conn.commit()


def get_doc(DocumentID):

    c.execute(
        """
        SELECT * FROM Documents
        WHERE DocumentID = ?
        """,
        (DocumentID,),
    )

    return c.fetchone()


def update_doc(document_id, title, content, modified_time):

    c.execute(
        """
        UPDATE Documents
        SET Title = ?, Content = ?, Modified_time = ?
        WHERE DocumentID = ?
        """,
        (title, content, modified_time, document_id),
    )

    conn.commit()

    c.execute(
        """
        UPDATE Doc_FTS
        SET Title = ?, Content = ?
        WHERE DocumentID = ?
    """,
        (title, content, document_id),
    )

    conn.commit()


def delete_doc(document_id):

    c.execute("DELETE FROM Documents WHERE DocumentID = ?", (document_id,))

    conn.commit()

    c.execute("DELETE FROM doc_FTS WHERE DocumentID = ?", (document_id,))

    conn.commit()


def get_all_ids():

    c.execute("SELECT DocumentID FROM Documents")

    return c.fetchall()


def search_doc(word):

    c.execute(
        """
        SELECT Title, Content
        FROM Doc_FTS
        WHERE Doc_FTS MATCH ?
    """,
        (word,),
    )

    return c.fetchall()


conn.commit()
create_table()
create_fts_table()
