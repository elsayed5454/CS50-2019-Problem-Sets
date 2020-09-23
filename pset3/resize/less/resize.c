// Resizes a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: number infile outfile\n");
        return 1;
    }

    // remember inputs
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // ensure scale number
    if (n < 0 || n > 100)
    {
        fprintf(stderr, "Invalid number %i.\n", n);
        return 2;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's and new infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bf_new;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's and new infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, bi_new;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // changing new headers
    bf_new = bf;
    bi_new = bi;
    bi_new.biWidth = n * bi.biWidth;
    bi_new.biHeight = n * bi.biHeight;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_new = (4 - (bi_new.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // changing new image size
    bi_new.biSizeImage = ((sizeof(RGBTRIPLE) * bi_new.biWidth) + padding_new) * abs(bi_new.biHeight);
    bf_new.bfSize = bi_new.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_new, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_new, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // recopy method
        for (int m = 0; m < n; m++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int l = 0; l < n; l++)
                {
                    // write RGB triple to outfile and to array
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add padding
            for (int k = 0; k < padding_new; k++)
            {
                fputc(0x00, outptr);
            }

            // send infile cursor back until n - 1, to avoid placing cursor in wrong place in the last time
            if (m < n - 1)
            {
                fseek(inptr, -(bi.biWidth * sizeof(RGBTRIPLE)), SEEK_CUR);
            }
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
