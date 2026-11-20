---
title: Hash Map
summary: Kalit va qiymat juftliklarini saqlaydigan tuzilma. O'rtacha O(1) da qidirish, qo'shish va o'chirish.
---

## Hash Map nima

Hash map (hash table, dictionary, associative array) ma'lumotni **kalit → qiymat** juftligi sifatida saqlaydi. Qiymatni indeks bilan emas, **kalit** bilan topasiz. Masalan, ismdan yoshni, so'zdan uning necha marta uchrashganini yoki sondan uning indeksini.

Asosiy afzalligi: qidirish, qo'shish va o'chirish **o'rtacha O(1)**. Arrayda xuddi shu qidiruv O(n) bo'lardi.

Turli tillarda nomi har xil, lekin g'oya bitta:

| Til | Nomi |
|-----|------|
| Python | `dict` |
| PHP | assotsiativ `array` |
| Go | `map` |

## Ichida qanday ishlaydi

Hash map ichida oddiy array turadi. Uning kataklari **bucket** deyiladi. Kalit bilan ishlash uch qadamda bo'ladi:

1. **Hash funksiya** kalitni butun songa aylantiradi: `hash("ali")` → masalan `918273645`.
2. Shu sondan bucket indeksi olinadi: `indeks = hash % bucketlar_soni`.
3. Qiymat shu bucketga yoziladi yoki o'sha yerdan o'qiladi.

Hash funksiya bir xil kalit uchun doim bir xil son beradi. Shuning uchun kalit bo'yicha to'g'ridan-to'g'ri kerakli katakka boriladi va butun tuzilmani ko'rib chiqish shart emas. Array indeksi bo'yicha O(1) ishlashi bilan bir xil g'oya.

## Kolliziya

Ikki xil kalit bir xil bucketga tushib qolishi mumkin. Bunga **kolliziya** deyiladi. Bu normal holat, uni hal qilish kerak. Ikki asosiy usul bor:

- **Chaining:** har bir bucketda kichik ro'yxat turadi, kolliziyaga uchragan juftliklar shu ro'yxatga qo'shiladi. Go `map` va Java `HashMap` shunga yaqin ishlaydi.
- **Open addressing:** bucket band bo'lsa, keyingi bo'sh bucket qidiriladi. Python `dict` shu usulni ishlatadi.

Kolliziya kam bo'lsa, amallar O(1) ga yaqin bo'ladi. Juda ko'p bo'lsa, bitta bucketda ko'p element yig'iladi va qidirish O(n) ga yaqinlashadi.

## Load factor va kengayish

**Load factor** = elementlar soni / bucketlar soni. U ma'lum chegaradan oshsa (odatda taxminan 0.7 dan), hash map bucketlar sonini oshirib, **barcha elementlarni qayta joylashtiradi** (rehash). Bu bir marta **O(n)** vaqt oladi, lekin kamdan-kam bo'ladi. Shuning uchun qo'shishning o'rtacha narxi **amortizatsiyalangan O(1)**.

## Amallar va murakkablik

