(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  /* motion while scrolling: add .in when an element comes into view */
  var anim = document.documentElement.classList.contains('anim');
  function stagger(list){ Array.prototype.forEach.call(list, function(el, i){ el.style.setProperty('--i', i); }); }
  stagger(document.querySelectorAll('.stats > li'));
  document.querySelectorAll('.kids').forEach(function(k){ stagger(k.children); });
  document.querySelectorAll('.tbl tbody tr').forEach(function(tr, i){ tr.style.setProperty('--i', i); });
  document.querySelectorAll('.flow').forEach(function(f){ stagger(f.children); });
  if (anim) {
    var rio = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -12% 0px'});
    document.querySelectorAll('.rv,.kids,.display,.rv-head,.bars,.tbl,.flow,.stats > li').forEach(function(el){ rio.observe(el); });

    /* thin reading-progress line at the top */
    var bar = document.querySelector('.progress'), ticking = false;
    function prog(){ ticking = false; var h = document.documentElement.scrollHeight - innerHeight; bar.style.setProperty('--sp', h > 0 ? Math.min(1, scrollY / h) : 0); }
    addEventListener('scroll', function(){ if (!ticking) { ticking = true; requestAnimationFrame(prog); } }, {passive:true});
    prog();
  }

  /* side rail: highlight the section in view */
  var links = document.querySelectorAll('.rail a');
  if (hasIO && links.length) {
    var map = {};
    links.forEach(function(a){ map[a.dataset.sec] = a; });
    var sio = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (e.isIntersecting) {
          links.forEach(function(a){ a.classList.remove('is-on'); a.removeAttribute('aria-current'); });
          var a = map[e.target.id]; if (a) { a.classList.add('is-on'); a.setAttribute('aria-current','true'); }
        }
      });
    }, {rootMargin:'-45% 0px -50% 0px'});
    ['top','work','experience','contact'].forEach(function(id){ var el = document.getElementById(id); if (el) sio.observe(el); });
  }

  /* Alzheimer's pipeline */
  var fig = document.getElementById('pipe');
  if (!fig) return;
  fig.classList.add('js');
  var scenes = fig.querySelectorAll('.scene');
  var btns = fig.querySelectorAll('.steps button');
  var text = fig.querySelector('.step-text');
  var playBtn = fig.querySelector('[data-act="play"]');
  var COPY = {};
  COPY.en = [
    '<b>Collect.</b> Download MRI, amyloid PET and clinical labels from public research cohorts, then clean them: scans that are incomplete or unusable are dropped before anything else happens.',
    '<b>Pair.</b> Match each MRI with the PET scan and clinical label of the same participant, so every record the model sees is complete and consistent.',
    '<b>Fix origins.</b> Registration failed on some scans. I traced it to wrong image origins and automated the correction, so no scan has to be fixed by hand.',
    '<b>Preprocess.</b> Register PET to MRI, normalise both to a common brain space, mask out everything that is not brain and standardise intensities, in MATLAB and SPM.',
    '<b>Train.</b> Feed the prepared 3D volumes to deep learning models, then train and evaluate them with PyTorch Lightning and MONAI.',
    '<b>Review.</b> Results go back to the research team and the neurology and nuclear medicine physicians. The model supports their analysis; it does not diagnose.'
  ];
  COPY.tr = [
    '<b>Topla.</b> Herkese açık araştırma kohortlarından MRI, amiloid PET ve klinik etiketleri indir, sonra temizle: eksik ya da kullanılamayan taramalar en başta ayıklanır.',
    '<b>Eşleştir.</b> Her MRI\'ı aynı katılımcının PET taramasıyla ve klinik etiketiyle eşleştir; böylece modelin gördüğü her kayıt eksiksiz ve tutarlı olur.',
    '<b>Orijinleri düzelt.</b> Bazı taramalarda çakıştırma başarısız oluyordu. Sebebi yanlış görüntü orijinleriydi; düzeltmeyi otomatikleştirdim, hiçbir taramanın elle düzeltilmesi gerekmiyor.',
    '<b>Ön işle.</b> PET\'i MRI\'a çakıştır, ikisini ortak bir beyin uzayına normalize et, beyin dışındaki her şeyi maskele ve yoğunlukları standartlaştır; MATLAB ve SPM ile.',
    '<b>Eğit.</b> Hazırlanan 3B hacimleri derin öğrenme modellerine ver, sonra PyTorch Lightning ve MONAI ile eğit ve değerlendir.',
    '<b>Gözden geçir.</b> Sonuçlar araştırma ekibine ve nöroloji ile nükleer tıp hekimlerine döner. Model onların analizini destekler; teşhis koymaz.'
  ];
  var TR = document.documentElement.lang === 'tr';
  var copy = TR ? COPY.tr : COPY.en;
  var DUR = 5200, step = 0, playing = !reduce, visible = false, t0 = 0, last = performance.now();

  function show(i){
    step = (i + scenes.length) % scenes.length;
    scenes.forEach(function(s){ s.classList.remove('on'); });
    void fig.offsetWidth;                       /* restart the scene's animations */
    scenes[step].classList.add('on');
    btns.forEach(function(b, k){
      b.classList.toggle('is-on', k === step);
      b.classList.toggle('done', k < step);
      if (k === step) b.setAttribute('aria-current','step'); else b.removeAttribute('aria-current');
      b.style.setProperty('--p', reduce || !playing ? 1 : 0);
    });
    text.innerHTML = copy[step];
    t0 = performance.now();
  }
  /* progress only moves while playing and on screen; otherwise the clock is held */
  function tick(now){
    requestAnimationFrame(tick);
    var dt = now - last; last = now;
    if (!playing || !visible) { t0 += dt; return; }
    var p = Math.min(1, (now - t0) / DUR);
    btns[step].style.setProperty('--p', p);
    if (p >= 1) show(step + 1);
  }
  function setPlaying(v){
    playing = v;
    playBtn.setAttribute('aria-pressed', v ? 'true' : 'false');
    playBtn.querySelector('span').textContent = v ? (TR ? 'Durdur' : 'Pause') : (TR ? 'Oynat' : 'Play');
  }

  btns.forEach(function(b){ b.addEventListener('click', function(){ setPlaying(false); show(+b.dataset.go); }); });
  fig.querySelector('[data-act="prev"]').addEventListener('click', function(){ setPlaying(false); show(step - 1); });
  fig.querySelector('[data-act="next"]').addEventListener('click', function(){ setPlaying(false); show(step + 1); });
  playBtn.addEventListener('click', function(){ setPlaying(!playing); });

  if (hasIO) {
    var first = true;
    new IntersectionObserver(function(es){
      visible = es[0].isIntersecting;
      if (visible && first) { first = false; show(step); }   /* start the scene when it is first seen */
    }, {threshold:.35}).observe(fig);
  } else { visible = true; }
  setPlaying(playing);
  show(0);
  requestAnimationFrame(tick);
})();
