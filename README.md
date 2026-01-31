# 👔 StyleSanctuary

AI destekli, hava durumuna göre kişiselleştirilmiş kombin önerisi uygulaması.

> **Note**: This application interface is in Turkish (Türkçe). The codebase and documentation use English for developer accessibility.

## ✨ Özellikler

- 🌤️ **Canlı Hava Durumu**: 5 şehir için anlık hava durumu
- 🎨 **Quick Outfit Gallery**: Sorulara cevap vermeden binlerce kombin önerisi
- 🤖 **AI Destekli Öneriler**: Ollama LLM ile kişiselleştirilmiş kombinler
- 📸 **Fashion Dataset**: HuggingFace FashionRec dataset ile gerçek kıyafet görselleri
- 💾 **Kombin Kaydetme**: Geçmiş kombinlerinizi saklayın
- 🎭 **Kişiselleştirme**: Ruh halinize, stilinize göre öneriler
- 🎨 **Modern UI**: Glassmorphism efektleri ile modern arayüz

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Ollama (yerel LLM için) - [İndir](https://ollama.ai/)
- OpenWeatherMap API Key - [Ücretsiz Alın](https://openweathermap.org/api)

### Adımlar

1. **Repo'yu klonlayın**
```bash
git clone https://github.com/okaybuyukdeveci/StyleSanctuary.git
cd StyleSanctuary
```

2. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

3. **Ollama'yı kurun ve modeli indirin**
```bash
# Ollama'yı yükleyin: https://ollama.ai/
# Ardından modeli indirin:
ollama pull qwen2.5:7b-instruct
```

4. **Environment ayarları**
```bash
cp .env.example .env
# .env dosyasını düzenleyin ve API key'inizi girin
```

`.env` dosyanızı düzenleyin:
```env
WEATHER_API_KEY=your_openweathermap_api_key_here
OLLAMA_URL=http://localhost:11434/api/generate
MODEL_NAME=qwen2.5:7b-instruct
```

5. **İlk kurulum**
```bash
python setup.py
```

Bu script:
- ✓ Gerekli klasörleri oluşturur
- ✓ FashionRec dataset'ini HuggingFace'den indirir ve cache'ler
- ✓ SQLite database'i oluşturur
- ✓ Ortam değişkenlerini kontrol eder

> **Not:** İlk kurulum sırasında FashionRec dataset'i indirilir (~500MB). Bu işlem 10-15 dakika sürebilir. Dataset cache'lendikten sonra yüklemeler hızlı olacaktır.

6. **Uygulamayı başlatın**

**Web Arayüzü (Modern UI):**
```bash
streamlit run app.py
```

**CLI Versiyonu (Klasik):**
```bash
python main.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin!

## 📁 Proje Yapısı

```
StyleSanctuary/
├── app.py                  # Streamlit web uygulaması ⭐
├── main.py                 # CLI versiyonu
├── setup.py                # İlk kurulum scripti
├── config.py               # Konfigürasyon
├── requirements.txt        # Python bağımlılıkları
│
├── backend/                # Backend modülleri
│   ├── __init__.py
│   ├── weather.py          # Hava durumu servisi
│   ├── agent.py            # LLM agent (Ollama)
│   ├── database.py         # SQLite işlemleri
│   └── dataset_loader.py   # Fashion dataset yönetimi
│
├── data/                   # Data klasörü
│   ├── fashion_dataset/    # Dataset cache
│   └── user_history.db     # SQLite database
│
├── assets/                 # Statik dosyalar
│   └── styles.css          # Custom CSS (app.py içinde)
│
├── .env.example            # Environment template
└── .gitignore              # Git ignore rules
```

## 🎮 Kullanım

### Web Arayüzü (Önerilen)

#### 1. Ana Sayfa 🏠
- **Weather Horizon**: Üstte 5 şehir için anlık hava durumu kartları
- **Quick Outfit Gallery**: 12 adet filtrelenebilir kombin önerisi
  - Cinsiyet, mevsim ve stil filtreleri
  - Görsel ön izleme
  - Detay görüntüleme
  - Hızlı kaydetme

#### 2. Kişisel Öneri ✨
1. Şehir, cinsiyet ve etkinlik bilgilerinizi girin
2. Stil tercihlerinizi seçin (birden fazla seçilebilir)
3. Ruh halinizi ayarlayın
4. "🎨 Kombin Öner" butonuna tıklayın
5. AI size özel kombin önerisi oluşturur
6. Önerilen kıyafetlerin görsellerini görün
7. Beğendiyseniz kaydedin!

#### 3. Kayıtlarım 💾
- Tüm kayıtlı kombinlerinizi görün
- Tarih, şehir ve hava durumu bilgileri ile
- Favori işaretleme
- Arama ve filtreleme
- Detaylı görüntüleme

#### 4. Hakkında ℹ️
- Proje bilgileri
- Özellikler listesi
- Teknoloji stack
- Geliştirici bilgisi

### CLI Versiyonu (Klasik)

```bash
python main.py
```

Terminal üzerinden adım adım:
1. Şehir adını girin
2. Cinsiyet bilgisi
3. Gideceğiniz yer
4. Stil tercihiniz
5. Ruh haliniz

AI, hava durumuna göre size özel kombin önerir!

## 🛠️ Teknoloji Stack

- **Frontend**: Streamlit 1.31.0
- **AI/LLM**: Ollama (Qwen 2.5:7b-instruct)
- **Weather API**: OpenWeatherMap
- **Database**: SQLite3
- **Dataset**: HuggingFace FashionRec Dataset
- **Python**: 3.8+

## 📊 Dataset

Bu proje [HuggingFace FashionRec Dataset](https://huggingface.co/datasets/Anony100/FashionRec) kullanmaktadır.

İlk kurulumda dataset'in yarısı otomatik olarak indirilir ve cache'lenir (~500MB).

**Dataset Özellikleri:**
- **Kaynak**: HuggingFace Anony100/FashionRec
- **İçerik**: Gerçek kıyafet görselleri ve ürün bilgileri
- **Kategoriler**: Tops, Bottoms, Shoes, Accessories
- **Stiller**: Casual, Formal, Sporty, Chic, Classic
- **Mevsimler**: Spring, Summer, Fall, Winter
- **Cinsiyetler**: Male, Female, Unisex

> **Not:** Dataset indirilemezse, uygulama otomatik olarak fallback mock data'ya geçer ve çalışmaya devam eder.

## 🎨 Özelleştirme

### Yeni Şehir Eklemek
`app.py` içinde `render_weather_horizon()` fonksiyonunu düzenleyin:

```python
cities = ["London", "Istanbul", "New York", "Tokyo", "Dubai"]
```

### Stil Seçenekleri Eklemek
`app.py` içinde `render_personalized_recommendation()` fonksiyonunu düzenleyin:

```python
style_options = ["Casual", "Classic", "Minimalist", "Sporty", "Chic", "Formal", "Vintage"]
```

### Dataset Boyutu Değiştirmek
`backend/dataset_loader.py` içinde `_create_mock_dataset()` fonksiyonunu düzenleyin:

```python
for i in range(1000):  # 500'den 1000'e çıkar
```

## 🐛 Sorun Giderme

### Ollama Hatası
```
❌ Öneri oluşturulamadı: Connection refused
```

**Çözüm**: Ollama servisinin çalıştığından emin olun:
```bash
ollama serve
```

### Hava Durumu Hatası
```
❌ Hava durumu alınamadı
```

**Çözüm**: 
1. `.env` dosyasında `WEATHER_API_KEY` kontrolü
2. İnternet bağlantısı kontrolü
3. API key'in geçerli olduğunu doğrulayın

### Database Hatası
```
❌ Veritabanı hatası
```

**Çözüm**: Setup scriptini tekrar çalıştırın:
```bash
python setup.py
```

### Streamlit Hatası
```
ModuleNotFoundError: No module named 'streamlit'
```

**Çözüm**: Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📝 Lisans

MIT License

## 👤 Geliştirici

**Okay Büyükdeveci**
- GitHub: [@okaybuyukdeveci](https://github.com/okaybuyukdeveci)

## 🙏 Teşekkürler

- [OpenWeatherMap API](https://openweathermap.org/)
- [Ollama](https://ollama.ai/)
- [Streamlit](https://streamlit.io/)
- [Hugging Face](https://huggingface.co/) - FashionRec Dataset
- [Anony100/FashionRec Dataset](https://huggingface.co/datasets/Anony100/FashionRec)

## 📄 Dataset Atıfı

Bu proje HuggingFace FashionRec dataset'ini kullanmaktadır:
- Dataset: Anony100/FashionRec
- Platform: HuggingFace
- URL: https://huggingface.co/datasets/Anony100/FashionRec

## 📸 Ekran Görüntüleri

> Ekran görüntüleri yakında eklenecek!

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
