"""Usage: python3 tools/make_tr.py .   (from the repo root)

Build tr/index.html from index.html: same markup, Turkish text, paths one level up.
Text nodes are matched exactly (after strip); anything unmapped that contains letters is reported."""
import re, sys

SRC = sys.argv[1] + "/index.html"
DST = sys.argv[1] + "/tr/index.html"

KEEP = {  # identical in both languages
    'ek', 'EN', 'Elif Konak', 'Ankara', 'neurolit-2e56.onrender.com', '15–30 min', '2.37 GB', '805 MB',
    'MRI', 'PET', 'MATLAB · SPM', 'PyTorch Lightning · MONAI', 'Gatherly', 'pg_basebackup',
    '39 ms', '43 ms', '3 ms', 'elif.konak@yahoo.com.tr', 'GitHub ↗', 'LinkedIn ↗',
    'Godetya Yapay Zeka ve Mühendislik, Ankara', 'Bisoft Bilgi Teknolojileri, Ankara',
    'PyTorch, PyTorch Lightning, MONAI, scikit-learn, NumPy, pandas.',
    'Python, FastAPI, PostgreSQL with pgvector, ONNX Runtime, Docker, GitHub Actions',
    'Python, Ollama, JSON Schema, Pydantic, asyncio, pandas',
}

