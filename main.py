# TODO: complete construct_dfa()

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
        return f"{self.derive_symbol} -> {self.derivations}, look ahead: {self.look_ahead}"


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


# For applying points to production rules
def apply_points(prod_rules, find_derive_symbol):
    for rule in prod_rules:
        if rule.derive_symbol == find_derive_symbol:
            track.append(find_derive_symbol)
            for i in range(len(rule.derivations)):
                rule.derivations[i] = f".{rule.derivations[i]}"
                if rule.derivations[i][1].isupper():
                    apply_points(prod_rules, rule.derivations[i][1])

    return prod_rules


# For extracting look ahead from production rules
def extract_look_ahead(prod_rules):
    for rule in prod_rules:
        if prod_rules.index(rule) > 0:
            prev_rule = prod_rules[prod_rules.index(rule) - 1]
            for prev_rule_derivation in prev_rule.derivations:
                if len(prev_rule_derivation) == 2:
                    rule.look_ahead.append(prev_rule.look_ahead[prev_rule.derivations.index(prev_rule_derivation)])
                elif len(prev_rule_derivation) > 2 and prev_rule_derivation[2].isupper():
                    for rule_j in prod_rules:
                        if rule_j.derive_symbol == prev_rule_derivation[2]:
                            for rule_j_derivation in rule_j.derivations:
                                if rule_j_derivation[1].islower():
                                    rule.look_ahead.append(rule_j_derivation[1])

    return prod_rules


# For constructing DFA from production_rules
def construct_dfa(prod_rules):
    pass


with open("input.txt", "r") as input_file:
    content = input_file.readlines()
    content = list(map(lambda x: x.rstrip("\n"), content))

    prod_rules = extract_prod_rules(content)
    augment_prod_rules(prod_rules)
    apply_points(prod_rules, prod_rules[0].derive_symbol)
    extract_look_ahead(prod_rules)

    fancy_print(prod_rules)
