# Rule-Based System for Suspect Inference
# First-Order Logic and Forward Chaining


# -----------------------------
# 1. FACTS
# -----------------------------

facts = {
    ("AtScene", "John", "CrimeScene"),
    ("AtScene", "Mary", "CrimeScene"),

    ("Motive", "John", "Victim"),
    ("Motive", "Steve", "Victim"),

    ("Owns", "John", "Gun"),
    ("FoundAt", "Gun", "CrimeScene"),

    ("Fingerprint", "John", "Gun"),

    ("NoAlibi", "John"),
    ("HasAlibi", "Mary"),
    ("HasAlibi", "Steve")
}


# -----------------------------
# 2. RULE R1
# AtScene(x) AND Motive(x)
#              -> Suspect(x)
# -----------------------------

def rule1(facts):
    new_facts = set()

    for fact in facts:
        if fact[0] == "AtScene":
            person = fact[1]

            if ("Motive", person, "Victim") in facts:
                conclusion = ("Suspect", person)

                if conclusion not in facts:
                    new_facts.add(conclusion)

                    print(
                        f"[R1] {person} was at the crime scene "
                        f"AND had a motive"
                    )
                    print(f"    => derived {conclusion}")

    return new_facts


# -----------------------------
# 3. RULE R2
# Suspect(x) AND NoAlibi(x)
#              -> PrimeSuspect(x)
# -----------------------------

def rule2(facts):
    new_facts = set()

    for fact in facts:
        if fact[0] == "Suspect":
            person = fact[1]

            if ("NoAlibi", person) in facts:
                conclusion = ("PrimeSuspect", person)

                if conclusion not in facts:
                    new_facts.add(conclusion)

                    print(
                        f"[R2] {person} is a Suspect "
                        f"AND has no alibi"
                    )
                    print(f"    => derived {conclusion}")

    return new_facts


# -----------------------------
# 4. RULE R3
# Owns(x,w) AND FoundAt(w,CrimeScene)
# AND Fingerprint(x,w)
#              -> LinkedToWeapon(x)
# -----------------------------

def rule3(facts):
    new_facts = set()

    for fact in facts:
        if fact[0] == "Owns":
            person = fact[1]
            weapon = fact[2]

            if (
                ("FoundAt", weapon, "CrimeScene") in facts
                and
                ("Fingerprint", person, weapon) in facts
            ):
                conclusion = ("LinkedToWeapon", person)

                if conclusion not in facts:
                    new_facts.add(conclusion)

                    print(
                        f"[R3] {person} owns {weapon}, "
                        f"{weapon} was found at the scene, "
                        f"and fingerprints are on {weapon}"
                    )
                    print(f"    => derived {conclusion}")

    return new_facts


# -----------------------------
# 5. RULE R4
# PrimeSuspect(x) AND LinkedToWeapon(x)
#              -> Guilty(x)
# -----------------------------

def rule4(facts):
    new_facts = set()

    for fact in facts:
        if fact[0] == "PrimeSuspect":
            person = fact[1]

            if ("LinkedToWeapon", person) in facts:
                conclusion = ("Guilty", person)

                if conclusion not in facts:
                    new_facts.add(conclusion)

                    print(
                        f"[R4] {person} is a PrimeSuspect "
                        f"AND is LinkedToWeapon"
                    )
                    print(f"    => derived {conclusion}")

    return new_facts


# -----------------------------
# 6. FORWARD CHAINING
# -----------------------------

def forward_chaining(facts):

    changed = True

    rules = [
        rule1,
        rule2,
        rule3,
        rule4
    ]

    while changed:

        changed = False

        for rule in rules:

            new_facts = rule(facts)

            if new_facts:

                facts = facts | new_facts

                changed = True

    return facts


# -----------------------------
# 7. MAIN PROGRAM
# -----------------------------

print("===================================")
print("     SUSPECT INFERENCE SYSTEM")
print("===================================")
print()

final_facts = forward_chaining(facts)

print()
print("===================================")
print("       FINAL KNOWLEDGE BASE")
print("===================================")

for fact in sorted(final_facts):
    print(fact)

print()
print("===================================")
print("             CONCLUSION")
print("===================================")

for fact in final_facts:

    if fact[0] == "Guilty":

        print(f"{fact[1]} is GUILTY.")