T = {
    'Skip to selected work': 'Seçili çalışmalara geç',
    'Intro': 'Giriş',
    'Work': 'Projeler',
    'Experience': 'Deneyim',
    'Contact': 'İletişim',
    'Machine learning engineer': 'Makine öğrenmesi mühendisi',
    'Open to junior ML and backend roles': 'Junior ML ve backend rollerine açığım',
    'Ankara, hybrid or remote · available now': 'Ankara, hibrit ya da uzaktan · hemen başlayabilirim',
    'I build machine learning systems and the backend that keeps them running.':
        'Makine öğrenmesi sistemleri ve onları ayakta tutan backend’i geliştiriyorum.',
    '2026 Computer Engineering graduate, TED University. Recent work: 3D models on brain MRI and PET, a cited search service, and PostgreSQL failover on Kubernetes. Before I decide how something should work, I measure it.':
        'TED Üniversitesi Bilgisayar Mühendisliği, 2026 mezunu. Son işlerim: beyin MRI ve PET üzerinde 3B modeller, kaynak gösteren bir arama servisi ve Kubernetes üzerinde PostgreSQL failover. Bir şeyin nasıl çalışması gerektiğine karar vermeden önce ölçerim.',
    'Ask NeuroLit a question': 'NeuroLit’e bir soru sor',
    'How I built and measured it': 'Nasıl kurdum, nasıl ölçtüm',
    'The live demo runs on a free server, so the first answer can take about a minute.':
        'Canlı demo ücretsiz bir sunucuda çalışıyor; ilk cevap bir dakika kadar sürebilir.',
    'wakes in ~1 min': '~1 dk’da uyanır',
    "A real answer from NeuroLit. It answers from 5,000 PubMed abstracts and cites a paper for every sentence. The medical findings are the papers', not mine.":
        'NeuroLit’ten gerçek bir cevap. 5.000 PubMed özetinden cevap veriyor ve her cümle için bir makale gösteriyor. Tıbbi bulgular makalelere ait, bana değil.',
    'Bisoft · database failover': 'Bisoft · veritabanı failover',
    'under 10 s': '10 sn altı',
    'The standby now takes over by itself instead of being promoted by hand.':
        'Yedek sunucu artık elle devreye alınmak yerine kendiliğinden devralıyor.',
    'Read the case': 'Projeyi oku',
    'NeuroLit · Docker image': 'NeuroLit · Docker imajı',
    'Small enough to run on a free server with 512 MB of memory.':
        '512 MB belleği olan ücretsiz bir sunucuda çalışacak kadar küçük.',
    'Award · Genç Beyinler Yeni Fikirler 2026': 'Ödül · Genç Beyinler Yeni Fikirler 2026',
    '1st': '1.',
    'of 100+ projects': '100’ü aşkın proje arasında',
    "For the Alzheimer's PET and MRI project. Inter-university competition, Turkish Informatics Association (Ankara Branch).":
        'Alzheimer PET ve MRI projesiyle. Üniversiteler arası yarışma, Türkiye Bilişim Derneği (Ankara Şubesi).',
    'For each one: the problem, what I did, what I measured and what it changed.':
        'Her birinde: sorun, ne yaptım, neyi ölçtüm ve bu neyi değiştirdi.',
    'Research · graduation project': 'Araştırma · bitirme projesi',
    "Deep learning on brain PET and MRI for Alzheimer's disease": 'Alzheimer hastalığı için beyin PET ve MRI üzerinde derin öğrenme',
    'Type': 'Tür',
    'University research project and my graduation project': 'Üniversite araştırma projesi ve bitirme projem',
    'When': 'Ne zaman',
    'September 2025 to now': 'Eylül 2025’ten bu yana',
    'Recognition': 'Ödül',
    'First place, Genç Beyinler Yeni Fikirler 2026': 'Birincilik, Genç Beyinler Yeni Fikirler 2026',
    'The project.': 'Proje.',
    "A research team at TED University, working with neurology and nuclear medicine physicians, is applying deep learning to amyloid PET and MRI to support the analysis of Alzheimer's disease. I joined through the Department of Computer Engineering and contribute as a volunteer.":
        'TED Üniversitesi’nde, nöroloji ve nükleer tıp hekimleriyle birlikte çalışan bir araştırma ekibi, Alzheimer hastalığının analizini desteklemek için amiloid PET ve MRI üzerinde derin öğrenme uyguluyor. Projeye Bilgisayar Mühendisliği Bölümü aracılığıyla katıldım ve gönüllü olarak katkı veriyorum.',
    'My part, as an intern.': 'Stajyer olarak benim payım.',
    'My internship at Godetya in January and February 2026 was on this project. I built the imaging data pipeline that takes the scans all the way to training-ready data: downloading and cleaning scans from public research cohorts, matching each MRI with its PET scan and clinical labels, and preprocessing both in MATLAB and SPM (registration, spatial normalisation, intensity standardisation and brain masking). When registration failed on some scans, I traced it to wrong image origins and automated the correction. I documented each stage in reports for the team.':
        'Ocak–Şubat 2026’daki Godetya stajım bu proje üzerineydi. Taramaları eğitime hazır veriye kadar götüren görüntü veri hattını kurdum: herkese açık araştırma kohortlarından taramaları indirip temizlemek, her MRI’ı PET taramasıyla ve klinik etiketleriyle eşleştirmek ve ikisini MATLAB ve SPM ile ön işlemek (çakıştırma, uzaysal normalizasyon, yoğunluk standartlaştırma ve beyin maskeleme). Bazı taramalarda çakıştırma başarısız olunca sebebini yanlış görüntü orijinlerinde buldum ve düzeltmeyi otomatikleştirdim. Her aşamayı ekip için raporlarla belgeledim.',
    'My part, as a volunteer.': 'Gönüllü olarak benim payım.',
    'After the internship, I extended the same pipeline to more public cohorts, and I train and evaluate the 3D models on the prepared data together with the team.':
        'Stajdan sonra aynı veri hattını yeni herkese açık kohortlara genişlettim; hazırlanan veri üzerinde 3B modelleri ekiple birlikte eğitiyor ve değerlendiriyorum.',
    'The pipeline, step by step': 'Veri hattı, adım adım',
    'Pause': 'Durdur',
    'Illustration of the imaging pipeline: collect scans, pair MRI with PET, fix image origins, preprocess, train 3D models, and review results with physicians.':
        'Görüntü veri hattının çizimi: taramaları topla, MRI ile PET’i eşleştir, görüntü orijinlerini düzelt, ön işle, 3B modelleri eğit ve sonuçları hekimlerle gözden geçir.',
    'Public': 'Açık',
    'cohorts': 'kohortlar',
    'Amyloid PET': 'Amiloid PET',
    'Clinical label': 'Klinik etiket',
    'Download, then drop unusable or incomplete scans': 'İndir, kullanılamayan ya da eksik taramaları ayıkla',
    'pair': 'eşle',
    '+ clinical label': '+ klinik etiket',
    'Same participant, one record': 'Aynı katılımcı, tek kayıt',
    'Image origin': 'Görüntü orijini',
    'Off centre, tilted': 'Merkez dışı, eğik',
    'registration fails': 'çakıştırma başarısız',
    'Corrected': 'Düzeltildi',
    'automatically, every scan': 'otomatik, her taramada',
    'Reference point': 'Referans noktası',
    'scan origin': 'tarama orijini',
    'Intensity': 'Yoğunluk',
    'Registration': 'Çakıştırma',
    'Spatial normalisation': 'Uzaysal normalizasyon',
    'Brain masking': 'Beyin maskeleme',
    'Intensity standardisation': 'Yoğunluk standartlaştırma',
    '3D volumes': '3B hacimler',
    '3D model': '3B model',
    'train': 'eğit',
    'validate': 'doğrula',
    'Model output': 'Model çıktısı',
    'Neurology +': 'Nöroloji +',
    'nuclear medicine': 'nükleer tıp',
    "It supports the physicians' analysis. It does not diagnose.": 'Hekimlerin analizini destekler. Teşhis koymaz.',
    'Collect': 'Topla',
    'my part': 'benim payım',
    'Pair': 'Eşleştir',
    'Fix origins': 'Orijin düzelt',
    'Preprocess': 'Ön işle',
    'Train': 'Eğit',
    'Review': 'Gözden geçir',
    'the team': 'ekip',
    'Collect.': 'Topla.',
    'Download MRI, amyloid PET and clinical labels from public research cohorts, then clean them: scans that are incomplete or unusable are dropped before anything else happens.':
        'Herkese açık araştırma kohortlarından MRI, amiloid PET ve klinik etiketleri indir, sonra temizle: eksik ya da kullanılamayan taramalar en başta ayıklanır.',
    'A drawing of the process, not patient data. The methods and results are unpublished, so they stay with the team for now. I am glad to talk about my part in an interview.':
        'Bu, sürecin bir çizimi; hasta verisi değil. Yöntemler ve sonuçlar henüz yayımlanmadığı için şimdilik ekipte kalıyor. Kendi payımı mülakatta anlatmaktan memnuniyet duyarım.',
    'Tools: Python, PyTorch, PyTorch Lightning, MONAI, ResNet3D, Vision Transformers, MATLAB, SPM, NIfTI, DICOM.':
        'Araçlar: Python, PyTorch, PyTorch Lightning, MONAI, ResNet3D, Vision Transformers, MATLAB, SPM, NIfTI, DICOM.',
    'First place among more than 100 projects at Genç Beyinler Yeni Fikirler 2026, an inter-university competition held with the Turkish Informatics Association.':
        'Türkiye Bilişim Derneği ile düzenlenen üniversiteler arası yarışma Genç Beyinler Yeni Fikirler 2026’da 100’ü aşkın proje arasında birincilik.',
    'Personal project': 'Kişisel proje',
    'NeuroLit: answers from neuroimaging papers, with sources': 'NeuroLit: nörogörüntüleme makalelerinden kaynaklı cevaplar',
    'November 2026': 'Kasım 2026',
    'Built with': 'Kullanılanlar',
    'Live demo ↗': 'Canlı demo ↗',
    'Code ↗': 'Kod ↗',
    'The problem.': 'Sorun.',
    "A language model asked about Alzheimer's imaging will answer confidently whether or not it knows. I wanted a tool that answers only from PubMed abstracts and shows which paper every sentence came from.":
        'Alzheimer görüntülemesi sorulan bir dil modeli, bilse de bilmese de kendinden emin cevap verir. Sadece PubMed özetlerinden cevap veren ve her cümlenin hangi makaleden geldiğini gösteren bir araç istedim.',
    'What I built.': 'Ne kurdum.',
    'A retrieval-augmented generation service over 5,000 PubMed abstracts from 2015 to 2026. A question is embedded, the closest passages are found in PostgreSQL, and a language model writes the answer from them. Then the answer is checked: it must match a schema, every sentence must cite a paper, and every cited paper must be one that was actually retrieved. If a check fails, the model gets one more try; if it fails again, the service says it could not answer.':
        '2015–2026 arasından 5.000 PubMed özeti üzerinde çalışan bir RAG (retrieval-augmented generation) servisi. Soru vektöre çevriliyor, en yakın pasajlar PostgreSQL’de bulunuyor ve bir dil modeli cevabı bu pasajlardan yazıyor. Sonra cevap kontrol ediliyor: bir şemaya uymalı, her cümle bir makaleye atıf yapmalı ve atıf yapılan her makale gerçekten getirilenlerden biri olmalı. Kontrol geçmezse model bir kez daha deniyor; yine geçmezse servis cevap veremediğini söylüyor.',
    'What I expected, and what I measured.': 'Ne bekledim, ne ölçtüm.',
    'My plan assumed that combining keyword search with vector search would find the right paper more often. I wrote 30 test questions and measured. The first run said otherwise: keyword search was so weak that it pulled the combined method down. The cause was PostgreSQL\'s built-in ranking, which treats "disease", found in 91% of passages, as just as informative as "gadolinium", found in only 10. I replaced it with a score that gives rare words more weight.':
        'Planım, kelime aramasını vektör aramasıyla birleştirmenin doğru makaleyi daha sık bulacağını varsayıyordu. 30 test sorusu yazdım ve ölçtüm. İlk çalıştırma aksini söyledi: kelime araması o kadar zayıftı ki birleşik yöntemi aşağı çekiyordu. Sebep PostgreSQL’in yerleşik sıralamasıydı: pasajların %91’inde geçen "disease" kelimesini, sadece %10’unda geçen "gadolinium" kadar bilgilendirici sayıyordu. Onu nadir kelimelere daha çok ağırlık veren bir skorla değiştirdim.',
    'Retrieval results on 30 test questions': '30 test sorusunda arama sonuçları',
    'Search method': 'Arama yöntemi',
    'Right paper in top 5': 'Doğru makale ilk 5’te',
    'Mean reciprocal rank': 'Ortalama karşılıklı sıra (MRR)',
    'Search time': 'Arama süresi',
    'Keyword, first version': 'Kelime, ilk sürüm',
    'Combined, first version': 'Birleşik, ilk sürüm',
    'Keyword, rare words weighted': 'Kelime, nadir kelimeler ağırlıklı',
    'Combined, after the fix': 'Birleşik, düzeltmeden sonra',
    'Vector only, kept': 'Sadece vektör, seçilen',
    'For each question: does the paper it was written from come back in the top five? Even after the fix, vector search alone stayed the most accurate and more than ten times faster, so it is the default. The gap is one question in 30, so I stopped there instead of tuning the method to my own test set.':
        'Her soru için: sorunun yazıldığı makale ilk beşte geliyor mu? Düzeltmeden sonra bile tek başına vektör araması en isabetlisi ve on kattan fazla hızlı kaldı; bu yüzden varsayılan o. Fark 30 soruda bir soru, o yüzden yöntemi kendi test setime göre ayarlamak yerine orada durdum.',
    'Fitting it on a free server.': 'Ücretsiz bir sunucuya sığdırmak.',
    'The first Docker image ran the embedding model with PyTorch and weighed 2.37 GB, too much for a server with 512 MB of memory. I switched to ONNX Runtime after checking that both produce identical vectors, so the stored data and the scores above did not change. The image dropped to 805 MB and runs in about 190 MB of memory.':
        'İlk Docker imajı embedding modelini PyTorch ile çalıştırıyordu ve 2,37 GB’tı; 512 MB belleği olan bir sunucu için fazla. İkisinin birebir aynı vektörleri ürettiğini kontrol ettikten sonra ONNX Runtime’a geçtim; böylece kayıtlı veri de yukarıdaki skorlar da değişmedi. İmaj 805 MB’a indi ve yaklaşık 190 MB bellekle çalışıyor.',
    'Result.': 'Sonuç.',
    'On the same 30 questions, 28 got a cited answer. None reached the user with an uncited sentence or a source that had not been retrieved. The project has 60 tests at 84% coverage, and GitHub Actions runs them against a real PostgreSQL database before publishing the image.':
        'Aynı 30 sorunun 28’i kaynaklı bir cevap aldı. Hiçbiri kullanıcıya kaynaksız bir cümleyle ya da getirilmemiş bir kaynakla ulaşmadı. Projede %84 kapsama ile 60 test var; GitHub Actions imajı yayımlamadan önce bunları gerçek bir PostgreSQL veritabanına karşı çalıştırıyor.',
    'Internship · Bisoft, Ankara': 'Staj · Bisoft, Ankara',
    'A database that takes over by itself': 'Kendiliğinden devralan bir veritabanı',
    'Role': 'Rol',
    'Backend and DevOps intern': 'Backend ve DevOps stajyeri',
    'July to August 2025': 'Temmuz–Ağustos 2025',
    'PostgreSQL, Docker, Kubernetes, Bash': 'PostgreSQL, Docker, Kubernetes, Bash',
    'When the primary PostgreSQL server failed, someone had to notice, connect and promote the standby by hand. That took 15 to 30 minutes, and the application was down the whole time.':
        'Ana PostgreSQL sunucusu çöktüğünde birinin bunu fark etmesi, bağlanması ve yedek sunucuyu elle devreye alması gerekiyordu. Bu 15–30 dakika sürüyordu ve uygulama bu süre boyunca kapalı kalıyordu.',
    'What I did.': 'Ne yaptım.',
    'I built a primary and standby pair kept in sync with WAL streaming replication, with the standby created automatically by':
        'WAL streaming replication ile eşzamanlı tutulan bir ana–yedek sunucu çifti kurdum; yedek sunucu',
    "and the setup scripted in Bash. I then moved the cluster to Kubernetes (StatefulSets, persistent volumes, ConfigMaps, Secrets and a headless Service) and connected it to the company's existing failover tools. I did not write those tools; my part was making the cluster work with them and testing failover end to end, again and again.":
        'ile otomatik oluşturuluyor, kurulum Bash ile betikleniyor. Sonra kümeyi Kubernetes’e taşıdım (StatefulSet’ler, kalıcı birimler, ConfigMap’ler, Secret’lar ve headless Service) ve şirketin mevcut failover araçlarına bağladım. O araçları ben yazmadım; benim payım kümenin onlarla çalışmasını sağlamak ve failover’ı uçtan uca, tekrar tekrar test etmekti.',
    'By hand': 'Elle',
    '15 to 30 minutes': '15–30 dakika',
    'Automated': 'Otomatik',
    'under 10 seconds': '10 saniyenin altında',
    '10 min': '10 dk',
    '20 min': '20 dk',
    '30 min': '30 dk',
    'Drawn to scale. The darker half of the top bar is the best case, 15 minutes. At this scale, 10 seconds is the thin line inside the highlight.':
        'Ölçekli çizim. Üst çubuğun koyu yarısı en iyi durum, 15 dakika. Bu ölçekte 10 saniye, vurgunun içindeki ince çizgi.',
    'Labelling product data with a local language model': 'Yerel bir dil modeliyle ürün verisi etiketleme',
    'An ingredient-safety checker needs labelled data: thousands of real ingredient lists, each marked safe or harmful. Labelling them by hand was not realistic, and sending them to a cloud model was not an option.':
        'Bir içerik güvenliği denetleyicisi etiketli veriye ihtiyaç duyar: her biri güvenli ya da zararlı olarak işaretlenmiş binlerce gerçek içerik listesi. Bunları elle etiketlemek gerçekçi değildi, buluttaki bir modele göndermek de seçenek değildi.',
    'I built the labelling pipeline. It downloads the OpenFoodFacts and OpenBeautyFacts product dumps, several gigabytes each, and reads them in 100,000-row chunks so memory stays low. Each cleaned ingredient list goes to a Mistral model served by Ollama on the same machine, several requests at a time, and the model must answer in a fixed JSON format. Every answer is checked against a schema before it counts as a label.':
        'Etiketleme hattını kurdum. Her biri birkaç gigabayt olan OpenFoodFacts ve OpenBeautyFacts ürün dökümlerini indiriyor ve bellek düşük kalsın diye 100.000 satırlık parçalar hâlinde okuyor. Temizlenen her içerik listesi, aynı makinede Ollama ile çalışan bir Mistral modeline aynı anda birden çok istekle gidiyor ve model sabit bir JSON formatında cevap vermek zorunda. Her cevap etiket sayılmadan önce bir şemaya göre kontrol ediliyor.',
    'Product dumps': 'Ürün dökümleri',
    'OpenFoodFacts and OpenBeautyFacts, read in chunks': 'OpenFoodFacts ve OpenBeautyFacts, parça parça okunur',
    'Cleaning and balancing': 'Temizleme ve dengeleme',
    'duplicates and very short lists removed': 'tekrarlar ve çok kısa listeler çıkarılır',
    'Mistral on Ollama, on the same machine': 'Ollama üzerinde Mistral, aynı makinede',
    'asked for a fixed JSON format, requests in parallel': 'sabit JSON formatı istenir, istekler paralel',
    'Schema validation': 'Şema doğrulaması',
    'an answer that fails is recorded as an error, never as a label': 'geçemeyen cevap hata olarak kaydedilir, asla etiket olarak değil',
    'Labelled dataset': 'Etiketli veri seti',
    "The labelling pipeline. The validation step is the point of the design: the model's output is treated as untrusted input until it passes the schema.":
        'Etiketleme hattı. Tasarımın özü doğrulama adımı: modelin çıktısı şemadan geçene kadar güvenilmeyen girdi sayılır.',
    'Smaller projects': 'Daha küçük projeler',
    'Real-time chat with servers, channels, voice rooms and roles. Node.js, Socket.IO, WebRTC, MongoDB.':
        'Sunucular, kanallar, sesli odalar ve rollerle gerçek zamanlı sohbet. Node.js, Socket.IO, WebRTC, MongoDB.',
    'Open the app': 'Uygulamayı aç',
    'Spades, multiplayer': 'Batak, çok oyunculu',
    'Four-player card game over WebSockets. The server holds the game state and rejects illegal moves, so a modified client cannot cheat.':
        'WebSocket üzerinden dört kişilik kart oyunu. Oyun durumunu sunucu tutuyor ve kurala aykırı hamleleri reddediyor; değiştirilmiş bir istemci hile yapamıyor.',
    'Play it': 'Oyna',
    'or': 'ya da',
    'read the code': 'koda bak',
    'Cargo delivery simulation': 'Kargo dağıtım simülasyonu',
    'Packages moving between cities in Java, on a stack, queue and linked list written from scratch, checked against four test scenarios.':
        'Java’da şehirler arasında taşınan paketler; sıfırdan yazılmış yığın, kuyruk ve bağlı liste üzerinde, dört test senaryosuyla doğrulanmış.',
    'Read the code': 'Koda bak',
    'Research, two internships and a degree taught in English.': 'Araştırma, iki staj ve İngilizce eğitimli bir lisans.',
    'Sep 2025 – now': 'Eyl 2025 – devam',
    'AI/ML research contributor, volunteer': 'AI/ML araştırma katkısı, gönüllü',
    'TED University research project, Ankara': 'TED Üniversitesi araştırma projesi, Ankara',
    "Extended the internship's data pipeline to more public cohorts, and train and evaluate the 3D models, for the Alzheimer's project above.":
        'Yukarıdaki Alzheimer projesi için stajdaki veri hattını yeni herkese açık kohortlara genişlettim; 3B modelleri eğitiyor ve değerlendiriyorum.',
    'Jan – Feb 2026': 'Oca – Şub 2026',
    'Software engineering intern, R&amp;D': 'Yazılım mühendisliği stajyeri, Ar-Ge',
    "The internship was on the same Alzheimer's project. I built its data pipeline, from public cohort scans to training-ready data (MRI–PET pairing, MATLAB and SPM preprocessing), and documented it in reports.":
        'Staj aynı Alzheimer projesi üzerineydi. Projenin veri hattını, herkese açık kohort taramalarından eğitime hazır veriye kadar kurdum (MRI–PET eşleştirme, MATLAB ve SPM ile ön işleme) ve raporlarla belgeledim.',
    'Jul – Aug 2025': 'Tem – Ağu 2025',
    'PostgreSQL high availability on Kubernetes, described above.': 'Kubernetes üzerinde PostgreSQL yüksek erişilebilirlik; yukarıda anlatıldı.',
    'B.Sc. in Computer Engineering': 'Bilgisayar Mühendisliği, lisans',
    'TED University, Ankara. Taught in English.': 'TED Üniversitesi, Ankara. Eğitim dili İngilizce.',
    'Courses closest to my work: Information Retrieval, Artificial Intelligence, Data Structures and Algorithms, Signals and Systems.':
        'İşime en yakın dersler: Bilgi Erişimi, Yapay Zekâ, Veri Yapıları ve Algoritmalar, Sinyaller ve Sistemler.',
    'Tools used in the work above': 'Yukarıdaki işlerde kullandığım araçlar',
    'Machine learning': 'Makine öğrenmesi',
    'LLMs and retrieval': 'LLM’ler ve bilgi erişimi',
    'RAG, LLM output validation (Pydantic, JSON Schema), embeddings, pgvector, hybrid search (IDF-weighted keyword + vector, RRF), retrieval evaluation (Recall@5, MRR), Groq, Ollama.':
        'RAG, LLM çıktı doğrulama (Pydantic, JSON Schema), embedding’ler, pgvector, hibrit arama (IDF ağırlıklı kelime + vektör, RRF), arama değerlendirmesi (Recall@5, MRR), Groq, Ollama.',
    'Medical imaging': 'Tıbbi görüntüleme',
    'PET, MRI, DICOM, NIfTI, nibabel, MATLAB and SPM, image registration.': 'PET, MRI, DICOM, NIfTI, nibabel, MATLAB ve SPM, görüntü çakıştırma.',
    'Backend and infrastructure': 'Backend ve altyapı',
    'Python, FastAPI, REST APIs, Java and Spring, SQL, PostgreSQL, Docker, Kubernetes, Git, GitHub Actions, pytest, Bash, Linux.':
        'Python, FastAPI, REST API’ler, Java ve Spring, SQL, PostgreSQL, Docker, Kubernetes, Git, GitHub Actions, pytest, Bash, Linux.',
    'Languages': 'Diller',
    'Turkish (native), English (B2), French (B2).': 'Türkçe (ana dil), İngilizce (B2), Fransızca (B2).',
    'Say hello': 'Merhaba de',
    'Email is the fastest way to reach me. I send my CV directly to each company, so if you would like it, just ask.':
        'Bana en hızlı e-postayla ulaşırsınız. CV’mi her şirkete doğrudan gönderiyorum; isterseniz yazmanız yeterli.',
    'Elif Konak · Ankara · 2026': 'Elif Konak · Ankara · 2026',
}

