# Project

## Authors

- Akshatha Bhat
- Quincy Conduff
- Sai Sruti

## Installation

### Requirements

- Java `>=7`
- Ant `>=1.10`
- Python `>=3.6.0`

```bash
git clone https://github.com/user404d/CS6601-Project.git
cd CS6601-Project
ant archive
```

## Usage

### Yao's Millionaire

```bash
# ./runmillionaire <Value of Alice> <Value of Bob>
./runmillionaire 123 23
```

Verify the output in `results/alice.out` and `results/bob.out`

### Millionaire Circuit

```plain
.input a 1 32
.input b 2 32
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

- Multiply corresponding components from each vector (ie. `s0 * t0`)
  1. Compute partial products
  2. Add all partial products together
- Add all intermediate products into scalar (ie. `(s0 * t0) + ... + (sn * tn) = u`)
- Compare scalar result to threshold (ie. `u < T`)

The final scalar value of the dotproduct will have at most `2 * R + ceiling(log_2(D))` bits so the threshold must be widened to allow for the comparison.