from concurrent.futures import ThreadPoolExecutor
def runTests(scorers: list):
    results = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        