ATTR = [  # (english, turkish) for attribute values and head tags; each must exist
    ('<html lang="en">', '<html lang="tr">'),
    ('<title>Elif Konak, machine learning engineer</title>', '<title>Elif Konak, makine öğrenmesi mühendisi</title>'),
    ('content="Elif Konak, machine learning engineer"', 'content="Elif Konak, makine öğrenmesi mühendisi"'),
    ('<meta name="description" content="Machine learning and backend engineer in Ankara. ML systems, retrieval and reliable infrastructure. TED University, 2026." />',
     '<meta name="description" content="Ankara’da makine öğrenmesi ve backend mühendisi. ML sistemleri, bilgi erişimi ve güvenilir altyapı. TED Üniversitesi, 2026." />'),
    ('<meta property="og:description" content="Machine learning and backend engineer in Ankara. ML systems, retrieval and reliable infrastructure. TED University, 2026." />',
     '<meta property="og:description" content="Ankara’da makine öğrenmesi ve backend mühendisi. ML sistemleri, bilgi erişimi ve güvenilir altyapı. TED Üniversitesi, 2026." />'),
    ('<meta name="twitter:description" content="Machine learning and backend engineer in Ankara. ML systems, retrieval and reliable infrastructure." />',
     '<meta name="twitter:description" content="Ankara’da makine öğrenmesi ve backend mühendisi. ML sistemleri, bilgi erişimi ve güvenilir altyapı." />'),
    ('<meta property="og:url" content="https://elifkk14.github.io/" />', '<meta property="og:url" content="https://elifkk14.github.io/tr/" />\n<meta property="og:locale" content="tr_TR" />'),
    ('href="assets/', 'href="../assets/'), ('src="assets/', 'src="../assets/'),
    ('href="fonts/', 'href="../fonts/'), ('src="images/', 'src="../images/'), ('srcset="images/', 'srcset="../images/'),
    ('alt="NeuroLit answering whether FDG-PET can distinguish Alzheimer\'s disease from frontotemporal dementia, with numbered citations and PubMed sources listed below"',
     'alt="NeuroLit’in FDG-PET’in Alzheimer hastalığını frontotemporal demanstan ayırıp ayıramayacağı sorusuna verdiği cevap; numaralı atıflar ve altta PubMed kaynakları"'),
    ('alt="Elif Konak receiving the first-place award at Genç Beyinler Yeni Fikirler 2026"', 'alt="Elif Konak, Genç Beyinler Yeni Fikirler 2026’da birincilik ödülünü alırken"'),
    ('aria-label="Open the NeuroLit live demo"', 'aria-label="NeuroLit canlı demosunu aç"'),
    ('aria-label="Highlights from the projects below"', 'aria-label="Aşağıdaki projelerden öne çıkanlar"'),
    ('aria-label="Sections"', 'aria-label="Bölümler"'),
    ('aria-label="Main"', 'aria-label="Ana menü"'),
    ('aria-label="Previous step"', 'aria-label="Önceki adım"'),
    ('aria-label="Next step"', 'aria-label="Sonraki adım"'),
    ('aria-label="Time until the standby takes over: 15 to 30 minutes by hand, under 10 seconds automated, drawn to scale."', 'aria-label="Yedek sunucunun devralma süresi: elle 15–30 dakika, otomatik 10 saniyenin altında, ölçekli çizim."'),
    ('<li class="lang"><a href="tr/" hreflang="tr" lang="tr" aria-label="Türkçe">TR</a></li>', '<li class="lang"><a href="../" hreflang="en" lang="en" aria-label="English">EN</a></li>'),
]

