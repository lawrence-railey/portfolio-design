#!/usr/bin/python3
"""Server-rendered portfolio contact form with authenticated SMTP delivery."""
import os, sys, json, time, secrets, hmac, hashlib, html, re, ssl, smtplib, fcntl
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from email.message import EmailMessage

PRIVATE = Path(os.environ.get('PORTFOLIO_CONTACT_DIR', '/home2/lawreod5/portfolio-contact/python-mailer'))
ROOT = Path(__file__).resolve().parent.parent
URL = '/contact.html'
COOKIE_PATH = '/'

def signature(value, secret):
    return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()

def token(secret):
    value = str(int(time.time())) + '.' + secrets.token_hex(24)
    return value + '.' + signature(value, secret)

def valid_token(value, secret):
    try:
        stamp, nonce, sig = value.split('.')
        return 0 <= time.time()-int(stamp) < 3600 and len(nonce)==48 and hmac.compare_digest(signature(stamp+'.'+nonce,secret),sig)
    except (ValueError, TypeError): return False

def validate(values):
    for key, limit in [('name',100),('email',254),('message',5000)]:
        if not values.get(key,'').strip() or len(values[key]) > limit:
            raise ValueError('Please complete all fields within their length limits.')
    if any(c in values['name']+values['email'] for c in '\r\n\x00') or not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',values['email']):
        raise ValueError('Please enter a valid name and email address.')
    if values.get('website'): raise ValueError('Unable to accept this submission.')

def deliver(config, values, request_token):
    validate(values)
    now = time.time()
    key = signature(request_token, config['secret'])
    ip = signature(os.environ.get('REMOTE_ADDR','unknown'), config['secret'])
    state_path = PRIVATE/'requests.json'
    # Keep the lock through delivery so concurrent requests cannot send duplicates.
    with state_path.open('a+',encoding='utf-8') as state_file:
        os.chmod(state_path,0o600)
        fcntl.flock(state_file, fcntl.LOCK_EX)
        state_file.seek(0)
        records = json.loads(state_file.read() or '{}')
        records = {k:v for k,v in records.items() if now-v['time']<3600}
        if key in records:
            if records[key]['status']=='sent': return
            raise ValueError('This submission may already have been sent. Please email me directly before retrying.')
        if len(records)>=30 or sum(r['ip']==ip for r in records.values())>=5:
            raise ValueError('Too many attempts. Please try again later or email me directly.')
        def save():
            state_file.seek(0);state_file.truncate();json.dump(records,state_file);state_file.flush();os.fsync(state_file.fileno())
        records[key]={'time':now,'ip':ip,'status':'pending'}
        save()
        message=EmailMessage()
        message['From']=config['from']; message['To']=config['to']
        message['Reply-To']=values['email']
        message['Subject']='Portfolio inquiry — Lawrence Railey'
        message.set_content('Name: '+values['name']+'\nEmail: '+values['email']+'\n\n'+values['message'])
        context=ssl.create_default_context()
        if config['encryption']=='ssl':
            smtp=smtplib.SMTP_SSL(config['host'],int(config['port']),timeout=15,context=context)
        else:
            smtp=smtplib.SMTP(config['host'],int(config['port']),timeout=15)
            smtp.starttls(context=context)
        with smtp:
            smtp.login(config['username'],config['password'])
            smtp.send_message(message)
            records[key]['status']='sent';save()

