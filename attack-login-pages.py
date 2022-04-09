import sys
import multiprocessing

import subdomain_scanner


domains_list = None
if "-d" in sys.argv:
    domains_list = [domain for domain in sys.argv[sys.argv.index('-d') + 1:]]
    domains_list = [domain.replace(',', '') for domain in domains_list]


if __name__ == '__main__':
    for domain in domains_list:
        print(f"Current domain is: {domain}")
        p = multiprocessing.Process(target=subdomain_scanner.SubDomainScanner(domain).scan())
        p.start()