# Project

## Authors

- Akshatha Bhat
- Quincy Conduff
- Sai Sruti

## Installation

### Requirements

- Java `>=7`
- Ant `>=1.10`
- Python `2` or `3`

```bash
git clone https://github.com/user404d/CS6601-Project.git
cd CS6601-Project
ant archive
```

## Usage

### Yao's Millionaire

```bash
# ./runmillionaire <bit width> <Value of Alice> <Value of Bob>
./runmillionaire 10 123 23
```

Verify the output in `results/alice.out` and `results/bob.out`

### Millionaire Circuit

```plain
.input a 1 <input bit width>
.input b 2 <input bit width>
yao gteu a b
.output yao
```

### Threshold Based Dotproduct

```bash
# echo "s0 <value>
# s1 <value>
# s2 <value>
# ...
# " > test/alice_vector
# echo "t0 <value>
# t1 <value>
# t2 <value>
# ...
# " > test/bob_vector
# ./runtbaseddotprod <bit width> <dimensions> <threshold>
echo "s0 2
s1 6
s2 3
" > test/alice_vector
echo "t0 3
t1 1
t2 2
" > test/bob_vector
./runtbaseddotprod 4 3 20
```

Verify the output in `results/alice.out` and `results/bob.out`

### Threshold Based Dotproduct Circuit

The circuit is generated each time for the specified domain size `R` (ie. bit width of vector components), number of dimensions `D`, and threshold `T`. The general structure of the generated circuit is as follows:

- Multiply corresponding components from each vector `si * ti`

  1. Compute partial products `si * tij`
      - For each bit `tij` in `ti` perform bitwise `AND` with `tij` and each bit in `si`
      - Concatenate the resulting bits together. \
        (ie. `si(n-1)^tij || si(n-2)^tij || ... || si0^tij`)
      - Shift the result to the left by `j` bits. `j` is from `tij`. \
        (ie. `j = 2 -> si^tij || 00`)
      - Zero extend by `R - j` bits. \
        (ie. `R = 4, j = 2 -> 00 || si^tij || 00`)

  2. Add all partial products together \
    (ie. `si * ti = (si * ti0) + (si * ti1) ... + (si * ti(n-1)`)

- Add all intermediate products into scalar \
(ie. `(s0 * t0) + ... + (sn * tn) = u`)

  1. Zero extend each value by `ceiling(log_2(D))` bits.
  2. Add widened values together.

- Compare scalar result to threshold \
(ie. `u < T`)

  - Both values should be bit width `2 * R + ceiling(log_2(D))`.