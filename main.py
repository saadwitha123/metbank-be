from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
 
db = create_client("https://lxnfwmegsjrrpkmwamuo.supabase.co", "sb_publishable_LCidkXiw0sqgLPCoQkq32w_Mze1A6rK")
 
app = FastAPI(title= "MET Bank")
 
@app.get('/accounts')
def get_all_accounts():
    result = db.table("accounts").select('*').execute()
    data = result.data
    print(data)
    if data:
        return JSONResponse(data)
 
@app.get('/accoounts/{account_no}')
def get_account_by_account_number(account_no):
    result = db.table('accounts').select('*').eq('account_no', account_no).execute()
    data = result.data
    if data:
        return JSONResponse(data)
 
#Transactions
# /transactions?source=125678212&dest=237568919&amount=500 POST
 
@app.get('/transactions')
def get_all_transactions():
    r = db.table('transactions').select('*').execute()
    d = r.data
    return JSONResponse(d)
 
@app.post('/transactions')
def perform_transaction(source, dest, amount):
    # First see enough balance in source account
    amount = int(amount)
    result = db.table('accounts').select('balance').eq('account_no', source).execute()
    data = result.data
    src_balance = data[0]['balance']
 
    if src_balance > int(amount):
        # Decuct balance in source account - record transaction as debit
        r1 = db.table('accounts').update({'balance': int(src_balance) - int(amount)}).eq('account_no', source).execute()
        db.table('transactions').insert({
            'amount': amount,
            'type': 'debit',
            'account_no': source
        }).execute()
 
        # Credit balance in dest account - record transactin as credit
        r3 = db.table('accounts').select('balance').eq('account_no', dest).execute()
        d = r3.data
        dest_balance = d[0]['balance']
        db.table('accounts').update({'balance': int(dest_balance) + int(amount)}).eq('account_no', dest).execute()
        db.table('transactions').insert({
            'amount': amount,
            'type': 'credit',
            'account_no': dest
        }).execute()
        return JSONResponse({'message': 'Transfer successfull'})
        # success
    else:
        return JSONResponse({'message': 'No Enough balance'})
