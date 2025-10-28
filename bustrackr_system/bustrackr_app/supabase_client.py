
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL="https://ugttejdzuuuwxegprhgc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVndHRlamR6dXV1d3hlZ3ByaGdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1ODEyNDAsImV4cCI6MjA3NTE1NzI0MH0.y2HdsZ0NeNQ2on8tLYUbVuiTCi2VST-CYGaPf6RQnXs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



