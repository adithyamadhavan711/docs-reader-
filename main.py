from drive import get_documents_drive
from docs import documentcontent
from sqlite import get_doc, insert, update_doc, delete_doc, get_all_ids, search_doc
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--command", choices=["load", "search"], required=True)

parser.add_argument("--word")

args = parser.parse_args()

if args.command == "load":

    documents = get_documents_drive()

    google_drive_id = []

    # goes thru every single doc and gets id and modified time and saves

    for document in documents:

        doc_id = document["id"]
        modified_time = document["modifiedTime"]
        google_drive_id.append(doc_id)

        # gets the id and if it returns none (new doc)
        old_id = get_doc(doc_id)

        if old_id is None:

            # gets the title and content
            title, content = documentcontent(doc_id)

            insert(doc_id, title, content, modified_time)

            print("Added:", title)

        # the document exists in the sqlite db but is changed (compare modified time)
        elif old_id[3] != modified_time:

            title, content = documentcontent(doc_id)

            update_doc(doc_id, title, content, modified_time)

            print("Updated:", title)

        # nothing was changed
        else:

            print("No change:", old_id[1])

    for document in get_all_ids():

        # storin all db ids
        db_id = document[0]

        # if the id is not in google_Drive_ID then delete that doc
        if db_id not in google_drive_id:

            delete_doc(db_id)

            print("Deleted:", db_id)


elif args.command == "search":

    results = search_doc(args.word)

    for title, content in results:

        print("Title:", title)
        print(content)
