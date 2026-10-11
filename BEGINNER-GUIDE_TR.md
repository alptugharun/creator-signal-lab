# Creator Signal Lab — Sıfırdan Kullanım Rehberi

Creator Signal Lab şu durum için:

> “İçerik fikirlerim veya post metriklerim var. Şeffaf bir yöntemle önceliklendirmek istiyorum ama AI'ın virallik tahmini yaptığını iddia etmek istemiyorum.”

Projede **iki yerel CSV aracı** var.

Scraping yok. Sosyal medya girişi yok. Model çağrısı yok. Gizli skor servisi yok.

---

## 1. CSV nedir?

CSV, tabloyu düz metin halinde saklayan basit bir formattır.

Örnek:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
AI before-after workflow,8,9,8,7,8,5
```

İlk satır sütun adlarıdır.

Sonraki her satır analiz edilecek bir kayıttır.

Spreadsheet programı, text editor veya export aracıyla hazırlanabilir.

---

# 2. Araç A — İçerik Fırsatı Skoru

Soru:

> “Benim verdiğim faktörlere göre hangi içerik fırsatına önce bakmalıyım?”

Gerekli başlık:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Anlamları:

- **name:** fikir adı
- **evidence_strength:** kanıt gücü
- **audience_fit:** kitle uyumu
- **freshness:** güncellik
- **repeatability:** tekrar edilebilir format/sistem olma potansiyeli
- **production_ease:** üretim kolaylığı
- **saturation:** kendi kanıtına göre doygunluk

Tool gizlice search volume çekmez.

## Önce synthetic örnek

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

Beklenen başlangıç:

```text
rank,name,score
1,Pinterest seasonal visual series,83.05
2,AI before-after workflow,79.00
3,Creator teardown carousel,74.10
```

Bu sonuç gelmiyorsa gerçek veriye geçmeden dur.

## Kendi CSV'ni önce doğrula

```bash
python tools/signal2content_score.py senin-firsatlarin.csv --validate-only
```

Sonra:

```bash
python tools/signal2content_score.py senin-firsatlarin.csv --top 5
```

---

# 3. Araç B — Post Outlier Skoru

Soru:

> “Hangi post benim normal sample'ıma göre sıra dışı performans gösterdi?”

Başlık:

```csv
platform,post_id,views,likes,comments,shares,saves
```

## Neden baseline?

10.000 görüntülenme bir hesap için olağanüstü, diğeri için normal olabilir.

Bu yüzden ham sayı tek başına yetmez.

Tool verilen dataset'in medyanını baseline olarak kullanır.

Median kullanımı bir aşırı viral postun bütün baseline'ı şişirmesini azaltır.

## Synthetic örnek

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

Örnek dataset'te `reel-004` ilk sıraya gelir.

## Kendi dosyan

```bash
python tools/outlier_score.py senin-postlarin.csv --validate-only
python tools/outlier_score.py senin-postlarin.csv --top 5
```

---

# 4. Skor ne demek?

Skor = **önceliklendirme heuristic'i**.

Şunu söyler:

> “Bu formül ve bu girdilere göre bu satır daha yukarıda.”

Şunu söylemez:

- %83 başarı;
- viral olma ihtimali;
- algoritmanın boost vereceği;
- satış/takipçi/erişim garantisi.

Formül ile gerçek outcome'u birbirine karıştırma.

---

# 5. Formül neden açık?

Black-box “AI score” üretmek kolaydır.

Ama neden öyle çıktığını anlayamazsın.

Burada:

- ağırlığı görürsün;
- değiştirirsin;
- aynı inputu tekrar çalıştırırsın;
- deterministik karşılaştırma yaparsın.

Amaç karar desteği.

---

# 6. Hangi veri kullanılmalı?

Önce synthetic örnek.

Sonra:

- kendi analytics export'un;
- yetkili client verisi;
- manuel evidence tablosu;
- kullanma hakkın olan public-safe veri.

Private analytics dosyanı public issue'ya yükleme.

---

# 7. CSV hata örnekleri

Tam sözleşme:

`docs/INPUTS.md`

Sık sorunlar:

- eksik sütun;
- duplicate header;
- satır genişliği bozuk;
- locale number formatı;
- sonsuz/NaN;
- quote problemi;
- encoding.

Parser bozuk veriyi sessizce 0'a çevirmek yerine hata verir.

---

# 8. Bu proje ne değildir?

- sosyal algoritma reverse-engineer değil;
- scraper değil;
- canlı analytics connector değil;
- trend API değil;
- LLM classifier değil;
- virallik tahmini değil;
- gelir tahmini değil.

Güncel dış trend gerekiyorsa o kanıt ayrıca toplanmalı ve tarih/kaynak etiketlenmeli.

---

# 9. İyi workflow

### Fırsat analizi

1. karar sorusunu belirle;
2. evidence topla;
3. CSV hazırla;
4. validate;
5. rank;
6. neden kazandığını incele;
7. gerçek içerik testi yap;
8. outcome ile heuristic'i karşılaştır.

### Outlier analizi

1. karşılaştırılabilir post cohort seç;
2. metrikleri çıkar;
3. validate;
4. outlier hesapla;
5. postları gerçekten incele;
6. tekrar edilebilir mekanizma ara;
7. özgün yeni test yap;
8. tekrar ölç.

Kazanan postu birebir kopyalama.

---

# 10. Test

```bash
python -m unittest discover -s tests -v
```

CI Linux ve Windows üzerinde çalışır.

---

# 11. Güvenlik / gizlilik

Proje yerel CSV okur ve stdout'a sonuç yazar.

Şunlara ihtiyaç duymamalı:

- API key;
- cookie;
- sosyal hesap credential;
- network.

Security vulnerability için `SECURITY.md` private reporting yolunu kullan.

Normal parser bug'ında synthetic reproducer kullan.

---

## Son kural

**Skoru belirsizliği yok saymak için değil, sıradaki testi seçmek için kullan.**
