AT_DEFAULT_CLASSES = ['at-status', 'tooltipped', 'tooltipped-nw']
AT_HINT_TEMPLATE = 'Last {last_nucliotides_count} bases at the 3`' \
                 + 'end {dont}include {residue_length} A or T residues'


def generate_A_T_hint(checkStatus, type):
    dont = '' if checkStatus else 'don`t '
    last_nucliotides_count = ''
    residue_length = ''

    if type == 'at5':
        last_nucliotides_count = '5'
        residue_length = '2-3'
    elif type == 'at3':
        last_nucliotides_count = '3'
        residue_length = '1-2'
    elif type == 'at2':
        last_nucliotides_count = '2'
        residue_length = '1'
    else:
        raise Exception('unsupported type in generate_A_T_hint')

    return AT_HINT_TEMPLATE.format(
        last_nucliotides_count=last_nucliotides_count,
        dont=dont,
        residue_length=residue_length
    )


def generate_A_T_classes(checkStatus):
    at_classes = AT_DEFAULT_CLASSES + ['at-status_green' if checkStatus else 'at-status_red']
    return ' '.join(at_classes)


def generate_A_T_status(checkStatus, type):
    return {
        'classes': generate_A_T_classes(checkStatus),
        'hint': generate_A_T_hint(checkStatus, type)
    }


def build_primers_view(primers):
    forwards = []

    for forward_primer in primers['forwards']:
        d = {}

        d['sequence'] = forward_primer['sequence']
        d['length'] = forward_primer['length']
        d['tm'] = forward_primer['tm']

        at_statuses = [
            generate_A_T_status(forward_primer['at5'], 'at5'),
            generate_A_T_status(forward_primer['at3'], 'at3'),
            generate_A_T_status(forward_primer['at2'], 'at2')
        ]

        d['at_statuses'] = at_statuses

        forwards.append(d)

    return {
        'forwards': forwards,
        'reverses': primers['reverses']
    }
