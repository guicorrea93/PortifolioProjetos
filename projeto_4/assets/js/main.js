
function setStickyHeights(){
  const ps = document.querySelector('.part-switcher');
  if(ps){
    document.documentElement.style.setProperty('--part-switch-h', `${ps.offsetHeight}px`);
  }
}

function scrollToTopInstant(){
  // garante que o header não fique “cortado” ao alternar as partes
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
}

function clearHash(){
  // evita que a troca de Parte 1/2 “ancore” no meio da página
  try {
    history.replaceState(null, '', window.location.pathname + window.location.search);
  } catch(e) {}
}

function showPart(n){
  const p1=document.getElementById('parte1');
  const p2=document.getElementById('parte2');
  const b1=document.getElementById('btnParte1');
  const b2=document.getElementById('btnParte2');

  if(n===1){
    p1.classList.add('active');
    p2.classList.remove('active');
    b1.classList.add('active');
    b2.classList.remove('active');
  } else {
    p2.classList.add('active');
    p1.classList.remove('active');
    b2.classList.add('active');
    b1.classList.remove('active');
  }

  // Atualiza alturas sticky e volta pro topo (sem cortar o cabeçalho)
  setStickyHeights();
  clearHash();
  // usa rAF pra garantir que o DOM já refletiu o display:none/block
  requestAnimationFrame(() => {
    scrollToTopInstant();
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  setStickyHeights();
  window.addEventListener('resize', setStickyHeights);
  showPart(1);
});


/* ===== Parte 1 ===== */

        function toggleNavP1() {
            const navMenu = document.getElementById('p1_navMenu');
            navMenu.classList.toggle('active');
        }

        // Smooth scroll
        document.querySelectorAll('#p1_navMenu a').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                if (window.innerWidth <= 768) {
                    document.getElementById('p1_navMenu').classList.remove('active');
                }
            });
        });

        // Active navigation highlight
        window.addEventListener('scroll', () => {
            const sections = document.querySelectorAll('#parte1 .card[id]');
            const navLinks = document.querySelectorAll('#p1_navMenu a');
            
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (pageYOffset >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.style.background = '';
                link.style.color = '';
                link.style.borderColor = '';
                if (link.getAttribute('href') === `#${current}`) {
                    link.style.background = 'var(--highlight)';
                    link.style.color = 'white';
                    link.style.borderColor = 'var(--highlight)';
                }
            });
        });

        console.log('🔍 Rossmann Sales - Parte 1 Loaded!');
        console.log('📊 Data processed: 1M+ records | 30 features ready');
    

/* ===== Parte 2 ===== */

        // Toggle mobile navigation
        function toggleNavP2() {
            const navMenu = document.getElementById('p2_navMenu');
            navMenu.classList.toggle('active');
        }

        // Close menu when clicking a link (mobile)
        document.querySelectorAll('#p2_navMenu a').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu
                if (window.innerWidth <= 768) {
                    document.getElementById('p2_navMenu').classList.remove('active');
                }
            });
        });

        // Animation for progress bars
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const fills = entry.target.querySelectorAll('.progress-fill');
                    fills.forEach(fill => {
                        const width = fill.style.width;
                        fill.style.width = '0%';
                        setTimeout(() => {
                            fill.style.width = width;
                        }, 100);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.card').forEach(card => {
            observer.observe(card);
        });

        // Active navigation highlight
        window.addEventListener('scroll', () => {
            const sections = document.querySelectorAll('#parte2 .card[id]');
            const navLinks = document.querySelectorAll('#p2_navMenu a');
            
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (pageYOffset >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.style.background = '';
                link.style.color = '';
                link.style.borderColor = '';
                if (link.getAttribute('href') === `#${current}`) {
                    link.style.background = 'var(--highlight)';
                    link.style.color = 'white';
                    link.style.borderColor = 'var(--highlight)';
                }
            });
        });

        console.log('🎉 Rossmann Sales Prediction Report Loaded!');
        console.log('📊 Modelo: XGBoost | R²: 0.9612 | RMSE: €685.42');
    