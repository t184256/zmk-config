singles = {i + 1: k for i, k in enumerate('teraonsi')}
with_space = {0: 'space', **singles}

mappings = {
    ('ef', '0123443210', ''): ('b', '&bootloader')
} | {
    ('ef', f'{i}{i}', ''): ('b', f'&kp {k.upper()}')
    for i, k in with_space.items()
} | {
    ('ec', f'{i}{j}{i}', f'{j}'): ('b', f'&kp {ki.upper()}')
    for i, ki in with_space.items() for j, kj in with_space.items() if i != j
} | {
    ('ef', f'{i}_{i}', ''): ('n', '&none')
    for i, k in with_space.items()
} | {
    ('ec', f'{i}_{j}{i}', f'{j}'): ('n', '&none')
    for i, ki in with_space.items() for j, kj in with_space.items() if i != j
} | {
    ('ef', f'{i}00{i}', ''): ('b', f'&kp LS({k.upper()})')
    for i, k in singles.items()
} | {
    ('ef', f'{i}0000{i}', ''): ('b', f'&kp LC({k.upper()})')
    for i, k in singles.items()
} | {
    ('ef', f'{i}_00{i}', ''): ('b', '&kp SPACE')  # unsure
    for i in singles
}

rocks = {
    (1, 2): ('&m_the', '&m_the_c'),
    (1, 3): 'L',
    (1, 4): 'M',
    (1, 6): ('&m_th', '&m_th_c'),
    (1, 7): 'G',
    (1, 8): 'D',
    (2, 1): 'C',
    (2, 3): 'P',
    (2, 4): 'W',
    (2, 5): 'V',
    (2, 6): 'H',
    (2, 7): 'K',
    (2, 8): 'F',
    (3, 1): 'B',
    (3, 2): 'U',
    (3, 4): 'Y',
    (3, 5): 'Q',
    (3, 6): 'Z',
    (3, 7): 'J',
    (3, 8): 'X',
    (4, 1): ('&kp COMMA', '&kp SEMI', '&kp QMARK', '&kp AMPS'),    # , ; ? &
    (4, 2): ('&kp DOT', '&kp COLON', '&kp EXCL', '&kp DOLLAR'),    # . : ! $
                                                          # (TODO: ellipsis)
    (4, 3): ('&kp SLASH', '&kp PIPE', '&kp BSLH'),                 # / | \
    (4, 5): ('&kp MINUS', '&kp UNDER', '&kp EQUAL', '&kp TILDE'),  # - _ = ~
    (4, 6): ('&kp COLON', '&kp SEMI', '&kp HASH', '&kp PERCENT'),  # : ; # %
                                                            # (TODO: decide)
    (4, 7): ('&kp SQT', '&kp DQT', '&kp GRAVE', '&kp CARET'),      # ' " ` ^
    (4, 8): ('&kp PLUS', '&kp STAR', '&kp AT'),                    # + * @
    (5, 1): 'N6',
    (5, 2): 'N7',
    (5, 3): 'N8',
    (5, 4): 'N9',
    (5, 6): 'N0',
    (5, 7): 'N1',
    (5, 8): 'N2',
    (6, 2): ('&m_he', '&m_he_c'),
    (6, 4): ('&m_ha', '&m_ha_c'),
    (6, 7): ('&kp LPAR', '&kp LBKT', '&kp LBRC', '&kp LT'),      # ( [ { <
    (6, 8): ('&kp RPAR', '&kp RBKT', '&kp RBRC', '&kp GT'),      # ) ] } >
    (8, 2): ('&m_wm R',),
    (8, 3): ('&m_wm S',),
    (8, 4): 'RETURN',
    (8, 6): 'TAB',
    (8, 7): 'ESC',
}
rocks = {
    k: v
    if isinstance(v, tuple) else
    (f'&kp {v}', f'&kp LS({v})', f'&kp LC({v})', f'&kp LC(LS({v}))')
    for k, v in rocks.items()
}
mappings |= {
    ('ec', f'{i}{j}{j}', f'{i}_'): ('b', bindings[0])
    for (i, j), bindings in rocks.items() if len(bindings) > 0
} | {
    ('ec', f'{i}_{j}{j}', f'{i}_'): ('b', bindings[0])
    for (i, j), bindings in rocks.items() if len(bindings) > 0
} | {
    ('ec', f'{i}{j}00{j}', f'{i}_'): ('b', bindings[1])
    for (i, j), bindings in rocks.items() if len(bindings) > 1
} | {
    ('ec', f'{i}_{j}00{j}', f'{i}_'): ('b', bindings[1])
    for (i, j), bindings in rocks.items() if len(bindings) > 1
} | {
    ('ec', f'{i}{j}0000{j}', f'{i}_'): ('b', bindings[2])
    for (i, j), bindings in rocks.items() if len(bindings) > 2
} | {
    ('ec', f'{i}_{j}0000{j}', f'{i}_'): ('b', bindings[2])
    for (i, j), bindings in rocks.items() if len(bindings) > 2
} | {
    ('ec', f'{i}{j}000000{j}', f'{i}_'): ('b', bindings[3])
    for (i, j), bindings in rocks.items() if len(bindings) > 3
} | {
    ('ec', f'{i}_{j}000000{j}', f'{i}_'): ('b', bindings[3])
    for (i, j), bindings in rocks.items() if len(bindings) > 3
}

