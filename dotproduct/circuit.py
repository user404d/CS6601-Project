from math import log2, ceil


def bit_table(si, ti, n, out):
    '''
    Generates a lookup table for the bits in the given vector components.
    The format of the table is as follows:

    <v><i>b<j> select <v><i> <j> <j+1>
    .
    .
    .

    jth bit of component i in vector v where b acts as a
    lexical separator.
    '''
    for j in range(n):
        sij = "{}b{}".format(si, j)
        tij = "{}b{}".format(ti, j)
        print("{} select {} {} {}".format(sij, si, j, j + 1), file=out)
        print("{} select {} {} {}".format(tij, ti, j, j + 1), file=out)


def and_1_to_n(si, tij, n, out):
    '''
    Takes vector component si and performs bitwise AND with bit tij.
    Returns the label of the variable which contains the resulting bits
    concatenated together.

    sib(n-1)^tibj || sib(n-2)^tibj || ... || sib1^tibj || sib0^tibj
    '''
    si_tij_label = "{}{}".format(si, tij)
    si_tij_bits = []
    for j in range(n):
        sij = "{}b{}".format(si, j)
        sij_and_tij = "{}{}".format(sij, tij)
        print("{} and {} {}".format(sij_and_tij, sij, tij), file=out)
        si_tij_bits.append(sij_and_tij)
    si_tij_value = " ".join(reversed(si_tij_bits))
    print("{} concat {}".format(si_tij_label, si_tij_value), file=out)
    return si_tij_label


def flat_adder(partials, n, offset, out):
    '''
    Performs a summation on a list of partial values of the same bit width.
    Returns the label of the variable containing the sum.
    '''
    sum_inst = "sum{} add {} 0:{}".format(
        offset, partials[0], n)
    print(sum_inst, file=out)
    for i in range(1, len(partials)):
        cur, prev = i + offset, i - 1 + offset
        sum_inst = "sum{} add sum{} {}".format(cur, prev, partials[i])
        print(sum_inst, file=out)
    sum_label = sum_inst.split(sep=" ")[0]
    return sum_label


def multiplier(si, ti, n, offset, out):
    '''
    Performs unsigned multiplication between two integers of the same bit width.
    Returns the label of the variable containing the result.
    '''
    partials = []
    bit_table(si, ti, n, out)
    for j in range(n):
        tij = "{}b{}".format(ti, j)
        si_tij = and_1_to_n(si, tij, n, out)
        shift = "shift{}".format(si_tij)
        print("{} concat {} 0:{}".format(shift, si_tij, j), file=out)
        partial = "{}x{}".format(si, tij)
        print("{} zextend {} {}".format(partial, shift, n * 2), file=out)
        partials.append(partial)
    sixti_label = flat_adder(partials, 2 * n, n + offset, out)
    return sixti_label


def widening_adder(partials, bit_width, out):
    '''
    Widens each value before performing summation.
    Returns the label of the variable and the final bit width of the resulting sum.
    '''
    height = ceil(log2(len(partials)))
    final_width = 2 * bit_width + height
    widened_partials = []
    for partial in partials:
        widened_partial = "wide{}".format(partial)
        print("{} zextend {} {}".format(
            widened_partial, partial, final_width), file=out)
        widened_partials.append(widened_partial)
    sum_label = flat_adder(widened_partials, final_width,
                           bit_width * bit_width, out)
    return sum_label, final_width


def generate(domain_size, dimensions, threshold):
    '''
    domain_size: the bit width for a component in a vector
    dimensions: the number of components/dimensions of a vector
    threshold: the value which the final dotproduct must be below
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
