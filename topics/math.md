---
title: Math
summary: Butun sonlar bilan ishlash: bo'lish, qoldiq, raqamlarni ajratish, teskari aylantirish va murakkablik.
---

## Math masalalari nima haqida

Bu turdagi masalalarda asosiy ish **sonning o'zi** bilan bajariladi, string yoki array yordamida emas. Odatda raqamlarni ajratish, sonni qismlarga bo'lish, bo'linuvchanlikni tekshirish yoki formula topish kerak bo'ladi. To'g'ri yondashuv bilan ko'p masala qo'shimcha xotirasiz (**O(1)**) yechiladi.

Uchta asosiy amal hamma narsaning asosi:

| Amal | Ma'nosi | Misol |
|------|---------|-------|
| `x % 10` | Oxirgi raqam | `1234 % 10 = 4` |
| `x // 10` | Oxirgi raqamni olib tashlash | `1234 // 10 = 123` |
| `x * 10 + d` | Oxiriga raqam qo'shish | `123 * 10 + 4 = 1234` |

## Bo'lish va qoldiq

Butun sonlarni bo'lish uchun tillar har xil operator beradi. Qoldiqni `%` bilan olasiz.

```python
print(17 // 5)    # 3, butun bo'lish
print(17 % 5)     # 2, qoldiq
print(17 / 5)     # 3.4, float qaytaradi
```

```php
echo intdiv(17, 5);   // 3, butun bo'lish
echo 17 % 5;          // 2, qoldiq
echo 17 / 5;          // 3.4, float qaytaradi
```

```go
fmt.Println(17 / 5)   // 3, int'lar uchun butun bo'lish
fmt.Println(17 % 5)   // 2, qoldiq
fmt.Println(float64(17) / 5) // 3.4, aniq float kerak bo'lsa
```

## Raqamlarni ajratib olish

Sonni raqam-raqam ko'rib chiqishning standart usuli: oxirgi raqamni `% 10` bilan olish, so'ng `// 10` bilan uni tashlab yuborish, son `0` bo'lguncha. Misol uchun raqamlar yig'indisi:

```python
x = 1234
total = 0

while x > 0:
    total += x % 10
    x //= 10

print(total)   # 10
```

```php
$x = 1234;
$total = 0;

while ($x > 0) {
    $total += $x % 10;
    $x = intdiv($x, 10);
}

echo $total;   // 10
```

```go
x := 1234
total := 0

for x > 0 {
	total += x % 10
	x /= 10
}

fmt.Println(total)   // 10
```

Sikl **raqamlar soni** marta ishlaydi. `n` sonida raqamlar taxminan `log10(n)` ta, shuning uchun murakkablik **O(log n)**.

## Sonni teskari aylantirish

Oxirgi raqamni olib, uni yangi sonning oxiriga yopishtiramiz: `rev = rev * 10 + x % 10`.

```python
x = 1234
rev = 0

while x > 0:
    rev = rev * 10 + x % 10
    x //= 10

print(rev)   # 4321
```

```php
$x = 1234;
$rev = 0;

while ($x > 0) {
    $rev = $rev * 10 + $x % 10;
    $x = intdiv($x, 10);
}

echo $rev;   // 4321
```

```go
x := 1234
rev := 0

for x > 0 {
	rev = rev*10 + x%10
	x /= 10
}

fmt.Println(rev)   // 4321
```

Palindromni tekshirish kabi masalalarda sonning **faqat yarmini** teskari o'girish kifoya. Bu ham tezroq, ham overflow xavfidan xoli.

## Manfiy sonlar

Manfiy sonlarda bo'lish va qoldiq tillarda **turlicha** ishlaydi. Bu eng ko'p xato chiqaradigan joy.

