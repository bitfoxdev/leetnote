---
title: String
summary: Belgilar ketma-ketligi. Indeks bilan o'qish, aylanib chiqish, qurish, qidirish va tillar o'rtasidagi farqlar.
---

## String nima

String (satr) **belgilar ketma-ketligi**. Tuzilishi jihatidan array'ga o'xshaydi: har bir belgining indeksi bor (`0` dan boshlanadi), indeks bo'yicha o'qish tez. Asosiy farqi: string'larda belgilar ustida maxsus amallar (qidirish, bo'lish, birlashtirish) ko'p, shuningdek ko'p tilda string **o'zgarmas** (immutable).

```python
s = "hello"
#   indeks: 0 1 2 3 4
```

```php
$s = "hello";
//  indeks: 0 1 2 3 4
```

```go
s := "hello"
//  indeks: 0 1 2 3 4
```

## O'zgarmaslik (immutability)

Python va Go'da string'ning belgisini o'zgartirib bo'lmaydi: `s[0] = "H"` xato beradi. O'zgartirish uchun **yangi string** yaratiladi. PHP'da `$s[0] = "H"` ishlaydi, lekin bunga ko'p tayanilmaydi.

Bu muhim oqibat beradi: string'ni sikl ichida `s = s + "x"` bilan to'ldirish har safar yangi nusxa yaratadi va umumiy narx **O(n²)** ga chiqadi. To'g'ri yo'li quyida ("Qurish" bo'limi).

## Unicode va baytlar

Lotin harflarida belgi = 1 bayt, lekin `ў`, `ё` yoki emoji kabi belgilar bir necha bayt oladi. Tillar bunda turlicha harakat qiladi:

| | `len("ўз")` | Indeks `s[i]` | Nima uchun |
|---|-----------|----------------|-----------|
| Python | `2` | 1 belgilik str | Python belgilarni (code point) sanaydi |
| PHP | `4` | 1 bayt | `strlen` baytlarni sanaydi, belgilar uchun `mb_strlen` |
| Go | `4` | 1 bayt (`byte`) | `len` baytlarni sanaydi, belgilar uchun `[]rune` yoki `range` |

LeetCode masalalarida odatda faqat ASCII (lotin harflari, raqamlar) bo'ladi, shuning uchun bu farq kam seziladi, lekin real kodda muhim.

## Amallar va murakkablik

| Amal | Vaqt | Izoh |
|------|------|------|
| Indeks bo'yicha o'qish `s[i]` | O(1) | Array kabi |
| Uzunlik `len(s)` | O(1) | Saqlab qo'yilgan |
| Aylanib chiqish | O(n) | Har belgi bir marta |
| Ikki string'ni birlashtirish `s + t` | O(n + m) | Yangi string yaratiladi |
| Kesim (slice) `s[a:b]` | O(k) | `k` = kesim uzunligi (Go'da O(1), ko'chirmaydi) |
| Taqqoslash `s == t` | O(n) | Eng yomon holda hamma belgi |
| Substring qidirish | O(n·m) | Sodda usulda, `n` = matn, `m` = namuna |
| Teskari aylantirish | O(n) | Yangi string yaratiladi |
| Xotira | O(n) | `n` belgi uchun |

## Read: belgi va kesim olish

```python
s = "hello"

print(s[0])      # h, birinchi
print(s[-1])     # o, oxirgi
print(len(s))    # 5
print(s[1:4])    # ell, 1-indeksdan 4-gacha (4 kirmaydi)
```

```php
$s = "hello";

echo $s[0];                // h, birinchi
echo $s[-1];               // o, oxirgi (PHP 7.1+)
echo strlen($s);           // 5
echo substr($s, 1, 3);     // ell, 1-indeksdan 3 belgi
```

```go
s := "hello"

fmt.Println(string(s[0]))        // h, birinchi (s[0] byte, shuning uchun string() kerak)
fmt.Println(string(s[len(s)-1])) // o, oxirgi
fmt.Println(len(s))              // 5
fmt.Println(s[1:4])              // ell, 1-indeksdan 4-gacha (4 kirmaydi)
```

> Go'da `s[0]` belgi emas, **bayt** (son) qaytaradi: `fmt.Println(s[0])` `104` chiqaradi. Belgini ko'rish uchun `string(s[0])`.

## Aylanib chiqish

```python
s = "hello"

for i, ch in enumerate(s):    # indeks va belgi
    print(i, ch)

for ch in s:                  # faqat belgi
    print(ch)
```

```php
$s = "hello";

for ($i = 0; $i < strlen($s); $i++) {   // indeks va bayt
    echo $i, " ", $s[$i], "\n";
}
```

```go
s := "hello"

for i := 0; i < len(s); i++ {   // indeks va bayt
	fmt.Println(i, string(s[i]))
}

for i, ch := range s {          // indeks va belgi (rune), Unicode'ga mos
	fmt.Println(i, string(ch))
}
```

## Qurish: string yig'ish

Natijani belgi-belgi yig'ayotgan bo'lsangiz, `s = s + ch` o'rniga maxsus usul ishlating.

```python
parts = []
for ch in "abc":
    parts.append(ch.upper())

result = "".join(parts)   # O(n), bir marta birlashtiradi
print(result)             # ABC
```

```php
$result = "";
foreach (str_split("abc") as $ch) {
    $result .= strtoupper($ch);   // PHP'da .= samarali
}
echo $result;                     // ABC
```

```go
var sb strings.Builder
for _, ch := range "abc" {
	sb.WriteString(strings.ToUpper(string(ch)))
}

fmt.Println(sb.String())   // ABC, O(n)
```

