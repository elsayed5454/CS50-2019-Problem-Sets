#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    //Prompt user for non negative integer no greater than 8
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    //Draw the half pyramid
    for (int i = 0; i < n; i++)
    {
        for (int s = n - (i + 1); s > 0; s--)
        {
            printf(" ");
        }

        for (int j = -1; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}