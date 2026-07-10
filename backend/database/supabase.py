"""Supabase client singleton — initialized at import time."""

import logging
from supabase import create_client

try:
    from config import SUPABASE_URL, SUPABASE_SECRET_KEY
except ImportError:
    from backend.config import SUPABASE_URL, SUPABASE_SECRET_KEY

logger = logging.getLogger(__name__)

supabase = None

if SUPABASE_URL and SUPABASE_SECRET_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
        logger.info("Supabase client initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
else:
    logger.warning("Supabase credentials missing. Client not initialized.")
