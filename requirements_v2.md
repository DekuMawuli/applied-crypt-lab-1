# Requirements v2

## Overview
The project is a file encryption/decryption program for Applied Cryptography Lab 1, Part I. Every byte of the input file is bit-permuted and then XORed with a byte from a 19-bit LFSR key stream. Decryption reverses this. The ciphertext must be interoperable with the instructor's implementation, so the bit-ordering conventions in items 12-14 are normative. Part II (written math answers) is delivered as a separate document and is not part of the program.

## Project Requirements

### General
1. The code shall be written in Python 3.
2. The user interface shall use tkinter. The cipher itself shall use only the standard library (no pip packages required).
3. The cipher logic shall be separate from the UI so it can be tested without a window.

### UI
4. The UI shall let the user select "Encrypt" or "Decrypt" (radio buttons, default Encrypt).
5. The UI shall let the user select an input file (Browse button with a file dialog).
6. The UI shall let the user specify an output file (Browse button with a save dialog, or typed path).
7. The UI shall have a "Start" button that runs the selected operation.
8. The UI shall have a progress bar that reflects the fraction of the input file processed.
9. The work shall run in a background thread so the window stays responsive and the progress bar updates. Start is disabled while an operation runs.
10. The UI shall show a status line: idle, running (bytes processed), done (bytes written, output path), or the error message.
11. Validation: Start shall show an error and do nothing if the input path is empty or does not exist, the output path is empty, or the output path is the same file as the input. If the output file already exists the user shall be asked before it is overwritten. Input files are never modified.

### Cipher
12. Parameters (Lecture 2, slide 19):
    a. Key: 19-bit initial register value 0x67BD5.
    b. Polynomial: p(x) = 1 + x^14 + x^17 + x^18 + x^19.
    c. Permutation of the 8 bits of a byte: pi(1)=2, pi(2)=6, pi(3)=3, pi(4)=5, pi(5)=1, pi(6)=8, pi(7)=4, pi(8)=7.
13. LFSR conventions:
    a. The leftmost bit of the register corresponds to "x" in the polynomial and is the register's LSB. The "1" term applies to the feedback bit.
    b. The feedback bit is shifted into the register on the left.
    c. The LSB of the seed goes into the LSB (leftmost) position.
    d. The first bit output when shifting is therefore the MSB of the seed.
    e. When building an output byte from LFSR bits, the first output bit becomes the LSB of the output byte.
14. Permutation convention: index "1" is the most significant bit of the byte. pi(i)=j is interpreted as "output bit i takes the value of input bit j" (confirmed: this is the reading under which the instructor's encrypted image decrypts to a valid JPEG; the other reading gave garbage).
15. Encryption: for each input byte, c = permute(p) XOR k, where k is the next key-stream byte.
16. Decryption: for each input byte, p = inversePermute(c XOR k).
17. The LFSR is initialised from the key once at the start of the file and runs continuously across the whole file (never reset per byte or per chunk).
18. The program shall work on any file type, reading and writing raw bytes. The output has the same length as the input. No header, padding or extension is added.

### Deliverables and verification
19. Encrypt the instructor's supplied image and submit the encrypted file.
20. Decrypt the instructor's supplied encrypted image and submit the decrypted image.
21. Tests: encrypt followed by decrypt returns the original bytes; the 8-bit permutation table is a bijection and its inverse round-trips; the first key-stream bytes match a hand-computed value from the conventions in item 13; decrypting the instructor's encrypted image gives a valid image file.
22. Part II (written answers) shall be in `part2_answers.md`: the proof, the four modular evaluations, and the units of Z*27 with their inverses.

## Open decisions (defaults assumed, please check)
- **Permutation direction (item 14): RESOLVED.** Reading A (input bit i goes to position pi(i)) failed; reading B (output bit i takes input bit pi(i)) works. The code keeps this as the flag `PERMUTATION_READING`.
- **Feedback form (confirmed by the same test):** a Fibonacci-style register, where the feedback is the XOR of the cells at x^14, x^17, x^18 and x^19, and the output is the cell at x^19 (rightmost, MSB). This follows from items 13a-d.
- **Platform:** no Windows-only or standalone .exe requirement was given, so the app is plain Python and runs anywhere tkinter does.
