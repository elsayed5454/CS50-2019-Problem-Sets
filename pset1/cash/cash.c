#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    double n;
    int c = 0;
    //Prompt user for non negative float
    do
    {
        n = get_double("Change owed: ");
    }
    while (n < 0);

    //Converting dollars to cents
    n = n * 100;
    double round(double n);

    //Greedy algorithm
    //Decrease by quarters
    while (n >= 25)
    {
        c = c + 1 ;
        n = n - 25 ;
    }

    //Decrease by dimes
    while (n >= 10)
    {
        c = c + 1 ;
        n = n - 10 ;
    }

    //Decrease by nickels
    while (n >= 5)
    {
        c = c + 1 ;
        n = n - 5 ;
    }

    //Decrease by pennies
    while (n >= 1)
    {
        c = c + 1 ;
        n = n - 1 ;
    }

    printf("%i\n", c);
}