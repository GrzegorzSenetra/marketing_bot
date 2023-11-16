from classes import Client, MailScraper
import os

MS = MailScraper()

class Main: 
    last = 0
    limit = 30
    sites = []
    emails = []
    emails_strs = set()
    
    def __init__(self) -> None:
        pass

    def input_options(self):
        self.file_get_last_client()
        print("Choose starting client id:")
        self.last = input()
        print("Choose limit:")
        self.limit = input()
        
    def get_sites(self, clients):
        for client in clients:
            print("Extracting sites from " + client.domain)
            try: 
                MS.extract_sites(client.domain)
                self.sites.append(MS.domains)
            except Exception as e:
                print(e)
                continue
    
    def get_emails(self):
        for domains in self.sites:
            for site in domains:
                print("Extracting emails from " + site)
                try: 
                    self.emails.append(MailScraper.get_emails(site))
                except Exception as e:
                    print(e)
                    continue
                
    def show_emails(self):
        KEY_SITE = 0
        KEY_EMAIL = 1
        for emails in self.emails:
            for email in emails:
                self.emails_strs.add(email[KEY_SITE] + " " + email[KEY_EMAIL])
        for email in self.emails_strs:
            print(email)
                
    def get_last_client_id(self) -> str: 
        return str(int(self.last)+int(self.limit))
    
    def file_put_last_client(self):
        os.system("echo " + str(self.get_last_client_id()) + " > last_client_id.txt")
        
    def file_get_last_client(self):
        with open("last_client_id.txt", "r") as f:
            self.last = f.readline()
            print("LAST CLIENT ID: " + self.last)
    
    def get_only_emails(self, emails: str) -> None:
        """
        Extracts only emails from list of emails

        Args:
            emails (str): _description_
        """
        emails = self.emails_strs
        for email in emails:
            print(email.split(" ")[1])
    

def main():
    # @todo: add sites where no emails found to file
    print("========Marketing Mailing Manager========\n\n")
    m = Main()
    m.input_options()
    clients = Client.get_clients(m.last, m.limit)
    m.get_sites(clients)
    print(m.sites)
    print(clients)
    m.get_emails()
    print(m.emails)
    print("========MAILS FOUND========\n\n")
    m.show_emails()
    print("NUMBER OF FOUND MAILS: " + str(len(m.emails_strs)))
    print("LAST CLIENT: ", m.get_last_client_id())
    m.file_put_last_client()
    print("ONLY EMAILS: ")
    m.get_only_emails(m.emails_strs)

if __name__ == "__main__":
    main()
