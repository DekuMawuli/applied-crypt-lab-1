Overview: The project is a file encryption/decryption program for Applied Cryptography Lab 1, Part I. For every byte of the input file it applies a fixed bit permutation and then XORs the result with a byte produced by a linear feedback shift register (LFSR). Decryption reverses this. The output must be interoperable with the instructor's implementation, so the bit-ordering conventions below are normative.

Project Requirements
1. The code will be written in python 3
2. The user interface will use tkinter
3. The UI will let the user select "Encrypt" or "Decrypt"
4. The UI will let the user select an input file
5. The UI will let the user specify an output file
6. The UI will have a "Start" button which runs the selected operation
7. The UI will have a progress bar showing progress through the file
8. Encryption: each input byte is first bit-permuted, then XORed with the next byte output by the LFSR
9. Decryption: each input byte is first XORed with the next byte output by the LFSR, then the inverse permutation is applied
10. The initial key (seed), LFSR polynomial and permutation are those shown on Slide 19 of lecture 2 (Lecture_02_AC_Fall2026.pdf):
    a. Key: 19-bit initial register value 0x67BD5
    b. Polynomial: p(x) = 1 + x^14 + x^17 + x^18 + x^19
    c. Permutation of the 8 bits of a byte (m = 8): pi(1)=2, pi(2)=6, pi(3)=3, pi(4)=5, pi(5)=1, pi(6)=8, pi(7)=4, pi(8)=7
11. LFSR conventions (for interoperability):
    a. The leftmost bit of the LFSR corresponds to "x" in the polynomial; this is the LSB of the register. The "1" term of the polynomial applies to the feedback bit
    b. The feedback bit is shifted into the register on the left side
    c. The LSB of the seed goes into the LSB position of the LFSR
    d. The first bit output when shifting is therefore the MSB of the seed
    e. When building an output byte from LFSR output bits, the first output bit becomes the LSB of the output byte
12. Permutation convention: index "1" is the most significant bit of the byte
13. Deliverables: the encrypted version of the instructor's supplied image, and the decrypted version of the instructor's supplied encrypted image

Part II (written answers, not part of the program)
14. Prove ab mod n = ((a mod n)(b mod n)) mod n
15. Evaluate 9716 mod 87, -9716 mod 87, 87 mod 9716, -87 mod 9716
16. For Z*27 = {0..26}, find which elements have a multiplicative inverse mod 27, each inverse, and what the elements have in common
