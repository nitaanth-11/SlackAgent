import json
import os


class ContactCache:

    def __init__(self, filename="contacts_cache.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def save_contacts(self, contacts):
        with open(self.filename, "w") as f:
            json.dump(contacts, f, indent=4)

    def get_contacts(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def add_contact(self, name, phone):
        contacts = self.get_contacts()

        contacts.append({
            "name": name,
            "phone": phone
        })

        self.save_contacts(contacts)


contact_cache = ContactCache()