| Amal | O'rtacha | Eng yomon | Izoh |
|------|----------|-----------|------|
| Get (kalit bo'yicha o'qish) | O(1) | O(n) | Hash → bucket → qiymat |
| Put (qo'shish yoki yangilash) | O(1) | O(n) | Ba'zan rehash bo'ladi |
| Delete | O(1) | O(n) | Kalit bo'yicha |
| Contains (kalit bormi) | O(1) | O(n) | `in`, `isset`, `ok` |
| Aylanib chiqish | O(n) | O(n) | Barcha juftliklar |
| Xotira | O(n) | O(n) | Array'dan ko'proq: bucketlar va hash'lar uchun joy kerak |

Eng yomon holat (O(n)) amalda kam uchraydi: hamma kalit bitta bucketga tushsagina bo'ladi. Yaxshi hash funksiya bunga yo'l qo'ymaydi, shuning uchun masalalarda odatda O(1) deb hisoblanadi.

## Yaratish, qo'shish, yangilash

Mavjud bo'lmagan kalitga yozsangiz, juftlik **qo'shiladi**. Mavjud kalitga yozsangiz, qiymat **yangilanadi**. Ikkalasi bir xil sintaksis bilan yoziladi.

```python
ages = {"ali": 20, "vali": 25}   # yaratish
empty = {}                       # bo'sh dict

ages["sami"] = 30                # yangi kalit: qo'shiladi
ages["ali"] = 21                 # mavjud kalit: yangilanadi
print(ages)                      # {'ali': 21, 'vali': 25, 'sami': 30}
```

```php
$ages = ["ali" => 20, "vali" => 25];   // yaratish
$empty = [];                           // bo'sh array

$ages["sami"] = 30;                    // yangi kalit: qo'shiladi
$ages["ali"] = 21;                     // mavjud kalit: yangilanadi
print_r($ages);                        // [ali => 21, vali => 25, sami => 30]
```

```go
ages := map[string]int{"ali": 20, "vali": 25} // yaratish
empty := make(map[string]int)                 // bo'sh map
_ = empty

ages["sami"] = 30                             // yangi kalit: qo'shiladi
ages["ali"] = 21                              // mavjud kalit: yangilanadi
fmt.Println(ages)                             // map[ali:21 sami:30 vali:25]
```

## Read: qiymatni o'qish

Kalit mavjud bo'lmasa, tillar har xil harakat qiladi. Shuning uchun "kalit bormi" ni xavfsiz tekshirish usulini bilish muhim.

```python
ages = {"ali": 20, "vali": 25}

print(ages["ali"])            # 20
# print(ages["zafar"])        # KeyError: kalit yo'q
print(ages.get("zafar"))      # None, xato bermaydi
print(ages.get("zafar", 0))   # 0, default qiymat bilan
```

```php
$ages = ["ali" => 20, "vali" => 25];

echo $ages["ali"];            // 20
// echo $ages["zafar"];       // Warning: Undefined array key
echo $ages["zafar"] ?? 0;     // 0, default qiymat bilan
```

```go
ages := map[string]int{"ali": 20, "vali": 25}

fmt.Println(ages["ali"])      // 20
fmt.Println(ages["zafar"])    // 0, kalit yo'q bo'lsa tur uchun nol qiymat

age, ok := ages["zafar"]      // "comma ok" idiomasi
fmt.Println(age, ok)          // 0 false
```

> Go'da `ages["zafar"]` xato bermaydi va `0` qaytaradi. Shuning uchun qiymat haqiqatan `0` mi yoki kalit yo'qmi, buni faqat ikkinchi qiymat `ok` aytib beradi.

## Contains: kalit bormi

```python
ages = {"ali": 20}

print("ali" in ages)      # True
print("zafar" in ages)    # False
```

```php
$ages = ["ali" => 20, "bek" => null];

var_dump(array_key_exists("ali", $ages));  // true
var_dump(isset($ages["ali"]));             // true
var_dump(isset($ages["bek"]));             // false! qiymat null bo'lgani uchun
var_dump(array_key_exists("bek", $ages));  // true
```

```go
ages := map[string]int{"ali": 20}

_, ok := ages["ali"]
fmt.Println(ok)     // true

_, ok = ages["zafar"]
fmt.Println(ok)     // false
```

## Delete: o'chirish

O'chirish kalit bo'yicha bo'ladi va o'rtacha **O(1)**. Arraydagidek elementlarni surish kerak emas.

```python
ages = {"ali": 20, "vali": 25, "sami": 30}

del ages["vali"]              # kalit yo'q bo'lsa KeyError
ages.pop("sami", None)        # xavfsiz: yo'q bo'lsa None qaytaradi
print(ages)                   # {'ali': 20}
```

```php
$ages = ["ali" => 20, "vali" => 25, "sami" => 30];

unset($ages["vali"]);         // kalit yo'q bo'lsa ham xato bermaydi
unset($ages["sami"]);
print_r($ages);               // [ali => 20]
```

```go
ages := map[string]int{"ali": 20, "vali": 25, "sami": 30}

delete(ages, "vali")          // kalit yo'q bo'lsa ham xato bermaydi
delete(ages, "sami")
fmt.Println(ages)             // map[ali:20]
```

## Aylanib chiqish va uzunlik

```python
ages = {"ali": 20, "vali": 25}

for name, age in ages.items():   # kalit va qiymat
    print(name, age)

print(len(ages))                 # 2
print(list(ages.keys()))         # ['ali', 'vali']
print(list(ages.values()))       # [20, 25]
```

```php
$ages = ["ali" => 20, "vali" => 25];

foreach ($ages as $name => $age) {   // kalit va qiymat
    echo "$name $age\n";
}

echo count($ages);                   // 2
print_r(array_keys($ages));          // [ali, vali]
print_r(array_values($ages));        // [20, 25]
```

```go
ages := map[string]int{"ali": 20, "vali": 25}

for name, age := range ages {   // kalit va qiymat
	fmt.Println(name, age)
}

fmt.Println(len(ages))          // 2
```

> Tartib: Python 3.7+ va PHP juftliklarni **qo'shilgan tartibda** saqlaydi. Go'da `range` tartibi **ataylab tasodifiy**, har ishga tushirishda boshqacha bo'lishi mumkin. Tartib kerak bo'lsa, kalitlarni alohida olib `sort` qiling.

## Sanash (frequency count)

Hash map'ning eng ko'p uchraydigan qo'llanishi: har bir elementning necha marta uchrashini sanash.

```python
words = ["a", "b", "a", "c", "a", "b"]
counts = {}

for w in words:
    counts[w] = counts.get(w, 0) + 1

print(counts)   # {'a': 3, 'b': 2, 'c': 1}
# tayyor variant: collections.Counter(words)
```

```php
$words = ["a", "b", "a", "c", "a", "b"];
$counts = [];

foreach ($words as $w) {
    $counts[$w] = ($counts[$w] ?? 0) + 1;
}

print_r($counts);   // [a => 3, b => 2, c => 1]
```

```go
words := []string{"a", "b", "a", "c", "a", "b"}
counts := make(map[string]int)

for _, w := range words {
	counts[w]++   // yo'q kalit uchun 0 dan boshlanadi
}

fmt.Println(counts)   // map[a:3 b:2 c:1]
```

## Set: faqat kalitlar

Ba'zan qiymat kerak emas, faqat "element bormi" degan savolga javob kerak. Buning uchun **set** ishlatiladi. U ichida hash map kabi ishlaydi, shuning uchun qo'shish va tekshirish ham o'rtacha **O(1)**. Ikki barobar bir xil element saqlanmaydi.

```python
seen = set()
seen.add(3)
seen.add(3)            # takror qo'shilmaydi
print(3 in seen)       # True
print(len(seen))       # 1
```

```php
$seen = [];
$seen[3] = true;       // PHP'da alohida set yo'q, kalitdan foydalaniladi
$seen[3] = true;       // takror qo'shilmaydi
var_dump(isset($seen[3]));   // true
echo count($seen);           // 1
```

```go
seen := make(map[int]struct{})   // struct{} xotira egallamaydi
seen[3] = struct{}{}
seen[3] = struct{}{}             // takror qo'shilmaydi
_, ok := seen[3]
fmt.Println(ok, len(seen))       // true 1
```

## Kalit uchun talablar

Kalit **o'zgarmas** va **hash qilinadigan** bo'lishi kerak, aks holda hash o'zgarib ketib, qiymatni topib bo'lmay qoladi.

| | Python | PHP | Go |
|---|--------|-----|----|
| Mumkin | `int`, `str`, `tuple`, `frozenset`, `bool` | `int`, `string` | `int`, `string`, `bool`, struct va array (agar ichidagilar ham taqqoslanuvchi bo'lsa) |
| Mumkin emas | `list`, `dict`, `set` (`TypeError`) | massiv va obyekt | `slice`, `map`, `func` (kompilyatsiya xatosi) |

Ikki o'lchamli koordinata kerak bo'lsa, Python'da `tuple` ishlatiladi: `grid[(2, 3)] = 1`. Go'da struct yoki `[2]int` ishlatiladi.

> PHP'da kalit faqat `int` yoki `string`. `"5"` kaliti avtomatik `5` ga aylanadi, `1.7` esa `1` ga qirqiladi, `true` esa `1` bo'ladi. Kutilmagan to'qnashuvlar shundan chiqadi.

## Tillar o'rtasidagi farqlar

| | Python | PHP | Go |
|---|--------|-----|----|
| Yo'q kalitga o'qish | `KeyError` | Ogohlantirish, `null` | Nol qiymat (`0`, `""`, `nil`) |
| Bo'sh holat | `{}` | `[]` | `nil` map (yozib bo'lmaydi!) |
| Tartib | Qo'shilgan tartib | Qo'shilgan tartib | Tasodifiy |
| Qiymat turi | Aralash | Aralash | Hammasi bir xil |
| Nusxalash | `b = a` ishora, `a.copy()` nusxa | `$b = $a` nusxa oladi | `b := a` bir xil map, nusxa qo'lda |

## Ko'p uchraydigan xatolar

- **Go'da `nil` map'ga yozish.** `var m map[string]int` yozsangiz, `m["a"] = 1` **panic** beradi. `make(map[string]int)` yoki `map[string]int{}` bilan yarating. O'qish va `len` esa `nil` map'da ishlaydi.
- **Yo'q kalitni o'qish.** Python'da `KeyError`, PHP'da ogohlantirish. `.get()`, `??` yoki oldin `in` bilan tekshiring.
- **Go'da nol qiymat bilan adashish.** `counts["x"]` natijasi `0` bo'lsa, kalit yo'q yoki qiymat haqiqatan `0` ekanini `ok` orqali ajrating.
- **PHP'da `isset` va `null`.** Qiymat `null` bo'lsa, `isset` kalit bor bo'lsa ham `false` beradi. Kalit mavjudligi uchun `array_key_exists`.
- **Aylanayotganda o'zgartirish.** Python'da sikl ichida `dict` ga kalit qo'shsangiz yoki o'chirsangiz `RuntimeError` chiqadi. Kalitlar nusxasidan aylaning: `for k in list(d):`.
- **Tartibga ishonish.** Go'da `map` tartibi kafolatlanmagan. Natijani tartiblangan holda chiqarish kerak bo'lsa, kalitlarni `sort` qiling.
- **O'zgaruvchan kalit.** Python'da `list` ni kalit qilib bo'lmaydi, `tuple` ga o'giring.

## Qachon hash map tanlanadi

Hash map yaxshi: kalit bo'yicha tez qidirish kerak, elementlarni sanash, takrorlanishni topish, "bu oldin uchraganmi" degan savolga javob berish, ma'lumotni guruhlash.

Hash map yomon: elementlar **tartiblangan** bo'lishi kerak (u holda tartiblangan array yoki balanced tree), kichik-katta bo'yicha oraliq qidirish kerak, xotira juda tor (hash map array'dan ko'proq joy oladi), indeks bo'yicha ketma-ket murojaat yetarli (u holda oddiy [Array](array.html)).
