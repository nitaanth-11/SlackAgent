from backend.ai.services.contact_cache import contact_cache

contact_cache.add_contact(
    "Tanaya",
    "+919999999999"
)

contact_cache.add_contact(
    "Nitaanth",
    "+918888888888"
)

print(contact_cache.get_contacts())