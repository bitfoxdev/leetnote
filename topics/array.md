---
title: Array
summary: Elementlar ketma-ket saqlanadigan eng oddiy ma'lumotlar tuzilmasi. Read, update, insert, delete amallari va ularning murakkabligi.
---

## Array nima

Array (massiv) bir xil turdagi elementlarni **tartib bilan** saqlaydi. Har bir elementning o'z **indeksi** bor. Indeks `0` dan boshlanadi: birinchi element `0`, ikkinchisi `1` va hokazo. Uzunligi `n` bo'lsa, oxirgi indeks `n - 1`.

```python
nums = [10, 20, 30, 40]
#  indeks:  0   1   2   3
```

```php
$nums = [10, 20, 30, 40];
//  indeks:  0   1   2   3
```

```go
nums := []int{10, 20, 30, 40}
//  indeks:  0   1   2   3
```

## Xotirada qanday saqlanadi

Klassik arrayda elementlar xotirada **yonma-yon** turadi. Kompyuter `i`-elementning manzilini formula bilan topadi:

`manzil = boshlang'ich manzil + i × element hajmi`

Shu sababli indeks bo'yicha murojaat massiv qanchalik katta bo'lishidan qat'i nazar bir xil tezlikda, ya'ni **O(1)** da bajariladi. Narxi esa o'rtaga qo'shish va o'chirishda to'lanadi: elementlarni surish kerak bo'ladi.

> Muhim: Python `list`, Go `slice` va PHP `array` aslida **dinamik** array. Ular o'zi kengayadi, lekin asosiy qoidalar (indeks bo'yicha O(1), o'rtada surish O(n)) o'sha-o'sha qoladi.

## Amallar va murakkablik

