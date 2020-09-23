# Questions

## What's `stdint.h`?

It's a header file in the C standard library to allow programmers to write more portable code by providing a set of `typdefs` that specify exact-width integer types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

To allow code to be portable among machines with different inherent data sizes (word sizes), so each type may have different ranges on different machines.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

ASCII: BM
decimal: 66 77
hexadecimal: 0x42 0x4D

## What's the difference between `bfSize` and `biSize`?

`bfSize` represents the file size in bytes of the full BMP (including both headers and image itself), while `biSize` represents the size of the `BITMAPINFOHEADER` only.
`bfSize` = `biSizeImage` + `biSize` + 14

## What does it mean if `biHeight` is negative?

It means the bitmap is a top-down DIB with the origin at the upper left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount`

## Why might `fopen` return `NULL` in `copy.c`?

To avoid dereferencing a null pointer, and so avoid segmentation fault.

## Why is the third argument to `fread` always `1` in our code?

Because the header files are each one element.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Sets file position by changing the offset of the file pointer.

## What is `SEEK_CUR`?

It's the current location of the file pointer.

