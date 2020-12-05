from copy import deepcopy


# TODO: complete dfa_apply_points()

# For more readability
def fancy_print(some_array):
    for elem in some_array:
        print(elem, "\n")


# Production Rule Format
class ProdRule:
    def __init__(self, derive_symbol, derivations, look_ahead=None):
        self.derive_symbol: str = derive_symbol
        self.derivations: list = derivations
        self.look_ahead: list or None = [] if look_ahead is None else look_ahead

    def __repr__(self):
        return f"{self.derive_symbol} -> {self.derivations}, look ahead: {self.look_ahead}"


# State Format
class State:
    state_num = 0

    def __init__(self, prod_rules):
        self.state_num: str = f"I{State.state_num}"
        self.prod_rules: list = prod_rules
        self.from_transitions: list = []
        self.to_transitions: list = []
        self.accept_state: bool = False

        State.state_num += 1

    def __repr__(self):
        return f"{self.state_num}: {self.prod_rules}\n" \
               f"From: {self.from_transitions} To: {self.to_transitions}\n" \
               f"Accept State: {self.accept_state}"

    def check_accept_state(self):
        for rule in self.prod_rules:
            for derivation in rule.derivations:
                if derivation[-1] == ".":
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
                dot_idx = rule.derivations[i].index(".")
                if dot_idx + 1 != len(rule.derivations[i]) and rule.derivations[i][dot_idx + 1].isupper():
                    apply_points(prod_rules, rule.derivations[i][dot_idx + 1], track)

    return prod_rules


# For extracting look ahead from production rules
def extract_look_ahead(prod_rules):
    for rule in prod_rules:
        if prod_rules.index(rule) > 0:
            prev_rule = prod_rules[prod_rules.index(rule) - 1]
            for prev_rule_derivation in prev_rule.derivations:
                dot_idx = prev_rule_derivation.index(".")
                if len(prev_rule_derivation) == 2:
                    rule.look_ahead.append(prev_rule.look_ahead[prev_rule.derivations.index(prev_rule_derivation)])
                elif len(prev_rule_derivation) > 2 and prev_rule_derivation[dot_idx + 2].isupper():
                    for rule_j in prod_rules:
                        if rule_j.derive_symbol == prev_rule_derivation[dot_idx + 2]:
                            for rule_j_derivation in rule_j.derivations:
                                if rule_j_derivation[1].islower():
                                    rule.look_ahead.append(rule_j_derivation[1])

    return prod_rules


# DFA transitions
def dfa_apply_transition(state_machine, state_idx):
    for state in state_machine:
        if state.state_num == state_idx:
            current_state = state
            temp_rules = deepcopy(current_state.prod_rules)
            for rule in temp_rules:
                for derivation in rule.derivations:
                    if "." in derivation:
                        dot_idx = derivation.index(".")
                        if dot_idx + 1 != len(derivation):
                            swap_str = derivation[dot_idx: dot_idx + 2]
                            swap_str_rev = swap_str[::-1]
                            derivation = derivation.replace(swap_str, swap_str_rev)
                            temp_rule = ProdRule(rule.derive_symbol, [derivation], rule.look_ahead)
                            temp_state = State([temp_rule])
                            temp_state.check_accept_state()
                            temp_state.from_transitions.append({derivation[dot_idx-1]: current_state.state_num})
                            current_state.to_transitions.append({derivation[dot_idx-1]: temp_state.state_num})
                            state_machine.append(temp_state)


# For constructing the DFA
def construct_dfa(state_machine, state_track):
    for states in state_track:
        for state_idx in states:
            dfa_apply_transition(state_machine, state_idx)


with open("input.txt", "r") as input_file:
    content = input_file.readlines()
    content = list(map(lambda x: x.rstrip("\n"), content))

    prod_rules = extract_prod_rules(content)
    augment_prod_rules(prod_rules)

    track = []
    apply_points(prod_rules, prod_rules[0].derive_symbol, track)
    extract_look_ahead(prod_rules)

    state_machine = [State(prod_rules)]
    state_track = [["I0"]]
    construct_dfa(state_machine, state_track)

    fancy_print(state_machine)
