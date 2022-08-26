from supabase import create_client, Client

def insert_data(roll_number: int):
    url: str = "https://neyhfutgzgrfxqgxqtav.supabase.co"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5leWhmdXRnemdyZnhxZ3hxdGF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTg4MzI2NTMsImV4cCI6MTk3NDQwODY1M30.af_vgVwCd7lw_wHy62NA3bXfdGL_4m9hBCDT4k3TyCA"
    supabase: Client = create_client(url, key)
    in_data = {'roll_number': roll_number}
    data = supabase.table('attendance_logs').insert(in_data).execute()
    print(data)