holdables = {
    (6, 5): '&kp PAGE_UP',
    (6, 1): '&kp PAGE_DOWN',
    (7, 1): '&kp HOME',
    (7, 2): '&kp DOWN',
    (7, 3): '&kp RETURN',
    (7, 4): '&kp END',
    (7, 5): '&kp LEFT',
    (7, 6): '&kp UP',
    (7, 8): '&kp RIGHT',
    (8, 1): '&kp DELETE',
    (8, 5): '&kp BACKSPACE',
}
mappings |= {
    ('ec', f'{i}{j}', f'{i}_{j}_'): ('d', binding)
    for (i, j), binding in holdables.items()
} | {
    ('ec', f'{i}_{j}', f'{i}_{j}_'): ('d', binding)
    for (i, j), binding in holdables.items()
} | {
    ('ec', f'{i}_{j}_{j}', f'{i}_'): ('u', binding)
    for (i, j), binding in holdables.items()
} | {
    ('ef', f'{i}_{j}_{i}', ''): ('u', binding)  # TODO: word jumps? wipes?
    for (i, j), binding in holdables.items()
}

extra_digits = {
    (5, 6, 2): '&kp N3',
    (5, 7, 3): '&kp N4',
    (5, 8, 4): '&kp N5',
}
mappings |= {
    ('ec', f'{i}{j}{k}', f'{i}_{j}_{k}'): ('n', '&none')
    for i, j, k in extra_digits
} | {
    ('ec', f'{i}{j}_{k}', f'{i}_{j}_{k}'): ('n', '&none')
    for i, j, k in extra_digits
} | {
    ('ec', f'{i}_{j}{k}', f'{i}_{j}_{k}'): ('n', '&none')
    for i, j, k in extra_digits
} | {
    ('ec', f'{i}_{j}_{j}', f'{i}_'): ('n', '&none')
    for i, j, _ in extra_digits
} | {
    ('ec', f'{i}_{j}_{k}{k}', f'{i}_{j}_'): ('b', binding)
    for (i, j, k), binding in extra_digits.items()
}

# TODO: rolls within the numbers context

bluetooth = {
    6: '&bt BT_SEL 0',
    7: '&bt BT_SEL 1',
    8: '&bt BT_SEL 2',
    2: '&bt BT_SEL 3',
    3: '&bt BT_SEL 4',
    4: '&bt BT_SEL 5',
    1: '&bt BT_CLR',
}
mappings |= {
    ('ef', f'50{i}', ''): ('b', binding) for i, binding in bluetooth.items()
}

#mappings = {
#    ('ef', '11', ''): ('b', '&kp N1'),
#    ('ec', '2', '2_'): ('d', '&kp N2'),
#    ('ef', '2_2', ''): ('u', '&kp N2'),
#    ('ef', '121', '2'): ('b', '&kp N1'),
#    ('pf', '122', '1_'): ('b', '&m_sh N1'),
#}

#def bin_(s):
#    for i in range(1, 10):
#        s = s.replace(f'{i}', f'\\{hex(i).lstrip('0')}')
#    return s

def genconfig(mappings):
    s = ''
    for k, v in mappings.items():
        partiality_finality, match, repl = k
        pressrelease, binding = v
        s += f'{partiality_finality}{pressrelease}{match},{repl}'
    return s

def genbindings(mappings):
    return ', '.join(f'<{binding}>' for _, binding in mappings.values())

def macro_seq(name, *keys, capitalize=False):
    keys = keys or name
    s = [f'<&kp {x.upper()}>' for x in keys]
    if capitalize:
        s[0] = f'<&kp LS({keys[0].upper()})>'
    return f'''
    m_{name}: m_{name} {{
        compatible = "zmk,behavior-macro";
        wait-ms = <0>;
        #binding-cells = <0>;
        bindings = {', '.join(s)};
    }};
    '''

#def macro_mod(name, key):
#    return f'''
#    m_{name}: m_{name} {{
#	compatible = "zmk,behavior-macro-one-param";
#	#binding-cells = <1>;
#	wait-ms = <0>;
#	bindings =
#		<&macro_press &kp {key}>,
#		<&macro_param_1to1>,
#		<&macro_press &kp MACRO_PLACEHOLDER>,
#		<&macro_pause_for_release>,
#		<&macro_param_1to1>,
#		<&macro_release &kp MACRO_PLACEHOLDER>,
#		<&macro_release &kp {key}>;
#    }};
#    '''

SNIPPET = f'''
    // generated with helpers/genengine.py
    {macro_seq('the', 'T', 'H', 'E', 'SPACE')}
    {macro_seq('the_c', 'T', 'H', 'E', 'SPACE', capitalize=True)}
    {macro_seq('th')}
    {macro_seq('th_c', 'T', 'H', capitalize=True)}
    {macro_seq('he')}
    {macro_seq('he_c', 'H', 'E', capitalize=True)}
    {macro_seq('ha')}
    {macro_seq('ha_c', 'H', 'A', capitalize=True)}
    eng: engine {{
        compatible = "zmk,behavior-engine";
        #binding-cells = <1>;
        // Partial(prefix)/Exact, Continued/Final, Up/Down/Both
        config = "{genconfig(mappings)}";
        bindings = {genbindings(mappings)};
    }};
'''.strip()

print(SNIPPET)
