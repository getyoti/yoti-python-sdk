# Git Merge Conflict Çözüm Rehberi

## Durum
- **Mevcut Branch:** SDK-2156-python-static-liveness-check
- **Hedef Branch:** development
- **Conflict Dosyaları:**
  - examples/doc_scan/requirements.in
  - examples/doc_scan/requirements.txt
  - requirements.in
  - requirements.txt
  - setup.py
  - sonar-project.properties
  - yoti_python_sdk/tests/test_anchor.py
  - yoti_python_sdk/version.py

## Çözüm Adımları

### 1. Değişikliklerinizi Commit Edin

```bash
# Tüm değişiklikleri stage'e ekle
git add .

# Commit yap
git commit -m "feat: Add Static Liveness Check support

- Added STATIC constant to constants.py
- Updated liveness check configuration with manual_check support
- Created ImageResponse and StaticLivenessResourceResponse classes
- Updated resource_container.py to parse STATIC liveness type
- Added static_liveness_resources filter property
- Created comprehensive unit tests (9 new tests)
- Updated example application success.html template
- All 180 doc_scan tests passing with no regressions"
```

### 2. Development Branch'ini Merge Edin

```bash
# Development branch'ini fetch edin
git fetch origin development

# Development'i merge edin
git merge origin/development
```

### 3. Conflict'leri Çözün

Conflict olan dosyalar için stratejiler:

#### A. Version Dosyaları (version.py, setup.py)
- **Strateji:** Development'taki version'ı kullan (THEIRS)
- **Sebep:** Version numaraları development'ta daha güncel

```bash
git checkout --theirs yoti_python_sdk/version.py
git checkout --theirs setup.py
git add yoti_python_sdk/version.py setup.py
```

#### B. Requirements Dosyaları (requirements.in, requirements.txt)
- **Strateji:** Development'taki dependency'leri kullan (THEIRS)
- **Sebep:** Development'ta güncel dependency versiyonları var

```bash
git checkout --theirs requirements.in
git checkout --theirs requirements.txt
git checkout --theirs examples/doc_scan/requirements.in
git checkout --theirs examples/doc_scan/requirements.txt
git add requirements.in requirements.txt
git add examples/doc_scan/requirements.in examples/doc_scan/requirements.txt
```

#### C. Sonar Properties
- **Strateji:** Development'taki ayarları kullan (THEIRS)

```bash
git checkout --theirs sonar-project.properties
git add sonar-project.properties
```

#### D. Test Dosyaları (test_anchor.py)
- **Strateji:** Manuel olarak incele ve birleştir
- **Sebep:** Her iki branch'te de test değişiklikleri olabilir

```bash
# Dosyayı editörde aç ve conflict marker'ları çöz
# <<<<<<< HEAD
# =======
# >>>>>>> development
```

### 4. Conflict Çözüldükten Sonra

```bash
# Tüm conflict'lerin çözüldüğünden emin olun
git status

# Merge'i tamamlayın
git commit -m "Merge development into SDK-2156-python-static-liveness-check

Resolved conflicts in:
- version.py (used development version)
- setup.py (used development version)
- requirements files (used development dependencies)
- sonar-project.properties (used development config)
- test_anchor.py (merged both changes)"
```

### 5. Test Edin

```bash
# Tüm testlerin çalıştığından emin olun
pytest yoti_python_sdk/tests/doc_scan/ -v

# Static liveness testlerini çalıştırın
pytest yoti_python_sdk/tests/doc_scan/session/create/check/test_liveness_check.py -v
pytest yoti_python_sdk/tests/doc_scan/session/retrieve/test_static_liveness_resource.py -v
```

### 6. Push Edin

```bash
# Branch'inizi push edin
git push origin SDK-2156-python-static-liveness-check
```

## Alternatif: Rebase Stratejisi

Eğer daha temiz bir history istiyorsanız:

```bash
# Mevcut değişiklikleri commit edin
git add .
git commit -m "feat: Add Static Liveness Check support"

# Development üzerine rebase yapın
git fetch origin development
git rebase origin/development

# Conflict'leri çözün (yukarıdaki stratejileri kullanın)
# Her conflict çözümünden sonra:
git add <dosya>
git rebase --continue

# Rebase tamamlandıktan sonra force push
git push origin SDK-2156-python-static-liveness-check --force-with-lease
```

## Önemli Notlar

1. **Version Dosyaları:** Development'taki version'ı kullanın
2. **Dependencies:** Development'taki güncel dependency'leri kullanın
3. **Kod Değişiklikleri:** Sizin Static Liveness değişikliklerinizi koruyun
4. **Test Dosyaları:** Her iki branch'teki değişiklikleri birleştirin
5. **Force Push:** Sadece rebase kullanıyorsanız gerekli

## Yardım

Eğer conflict çözümünde sorun yaşarsanız:

```bash
# Merge'i iptal edin ve baştan başlayın
git merge --abort

# Veya rebase'i iptal edin
git rebase --abort
```
