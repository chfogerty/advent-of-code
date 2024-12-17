B = A % 8 (B gets lowest 3 bits of A)
B = XOR(B, 2)
C = A / (2 ^ B) (C gets A >> B)
B = XOR(B, C) (B gets lowest 3 bits of A XORd with the top ((len A) - B) bits of A)
A = A / 8 (A >> 3)
B = XOR(B, 7)
OUT(B % 8)
JNZ 0

In order, the low 3 bits of B as ints when output are:
5,3,6,5,0,2,3,4,7,4,6,0,2,2,4,7

binary:
101, 011, 110, 101, 000, 010, 011, 100, 111, 100, 110, 000, 010, 010, 100, 111

A only loses 3 bits each time, so A must be no more than 48 bits