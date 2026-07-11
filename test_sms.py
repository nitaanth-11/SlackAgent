from backend.ai.services.sms import sms_provider
from backend.ai.services.contact_cache import contact_cache


contacts = contact_cache.get_contacts()

for contact in contacts:
    sms_provider.send_sms(
        contact["phone"],
        "OpsPilot Alert: Internet connection lost."
    )