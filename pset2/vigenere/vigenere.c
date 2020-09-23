#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    string k, p;
    //Prompt user for inputs and validate it
    if (argc == 2)
    {
        k = argv[1];
        for (int i = 0, n = strlen(k); i < n; i++)
        {
            if (isalpha(k[i]))
            {
                continue;
            }
            else
            {
                printf("ERROR\n");
                return 1;
            }
        }
        p = get_string("plaintext: ");
        printf("ciphertext: ");
        //Vigenere's cipher
        for (int i = 0, j = -1, n = strlen(p), m = strlen(k); i < n; i++)
        {
            //Check for alphabetical
            if (isalpha(p[i]))
            {
                j++;
                if (j == m)
                {
                    j = 0;
                }
                //Check for upper case
                if (isupper(p[i]))
                {
                    p[i] -= 65;
                    if (isupper(k[j]))
                    {
                        k[j] -= 65;
                        p[i] = (p[i] + k[j]) % 26;
                        k[j] += 65;
                    }
                    else
                    {
                        k[j] -= 97;
                        p[i] = (p[i] + k[j]) % 26;
                        k[j] += 97;
                    }
                    p[i] += 65;
                    printf("%c", p[i]);
                }
                //Check for lower case
                else
                {
                    p[i] -= 97;
                    if (isupper(k[j]))
                    {
                        k[j] -= 65;
                        p[i] = (p[i] + k[j]) % 26;
                        k[j] += 65;
                    }
                    else
                    {
                        k[j] -= 97;
                        p[i] = (p[i] + k[j]) % 26;
                        k[j] += 97;
                    }
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
        printf("ERROR\n");
        return 1;
    }
}