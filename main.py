# TODO: complete dfa_apply_points()

# For more readability
def fancy_print(some_array):
    for elem in some_array:
        print(elem, "\n")


# Production Rule Format
class ProdRule:
    def __init__(self, derive_symbol, derivations, look_ahead=None):
        self.derive_symbol = derive_symbol
        self.derivations = derivations
        self.look_ahead = [] if look_ahead is None else look_ahead

    def __repr__(self):
        return f"{self.derive_symbol} -> {self.derivations}, look ahead: {self.look_ahead}"


# State Format
class State:
    state_num = 0

    def __init__(self, prod_rules):
        self.state_num = f"I{State.state_num}"
        self.prod_rules = prod_rules
        self.from_transitions = []
        self.to_transitions = []
        self.accept_state = False

        State.state_num += 1

    def __repr__(self):
        return f"{self.state_num}: {self.prod_rules}\n" \
               f"From: {self.from_transitions} To: {self.to_transitions}\n" \
               f"Accept State: {self.accept_state}"

    def check_accept_state(self):
        if len(self.to_transitions) == 0:
            self.accept_state = True


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


# For applying points to production rules
def apply_points(prod_rules, find_derive_symbol, track):
    for rule in prod_rules:
        if rule.derive_symbol == find_derive_symbol:
            track.append(find_derive_symbol)
            for i in range(len(rule.derivations)):
                rule.derivations[i] = f".{rule.derivations[i]}"
                dot_index = rule.derivations[i].index(".")
                if dot_index + 1 != len(rule.derivations[i]) and rule.derivations[i][dot_index + 1].isupper():
                    apply_points(prod_rules, rule.derivations[i][dot_index + 1], track)

    return prod_rules


# For extracting look ahead from production rules
def extract_look_ahead(prod_rules):
    for rule in prod_rules:
        if prod_rules.index(rule) > 0:
            prev_rule = prod_rules[prod_rules.index(rule) - 1]
            for prev_rule_derivation in prev_rule.derivations:
                dot_index = prev_rule_derivation.index(".")
                if len(prev_rule_derivation) == 2:
                    rule.look_ahead.append(prev_rule.look_ahead[prev_rule.derivations.index(prev_rule_derivation)])
                elif len(prev_rule_derivation) > 2 and prev_rule_derivation[dot_index + 2].isupper():
                    for rule_j in prod_rules:
                        if rule_j.derive_symbol == prev_rule_derivation[dot_index + 2]:
                            for rule_j_derivation in rule_j.derivations:
                                if rule_j_derivation[1].islower():
                                    rule.look_ahead.append(rule_j_derivation[1])

    return prod_rules


def dfa_apply_points(state_machine):
    pass


# For constructing DFA from production_rules
def construct_dfa(state_machine):
    state = state_machine[0]
    for rule in state.prod_rules:
        for derivation in rule.derivations:
            dot_index = derivation.index(".")
            derivation_index = rule.derivations.index(derivation)
            if dot_index + 1 != len(derivation):
                swap_string = derivation[dot_index: dot_index + 2]
                swap_string = swap_string[::-1]
                rule.derivations[derivation_index] = derivation[:dot_index] + swap_string + derivation[dot_index + 3:]
            state_machine.append(
                State(ProdRule(rule.derive_symbol, rule.derivations[derivation_index], rule.look_ahead)))


with open("input.txt", "r") as input_file:
    content = input_file.readlines()
    content = list(map(lambda x: x.rstrip("\n"), content))

    prod_rules = extract_prod_rules(content)
    augment_prod_rules(prod_rules)

    track = []
    apply_points(prod_rules, prod_rules[0].derive_symbol, track)
    extract_look_ahead(prod_rules)

    state_machine = [State(prod_rules)]
    construct_dfa(state_machine)

    fancy_print(state_machine)
