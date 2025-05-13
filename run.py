from concurrent.futures import ThreadPoolExecutor
from scorer import ScoreChecker
numChecks = 10


def runTests(scorers: list):
    results = []
    with ThreadPoolExecutor(max_workers=numChecks) as pool:
        futures = {pool.submit(scorer.test): scorer for scorer in scorers}
        for future in futures:
            scorer = futures[future]
            try:
                result = future.result()
                results.append((scorer.name,scorer.ip,scorer.type,result))
            except Exception as e:
                results.append((scorer.name,scorer.ip,scorer.type,e))
    return results

checker = ScoreChecker("test","172.253.115.101",443)
print(checker.url("https"))

# a new ScoreChecker object should be instantiated for every vuln in the config CSV, stored as a list