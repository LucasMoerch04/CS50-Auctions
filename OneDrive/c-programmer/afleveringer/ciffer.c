#include <stdio.h>

// Define MIN & MAX constants
#define MIN_NUMBER 1
#define MIN_DIGIT 0
#define MAX_DIGIT 9

int main(void){
    int c, n;

    // Get valid inputs c & n from user
    do {
        printf("Write a number bigger than 0: ");
        scanf(" %d", &n);
        if (n < MIN_NUMBER){
            printf("Invalid number. Please try again\n");
        }
    } while(n < MIN_NUMBER);

    do {
        printf("Write a number from 0-9: ");
        scanf(" %d", &c);
        if (c < MIN_DIGIT || c > MAX_DIGIT){
            printf("Invalid number. Please try again\n");
        }
    } while(c < MIN_DIGIT || c > MAX_DIGIT);
   
    int counter = 0;
    // Loop through all numbers from 1 up to n
    for (int i = 1; i <= n; i++) {
        int current_number = i;
        // Check for digit in number
        while(current_number != 0){
            // Add 1 to counter if number ends with same digit, else divide by 10
            if (c == current_number % 10){
                counter++;
                break;
            } else {
                current_number = current_number / 10;
            }
        }
    }
    // Print result
    printf("The digit %d appears in the numbers from 1 up to %d - %d times \n", c, n, counter);

    return 0;
}