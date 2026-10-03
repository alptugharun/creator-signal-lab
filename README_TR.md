# Creator Signal Lab

[![English](https://img.shields.io/badge/English-0D1117?style=flat-square)](README.md) [![Türkçe](https://img.shields.io/badge/Türkçe-E30A17?style=flat-square)](README_TR.md)

**Creator araştırması için iki küçük ve şeffaf skor aracı — virallik tahmini yaptığını iddia etmeden.**

Creator Signal Lab iki soruya cevap üretmek için tasarlandı:

1. **Hangi içerik fırsatına önce bakmalıyım?**
2. **Hangi gönderi kendi normal performansıma göre gerçekten aykırıydı?**

Araçlar platform scrape etmez, AI modeli çağırmaz, trend verisi uydurmaz ve erişim garantisi vermez. Verdiğin açık girdileri, açıklanabilir sıralamalara dönüştürür.

## 1 — İçerik fırsatı skoru

Gerekli CSV başlığı:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Çalıştır:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

Puan formülü kaynak kodda açıkça görülebilir. Bu puan başarı olasılığı değil; önceliklendirme heuristic'idir.

## 2 — Sosyal gönderi outlier skoru

Gerekli CSV başlığı:

```csv
platform,post_id,views,likes,comments,shares,saves
```

Çalıştır:

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

Araç her metriği veri kümesinin medyanına göre karşılaştırır. Böylece tek bir aşırı viral gönderi baseline'ı tek başına şişirmez.

## Neden şeffaf?

Creator analitiğinde güzel görünen ama açıklanamayan skorlar çok kolay üretiliyor.

Bu repo özellikle şunları açık bırakır:

- ağırlıklar;
- input sözleşmesi;
- örnek veri;
- hata mesajları;
- skor mantığı;
- sınırlamalar.

Ağırlıkları beğenmeyebilirsin; değiştirebilirsin. Önemli olan neyin hesaplandığını görebilmen.

## Kendi CSV dosyanı kullan

Önce [docs/INPUTS.md](docs/INPUTS.md) dosyasını oku.

```bash
python tools/signal2content_score.py senin-firsatlarin.csv --validate-only
python tools/outlier_score.py senin-postlarin.csv --validate-only
```

Araçlar bozuk veriyi sessizce sıfıra çevirmek yerine hata verir.

## Test

```bash
python -m unittest discover -s tests -v
```

CI Linux ve Windows üzerinde çalışır.

## Bu araç ne değildir?

- sosyal medya algoritması çözümleyicisi değildir;
- virallik tahmini değildir;
- canlı analytics bağlantısı değildir;
- gelir veya erişim garantisi değildir.

Bu, varsayımlarını görünür yapan küçük bir araştırma aracıdır.

Proje [AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit) içindeki test edilmiş creator araçlarından ayrıştırıldı.

## Lisans

MIT.