s = open(SRC, encoding="utf-8").read()
for a, b in ATTR:
    if a not in s:
        sys.exit(f"missing attr: {a[:70]}")
    s = s.replace(a, b)

head_end = s.index("<body")
head, body = s[:head_end], s[head_end:]
missing = []

def sub(m):
    raw = m.group(1)
    t = raw.strip()
    if not t or t in KEEP or not re.search(r"[A-Za-z]", t):
        return m.group(0)
    if t in T:
        return ">" + raw.replace(t, T[t]) + "<"
    missing.append(t)
    return m.group(0)

# translate text nodes outside <script>
parts = re.split(r"(<script.*?</script>)", body, flags=re.S)
for i in range(0, len(parts), 2):
    parts[i] = re.sub(r">([^<>]+)<", sub, parts[i])
body = "".join(parts)

# remaining aria-labels / titles in body: report English ones
for m in re.finditer(r'(aria-label|title|alt)="([^"]*[A-Za-z][^"]*)"', body):
    if re.search(r"\b(the|and|of|to|Open|Play|Pause|Next|Previous|step)\b", m.group(2)):
        missing.append(f"ATTR {m.group(1)}: {m.group(2)}")

if missing:
    print("UNMAPPED:")
    for x in dict.fromkeys(missing):
        print(" ", repr(x))
open(DST, "w", encoding="utf-8").write(head + body)
print("wrote", DST)
