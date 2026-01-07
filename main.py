from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from supabase import create_client

db_url = "https://bkldnlrrpconcjuqkhja.supabase.co"
db_key = "sb_publishable_2EEWlonB1GPZDCcKT_vM0A_TbIMpl8A"

db = create_client(db_url, db_key)

app = FastAPI()


@app.post('/add/contact')
async def add_contact(request : Request):
    data = await request.json()
    db.table('contacts').insert(data).execute()
    return {"message":"successfull"}


@app.get('/contacts')
def get_all_contacts():
    result = db.table('contacts').select('*').execute()
    # contacts = result.data
    return result.data


@app.get('/contact/{contact_id}')
def get_contact(contact_id: int):
    result = db.table('contacts').select('*').eq('id', contact_id).execute()
    # contacts = result.data
    return result.data

@app.put('/contact/{contact_id}')
async def add_contact(request: Request,contact_id):
    data = await request.json()
    result = db.table('contacts').update(data).eq('id', contact_id).execute()
    return "updated successfully"


@app.delete('/contact/{contact_id}')
def delete_contacts(contact_id):
    result = db.table('contacts').delete().eq('id', contact_id).execute()
    return "deleted successfully"