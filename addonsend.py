class Send():
    def __init__(self,
    email,
    dkimverify,
    session,envelope,
    email_dict,
    hmactime,
    hmac_digest,
    webhook_headers) -> str:
        
        self.email = email
        self.dkimverify = dkimverify
        self.session = session
        self.envelope = envelope
        self.email_dict = email_dict
        self.hmactime = hmactime
        self.hmac_digest = hmac_digest
        self.webhook_headers = webhook_headers

        self.response()

    def response():
        return '250 Message accepted'
