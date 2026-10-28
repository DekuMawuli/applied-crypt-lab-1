# Lab 1: LFSR + Permutation File Cipher

A small Python/Tkinter program that encrypts and decrypts files. Each byte is bit-permuted and then XORed with a byte from a 19-bit LFSR key stream. Decryption reverses this (XOR first, then the inverse permutation).

The key, polynomial and permutation come from slide 19 of Lecture 2. The assignment is in [lab1_question.md](lab1_question.md).

## Folder structure

```
lab1/
├── README.md                  this file
├── lab1_question.md           the assignment text (Part I and Part II)
│
├── lab1_cipher/               the program (Part I)
│   ├── main.py                entry point: opens the window
│   ├── ui.py                  Tkinter interface (the only file that imports tkinter)
│   ├── cipher.py              LFSR, permutation, encrypt/decrypt, file processing
│   ├── requirements.txt       no third-party packages needed
│   └── tests/
│       └── test_cipher.py     unit tests
│
├── results/                   the files to hand in
│   ├── image2.jpg.enc         the instructor's image2.jpg, encrypted by this program
│   └── image1_decrypted.jpg   the instructor's image1.jpg.enc, decrypted by this program
│
├── part_2.pdf                 Part II written answers (proof, modular evaluations, Z*27)
│
├── Requirements_v1.md         first requirements draft
├── requirements_v2.md         requirements after questions and decisions
├── design_v1.md               design: LFSR, permutation, structure, test plan
└── project_chat.md            log of the conversation with Claude and the decisions made
```

The documents follow the same flow as the course demo: requirements, then design, then code, with `project_chat.md` recording how it came about.

## Run the program

Requires Python 3 with tkinter (included with the python.org installer; with Homebrew run `brew install python-tk`). No packages to install.

```
cd lab1_cipher
python3 main.py
```

In the window:
1. Choose **Encrypt** or **Decrypt**.
2. Pick the **input file** (Browse...). A suggested output name is filled in (`.enc` added when encrypting, removed when decrypting). Change it if you like.
3. Check or pick the **output file**.
4. Press **Start**. The progress bar fills as the file is processed, and the status line shows the result.

The program asks before overwriting an existing output file and refuses to use the input file as the output.

You can also call the cipher without the window:

```
cd lab1_cipher
python3 -c "import cipher; cipher.process('../image2.jpg', '/tmp/out.enc', 'encrypt')"
```

## Run the tests

```
cd lab1_cipher
python3 -m unittest discover tests
```

The tests check that the permutation is a bijection and its inverse round-trips, the first key byte is 0xF3, a zero input gives the raw key stream, encrypt then decrypt returns the original for several sizes (including an empty file and different chunk sizes), and that the instructor's encrypted image decrypts to a JPEG. The last test is skipped if `image1.jpg.enc` is not in the folder above `lab1_cipher/`.

## How the cipher works

For each byte:
- **Encrypt:** `cipher = permute(plain) XOR next_key_byte`
- **Decrypt:** `plain = inverse_permute(cipher XOR next_key_byte)`

The LFSR starts from the seed once and runs continuously across the whole file. The output file is exactly the same length as the input, with no header.

Conventions (from the assignment):
- Seed `0x67BD5`, polynomial `1 + x^14 + x^17 + x^18 + x^19`.
- The leftmost cell is x (the LSB). Feedback enters on the left. The seed's LSB goes into the LSB position, so the first bit out is the seed's MSB.
- The first bit out of the LFSR becomes the LSB of the key byte.
- In the permutation, index 1 is the most significant bit.

One point the slide does not settle is the permutation direction: whether pi(i)=j means "bit i moves to position j" or "output bit i takes input bit j". The program uses the second reading, because it is the one under which the instructor's encrypted image decrypts to a valid JPEG (the other gave garbage). It is set by `PERMUTATION_READING` in `cipher.py`.

## Where to find things

| You want to see | Look at |
|---|---|
| The LFSR | `LFSR` class in `lab1_cipher/cipher.py` |
| The permutation and its inverse | `permute_byte` and `_tables` in `lab1_cipher/cipher.py` |
| Chunked file processing and progress | `process` in `lab1_cipher/cipher.py` |
| The window, progress bar and threading | `lab1_cipher/ui.py` |
| Why decisions were made | `project_chat.md`, `requirements_v2.md`, `design_v1.md` |
| The submitted images | `results/` |
| Part II answers | `part_2.pdf` |

## Checking the results

- Encrypting `image2.jpg` with this program reproduces `results/image2.jpg.enc` byte for byte, and decrypting that file gives back `image2.jpg`.
- The first plaintext byte `0xFF` becomes `0x0C` (permuted `0xFF` XOR the first key byte `0xF3`), which is the first byte of `image2.jpg.enc`.
- Decrypting the instructor's `image1.jpg.enc` produces a valid, complete JPEG (`results/image1_decrypted.jpg`).

## Notes

- The instructor-supplied images and lecture PDFs are not tracked in git (see `.gitignore`). To run the last unit test, put `image1.jpg.enc` in this folder.
- This repository was started after most of the work was done. See the first commit message and `project_chat.md` for the earlier timeline.
