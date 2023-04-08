from spf import check2
from requests import post
from os import environ
from json import dumps, loads
from email.message import MIMEPart
from email.parser import Parser
from email.policy import default
from aiosmtpd.smtp import SMTP as SMTPServer
from aiosmtpd.smtp import Envelope as SMTPEnvelope
from aiosmtpd.smtp import Session as SMTPSession
from aiosmtpd.controller import Controller
from dkim import verify
from time import sleep, time
from hashlib import sha256
from hmac import digest

host = environ.get('HOST','0.0.0.0')
port = environ.get('PORT',25)

target_email = environ.get('TARGET_EMAIL',None)
source_email = environ.get('SOURCE_EMAIL',None)

spf_allow_list = environ.get('SPF_ALLOW_LIST',[])
if spf_allow_list:
    spf_allow_list = loads(spf_allow_list)

dkim_reject = environ.get('DKIM_REJECT',None)

ident = environ.get('IDENT','')
email_size = environ.get('EMAIL_SIZE',5048576)
log_off = environ.get('LOG_OFF',None)

webhook = environ.get('WEBHOOK_URL',None)
webhook_headers = environ.get('WEBHOOK_HEADERS',{})
if webhook_headers:
    webhook_headers = loads(webhook_headers)

hmac_secret = environ.get('HMAC_SECRET',None)

class InboundChecker:
    async def handle_RCPT(self, server, session: SMTPSession, envelope: SMTPEnvelope, address :str, rcpt_options):

        if target_email:
            if not address.endswith(target_email):
                return '556 Not accepting for that domain'
        
        if source_email:
            if not envelope.mail_from.endswith(source_email):
                return '550 Not accepting emails from your email'
        
        self.sfp = check2(i=session.peer[0],
                        s=envelope.mail_from,
                        h=session.host_name,verbose=False)
        
        if spf_allow_list:
            if self.sfp[0] not in spf_allow_list:
                return f'550 Refused because SPF record is {self.sfp}'
            
        envelope.rcpt_tos.append(address)

        if log_off is None:
            print(f'Accepted connection from {session.peer[0]}, for {address}, from {envelope.mail_from}',flush=True)
        
        return '250 OK' 

    async def handle_DATA(self, server: SMTPServer, session: SMTPSession, envelope: SMTPEnvelope):

        email:MIMEPart = Parser(policy=default).parsestr(envelope.content.decode('utf8', errors='replace'))

        dkimverify = verify(envelope.content)
        
        if dkim_reject:
            if dkimverify is not True:
                return '550 DKIM failed email is rejected'

        def payload(part):
            body = email.get_body(preferencelist=(part))
            if body:
                return body.get_payload(decode=False)
            return None
        
        email_dict = {}
        for i in email.keys():
            email_dict[i] = email.get(i)
        email_dict['Spf'] = self.sfp
        email_dict['Dkim-Pass'] = dkimverify
        email_dict['Session-IP'] = session.peer[0]
        email_dict['From-RCPT'] = envelope.mail_from
        email_dict['To-RCPT'] = envelope.rcpt_tos[0]
        email_dict['Bodyplain'] = payload('plain')
        email_dict['Bodyhtml'] = payload('html')
        email_dict['Raw'] = envelope.content.decode('utf8', errors='replace')
        
        try: # Not the the most pythonic way but made for docker
            from addonparse import Parse
            Parse(email,dkimverify,session,envelope,email_dict)
            email = Parse.email
            dkimverify = Parse.dkimverify
            session = Parse.session
            envelope = Parse.envelope
            email_dict = Parse.email_dict
        except: pass # No addon found

        if hmac_secret:
            hmactime = str(time())
            hmac_digest = digest(f'{hmac_secret+hmactime}'.encode(),dumps(email_dict).encode(),sha256).hex()
        
        try: # if you want to make your own sender, have to return response as SMTP server
            from addonsend import Send
            return Send(email,dkimverify,session,envelope,email_dict,hmactime,hmac_digest,webhook_headers)
            
        except:
            #addon sender takes care of the rest including return
            if webhook:
                if hmac_secret:
                    webhook_headers['HMAC-Time'] = hmactime
                    webhook_headers['HMAC-Signature'] = hmac_digest
                res = post(webhook,json=email_dict,headers=webhook_headers)
                if log_off is None:
                    print(res.text,flush=True)
            else:
                print(dumps(email_dict,indent=4),flush=True)

            return '250 Message accepted'

if __name__ == '__main__':
    controller = Controller(InboundChecker(),hostname=host,port=port,ident=ident,data_size_limit=email_size)
    controller.start()
    while True:
        sleep(100)
