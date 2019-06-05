#include <stdio.h>

int main(int argc, char const *argv[])
{
    int arr[10];
    for (int i = 0; i < 10; i++)
    {
        arr[i] = i;
    }

    printf("%d\n",arr[1]);
    printf("%d\n",arr[10]);
}