| Ifoda | Python | PHP | Go |
|-------|--------|-----|----|
| `-7 // 2` yoki `-7 / 2` | `-4` (pastga yaxlitlaydi) | `intdiv(-7, 2)` = `-3` (nolga qarab) | `-3` (nolga qarab) |
| `-7 % 2` | `1` (bo'luvchi ishorasida) | `-1` (bo'linuvchi ishorasida) | `-1` (bo'linuvchi ishorasida) |

Shuning uchun manfiy sonlar bilan ishlaganda avval ishorani alohida ajratib oling (`abs`), yoki masala shartiga ko'ra manfiylarni darrov rad eting.

## Overflow

| Til | Butun son |
|-----|-----------|
| Python | Cheksiz kattalikda, overflow bo'lmaydi |
| PHP | 64-bit `int`. Chegaradan oshsa avtomatik `float` ga o'tadi va aniqlik yo'qoladi |
| Go | `int` 64-bit (platformaga bog'liq), chegaradan oshsa **jimgina aylanib ketadi** (wrap) |

LeetCode masalalarida ko'pincha "32-bit signed integer" chegarasi (`-2³¹ .. 2³¹ - 1`) so'raladi. Python'da buni qo'lda tekshirasiz. Overflowni oldini olishning eng yaxshi yo'li: kattaligi noma'lum natijani to'liq yig'maslik (masalan, sonning faqat yarmini aylantirish).

## Tez-tez uchraydigan misollar

**Eng katta umumiy bo'luvchi (GCD)**, Evklid algoritmi. Murakkablik **O(log min(a, b))**.

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(gcd(48, 18))   # 6
```

```php
function gcd(int $a, int $b): int {
    while ($b != 0) {
        [$a, $b] = [$b, $a % $b];
    }
    return $a;
}

echo gcd(48, 18);   // 6
```

```go
func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// gcd(48, 18) == 6
```

**Tub son tekshiruvi.** Bo'luvchilarni `√n` gacha tekshirish yetarli, chunki har bir bo'luvchi juftining kichigi `√n` dan oshmaydi. Murakkablik **O(√n)**.

```python
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

```php
function isPrime(int $n): bool {
    if ($n < 2) {
        return false;
    }
    for ($i = 2; $i * $i <= $n; $i++) {
        if ($n % $i == 0) {
            return false;
        }
    }
    return true;
}
```

```go
func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	for i := 2; i*i <= n; i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}
```

## Murakkablik

| Amal | Vaqt |
|------|------|
| `+ - * // %` (oddiy arifmetika) | O(1) |
| Barcha raqamlarni ko'rib chiqish | O(log n) |
| Evklid algoritmi (GCD) | O(log min(a, b)) |
| Tub son tekshiruvi | O(√n) |
| Qo'shimcha xotira (raqamlar bilan ishlaganda) | O(1) |

Bu yerda `n` sonning **qiymati**, uning raqamlar soni emas. Raqamlar soni `d` bilan belgilansa, raqamlarni ko'rib chiqish O(d) bo'ladi.

## Ko'p uchraydigan xatolar

- **Sonni stringga aylantirish.** `str(x)` ishlaydi, lekin O(log n) qo'shimcha xotira ketadi. Masala "stringsiz" yechishni so'rasa ruxsat etilmaydi.
- **Python'da `/` va `//` aralashishi.** `/` doim `float` beradi va katta sonlarda aniqlik yo'qoladi. Butun bo'lish uchun `//`.
- **PHP'da `/` o'rniga `intdiv`.** `7 / 2` PHP'da `3.5` beradi. Butun natija uchun `intdiv(7, 2)`.
- **Manfiy sonlar.** `%` va bo'lish natijasi tilga qarab farq qiladi (yuqoridagi jadval).
- **Oxiri nol bilan tugaydigan sonlar.** Sonni teskari aylantirganda bosh nollar yo'qoladi: `120` → `21`. Palindrom kabi masalalarda bu alohida holat sifatida tekshiriladi.
- **`0` ni unutish.** `x % 10 == 0` sharti `0` uchun ham to'g'ri keladi, lekin `0` o'zi palindrom.
