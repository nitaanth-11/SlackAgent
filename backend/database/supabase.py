import logging
from typing import Optional
from supabase import create_client, Client
from backend import config

logger = logging.getLogger(__name__)

is_supabase_configured = (
    config.SUPABASE_URL 
    and config.SUPABASE_KEY 
    and not config.SUPABASE_URL.startswith("https://your-project")
    and config.SUPABASE_KEY != "your-supabase-anon-or-service-role-key"
)

supabase_client: Optional[Client] = None

if is_supabase_configured:
    try:
        supabase_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logger.info("Successfully connected to Supabase client.")
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}.")
else:
    logger.warning("Supabase URL or Key not set. Supabase client will be initialized as None (using in-memory fallback).")
