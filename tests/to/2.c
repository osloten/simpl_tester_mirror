// Каюсь, это ИИ написал, просто я не умею прогрммировать на C а протестить стоило

#include <stdio.h>

int main(void) {
    unsigned long long n;
    if (scanf("%llu", &n) != 1) return 1;
    printf("%llu\n", n * n);
    return 0;
}
