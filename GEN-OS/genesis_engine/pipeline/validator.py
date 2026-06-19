class Validator:
    def run(self, items):
        valid = []
        for item in items:
            if item:
                valid.append(item)
        return valid
