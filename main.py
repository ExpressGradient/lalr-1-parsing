# For more readability
def fancy_print(some_array):
    for elem in some_array:
        print(elem, "\n")


# Production Rule Format
class ProdRule:
    def __init__(self, derive_symbol, derivations):
        self.derive_symbol = derive_symbol
        self.derivations = derivations
        self.look_ahead = []

    def __repr__(self):
        return f"{self.derive_symbol} -> {self.derivations}, {self.look_ahead}"


# For extracting production rules
def extract_prod_rules(content):
    for line in content:
        derive_symbol, derivations = line.split("->")
        derivations = derivations.split("/")
        content[content.index(line)] = ProdRule(derive_symbol, derivations)

    return content


# For augmenting the production rules
def augment_prod_rules(prod_rules):
    start_symbol = prod_rules[0].derive_symbol
    prod_rules.insert(0, ProdRule(f"{start_symbol}`", [start_symbol]))
    prod_rules[0].look_ahead.append("$")

    return prod_rules


track = []


# For applying points
def apply_points(prod_rules, find_derive_symbol):
    for rule in prod_rules:
        if rule.derive_symbol == find_derive_symbol:
            track.append(find_derive_symbol)

            for i in range(len(rule.derivations)):
                rule.derivations[i] = f".{rule.derivations[i]}"

                if rule.derivations[i][1].isupper():
                    apply_points(prod_rules, rule.derivations[i][1])


# For extracting look ahead
def extract_look_ahead(prod_rules):
    pass


input_file = open("input.txt", "r")
content = input_file.readlines()
content = list(map(lambda x: x.rstrip("\n"), content))

prod_rules = extract_prod_rules(content)
augment_prod_rules(prod_rules)
apply_points(prod_rules, prod_rules[0].derive_symbol)

fancy_print(prod_rules)
input_file.close()

# TODO: complete extract_look_ahead()
