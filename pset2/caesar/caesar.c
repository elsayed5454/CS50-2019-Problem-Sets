#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    int k;
    string p;
    if (argc == 2)
    {
        //Prompt user for inputs
        k = atoi(argv[1]);
        p = get_string("plaintext: ");
        //Caesar's cipher
        printf("ciphertext: ");
        for (int i = 0, n = strlen(p); i < n; i++)
        {
            //Check for alphabtical
            if (isalpha(p[i]))
            {
                if (isupper(p[i]))
                {
                    p[i] -= 65;
                    p[i] = (p[i] + k) % 26;
                    p[i] += 65;
                    printf("%c", p[i]);
                }
                else
                {
                    p[i] -= 97;
                    p[i] = (p[i] + k) % 26;
                    p[i] += 97;
                    printf("%c", p[i]);
                }
            }
            else
            {
                printf("%c", p[i]);
            }
        }
        printf("\n");
    }
    //Print an error message
    else
    {
        return 1;
    }
}