## Qidirish

```python
s = "hello"

print("ell" in s)       # True, bormi
print(s.find("ell"))    # 1, indeksi (topilmasa -1)
print(s.count("l"))     # 2, necha marta
```

```php
$s = "hello";

var_dump(str_contains($s, "ell"));   // true, bormi (PHP 8+)
var_dump(strpos($s, "ell"));         // int(1), indeksi (topilmasa false)
echo substr_count($s, "l");          // 2, necha marta
```

```go
s := "hello"

fmt.Println(strings.Contains(s, "ell"))   // true, bormi
fmt.Println(strings.Index(s, "ell"))      // 1, indeksi (topilmasa -1)
fmt.Println(strings.Count(s, "l"))        // 2, necha marta
```

> PHP'da `strpos` topilmasa `false`, boshida topilsa `0` qaytaradi. `if (strpos(...))` yozsangiz `0` ham "yolg'on" hisoblanadi. Doim `!== false` bilan tekshiring.

## O'zgartirish

String o'zgarmas bo'lgani uchun bu amallar hammasi **yangi string** qaytaradi.

```python
s = "  Hello  "

print(s.strip())              # "Hello"
print(s.lower())              # "  hello  "
print(s.upper())              # "  HELLO  "
print(s.replace("l", "L"))    # "  HeLLo  "
```

```php
$s = "  Hello  ";

echo trim($s);                  // "Hello"
echo strtolower($s);            // "  hello  "
echo strtoupper($s);            // "  HELLO  "
echo str_replace("l", "L", $s); // "  HeLLo  "
```

```go
s := "  Hello  "

fmt.Println(strings.TrimSpace(s))          // "Hello"
fmt.Println(strings.ToLower(s))            // "  hello  "
fmt.Println(strings.ToUpper(s))            // "  HELLO  "
fmt.Println(strings.ReplaceAll(s, "l", "L")) // "  HeLLo  "
```

## Bo'lish va birlashtirish

```python
parts = "a,b,c".split(",")   # ['a', 'b', 'c']
text = "-".join(parts)       # "a-b-c"
```

```php
$parts = explode(",", "a,b,c");   // [a, b, c]
$text = implode("-", $parts);     // "a-b-c"
```

```go
parts := strings.Split("a,b,c", ",")   // [a b c]
text := strings.Join(parts, "-")       // "a-b-c"
```

## Belgi va son

Raqam belgisini songa o'girish va belgi kodini olish masalalarda tez-tez kerak bo'ladi.

```python
print(ord("a"))             # 97, belgi kodi
print(chr(97))              # a
print(int("7"))             # 7, string -> son
print(ord("7") - ord("0"))  # 7, raqam belgisi -> son
print(str(7))               # "7", son -> string
```

```php
echo ord("a");              // 97, belgi kodi
echo chr(97);               // a
echo (int)"7";              // 7, string -> son
echo ord("7") - ord("0");   // 7, raqam belgisi -> son
echo (string)7;             // "7", son -> string
```

```go
fmt.Println('a')                       // 97, belgi kodi
fmt.Println(string(rune(97)))          // a
n, _ := strconv.Atoi("7")              // 7, string -> son
fmt.Println(n)
fmt.Println(int("7"[0] - '0'))         // 7, raqam belgisi -> son
fmt.Println(strconv.Itoa(7))           // "7", son -> string
```

## Teskari aylantirish

```python
s = "hello"
print(s[::-1])   # olleh
```

```php
$s = "hello";
echo strrev($s);   // olleh
```

```go
s := "hello"
r := []rune(s)

for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
	r[i], r[j] = r[j], r[i]
}

fmt.Println(string(r))   // olleh
```

## Tillar o'rtasidagi farqlar

| | Python | PHP | Go |
|---|--------|-----|----|
| O'zgarmas | Ha | Yo'q (lekin ko'p amallar nusxa qaytaradi) | Ha |
| Indeks natijasi | 1 belgilik `str` | 1 baytlik `string` | `byte` (son) |
| Manfiy indeks | `s[-1]` | `$s[-1]` (7.1+) | Yo'q |
| Uzunlik | Belgilar soni | Baytlar soni | Baytlar soni |
| Birlashtirish | `+`, `join` | `.`, `.=` | `+`, `strings.Builder` |
| Belgi turi | Alohida tur yo'q | Alohida tur yo'q | `byte` va `rune` |

## Ko'p uchraydigan xatolar

- **Sikl ichida `s += ch`.** Har safar yangi nusxa yaratiladi, umumiy O(n²). Python'da `join`, Go'da `strings.Builder` ishlating.
- **Go'da `s[i]` belgi deb o'ylash.** U `byte`. Belgi sifatida chiqarish uchun `string(s[i])`, solishtirish uchun `s[i] == 'a'`.
- **Unicode.** Go va PHP'da `len` baytlarni sanaydi. Lotin bo'lmagan matnda `[]rune` (Go) yoki `mb_strlen` (PHP).
- **PHP'da `strpos` natijasi.** `0` va `false` ni `!==` bilan ajrating.
- **Chegaradan chiqish.** `s[i]` da `i` `0..len-1` oralig'ida bo'lsin. Python `IndexError`, Go `panic`, PHP ogohlantirish beradi.
- **Katta-kichik harf.** `"A" != "a"`. Taqqoslashdan oldin `lower()` qiling.
- **Bo'sh string.** `s[0]` yoki `s[len-1]` dan oldin `len(s) > 0` ni tekshiring.