def render_page(csrf, status='', values=None, success=False):
    values=values or {}
    page=(ROOT/'contact.html').read_text(encoding='utf-8')
    if success:
        form=re.search(r'<form class="contact-form".*?</form>',page,re.S).group()
        secondary=re.search(r'<div class="contact-secondary-actions">.*?</div>',form,re.S).group()
        confirmation=(ROOT/'content/contact-confirmation.html').read_text(encoding='utf-8')
        confirmation=confirmation.replace('<!-- SECONDARY_ACTIONS -->',secondary)
        page=page.replace(form,confirmation)
        page=page.replace("<span>Let's connect.</span>",'<span>Message sent.</span>')
        page=page.replace('<title>Contact |','<title>Message sent |')
    else:
        page=page.replace('<!-- CONTACT_TOKEN -->','<input type="hidden" name="csrf" value="'+html.escape(csrf,quote=True)+'">')
        if status:
            error='<div class="contact-status" role="alert"><p>'+html.escape(status)+'</p></div>'
            page=page.replace('<!-- CONTACT_ERROR -->',error)
        for field in ('name','email'):
            page=page.replace('name="'+field+'"','name="'+field+'" value="'+html.escape(values.get(field,''),quote=True)+'"',1)
        page=page.replace('aria-describedby="contact-message-error"></textarea>','aria-describedby="contact-message-error">'+html.escape(values.get('message',''))+'</textarea>')
    return page

def main():
    config=json.loads((PRIVATE/'config.json').read_text())
    status=''
    values={}; success=False
    cookies=SimpleCookie()
    try: cookies.load(os.environ.get('HTTP_COOKIE',''))
    except Exception: pass
    current=cookies.get('portfolio_contact_token')
    csrf=current.value if current and valid_token(current.value,config['secret']) else token(config['secret'])
    method=os.environ.get('REQUEST_METHOD','GET')
    if method not in ('GET','POST'):
        print('Status: 405 Method Not Allowed\r\nAllow: GET, POST\r\nContent-Type: text/plain\r\n\r\nMethod not allowed.');return
    receipt=cookies.get('portfolio_contact_receipt')
    if method=='GET' and os.environ.get('QUERY_STRING')=='sent=1' and receipt:
        success=valid_token(receipt.value,config['secret']+':receipt')
    if method=='POST':
        try:
            if os.environ.get('HTTP_ORIGIN','') not in ('',config['origin']) or os.environ.get('HTTP_SEC_FETCH_SITE')=='cross-site':
                raise ValueError('Please submit from this website.')
            length=int(os.environ.get('CONTENT_LENGTH','0'))
            if length<=0 or length>32768: raise ValueError('The message is too large.')
            if os.environ.get('CONTENT_TYPE','').split(';')[0]!='application/x-www-form-urlencoded':
                raise ValueError('Unsupported form submission.')
            fields=parse_qs(sys.stdin.buffer.read(length).decode('utf-8'),keep_blank_values=True,max_num_fields=10)
            if any(len(v)!=1 for v in fields.values()): raise ValueError('Invalid form submission.')
            values={k:v[0].strip() for k,v in fields.items()}
            if not current or not valid_token(values.get('csrf',''),config['secret']) or not hmac.compare_digest(current.value,values.get('csrf','')):
                raise ValueError('Your form expired. Please submit again.')
            deliver(config,values,csrf)
            receipt=token(config['secret']+':receipt')
            print('Status: 303 See Other\r\nLocation: '+URL+'?sent=1\r\nCache-Control: no-store\r\nSet-Cookie: portfolio_contact_receipt='+receipt+'; Path='+COOKIE_PATH+'; Max-Age=3600; Secure; HttpOnly; SameSite=Strict\r\nSet-Cookie: portfolio_contact_token=; Path='+COOKIE_PATH+'; Max-Age=0; Secure; HttpOnly; SameSite=Strict\r\n\r\n')
            return
        except ValueError as error: status=str(error)
        except Exception:
            status='We could not confirm delivery. Please email lawrence@lawrencerailey.com directly.'
    page=render_page(csrf,status,values,success)
    print('Content-Type: text/html; charset=utf-8\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nReferrer-Policy: same-origin\r\nSet-Cookie: portfolio_contact_token='+csrf+'; Path='+COOKIE_PATH+'; Secure; HttpOnly; SameSite=Strict\r\n\r\n'+page)

if __name__=='__main__':
    try: main()
    except Exception:
        print('Status: 503 Service Unavailable\r\nContent-Type: text/plain\r\nCache-Control: no-store\r\n\r\nThe contact form is unavailable. Please email lawrence@lawrencerailey.com.')
