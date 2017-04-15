from Bio.SeqUtils import MeltingTemp as mt


def to_dna(rna):
    return "".join(map(lambda n: 'T' if n == 'U' else n, rna))


def get_compl(dna):
    return ''.join(list(map(lambda n: {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}[n], dna)))


def calc_melt_temp(dna):
    return mt.Tm_NN(to_dna(dna), dnac1=400, dnac2=400, saltcorr=4, Na=150)


def validate_rna(rna):
    return set(rna) <= set(['A', 'C', 'G', 'U'])


def validate_rna_length(rna):
    return len(rna) > 15 and len(rna) < 40


def count_of_A_or_T_in_range(dna, range):
    return dna.count('A') in range or dna.count('T') in range


def last_five_nucliotides_are_ok(dna):
    return count_of_A_or_T_in_range(dna[-5:], range(2,4)) or \
        count_of_A_or_T_in_range(dna[-3:], range(1,3)) or \
        count_of_A_or_T_in_range(dna[-2:], range(1,2))


def calculate_at_statuses(dna):
    return {
        'at5': count_of_A_or_T_in_range(dna[-5:], range(2,4)),
        'at3': count_of_A_or_T_in_range(dna[-3:], range(1,3)),
        'at2': count_of_A_or_T_in_range(dna[-2:], range(1,2))
    }


def create_primer_entry(sequence, at_statuses):
    d = {}
    d['sequence'] = sequence
    d['length'] = len(sequence)
    d['tm'] = round(calc_melt_temp(sequence), 3)
    d['at5'] = at_statuses['at5']
    d['at3'] = at_statuses['at3']
    d['at2'] = at_statuses['at2']

    return d


def calculate_primers(mi_rna):
    purified_mi_rna = ''.join(mi_rna.upper().split())

    if not validate_rna(purified_mi_rna):
        raise Exception('Not an RNA string')

    if not validate_rna_length(purified_mi_rna):
        raise Exception('MiRNA string length should be lay between 15 and 40 nucleotides')

    mi_rna_dna = to_dna(purified_mi_rna)
    reversed_mi_rna_dna = mi_rna_dna[::-1]

    forwards = []
    reverses = []

    forward = ''

    for i in range(12, min(18, len(mi_rna_dna) - 4)):
        if not last_five_nucliotides_are_ok(mi_rna_dna[:i]):
            continue

        addition = 'CGCAG'

        for j in range(1, 5):
            forward = addition[-j:] + mi_rna_dna[:i]

            if calc_melt_temp(forward) > 59:
                break

        if calc_melt_temp(forward) > 59:
            at_statuses = calculate_at_statuses(mi_rna_dna[:i])
            forwards.append(create_primer_entry(forward, at_statuses))
            print('forvard', i, mi_rna_dna[:i], forward, calc_melt_temp(forward))

    reverse = ''
    addition = 'CAGGTCCAG'

    for i in reversed(range(4, 9)):
        reverse_candidate = get_compl(mi_rna_dna[len(mi_rna_dna)-i:][::-1])

        if not last_five_nucliotides_are_ok(reverse_candidate):
            continue

        reverse_candidate = 'TTTTTTTTTTTTTTT' + reverse_candidate

        for j in range(1, 9):
            reverse = addition[-j:] + reverse_candidate

            if calc_melt_temp(reverse) > 59:
                break

        if calc_melt_temp(reverse) > 59:
            at_statuses = calculate_at_statuses(reverse_candidate)
            reverses.append(create_primer_entry(reverse, at_statuses))
            print('reverse', i, reverse_candidate, reverse, calc_melt_temp(reverse))

    return {'reverses': reverses, 'forwards': forwards}
