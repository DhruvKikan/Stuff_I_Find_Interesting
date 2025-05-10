/*
This is basically ported from the .py file
I don't like how bloated Java is.
I don't like that python is interpreted and has no braces or terminators
*/

import java.util.List;
import java.util.Arrays;
import java.util.Scanner;
import java.math.BigInteger;
import java.security.SecureRandom;

public class PurpleBrain_PrimeGenerator {
    private static final SecureRandom random = new SecureRandom();
    private static final List<Integer> small_Primes = Arrays.asList(
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
            79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
            167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
            257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
            353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
            449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
            563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
            653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757,
            761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
            877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
            991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069
    );
    public static BigInteger generate_random_odd(int size) {
        BigInteger min = BigInteger.TEN.pow(size - 1);
        BigInteger max = BigInteger.TEN.pow(size).subtract(BigInteger.ONE);
        BigInteger num;
        while (true){
            num = new BigInteger(max.bitLength(), random);
            boolean inRange = (min.compareTo(num) < 1) && (num.compareTo(max) < 1);
            boolean isOdd = num.mod(BigInteger.TWO).equals(BigInteger.ONE);
            if (inRange && isOdd){
                return num;
            }
        }
    }

    public static boolean is_Prime_Multiple(BigInteger number) {
        for (int primes : small_Primes) {
            if (number.mod(BigInteger.valueOf(primes)).equals(BigInteger.ZERO)) {
                return true;
            }
        }
        return false;
    }

    public static double confidence(int iterations) {
        return (1 - (Math.pow(0.25, iterations)));
    }

    public static double bayesian_confidence(int size, int iterations) {
        double confid = confidence(iterations);
        double factor = size * Math.log(10);

        return 1.0 / (1.0 + factor * (1.0 - confid));
    }

    public static boolean Miller_Rabin_Iteration_test(BigInteger number) {
        if (is_Prime_Multiple(number)) { return false; }

        // ensures that the number generated lies in the range - [2, number)
        BigInteger base = new BigInteger(number.bitLength(), random)
                .mod(number.subtract(BigInteger.TWO))
                .add(BigInteger.TWO);
        BigInteger exponent = number.subtract(BigInteger.ONE);

        // Fermat's little theorem
        if (!base.modPow(exponent, number).equals(BigInteger.ONE)) { return false; }

        boolean is_prev_1 = true;
        while (exponent.mod(BigInteger.TWO).equals(BigInteger.ZERO)) {
            exponent = exponent.shiftRight(1);
            BigInteger newBase = base.modPow(exponent, number);
            if (is_prev_1) {
                if (newBase.equals(number.subtract(BigInteger.ONE))) {
                    is_prev_1 = false;
                }
                else if (!newBase.equals(BigInteger.ONE)) {
                    is_prev_1 = false;
                }
            }
        }
        return true;
    }

    public static boolean Miller_Rabin_Test(BigInteger number, int iterations) {
        for (int i = 0; i < iterations; i++) {
            if (!Miller_Rabin_Iteration_test(number)) { return false; }
        }
        return true;
    }

    public static BigInteger generatePrime(int size, int iterations) {
        int i = 0;
        while (true) {
            i++;
            System.out.println("Iteration no. " + i + "(expected " + ((int) 2.3 * size) + ") total");
            BigInteger randomOdd = generate_random_odd(size);
            if (Miller_Rabin_Test(randomOdd, 20)) {
                return randomOdd;
            }
        }
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter size of required probable prime number: ");
        int sizeOfPrime = input.nextInt();
        System.out.print("Enter number of checks to be performed: ");
        int checks = input.nextInt();
        BigInteger generatedPrime = generatePrime(sizeOfPrime, checks);
        System.out.println(generatedPrime);
        System.out.println("Naive confidence is: " + confidence(checks));
        System.out.println("Bayesian confidence : " + bayesian_confidence(sizeOfPrime, checks));
    }
}
