// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int eighths = 0;
    //1/8 or 3/8
    if (fraction[2] == '8')
    {
        if (fraction[0] == '1')
        {
            eighths += 1;
        }
        else
        {
            eighths += 3;
        }
    }
    //1/4
    else if (fraction[2] == '4')
    {
        eighths += 2;
    }
    //1/2
    else
    {
        eighths += 4;
    }
    return eighths;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    float frequency;
    int i;
    //Natural keys and initializing the counter
    if (note[0] == 'A')
    {
        frequency = 27.5;
        i = 0;
    }
    else if (note[0] == 'B')
    {
        frequency = 30.86770633;
        i = 0;
    }
    else if (note[0] == 'C')
    {
        frequency = 32.70319566;
        i = 1;
    }
    else if (note[0] == 'D')
    {
        frequency = 36.70809599;
        i = 1;
    }
    else if (note[0] == 'E')
    {
        frequency = 41.20344461;
        i = 1;
    }
    else if (note[0] == 'F')
    {
        frequency = 43.65352893;
        i = 1;
    }
    else if (note[0] == 'G')
    {
        frequency = 48.9994295;
        i = 1;
    }
    //If there is an accidental
    if (note[1] == '#' || note[1] == 'b')
    {
        int octave = atoi(&note[2]);
        for (int j = i; j < octave; j++)
        {
            frequency *= 2;
        }
        if (note[1] == '#')
        {
            frequency *= pow(2.0, 1.0 / 12.0);
        }
        else
        {
            frequency /= pow(2.0, 1.0 / 12.0);
        }
    }
    //If not
    else
    {
        int octave = atoi(&note[1]);
        for (int j = i; j < octave; j++)
        {
            frequency *= 2;
        }
    }
    return round(frequency);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    //Comparing the line to blank
    if (strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
