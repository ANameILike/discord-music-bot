# Displays duplicate items in a list and returns a new list with duplicates removed, preserving the first instance.
def remove_dupes(list_with_dupes):
    duped_values = []
    temporarily_alphabetized = sorted(list_with_dupes)
    for i in range(len(temporarily_alphabetized) - 1):
        if temporarily_alphabetized[i] == temporarily_alphabetized[i+1]:
            duped_values.append(temporarily_alphabetized[i])
    reversed_original = list_with_dupes[::-1]
    for duped_value in duped_values:
        reversed_original.remove(duped_value)
    list_of_uniques = reversed_original[::-1]
    print(f"Duplicates: {duped_values}")
    return list_of_uniques

