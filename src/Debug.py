import src.scraper.InfaticaRequests as InfaticaRequests
from pathlib import Path

def main():
    check_connection()

def check_connection():
    response = InfaticaRequests.get_response('https://www.google.com/')
    response = response[0]

    html = response['html']

    path = Path('test.txt')
    with open(path, 'w', encoding='utf-8') as f:
        print(html, file=f)

    print(f'Http response saved to {path}.')

# From the python docs tutorial:
# excs = []
# for test in tests:
#     try:
#         test.run()
#     except Exception as e:
#         excs.append(e)

# if excs:
#    raise ExceptionGroup("Test Failures", excs)

if __name__ == '__main__':
    main()
