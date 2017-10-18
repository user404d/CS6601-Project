from math import log2, ceil


def bit_table(si, ti, n, out):
    for j in range(n):
        sij = "{}{}".format(si, j)
        tij = "{}{}".format(ti, j)
        print("{} select {} {} {}".format(sij, si, j, j + 1), file=out)
        print("{} select {} {} {}".format(tij, ti, j, j + 1), file=out)


def and_1_to_n(si, tij, n, out):
    si_tij_label = "{}{}".format(si, tij)
    si_tij_bits = []
    for j in range(n):
        sij = "{}{}".format(si, j)
        sij_and_tij = "{}{}".format(sij, tij)
        print("{} and {} {}".format(sij_and_tij, sij, tij), file=out)
        si_tij_bits.append(sij_and_tij)
    si_tij_value = " ".join(reversed(si_tij_bits))
    print("{} concat {}".format(si_tij_label, si_tij_value), file=out)
    return si_tij_label


def flat_adder(partials, offset, out):
    sum_inst = "sum{} add {} 0:{}".format(
        offset, partials[0], len(partials) * 2)
    print(sum_inst, file=out)
    for i in range(1, len(partials)):
        cur, prev = i + offset, i - 1 + offset
        sum_inst = "sum{} add sum{} {}".format(cur, prev, partials[i])
        print(sum_inst, file=out)
    sum_label = sum_inst.split(sep=" ")[0]
    return sum_label


def multiplier(si, ti, n, offset, out):
    partials = []
    bit_table(si, ti, n, out)
    for j in range(n):
        tij = "{}{}".format(ti, j)
        si_tij = and_1_to_n(si, tij, n, out)
        shift = "shift{}".format(si_tij)
        print("{} concat {} 0:{}".format(shift, si_tij, j), file=out)
        partial = "{}x{}".format(si, tij)
        print("{} zextend {} {}".format(partial, shift, n * 2), file=out)
        partials.append(partial)
    sixti_label = flat_adder(partials, n + offset, out)
    return sixti_label


def widening_adder(partials, bit_width, out):
    # TODO: either fix for unbalanced trees or switch to flat adder design
    height = ceil(log2(len(partials)))
    final_width = 2 * bit_width + height
    widened_partials = []
    for partial in partials:
        widened_partial = "wide{}".format(partial)
        print("{} zextend {} {}".format(
            widened_partial, partial, final_width), file=out)
        widened_partials.append(widened_partial)
    pairs = list(zip(widened_partials[::2], widened_partials[1::2]))
    zero = "0:{}".format(final_width)
    # doesn't sufficiently address unbalanced trees where len(partials) is
    # between powers of 2
    if len(partials) % 2 == 1 and len(partials) > 1:
        pairs.append((widened_partials[-1], zero))
    if len(pairs) % 2 == 1 and len(pairs) > 1:
        pairs.append((zero, zero))
    for depth in reversed(range(height)):
        intermediate_partials = []
        for i, (inter_i, inter_j) in enumerate(pairs):
            partial = "inter{}{}".format(depth, i)
            print("{} add {} {}".format(partial, inter_i, inter_j), file=out)
            intermediate_partials.append(partial)
        pairs = zip(intermediate_partials[::2], intermediate_partials[1::2])
    return "inter00", final_width


def generate(domain_size, dimensions, threshold):
    '''
    domain_size: the bit width for a component in a vector
    dimensions: the number of components/dimensions of a vector
    '''
    with open("tbaseddotprod.cir", mode="w") as out:
        for i in range(dimensions):
            print(".input s{} 1 {}".format(i, domain_size), file=out)
            print(".input t{} 2 {}".format(i, domain_size), file=out)
        partials = []
        for i in range(dimensions):
            si = "s{}".format(i)
            ti = "t{}".format(i)
            sixti = multiplier(si, ti, domain_size, i * domain_size, out)
            partials.append(sixti)
        s_dot_t, final_width = widening_adder(partials, domain_size, out)
        print("out ltu {} {}:{}".format(
            s_dot_t, threshold, final_width), file=out)
        print(".output out", file=out)
