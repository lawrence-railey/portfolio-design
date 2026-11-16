"""Checks Python contact rendering and submission without sending email."""
import contextlib, io, json, os, runpy, sys, tempfile, types, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
if os.name=='nt':
    sys.modules['fcntl']=types.SimpleNamespace(LOCK_EX=1,flock=lambda *args:None)
MODULE=runpy.run_path(str(ROOT/'contact/index.cgi'),run_name='contact_test')
class ContactTests(unittest.TestCase):
    def test_confirmation(self):
        page=MODULE['render_page']('token',success=True)
        self.assertIn('Message sent.',page)
        self.assertIn('Thanks for reaching out.',page)
        self.assertIn('Connect on LinkedIn',page)
        self.assertIn('Download my résumé',page)
        self.assertNotIn('<form ',page)
        self.assertNotIn('<textarea',page)
        self.assertIn('hero-video',page)
    def test_error_preserves_and_escapes(self):
        page=MODULE['render_page']('token','Try again',{'name':'<script>','email':'a@example.com','message':'</textarea><script>alert(1)</script>'})
        self.assertIn('role="alert"',page)
        self.assertIn('&lt;script&gt;',page)
        self.assertNotIn('<script>alert(1)</script>',page)
        self.assertIn('<form ',page)
    def test_token(self):
        token=MODULE['token']('secret')
        self.assertTrue(MODULE['valid_token'](token,'secret'))
        self.assertFalse(MODULE['valid_token'](token,'wrong'))
        self.assertFalse(MODULE['valid_token']('broken','secret'))
    def test_invalid_input(self):
        for bad in [{'name':'bad\r\n','email':'a@example.com','message':'hello'},{'name':'ok','email':'bad','message':'hello'},{'name':'ok','email':'a@example.com','message':'a'*5001}]:
            with self.assertRaises(ValueError): MODULE['validate'](bad)
    def run_request(self, env, body=b''):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory,'config.json').write_text(json.dumps({'secret':'secret','origin':'https://lawrencerailey.com'}))
            output=io.StringIO()
            fake_stdin=types.SimpleNamespace(buffer=io.BytesIO(body))
            with patch.dict(MODULE['main'].__globals__,PRIVATE=Path(directory)), patch.dict(os.environ,env,clear=True), patch('sys.stdin',fake_stdin), contextlib.redirect_stdout(output), patch.dict(MODULE['main'].__globals__,deliver=lambda *args:None):
                MODULE['main']()
            return output.getvalue()
    def test_post_redirect_and_get_confirmation(self):
        from urllib.parse import urlencode
        token=MODULE['token']('secret')
        body=urlencode({'csrf':token,'name':'Test','email':'test@example.com','message':'Hello'}).encode()
        result=self.run_request({'REQUEST_METHOD':'POST','CONTENT_LENGTH':str(len(body)),'CONTENT_TYPE':'application/x-www-form-urlencoded','HTTP_COOKIE':'portfolio_contact_token='+token},body)
        self.assertIn('Status: 303 See Other',result)
        receipt=result.split('portfolio_contact_receipt=')[1].split(';')[0]
        page=self.run_request({'REQUEST_METHOD':'GET','QUERY_STRING':'sent=1','HTTP_COOKIE':'portfolio_contact_receipt='+receipt})
        self.assertIn('Thanks for reaching out.',page)
        self.assertNotIn('<form ',page)
    def test_success_cannot_be_spoofed_by_query(self):
        page=self.run_request({'REQUEST_METHOD':'GET','QUERY_STRING':'sent=1'})
        self.assertIn('<form ',page)
        self.assertNotIn('Thanks for reaching out.',page)
if __name__=='__main__':unittest.main()
