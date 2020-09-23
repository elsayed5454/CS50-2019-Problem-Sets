// recovers JPEGs from a forensic image
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover file\n");
        return 1;
    }

    // remember filename
    char *file = argv[1];

    // open file
    FILE *ptr = fopen(file, "r");
    if (ptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", file);
        return 2;
    }

    // declaring of buffer, found to decide whether it is new JPEG, i for tracking file numbers and file name string
    unsigned char bf[BLOCK_SIZE];
    int i = -1, found = 0;
    char fname[8];

    // img file declaration
    FILE *img = NULL;

    // iterate over blocks of the file till EOF block which is < BLOCK_SIZE
    while (fread(&bf, sizeof(unsigned char), BLOCK_SIZE, ptr) == BLOCK_SIZE)
    {
        // checking signature of JPEG
        if (bf[0] == 0xff && bf[1] == 0xd8 && bf[2] == 0xff && (bf[3] & 0xf0) == 0xe0)
        {
            // new JPEG or not ?
            if (found == 1)
            {
                fclose(img);
            }

            else
            {
                found = 1;
            }

            // creating new img
            i++;
            sprintf(fname, "%03i.jpg", i);
            img = fopen(fname, "w");
        }

        // write to JPEG the blocks
        if (found == 1)
        {
            fwrite(&bf, sizeof(unsigned char), BLOCK_SIZE, img);
        }


    }

    // close all
    fclose(img);
    fclose(ptr);

    // success
    return 0;
}