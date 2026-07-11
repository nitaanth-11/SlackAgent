from backend.ai.services.location_cache import location_cache

location_cache.save(
    19.0760,
    72.8777
)

print(location_cache.get())