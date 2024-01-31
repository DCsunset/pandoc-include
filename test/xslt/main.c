#include <stdio.h>
#include <math.h>

/**
 * @file calculator.c
 * @brief Simple calculator program with basic arithmetic operations, square root, and power.
 */

/**
 * @brief Adds two numbers.
 * @param a The first number.
 * @param b The second number.
 * @return The sum of the two numbers.
 */
double add(double a, double b);

/**
 * @brief Subtracts one number from another.
 * @param a The first number (minuend).
 * @param b The second number (subtrahend).
 * @return The result of subtracting b from a.
 */
double subtract(double a, double b);

/**
 * @brief Multiplies two numbers.
 * @param a The first number.
 * @param b The second number.
 * @return The product of the two numbers.
 */
double multiply(double a, double b);

/**
 * @brief Divides one number by another.
 * @param a The numerator.
 * @param b The denominator.
 * @return The result of dividing a by b.
 */
double divide(double a, double b);

/**
 * @brief Calculates the square root of a number.
 * @param a The number to calculate the square root of.
 * @return The square root of the given number.
 */
double squareRoot(double a);

/**
 * @brief Raises a base to the power of an exponent.
 * @param base The base number.
 * @param exponent The exponent.
 * @return The result of raising the base to the power of the exponent.
 */
double power(double base, double exponent);

int main() {
    char operator;
    double num1, num2, result;

    // Get operator and operands from user
    printf("Enter operator (+, -, *, /, sqrt, pow): ");
    scanf(" %c", &operator);  // Note the space before %c to consume the newline character

    if (operator != 'sqrt' && operator != 'pow') {
        printf("Enter first number: ");
        scanf("%lf", &num1);
    }

    // For sqrt, only one number is needed
    if (operator != 'sqrt') {
        printf("Enter second number: ");
        scanf("%lf", &num2);
    }

    // Perform calculation based on the operator
    switch (operator) {
        case '+':
            result = add(num1, num2);
            break;
        case '-':
            result = subtract(num1, num2);
            break;
        case '*':
            result = multiply(num1, num2);
            break;
        case '/':
            if (num2 != 0) {
                result = divide(num1, num2);
            } else {
                printf("Error: Division by zero is not allowed.\n");
                return 1;  // Exit with an error code
            }
            break;
        case 'sqrt':
            result = squareRoot(num1);
            break;
        case 'pow':
            result = power(num1, num2);
            break;
        default:
            printf("Error: Invalid operator.\n");
            return 1;  // Exit with an error code
    }

    // Display the result
    printf("Result: %lf\n", result);

    return 0;  // Exit successfully
}

// Function definitions remain unchanged
