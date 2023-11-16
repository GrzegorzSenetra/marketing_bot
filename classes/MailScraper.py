import validators
import requests
import urllib.parse
import html
from bs4 import BeautifulSoup

CONN_TIMEOUT_SEC = 30

class MailScraper: 
    domains = []
    
    def extract_sites(self, domain):
        self.domains = domain.split("++")
        
        # Validate domains
        for domain in self.domains:
            if validators.domain(domain):
                print("Valid domain")
            else: 
                print("Invalid domain")
                self.domains.remove(domain)
                
        if self.domains:
            print("Domains extracted")
            return True
        else:
            raise Exception("No domains extracted")
        
    @staticmethod
    def get_emails(site):
        print("Extracting emails from " + site)
        KEY_EMAIL = 1
        emails = []
        regulamin_link = MailScraper.find_site_link(site, "regulamin")
        
        # if not exception raised, regulamin link found
        if not regulamin_link:
            html_data = MailScraper.conn_to_site(site)
        else:
            html_data = MailScraper.conn_to_site(regulamin_link)
            
        print("REGULAMIN LINK: " + regulamin_link)
        for link in html_data.find_all('a'):
            if link.has_attr('href'):
                if link['href'].startswith("mailto:"):
                    emails.append([site, link['href'].replace("mailto:", "")])
                    
        # find emails not by mailto but by regex
        for link in html_data.find_all('a'):
            if link.has_attr('href'):
                if link['href'].startswith("mailto:"):
                    continue
                else:
                    # check if link has text in href or content
                    if "@" in link['href'] or "@" in link.text:
                        emails.append([site, link['href']])
                        
        if emails:
            # @todo: decode emails, save sites that has errors in file
            # decode html encoded emails
            for email in emails:
                email[KEY_EMAIL] = MailScraper.decode_email(email[KEY_EMAIL])
                if not MailScraper.validate_email(email[KEY_EMAIL]):
                    emails.remove(email)
            print("Emails found: " + str(emails))
            return emails
        else:
            raise Exception("No emails found")
        
    @staticmethod
    def validate_email(email):
        if validators.email(email):
            print("Valid email")
            return True
        else:
            print("Invalid email")
            return False
        
    @staticmethod
    def decode_email(email):
        result = MailScraper.html_encode(email)
        if result is None:
            return email
        return result

    @staticmethod
    def html_encode(input_string):
        decoded_string = None
        # Try URL decoding first
        try:
            decoded_string = urllib.parse.unquote(input_string)
        except:
            pass
        # If URL decoding fails, try HTML decoding
        if decoded_string is None:
            decoded_string = html.unescape(input_string)
    
    @staticmethod
    def conn_to_site(domain):
        print("Connecting to " + domain)
        r = requests.session()
        
        try:
            if not domain.startswith("https://"):
                domain = "https://" + domain
            response = r.get(domain, timeout=CONN_TIMEOUT_SEC)
        except Exception as e:
            raise Exception("Could not connect to " + domain)
        
        if response.status_code == 200:
            print("Connected to " + domain)
        else:
            raise Exception("Could not connect to " + domain)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    @staticmethod
    def find_site_link(domain, text):
        founded_link = ""
        
        try: 
            html_data = MailScraper.conn_to_site(domain)
        except Exception as e:
            raise Exception("Could not connect to " + domain)
        
        for link in html_data.find_all('a'):
            if link.has_attr('href'):
                # check if link has text in href or content
                if text in link['href'] or text in link.text:
                    founded_link = link['href']
                    break
        
        if founded_link:
            print("Link found: " + founded_link)
            return founded_link
        else:
            raise Exception("Link not found")