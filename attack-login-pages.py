import sys
import multiprocessing

import subdomain_scanner

# I would run on the domains with the help of the library asyncio

if __name__ == '__main__':
    
    # extract the domains list
    domains_list = None
    if "-d" in sys.argv:
        domains_list = [domain for domain in sys.argv[sys.argv.index('-d') + 1:]]
        domains_list = [domain.replace(',', '') for domain in domains_list]

    for domain in domains_list:
        print(f"Current domain is: {domain}")
        p = multiprocessing.Process(target=subdomain_scanner.SubDomainScanner(domain).scan)
        p.start()
