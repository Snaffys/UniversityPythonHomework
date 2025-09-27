# a = b * q + r 
def gcd(a, b):
    if b == 0:
        return (a, 1, 0)

    a = abs(a)
    b = abs(b)
    if(b > a):
        a, b = b, a   

    old_a_coef = 1
    old_b_coef = 0
    current_a_coef = 0
    current_b_coef =1
    
    while (a % b) > 0:
        q = a // b
        new_a_coef = old_a_coef - current_a_coef * q
        new_b_coef = old_b_coef - current_b_coef * q
        old_a_coef = current_a_coef
        old_b_coef = current_b_coef
        current_a_coef = new_a_coef
        current_b_coef = new_b_coef

        r = a % b
        a = b
        b = r
    return (b, current_a_coef, current_b_coef)

def main():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    result, a_mult, b_mult = (gcd(a, b))
    print("GCD is:", result, "\nlinear combination:", result, "=", a, "*", a_mult,"+", b, "*", b_mult)

if __name__ == "__main__":
    main()