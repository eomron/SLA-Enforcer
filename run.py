from concurrent.futures import ThreadPoolExecutor
from scorer import ScoreChecker

def main():
    checker = ScoreChecker("test","172.253.115.101",443)
    print("\"" + str(checker.url("https")[0]) + "\"")

def runTests(scorers: list,numChecks:int):
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

if __name__ == "__main__":
    main()

# a new ScoreChecker object should be instantiated for every vuln in the config CSV, stored as a list