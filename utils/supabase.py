from collections import deque
import os
import requests
from supabase import create_client, Client
from configuration import SUPABASE_PROJECT_URL, SUPABASE_API_KEY, MAX_MESSAGE