| Amal | Vaqt | Izoh |
|------|------|------|
| Read (indeks bo'yicha o'qish) | O(1) | Formula bilan to'g'ridan-to'g'ri manzilga boriladi |
| Update (indeks bo'yicha yozish) | O(1) | Qiymat o'sha katakka yoziladi |
| Qidirish (tartiblanmagan) | O(n) | Eng yomon holda hammasini ko'rib chiqish kerak |
| Qidirish (tartiblangan, binary search) | O(log n) | Har qadamda qidiruv oralig'i yarmiga kamayadi |
| Insert, oxiriga | O(1) | Amortizatsiyalangan: ba'zan array kengayadi |
| Insert, boshiga yoki o'rtaga | O(n) | Keyingi elementlar bir katakka suriladi |
| Delete, oxiridan | O(1) | Faqat uzunlik kamayadi |
| Delete, boshidan yoki o'rtadan | O(n) | Bo'sh joyni yopish uchun elementlar suriladi |
| Butun arrayni aylanib chiqish | O(n) | Har element bir marta ko'riladi |
| Xotira | O(n) | `n` ta element uchun |

## Read: elementni o'qish

Indeks bo'yicha o'qish har doim **O(1)**. Indeks `0 .. n-1` oralig'idan tashqarida bo'lsa, xato chiqadi.

```python
nums = [10, 20, 30, 40]

print(nums[0])     # 10, birinchi
print(nums[2])     # 30
print(nums[-1])    # 40, oxirgi (Python'da manfiy indeks ruxsat etiladi)
print(len(nums))   # 4, uzunlik
```

```php
$nums = [10, 20, 30, 40];

echo $nums[0];                  // 10, birinchi
echo $nums[2];                  // 30
echo $nums[count($nums) - 1];   // 40, oxirgi (PHP'da manfiy indeks yo'q)
echo count($nums);              // 4, uzunlik
```

```go
nums := []int{10, 20, 30, 40}

fmt.Println(nums[0])            // 10, birinchi
fmt.Println(nums[2])            // 30
fmt.Println(nums[len(nums)-1])  // 40, oxirgi (Go'da manfiy indeks yo'q)
fmt.Println(len(nums))          // 4, uzunlik
```

## Update: elementni o'zgartirish

Mavjud katakka yangi qiymat yozish ham **O(1)**: boshqa elementlarga tegilmaydi.

```python
nums = [10, 20, 30, 40]
nums[1] = 25
print(nums)   # [10, 25, 30, 40]
```

```php
$nums = [10, 20, 30, 40];
$nums[1] = 25;
print_r($nums);   // [10, 25, 30, 40]
```

```go
nums := []int{10, 20, 30, 40}
nums[1] = 25
fmt.Println(nums)   // [10 25 30 40]
```

## Insert: element qo'shish

**Oxiriga** qo'shish odatda **O(1)**. Dinamik array to'lib qolsa, o'zidan taxminan 2 baravar katta yangi joy ajratadi va hammasini ko'chiradi (bu **O(n)**). Lekin bu kamdan-kam bo'lgani uchun o'rtacha narx O(1) bo'ladi. Buni *amortizatsiyalangan O(1)* deyiladi.

**Boshiga yoki o'rtaga** qo'shishda undan keyingi hamma elementlar bir katakka suriladi, shuning uchun **O(n)**.

```python
nums = [10, 20, 30]

nums.append(40)       # oxiriga, O(1)
nums.insert(1, 15)    # 1-indeksga, O(n)
print(nums)           # [10, 15, 20, 30, 40]
```

```php
$nums = [10, 20, 30];

$nums[] = 40;                      // oxiriga, O(1)
array_splice($nums, 1, 0, [15]);   // 1-indeksga, O(n)
print_r($nums);                    // [10, 15, 20, 30, 40]
```

```go
nums := []int{10, 20, 30}

nums = append(nums, 40)         // oxiriga, O(1)
nums = slices.Insert(nums, 1, 15) // 1-indeksga, O(n), Go 1.21+, "slices" paketi
fmt.Println(nums)               // [10 15 20 30 40]
```

## Delete: element o'chirish

**Oxiridan** o'chirish **O(1)**. **Boshidan yoki o'rtadan** o'chirsangiz, bo'sh qolgan joyni yopish uchun keyingi elementlar chapga suriladi, ya'ni **O(n)**.

```python
nums = [10, 20, 30, 40]

nums.pop()        # oxiridan, O(1) -> 40
nums.pop(1)       # 1-indeksdan, O(n) -> 20
print(nums)       # [10, 30]
```

```php
$nums = [10, 20, 30, 40];

array_pop($nums);              // oxiridan, O(1)
array_splice($nums, 1, 1);     // 1-indeksdan, O(n), indekslar qayta tartiblanadi
print_r($nums);                // [10, 30]
```

```go
nums := []int{10, 20, 30, 40}

nums = nums[:len(nums)-1]        // oxiridan, O(1)
nums = slices.Delete(nums, 1, 2) // [1, 2) oralig'ini, O(n)
fmt.Println(nums)                // [10 30]
```

> PHP'da `unset($nums[1])` elementni o'chiradi, lekin indekslarni **qayta tartiblamaydi**: `[0, 2, 3]` kabi "teshik" qoladi. Tartibli massiv kerak bo'lsa `array_splice` yoki `array_values` ishlating.

## Qidirish va aylanib chiqish

Tartiblanmagan arrayda elementni topish uchun boshidan boshlab ko'rib chiqiladi: **O(n)**. Massiv tartiblangan bo'lsa, binary search bilan **O(log n)** da topiladi.

```python
nums = [10, 20, 30, 40]

print(30 in nums)          # True, mavjudmi
print(nums.index(30))      # 2, indeksi (topilmasa ValueError)

for i, x in enumerate(nums):   # indeks va qiymat bilan
    print(i, x)
```

```php
$nums = [10, 20, 30, 40];

var_dump(in_array(30, $nums));      // true, mavjudmi
var_dump(array_search(30, $nums));  // int(2), indeksi (topilmasa false)

foreach ($nums as $i => $x) {       // indeks va qiymat bilan
    echo "$i $x\n";
}
```

```go
nums := []int{10, 20, 30, 40}

fmt.Println(slices.Contains(nums, 30)) // true, mavjudmi
fmt.Println(slices.Index(nums, 30))    // 2, indeksi (topilmasa -1)

for i, x := range nums {               // indeks va qiymat bilan
	fmt.Println(i, x)
}
```

## Tillar o'rtasidagi farqlar

| | Python | PHP | Go |
|---|--------|-----|----|
| Turi | `list` | `array` | `slice` (`[]T`), qat'iy uzunlikdagi `[n]T` array ham bor |
| Elementlar turi | Aralash bo'lishi mumkin | Aralash bo'lishi mumkin | Hammasi bir xil tur |
| Manfiy indeks | `nums[-1]` ishlaydi | Yo'q | Yo'q (panic) |
| Chegaradan chiqish | `IndexError` | Ogohlantirish va `null` | `panic` |
| Nusxalash | `b = a` bitta obyektga ishora | `$b = $a` nusxa oladi | Slice'lar bir xotirani bo'lishishi mumkin |
| Ichki tuzilma | Dinamik array | Tartiblangan hash map | Dinamik array ustidagi ko'rinish |

## Ko'p uchraydigan xatolar

- **Off-by-one:** oxirgi indeks `n - 1`, `n` emas. Siklda `i < n` yozing, `i <= n` emas.
- **Bo'sh array:** `nums[0]` yoki `nums[-1]` ga murojaatdan oldin `len(nums) > 0` ni tekshiring.
- **Aylanayotganda o'zgartirish:** arrayni sikl ichida o'chirish yoki qo'shish elementlarni o'tkazib yuboradi. Yangi array yarating yoki oxiridan boshlab aylaning.
- **Nusxa va ishora:** Python'da `b = a` yangi array yaratmaydi, ikkalasi bitta list. Nusxa uchun `b = a[:]` yoki `a.copy()`. Go'da `b := a` ham bir xil xotiraga ishora qiladi, nusxa uchun `slices.Clone(a)`.
- **O'rtadan o'chirish sikl ichida:** har bir `pop(i)` O(n), umumiy narx O(n²) bo'lib ketadi.

## Qachon array tanlanadi

Array yaxshi: indeks bo'yicha tez murojaat kerak, elementlar tartibli, asosan oxiriga qo'shiladi, xotira zich va tez ishlaydi.

Array yomon: boshiga yoki o'rtaga tez-tez qo'shish va o'chirish kerak (u holda linked list, deque), kalit bo'yicha qidirish kerak (u holda [Hash Map](hash-map.html)).
