Lab 1
Part I: 80 points
1.) As outlined in class, use Claude to write an encryption
program. Use python and Tkinter for the UI. The UI
should allow you to select “encrypt” or “decrypt”, select
an input file, and specify an output file. It should also
have a start button.
a. When encrypting, the program should permute every
byte, and then xor the permuted byte with a byte
output from the LFSR. Use the intital key, the LFSR
polynomial, and the permutation shown on Slide 19
of lecture 2.
b. To ensure interoperability make sure:
i. The leftmost bit of your LFSR corresponds to “x”
in the polynomial. We’ll call this the LSB (Least
Significant Bit). Think of the “1” in the
polynomial as applying to the feedback bit.
ii. The feedback bit is shifted into the shift register
on the left side
iii. The LSB of the seed should go into the LSB
position of the LFSR
iv. The first bit output from the LFSR when shifting
is therefore the MSB of the seed
v. When building an output byte from the bits
output from the LFSR, the first output bit
becomes the LSB of the output byte
vi. When applying the permutation function, index
“1” is the most significant bit of the byte
c. Make sure your implementation includes a progress
bar
I have uploaded an image to encrypt to canvas. You should
encrypt that image and send it to me. I will verify I can decrypt
it. I have also uploaded an encrypted image, and you should
decrypt it and send me the image you decrypted.
Part II: 20 points
2.) Prove: ab mod n = ( (a mod n)(b mod n) ) mod n Hint:
express a and b as a multiple of n plus a remainder
3.) Evaluate: 9716 mod 87, -9716 mod 87, 87 mod 9716, -87
mod 9716
4.) Consider the set Z*{27} = {0, 1, 2, ..., 26}. Which elements in
Z*{27} have a multiplicative inverse mod 27 and what is the
inverse of each such element? What do you observe that these
elements have in common? (You may use Claude, but you
must make sure you understand what isgoing on)
