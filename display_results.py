class Results:
    def __init__(self, results=None):
        self.results = results

    def print_results(self):
        if type(self.results) is not dict:
            print("Error: results are not a dictionary!")
            return False

        for x, y in self.results.items():
            print(x, y)
            for a, b in y.items():
                if b == '':
                    continue
                else:
                    print(a, b)
            print("\r")

        return True
