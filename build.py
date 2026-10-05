import re
#!/usr/bin/env python3
"""Builds the bilingual Polish Matchmaker site (English at /, Polish at /pl/).
Run:  python3 build.py        (rewrites all HTML pages, sitemap and robots.txt)
Edit the copy below, re-run, commit the result to GitHub.
"""
import json, os, html

# ------------------------------------------------------------------ CONFIG
DOMAIN   = "https://polishmatchmaker.com"
EMAIL    = "hello@sparkedconnection.com"
SC_URL   = "https://sparkedconnection.com/"
ENQUIRY  = "https://sparkedconnection.com/enquiry/"
PLANS    = "https://sparkedconnection.com/plans/"
EVENTS   = "https://sparkedconnection.com/#events"
PRIVACY  = "https://sparkedconnection.com/privacy-notice"
TERMS    = "https://sparkedconnection.com/terms-and-conditions"
REFUND   = "https://sparkedconnection.com/refund-cancellation-policy"
ACCESS   = "https://sparkedconnection.com/accessibility-statement"
ABIA     = "https://abia.org.uk/"
INSTA    = "https://www.instagram.com/sparked_connection/"
FB       = "https://www.facebook.com/people/Sparked-Connection/61584598310374/"
LI       = "https://www.linkedin.com/company/sparked-connection"
PHOTO    = "https://sparkedconnection.com/anna-matchmaker.jpg"   # or put a copy at /assets/anna.jpg and use that path
GA_ID    = ""   # e.g. "G-XXXXXXXXXX" - leave empty until you create a GA4 property; no cookie banner/analytics loads while empty
COMPANY  = "Sparked Connection Ltd"
CO_NO    = "16967307"
ICO      = "ZC080494"
REG_ADDR = "[REGISTERED OFFICE ADDRESS - REQUIRED BEFORE GOING LIVE]"

LOGO_W, LOGO_H = 875, 300
STK_W, STK_H = 891, 400
ROOT = os.path.dirname(os.path.abspath(__file__))

# key -> (pl path, en path)
URLS = {
    "home":    ("/pl/",               "/"),
    "how":     ("/pl/jak-to-dziala/", "/how-it-works/"),
    "offer":   ("/pl/oferta/",        "/services/"),
    "about":   ("/pl/o-mnie/",        "/about/"),
    "contact": ("/pl/kontakt/",       "/contact/"),
}
NAV = {
    "pl": [("home","Strona główna"),("how","Jak to działa"),("offer","Oferta"),("about","O mnie"),("articles","Artykuły"),("contact","Kontakt")],
    "en": [("home","Home"),("how","How it works"),("offer","Services"),("about","About"),("articles","Articles"),("contact","Contact")],
}
def url(key, lang): return URLS[key][0 if lang == "pl" else 1]
def esc(s): return html.escape(s, quote=True)

SPARK = ('<svg viewBox="0 0 36 36" fill="none" aria-hidden="true"><circle cx="18" cy="18" r="16" stroke="rgba(230,169,97,.55)"/>'
         '<circle cx="13" cy="15" r="3.6" fill="#CE7E98"/><circle cx="23" cy="15" r="3.6" fill="#E6A961"/>'
         '<path d="M9 26c1-4 4-6.2 9-6.2s8 2.2 9 6.2" stroke="#E6A961" stroke-width="1.8" stroke-linecap="round"/></svg>')

FLAG_PL = '<svg class="flag" viewBox="0 0 16 10" role="img" aria-label="Polska"><rect width="16" height="5" fill="#fff"/><rect y="5" width="16" height="5" fill="#DC143C"/></svg>'
FLAG_GB = ('<svg class="flag" viewBox="0 0 60 30" role="img" aria-label="United Kingdom"><clipPath id="fs"><path d="M0,0v30h60V0z"/></clipPath><clipPath id="ft"><path d="M30,15h30v15zv15h-30zh-30v-15zv-15h30z"/></clipPath>'
           '<g clip-path="url(#fs)"><path d="M0,0v30h60V0z" fill="#012169"/><path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0L60,30M60,0L0,30" clip-path="url(#ft)" stroke="#C8102E" stroke-width="4"/>'
           '<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/><path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></g></svg>')

def partner(lang, light=False):
    eb = "W partnerstwie z" if lang == "pl" else "In Partnership with"
    return (f'<a class="partner" href="{SC_URL}" target="_blank" rel="noopener" aria-label="{eb} Sparked Connection">'
            f'<span class="pe">{eb}</span><img src="/assets/sparked-logo-white.svg" alt="Sparked Connection" width="702" height="355"></a>')

# ------------------------------------------------------------------ COPY
def faq_items(l):
    P = l == "pl"
    return [
      ("Czy muszę mówić po polsku?" if P else "Do I need to speak Polish?",
       "Nie. Rozmowy prowadzę po polsku lub po angielsku. Osoby o polskich korzeniach, wychowane w Wielkiej Brytanii, są tak samo mile widziane."
       if P else "No. I hold consultations in Polish or English. People with Polish roots who grew up in the UK are just as welcome."),
      ("Czy poznam wyłącznie osoby polskiego pochodzenia?" if P else "Will I only meet people of Polish background?",
       "Jeśli jest to dla Pana/Pani ważne, uwzględniam to w dopasowaniu. Jeśli jest Pan/Pani otwarta lub otwarty na szersze grono, mogę skorzystać z całej sieci Sparked Connection. Podczas rozmowy szczerze powiem, jak wygląda aktualna sieć w Pana/Pani regionie, bez składania obietnic, których nie mogę dotrzymać."
       if P else "If that matters to you, I take it into account when matching. If you are open to a wider circle, I can draw on the whole Sparked Connection network. During our conversation I will be honest about what the network currently looks like in your area, without making promises I cannot keep."),
      ("Ile to kosztuje?" if P else "How much does it cost?",
       "Rozmowa wstępna jest bezpłatna i niezobowiązująca. Członkostwo Bronze (dostęp do Singles Network) jest bezpłatne, a pakiety Gold i Platinum są płatne. Szczegóły znajdzie Pan/Pani na stronie Oferta."
       if P else "The initial consultation is free and without obligation. Bronze membership (access to the Singles Network) is free, while Gold and Platinum are paid packages. You will find the details on the Services page."),
      ("Czy moje dane są poufne?" if P else "Is my information kept private?",
       "Tak. Dane są traktowane dyskretnie i nigdy nie są udostępniane bez Pana/Pani zgody. Matchmaking jest procesem bardzo osobistym, a poufność jest fundamentem mojej pracy."
       if P else "Yes. Your details are handled discreetly and are never shared without your consent. Matchmaking is a personal process, and confidentiality is core to how I work."),
      ("Czy działa Pani tylko w Londynie?" if P else "Do you only work in London?",
       "Pracuję z osobami z Londynu i z całej Wielkiej Brytanii. Chętnie ustalimy dogodną formę pierwszej rozmowy."
       if P else "I work with people in London and across the whole of the UK. We can agree whichever format suits you best for the first conversation."),
      ("Jak wygląda pierwsza rozmowa?" if P else "What is the first conversation like?",
       "To spokojna, poufna rozmowa jeden na jeden, bez presji. Poznajemy Pana/Pani wartości, styl życia i to, jak wygląda dla Pana/Pani dobry związek. Dopiero potem wspólnie decydujemy, czy i jak działać dalej."
       if P else "A calm, confidential one-to-one conversation with no pressure. We talk about your values, your lifestyle and what a good relationship looks like to you. Only then do we decide together whether and how to go further."),
    ]

def faq_html(l):
    out = '<div class="faq">'
    for q, a in faq_items(l):
        out += f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
    return out + '</div>'

def cta(l, h2=None, p=None):
    P = l == "pl"
    h2 = h2 or ("Czas poznać właściwą osobę" if P else "Time to meet the right person")
    p = p or ("Pierwsza rozmowa jest bezpłatna, poufna i niezobowiązująca." if P else "Your first conversation is free, confidential and without obligation.")
    btn = "Umów bezpłatną rozmowę" if P else "Book a free consultation"
    sp = "Bezpłatna rozmowa · Bez zobowiązań · Pełna poufność" if P else "Free consultation · No commitment · Complete confidentiality"
    return (f'<section class="cta"><div class="wrap"><h2>{h2}</h2><p>{p}</p>'
            f'<div class="btns"><a class="btn btn-gold" href="{url("contact", l)}">{btn}</a></div>'
            f'<div class="small-print">{sp}</div></div></section>')

def band(l):
    P = l == "pl"
    return f'''<section class="band"><div class="wrap">
<span class="eyebrow">{"Zaufanie i przejrzystość" if P else "Trust and transparency"}</span>
<h2>{"W partnerstwie z Sparked Connection" if P else "In partnership with Sparked Connection"}</h2>
<p>{("Dobrani (Polish Matchmaker) działa w ramach Sparked Connection Ltd, brytyjskiej agencji matchmakingowej zarejestrowanej i zatwierdzonej przez ABIA. Dzięki temu ma Pan/Pani dostęp do sprawdzonych procesów, wydarzeń i szerszej sieci singli, a jednocześnie osobiste, polskojęzyczne podejście."
     if P else "Dobrani (Polish Matchmaker) operates as part of Sparked Connection Ltd, a UK matchmaking agency registered and approved by ABIA. That means access to established processes, events and a wider network of singles, together with a personal, Polish-speaking approach.")}</p>
{partner(l, light=True)}
</div></section>'''

def body_home(l):
    P = l == "pl"
    t = lambda pl, en: pl if P else en
    hero = f'''<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow">{FLAG_PL}{t("Polska swatka · Londyn i cała Wielka Brytania","Polish matchmaker · London and the whole UK")}</span>
<div class="hero-pw"><a class="pw" href="{SC_URL}" target="_blank" rel="noopener" aria-label="{t("W partnerstwie z","In Partnership with")} Sparked Connection"><span>{t("W partnerstwie z","In Partnership with")}</span><img src="/assets/sparked-badge.svg" alt="Sparked Connection" width="48" height="48"></a></div>
<h1>{t("Polska swatka w Londynie i w całej Wielkiej Brytanii","Polish matchmaking in London and across the UK")}</h1>
<p class="lead">{t("Prywatny, osobisty matchmaking dla osób, które szukają poważnego związku. Rozmowa po polsku lub po angielsku, bez aplikacji i bez przypadkowych randek.",
                   "Private, personal matchmaking for people looking for a serious relationship. Your consultation in Polish or English, with no apps and no random dates.")}</p>
<div class="btns"><a class="btn btn-gold" href="{url("contact", l)}">{t("Umów bezpłatną rozmowę","Book a free consultation")}</a>
<a class="btn btn-ghost" href="{url("how", l)}">{t("Jak to działa","How it works")}</a></div>
</div>
<div class="hero-side"><aside class="hero-card"><h2>{t("Czego można się spodziewać","What you can expect")}</h2><ul>
<li>{t("Pierwsza rozmowa po polsku lub po angielsku","A first conversation in Polish or English")}</li>
<li>{t("Osobiste dopasowanie, a nie algorytm","Personal matching, not an algorithm")}</li>
<li>{t("Każda osoba zweryfikowana i nastawiona na poważny związek","Every person vetted and committed to a real relationship")}</li>
<li>{t("Pełna poufność i brak zobowiązań","Complete confidentiality and no obligation")}</li></ul></aside>
<a class="abia" href="{ABIA}" target="_blank" rel="noopener" aria-label="ABIA - Association of British Introduction Agencies"><img src="/assets/abia-badge.svg" alt="ABIA" width="128" height="128"></a></div></div></section>'''
    trust = f'''<div class="trust"><div class="wrap"><ul>
<li><a href="{ABIA}" target="_blank" rel="noopener">{t("Swatka zarejestrowana w ABIA","ABIA-registered matchmaker")}</a></li>
<li>{t("Pełna poufność","Complete confidentiality")}</li><li>{t("Bezpłatna rozmowa wstępna","Free initial consultation")}</li>
<li>{t("Po polsku i po angielsku","Polish &amp; English")}</li></ul></div></div>'''
    namestrip = "" if P else f'''<div class="namestrip"><div class="wrap"><span class="nl"></span><p>{t("<b>Dobrani</b> (doh-BRAH-ni) - po polsku „dobrani do siebie”: osoby, które do siebie pasują.","<b>Dobrani</b> (doh-BRAH-nee) - Polish for “the well-matched”: people who suit one another.")}</p><span class="nl"></span></div></div>'''
    why = f'''<section><div class="wrap"><div class="head"><span class="eyebrow">{t("Dlaczego polska swatka","Why a Polish matchmaker")}</span>
<h2>{t("Życie między dwiema kulturami ma swoje wyzwania - także w miłości","Living between two cultures has its challenges - in love as well")}</h2>
<p class="lead">{t("Wiele osób o polskich korzeniach porusza się dziś między dwoma językami, dwoma zestawami oczekiwań i często dwoma rodzinami, z których każda ma własne wyobrażenie o idealnym partnerze. Aplikacje randkowe tego nie uwzględniają. Dobra swatka - tak.",
 "Many people with Polish roots move between two languages, two sets of expectations and often two families, each with its own idea of the ideal partner. Dating apps do not account for any of that. A good matchmaker does.")}</p></div>
<div class="grid3">
<div class="card"><hr class="rule"><h3>{t("Rozmowa we własnym języku","A conversation in your own language")}</h3><p>{t("Pierwsza rozmowa odbywa się po polsku lub po angielsku, tak, jak jest wygodniej. Łatwiej mówić o wartościach, rodzinie i oczekiwaniach, gdy nie trzeba szukać słów.","Your first conversation takes place in Polish or English, whichever feels more natural. It is easier to talk about values, family and expectations when you do not have to search for the words.")}</p></div>
<div class="card"><hr class="rule"><h3>{t("Dopasowanie z namysłem","Matching with care")}</h3><p>{t("Łączę wiedzę o kompatybilności osobowości z osobistą oceną i zaufaną siecią kontaktów. Odzywam się tylko wtedy, gdy pojawia się ktoś naprawdę pasujący, a nie tylko dostępny.","I combine personality compatibility with personal judgement and a trusted network. I only get in touch when there is someone genuinely aligned with you, not simply available.")}</p></div>
<div class="card"><hr class="rule"><h3>{t("Dyskrecja i szacunek","Discretion and respect")}</h3><p>{t("Dane są traktowane dyskretnie i nigdy nie są udostępniane bez zgody. Życzliwość i szacunek są warunkiem dla każdej osoby w mojej sieci.","Your details are handled discreetly and never shared without consent. Kindness and respect are non-negotiable for everyone in my network.")}</p></div>
</div></div></section>'''
    steps = f'''<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">{t("Proces","The process")}</span>
<h2>{t("Spokojna, przemyślana droga do właściwej osoby","A calm, considered route to the right person")}</h2></div>
<div class="steps">
<div class="step"><span class="num">I</span><h3>{t("Zaczynamy od rozmowy","It starts with a conversation")}</h3><p>{t("Prywatna rozmowa jeden na jeden o wartościach, stylu życia i o tym, kogo naprawdę Pan/Pani szuka.","A private one-to-one conversation about your values, your lifestyle and who you are truly looking for.")}</p></div>
<div class="step"><span class="num">II</span><h3>{t("Przemyślane dopasowanie","Matched thoughtfully")}</h3><p>{t("Wskazuję osoby, które pasują do siebie pod względem wartości i oczekiwań, a nie tylko są dostępne.","I identify people who align on values and expectations, not just people who happen to be available.")}</p></div>
<div class="step"><span class="num">III</span><h3>{t("Przedstawienie z intencją","Introduced with intention")}</h3><p>{t("Gdy dopasowanie jest właściwe, następuje dyskretne, spokojne przedstawienie. Bez niezręczności i domysłów.","When the match is right, an introduction is made discreetly and calmly. No awkwardness, no guesswork.")}</p></div>
</div><div class="center" style="margin-top:2.4rem"><a class="btn btn-line" href="{url("how", l)}">{t("Zobacz szczegóły","See the details")}</a></div></div></section>'''
    about = f'''<section><div class="wrap grid2"><div><img class="portrait" src="{PHOTO}" alt="{t("Ania, założycielka i główna swatka Dobrani","Ania, founder and lead matchmaker of Dobrani")}" width="360" height="450" loading="lazy"></div>
<div><span class="eyebrow">{t("Osoba stojąca za każdym dopasowaniem","The person behind every match")}</span><h2>{t("Poznaj Anię, założycielkę Dobrani","Meet Ania, founder of Dobrani")}</h2><p class="aka">{t("","or simply Anna, to my English-speaking clients")}</p>
<p>{t("Jestem założycielką i główną swatką Sparked Connection. Swataniem zajmuję się od lat - najpierw wśród przyjaciół i rodziny, dziś zawodowo. Po latach pracy z ambitnymi, zapracowanymi ludźmi widziałam wciąż tę samą historię: kariera ułożona, życie prywatne w zawieszeniu.",
      "I am the founder and lead matchmaker of Sparked Connection. I have been matchmaking for years - first among friends and family, now professionally. After years of working with driven, busy people I kept seeing the same story: a career in order, a personal life on hold.")}</p>
<p>{t("Jako Polka mieszkająca w Wielkiej Brytanii dobrze znam świat, w którym trzeba pogodzić wymagającą pracę, dwie kultury i marzenie o prawdziwej bliskości. Jestem zaangażowana na każdym etapie - tego nie zrobi żaden algorytm.",
      "As a Polish woman living in the UK, I know the world in which demanding work, two cultures and the wish for real closeness have to fit together. I am involved at every step - something no algorithm can do.")}</p>
<a class="btn btn-gold" href="{url("contact", l)}">{t("Umów konsultację","Book a consultation")}</a></div></div></section>'''
    faq = f'''<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">{t("Pytania","Questions")}</span><h2>{t("Najczęstsze pytania","Frequently asked questions")}</h2></div>{faq_html(l)}</div></section>'''
    return hero + trust + namestrip + why + steps + about + band(l) + faq + cta(l)

def body_how(l):
    P = l == "pl"
    t = lambda pl, en: pl if P else en
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{t("Jak to działa","How it works")}</span>
<h1>{t("Prywatny, przemyślany proces","A private, considered process")}</h1>
<p class="lead">{t("Od pierwszej rozmowy do pierwszego spotkania: trzy spokojne kroki, prowadzone osobiście.","From the first conversation to the first meeting: three calm steps, led personally.")}</p></div></section>'''
    steps = f'''<section><div class="wrap"><div class="grid3">
<div class="card"><span class="eyebrow">{t("Krok 1","Step 1")}</span><h3>{t("Rozmowa wstępna","Initial conversation")}</h3><p>{t("Zaczynamy od prywatnej rozmowy jeden na jeden, po polsku lub po angielsku. Rozmawiamy o wartościach, stylu życia i o tym, jak wygląda dobry związek. Nie tylko o tym, kim Pan/Pani jest, ale przede wszystkim o tym, kogo naprawdę Pan/Pani szuka. Rozmowa jest bezpłatna i niezobowiązująca.",
 "We begin with a private one-to-one conversation, in Polish or English. We talk about your values, your lifestyle and what a good relationship looks like. Not only who you are, but above all who you are truly looking for. The conversation is free and without obligation.")}</p></div>
<div class="card"><span class="eyebrow">{t("Krok 2","Step 2")}</span><h3>{t("Przemyślane dopasowanie","Thoughtful matching")}</h3><p>{t("Łączę wiedzę o kompatybilności, osobistą ocenę i zaufaną sieć kontaktów, aby wskazać osoby, które naprawdę do siebie pasują. Odzywam się dopiero wtedy, gdy pojawia się ktoś rzeczywiście zgodny pod względem wartości i oczekiwań, a nie tylko dostępny.",
 "I combine compatibility insight, personal judgement and a trusted network to identify people who genuinely suit one another. I only get in touch when someone is truly aligned on values and expectations, not merely available.")}</p></div>
<div class="card"><span class="eyebrow">{t("Krok 3","Step 3")}</span><h3>{t("Przedstawienie z intencją","Introduction with intention")}</h3><p>{t("Gdy dopasowanie jest właściwe, następuje przedstawienie - dyskretne i spokojne. Bez niezręcznych wymian wiadomości i bez domysłów. Po prostu dobry początek.",
 "When the match is right, an introduction is made - discreetly and calmly. No awkward message exchanges and no guesswork. Simply a good beginning.")}</p></div>
</div></div></section>'''
    expect = f'''<section class="alt"><div class="wrap grid2"><div><span class="eyebrow">{t("Obietnica","My commitment")}</span><h2>{t("Czego można oczekiwać","What you can expect")}</h2>
<ul class="ticks">
<li>{t("Bezpłatna, poufna rozmowa wstępna, bez presji","A free, confidential initial conversation with no pressure")}</li>
<li>{t("Rozmowa i komunikacja po polsku lub po angielsku","Conversation and communication in Polish or English")}</li>
<li>{t("Osoby zweryfikowane i szczerze nastawione na poważny związek","People who are vetted and sincerely committed to a serious relationship")}</li>
<li>{t("Życzliwość i szacunek jako warunek dla każdej osoby w sieci","Kindness and respect as a condition for everyone in the network")}</li>
<li>{t("Dyskrecja: dane nigdy nie są udostępniane bez zgody","Discretion: your details are never shared without consent")}</li>
<li>{t("Moje osobiste zaangażowanie na każdym etapie","My personal involvement at every stage")}</li></ul></div>
<div class="card"><span class="eyebrow">{t("Dla kogo","Who it is for")}</span><h3>{t("Dla osób, które cenią swój czas","For people who value their time")}</h3>
<p>{t("To usługa dla dorosłych osób szukających poważnego związku, mieszkających w Londynie lub gdziekolwiek w Wielkiej Brytanii: mówiących po polsku, mających polskie korzenie albo pragnących poznać kogoś o podobnym pochodzeniu i wartościach.",
 "This service is for adults looking for a serious relationship, living in London or anywhere in the UK: Polish speakers, people with Polish roots, or anyone who would like to meet someone with a similar background and values.")}</p>
<p class="note">{t("Dobrani nie jest aplikacją randkową. To osobista usługa prowadzona przez jedną osobę.","Dobrani is not a dating app. It is a personal service led by one person.")}</p></div></div></section>'''
    return hero + steps + expect + cta(l)

def tier(l, name, price, per, items, feat=False, badge=None):
    b = f'<span class="badge">{badge}</span><br>' if badge else ""
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="card tier{" featured" if feat else ""}">{b}<h3>{name}</h3><div class="price">{price}</div><span class="per">{per}</span><ul>{li}</ul></div>'

def body_offer(l):
    P = l == "pl"
    t = lambda pl, en: pl if P else en
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{t("Oferta","Services")}</span>
<h1>{t("Członkostwo dopasowane do Pana/Pani potrzeb","Membership shaped around your needs")}</h1>
<p class="lead">{t("Dobrani korzysta z członkostw Sparked Connection. Wszystko zaczyna się od bezpłatnej rozmowy.","Dobrani offers the Sparked Connection memberships. Everything begins with a free conversation.")}</p></div></section>'''
    tiers = f'''<section><div class="wrap"><div class="grid3">
{tier(l,"Bronze",t("Bezpłatnie","Free"),t("dostęp do Singles Network","access to the Singles Network"),
  [t("Dostęp do Singles Network","Access to the Singles Network"),t("Możliwość udziału w wydarzeniach (niektóre biletowane osobno)","Option to attend events (some ticketed separately)"),t("Bezpłatna rozmowa wstępna","Free initial consultation")])}
{tier(l,"Gold","£1,500",t("12 miesięcy","12 months"),
  [t("Konsultacje jeden na jeden","One-to-one consultations"),t("Indywidualne poszukiwanie dopasowań","A bespoke search for your matches"),t("Coaching randkowy","Dating coaching"),t("Dostęp VIP do wydarzeń","VIP event access"),t("Profesjonalna sesja zdjęciowa","Professional photoshoot")],
  feat=True,badge=t("Indywidualne podejście","Personal service"))}
{tier(l,"Platinum","£2,800",t("dla dwóch osób","for two people"),
  [t("Pełne doświadczenie Gold dla każdej z dwóch osób","The full Gold experience for each of two people"),t("Priorytetowe dopasowanie","Priority matching"),t("Dedykowana swatka","A dedicated matchmaker")])}
</div><p class="note center" style="margin-top:1.8rem">{t(f'Aktualne ceny i warunki znajdą Państwo na stronie <a href="{PLANS}" target="_blank" rel="noopener">Sparked Connection (po angielsku)</a>. Opłaty za pakiety płatne są z góry i podlegają <a href="{TERMS}" target="_blank" rel="noopener">Regulaminowi</a> oraz <a href="{REFUND}" target="_blank" rel="noopener">Polityce zwrotów i rezygnacji</a> (po angielsku).',
 f'Current prices and terms are on the <a href="{PLANS}" target="_blank" rel="noopener">Sparked Connection plans page</a>. Package fees are payable in advance and are subject to the <a href="{TERMS}" target="_blank" rel="noopener">Terms &amp; Conditions</a> and the <a href="{REFUND}" target="_blank" rel="noopener">Refund &amp; Cancellation Policy</a>.')}</p></div></section>'''
    events = f'''<section class="alt"><div class="wrap grid2"><div><span class="eyebrow">{t("Wydarzenia","Events")}</span><h2>{t("Poznać kogoś na żywo","Meeting people in person")}</h2></div>
<div><p>{t("Członkowie mogą uczestniczyć w wydarzeniach Sparked Connection: spotkaniach towarzyskich, warsztatach, wyjazdach i wieczorach dla singli. To naturalny sposób, by poznawać ludzi twarzą w twarz, nie tylko na zdjęciach.",
 "Members can take part in Sparked Connection events: social evenings, creative workshops, trips and singles nights. It is a natural way to meet people face to face rather than only as profiles on a screen.")}</p>
<a class="btn btn-line" href="{EVENTS}" target="_blank" rel="noopener">{t("Zobacz wydarzenia","See the events")}</a></div></div></section>'''
    return hero + tiers + events + cta(l)

def body_about(l):
    P = l == "pl"
    t = lambda pl, en: pl if P else en
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{t("O mnie","About me")}</span>
<h1>{t("Ania, założycielka i główna swatka","Ania, founder and lead matchmaker")}</h1>
<p class="aka" style="margin:-.2rem 0 .6rem">{t("","or simply Anna, to my English-speaking clients")}</p>
<p class="lead">{t("Osoba, która stoi za każdym dopasowaniem.","The person behind every match.")}</p></div></section>'''
    story = f'''<section><div class="wrap grid2"><div><img class="portrait" src="{PHOTO}" alt="{t("Ania, założycielka i główna swatka Dobrani","Ania, founder and lead matchmaker of Dobrani")}" width="360" height="450" loading="lazy"></div>
<div><h2>{t("Skąd to się wzięło","How it began")}</h2>
<p>{t("Przez lata pracowałam z ambitnymi, wymagającymi profesjonalistami i widziałam wciąż to samo: ludzie, którzy zbudowali karierę, czuli się zagubieni w życiu prywatnym. Nie dlatego, że się nie starali. Przesuwanie profili między spotkaniami nie jest randkowaniem, a żadna aplikacja nie powstała dla osób, które nie mają czasu na niewłaściwych ludzi.",
 "For years I worked with driven, high-achieving professionals and kept seeing the same thing: people who had built successful careers felt stuck in their personal lives. Not because they were not trying. Swiping between meetings is not dating, and no app was built for people with no time to waste on the wrong person.")}</p>
<p>{t("Swataniem zajmowałam się od dawna, nieformalnie, wśród przyjaciół i rodziny, z kilkoma udanymi połączeniami. Gdy zobaczyłam, jak wiele osób wokół mnie zmaga się z aplikacjami randkowymi, postanowiłam robić to zawodowo.",
 "I had been matchmaking for a long time, informally, among friends and family, with several successful matches. When I saw how many people around me struggled with dating apps, I decided to do it professionally.")}</p>
<blockquote>{t("Każda osoba, którą przedstawiam, jest zweryfikowana i szczerze nastawiona na poważny związek. Życzliwość i szacunek nie podlegają negocjacji.","Every person I introduce is vetted and sincere about finding a real relationship. Kindness and respect are non-negotiable.")}</blockquote>
<p>{t("Jako Polka mieszkająca w Wielkiej Brytanii wiem, jak to jest łączyć dwa światy. Dlatego chcę, by osoby o polskich korzeniach miały swatkę, z którą porozmawiają w swoim języku i która zrozumie, czego szukają.",
 "As a Polish woman living in the UK, I know what it is to bring two worlds together. That is why I want people with Polish roots to have a matchmaker they can talk to in their own language, and who understands what they are looking for.")}</p>
<div class="sign">Ania</div></div></div></section>'''
    namesec = f'''<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">{t("Skąd nazwa","Where the name comes from")}</span><h2>Dobrani</h2>
<p class="lead">{t("Po polsku „dobrani” to osoby dobrane do siebie: takie, które pasują do siebie i zostały świadomie połączone. Wymowa: doh-BRAH-ni. „Ania” to polska forma imienia Anna, a dla moich anglojęzycznych klientów po prostu Anna.","In Polish, “dobrani” means “the well-matched”: people chosen with care because they suit one another. Pronounced doh-BRAH-nee. “Ania” is the Polish form of Anna, which is how my English-speaking clients know me.")}</p></div></div></section>'''
    appr = f'''<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">{t("Moje podejście","My approach")}</span><h2>{t("Trzy zasady","Three principles")}</h2></div><div class="grid3">
<div class="card"><hr class="rule"><h3>{t("Zaangażowanie","Involvement")}</h3><p>{t("To nie aplikacja działająca w tle Pana/Pani życia. To ja, zaangażowana na każdym etapie, wykonująca pracę, której nie wykona algorytm.","This is not an app quietly running in the background of your life. It is me, involved at every step, doing the work an algorithm never could.")}</p></div>
<div class="card"><hr class="rule"><h3>{t("Szacunek","Respect")}</h3><p>{t("Życzliwość i szacunek są warunkiem dla każdej osoby w mojej sieci. Bez ghostingu, bez gier.","Kindness and respect are conditions for everyone in my network. No ghosting, no games.")}</p></div>
<div class="card"><hr class="rule"><h3>{t("Dyskrecja","Discretion")}</h3><p>{t("Dane są traktowane poufnie i nigdy nie są udostępniane bez zgody. Matchmaking to proces osobisty i tak do niego podchodzę.","Your details are handled in confidence and never shared without consent. Matchmaking is a personal process and I treat it as one.")}</p></div>
</div></div></section>'''
    cred = f'''<section><div class="wrap grid2"><div><span class="eyebrow">{t("Kwalifikacje i przejrzystość","Credentials and transparency")}</span><h2>{t("Na czym można polegać","What you can rely on")}</h2></div>
<div><ul class="ticks">
<li>{t("Certyfikowana swatka (Certified Matchmaker)","Certified Matchmaker")}</li>
<li>{t(f'Agencja zarejestrowana i zatwierdzona przez <a href="{ABIA}" target="_blank" rel="noopener">ABIA</a>',f'Agency registered and approved by <a href="{ABIA}" target="_blank" rel="noopener">ABIA</a>')}</li>
<li>{t("Założycielka Sparked Connection Ltd (Wielka Brytania)","Founder of Sparked Connection Ltd (UK)")}</li>
<li>{t("Wieloletnie doświadczenie zawodowe w pracy z wymagającymi profesjonalistami","Many years of professional experience working with demanding professionals")}</li>
<li>{t("Rozmowy po polsku i po angielsku","Consultations in Polish and English")}</li></ul>{partner(l, light=True)}</div></div></section>'''
    return hero + story + namesec + appr + cred + cta(l)

def body_contact(l):
    P = l == "pl"
    t = lambda pl, en: pl if P else en
    subj = esc(t("Zapytanie - Dobrani","Enquiry - Dobrani"))
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{t("Kontakt","Contact")}</span>
<h1>{t("Porozmawiajmy","Let us talk")}</h1>
<p class="lead">{t("Pierwszy krok to bezpłatna, poufna rozmowa. Bez zobowiązań.","The first step is a free, confidential conversation. No commitment.")}</p></div></section>'''
    def f(pl,en): return t(pl,en)
    form = f"""<form id="enquiry" class="enq" data-lang="{l}" novalidate accept-charset="UTF-8">
<div class="hp" aria-hidden="true"><label for="website">Website</label><input type="text" id="website" name="website" tabindex="-1" autocomplete="off"></div>
<div class="row2"><div class="fld"><label for="fn">{f("Imię","First name")} *</label><input id="fn" name="first_name" type="text" autocomplete="given-name" required></div>
<div class="fld"><label for="ln">{f("Nazwisko","Last name")} *</label><input id="ln" name="last_name" type="text" autocomplete="family-name" required></div></div>
<div class="fld"><label for="em">{f("Adres e-mail","Email address")} *</label><input id="em" name="fi-sender-email" type="email" autocomplete="email" required></div>
<div class="fld"><label for="ph">{f("Telefon","Phone")}</label><div class="phone"><select name="fi-select-countryCode" aria-label="{f("Numer kierunkowy","Country code")}"><option>+44</option><option>+48</option><option>+353</option><option>+1</option><option>{f("Inny","Other")}</option></select><input id="ph" name="fi-text-phoneLocal" type="tel" autocomplete="tel-national"></div></div>
<div class="row2"><div class="fld"><label for="lc">{f("Miejscowość / region w Wielkiej Brytanii","Town or region in the UK")} *</label><input id="lc" name="location" type="text" required></div>
<div class="fld"><label for="lg">{f("Preferowany język rozmowy","Preferred language for our conversation")} *</label><select id="lg" name="preferred_language" required><option value="">{f("Wybierz…","Select…")}</option><option value="Polish">{f("Polski","Polish")}</option><option value="English">{f("Angielski","English")}</option><option value="Either">{f("Obojętnie","Either")}</option></select></div></div>
<div class="row2"><div class="fld"><label for="am">{f("Jestem","I am")}</label><select id="am" name="i_am"><option value="">{f("Wybierz…","Select…")}</option><option value="Woman">{f("Kobietą","A woman")}</option><option value="Man">{f("Mężczyzną","A man")}</option><option value="Prefer to say in conversation">{f("Wolę powiedzieć w rozmowie","I would rather say in conversation")}</option></select></div>
<div class="fld"><label for="lf">{f("Szukam","I am looking for")}</label><select id="lf" name="looking_for"><option value="">{f("Wybierz…","Select…")}</option><option value="A woman">{f("Kobiety","A woman")}</option><option value="A man">{f("Mężczyzny","A man")}</option><option value="Prefer to say in conversation">{f("Wolę powiedzieć w rozmowie","I would rather say in conversation")}</option></select></div></div>
<div class="row2"><div class="fld"><label for="ag">{f("Wiek","Age")} *</label><input id="ag" name="age" type="number" inputmode="numeric" min="18" max="99" step="1" autocomplete="off" required></div>
<div class="fld"><label for="pl">{f("Zainteresowanie","Interested in")} *</label><select id="pl" name="interested_in" required><option value="">{f("Wybierz…","Select…")}</option><option value="Joining the Singles Network (free membership)">{f("Dołączenie do Singles Network (bezpłatne członkostwo)","Joining the Singles Network (free membership)")}</option><option value="1:1 Matchmaking service (Gold/Platinum membership)">{f("Matchmaking 1:1 (członkostwo Gold/Platinum)","1:1 Matchmaking service (Gold/Platinum membership)")}</option></select></div></div>
<div class="fld"><label for="hd">{f("Skąd Pan/Pani o nas wie?","How did you hear about us?")}</label><select id="hd" name="heard_about"><option value="">{f("Wybierz…","Select…")}</option><option>Instagram</option><option>Facebook</option><option>LinkedIn</option><option>Google</option><option>{f("Polecenie","Recommendation")}</option><option>{f("Wydarzenie","An event")}</option><option>{f("Inne","Other")}</option></select></div>
<div class="fld"><label for="ms">{f("Kilka słów o sobie i o tym, kogo Pan/Pani szuka","A few words about yourself and what you are looking for")}</label><textarea id="ms" name="message" rows="5"></textarea></div>
<label class="chk"><input type="checkbox" name="consent_privacy" value="Yes" required> <span>{f(f'Wyrażam zgodę na przetwarzanie moich danych w celu odpowiedzi na to zapytanie, zgodnie z <a href="{PRIVACY}" target="_blank" rel="noopener">Polityką prywatności (po angielsku)</a>. *', f'I agree to my details being used to respond to this enquiry, as set out in the <a href="{PRIVACY}" target="_blank" rel="noopener">Privacy Notice</a>. *')}</span></label>
<div class="cf-turnstile" data-sitekey="0x4AAAAAAExsZ2hUtz55GptX"></div>
<div id="enq-error" class="enq-error" role="alert"></div>
<button type="submit" id="enq-submit" class="btn btn-gold">{f("Wyślij zapytanie","Send enquiry")}</button>
<p class="note" style="margin-top:.9rem">{f("Odpowiem w ciągu kilku dni roboczych. Zapytanie jest poufne i niezobowiązujące.","I will reply within a few working days. Your enquiry is confidential and carries no obligation.")}</p>
</form>
<div id="enq-success" class="enq-success" role="status"><span class="tick">&#10003;</span><h3>{f("Dziękuję, zapytanie dotarło","Thank you, your enquiry has arrived")}</h3><p>{f("Odezwę się wkrótce, aby ustalić dogodny termin i język rozmowy.","I will be in touch shortly to agree a convenient time and the language of our conversation.")}</p></div>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<script src="/assets/enquiry.js" defer></script>"""
    main = f'''<section><div class="wrap grid2" style="align-items:start"><div class="card"><h2>{t("Umów bezpłatną rozmowę","Book a free consultation")}</h2>
<p class="note" style="margin-bottom:1.4rem">{t("Pola oznaczone * są wymagane. Rozmowę można prowadzić po polsku lub po angielsku.","Fields marked * are required. We can speak in Polish or in English.")}</p>
{form}</div>
<div class="contact-box"><ul class="kv">
<li><b>{t("E-mail","Email")}</b><span><a href="mailto:{EMAIL}?subject={subj}">{EMAIL}</a></span></li>
<li><b>{t("Języki","Languages")}</b><span>{t("Polski, angielski","Polish, English")}</span></li>
<li><b>{t("Obszar","Area")}</b><span>{t("Londyn i cała Wielka Brytania","London and the whole UK")}</span></li>
<li><b>{t("Partner","Partner")}</b><span>{partner(l, light=True)}</span></li>
<li><b>{t("Social media","Social")}</b><span><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></span></li>
</ul></div></div></section>'''
    return hero + main

BODIES = {"home": body_home, "how": body_how, "offer": body_offer, "about": body_about, "contact": body_contact}

META = {
 "home": {"pl": ("Polska swatka w Londynie i UK | Dobrani by Ania – Polish Matchmaker",
                 "Dobrani by Ania, Polish Matchmaker: prywatny matchmaking po polsku i po angielsku w Londynie i całej Wielkiej Brytanii. Bezpłatna, poufna rozmowa z Anią, założycielką Sparked Connection."),
          "en": ("Polish Matchmaker in London & the UK | Dobrani by Ania",
                 "Dobrani by Ania, Polish Matchmaker: private matchmaking in Polish or English across London and the UK. Book a free, confidential consultation with Ania, founder of Sparked Connection.")},
 "how":  {"pl": ("Jak działa matchmaking po polsku | Dobrani - Polish Matchmaker",
                 "Trzy kroki prywatnego matchmakingu: rozmowa wstępna, przemyślane dopasowanie i dyskretne przedstawienie. Po polsku lub po angielsku, w Londynie i całej Wielkiej Brytanii."),
          "en": ("How Polish Matchmaking Works | Dobrani - Polish Matchmaker",
                 "Three steps of private matchmaking: an initial conversation, thoughtful matching and a discreet introduction. In Polish or English, in London and across the UK.")},
 "offer":{"pl": ("Matchmaking dla Polaków w UK: oferta i członkostwa | Dobrani",
                 "Członkostwa Bronze, Gold i Platinum oraz wydarzenia dla singli. Polska swatka w Londynie i UK w partnerstwie ze Sparked Connection."),
          "en": ("Polish Matchmaking Services & Memberships UK | Dobrani",
                 "Bronze, Gold and Platinum memberships plus singles events. A Polish matchmaker for London and the UK, in partnership with Sparked Connection.")},
 "about":{"pl": ("O mnie - Ania, polska swatka | Dobrani - Polish Matchmaker",
                 "Ania, założycielka i główna swatka Sparked Connection. Certyfikowana swatka, zarejestrowana w ABIA, pracująca po polsku i po angielsku w Londynie i UK."),
          "en": ("About Ania | Dobrani - Polish Matchmaker",
                 "Ania, founder and lead matchmaker of Sparked Connection. A certified matchmaker, ABIA registered, working in Polish and English in London and the UK.")},
 "contact":{"pl": ("Kontakt - bezpłatna rozmowa | Dobrani - Polish Matchmaker",
                 "Umów bezpłatną, poufną rozmowę z polską swatką. Londyn i cała Wielka Brytania, po polsku lub po angielsku."),
          "en": ("Contact - Free Consultation | Dobrani - Polish Matchmaker",
                 "Book a free, confidential consultation with a Polish matchmaker. London and the whole UK, in Polish or English.")},
}

# ---------------- Articles ----------------
from articles import ARTS
URLS["articles"] = ("/pl/artykuly/", "/articles/")
META["articles"] = {"pl": ("Artykuły o matchmakingu i randkowaniu po polsku | Dobrani",
                           "Praktyczne artykuły o matchmakingu, randkowaniu w Londynie i pracy ze swatką, dla Polaków mieszkających w Wielkiej Brytanii."),
                    "en": ("Articles on Polish Matchmaking & Dating in the UK | Dobrani",
                           "Practical articles on matchmaking, dating in London and working with a matchmaker, for Poles living in the UK.")}
ART_BY_KEY = {}
for _a in ARTS:
    k = "art_" + _a["id"]
    URLS[k] = (f'/pl/artykuly/{_a["pl"]["slug"]}/', f'/articles/{_a["en"]["slug"]}/')
    META[k] = {"pl": (_a["pl"]["title"] + " | Dobrani", _a["pl"]["desc"]), "en": (_a["en"]["title"] + " | Dobrani", _a["en"]["desc"])}
    ART_BY_KEY[k] = _a

def art_cards(l, exclude=None):
    P = l == "pl"
    out = ""
    for a in ARTS:
        if exclude and a["id"] == exclude: continue
        d = a[l]
        out += (f'<a class="card art-card" href="{url("art_"+a["id"], l)}"><h3>{esc(d["title"])}</h3><p>{esc(d["desc"])}</p>'
                f'<span class="more">{"Czytaj dalej" if P else "Read more"} &rarr;</span></a>')
    return out

def body_articles(l):
    P = l == "pl"
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{"Artykuły" if P else "Articles"}</span>
<h1>{"Matchmaking i randkowanie po polsku" if P else "Polish matchmaking and dating"}</h1>
<p class="lead">{"Praktyczne wskazówki dla Polaków w Londynie i w całej Wielkiej Brytanii." if P else "Practical guidance for Poles in London and across the UK."}</p></div></section>'''
    return hero + f'<section><div class="wrap"><div class="grid2x">{art_cards(l)}</div></div></section>' + cta(l)

def body_article(key, l):
    P = l == "pl"
    a = ART_BY_KEY[key]; d = a[l]
    hero = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow"><a href="{url("articles", l)}">{"Artykuły" if P else "Articles"}</a></span>
<h1>{esc(d["title"])}</h1><p class="lead">{esc(d["lead"])}</p>
<p class="byline">{"Autor: Ania, Dobrani · " if P else "By Ania (Anna), Dobrani · "}<time datetime="{a["date"]}">{a["date"]}</time></p></div></section>'''
    body = "".join(f'<h2>{esc(h)}</h2>' + "".join(f'<p>{esc(p)}</p>' for p in ps) for h, ps in d["sections"])
    links = (f'<p class="inl">{"Zobacz także: " if P else "See also: "}<a href="{url("how", l)}">{"Jak to działa" if P else "How it works"}</a> · '
             f'<a href="{url("offer", l)}">{"Oferta" if P else "Services"}</a> · <a href="{url("contact", l)}">{"Bezpłatna rozmowa" if P else "Free consultation"}</a></p>')
    more = f'<section class="alt"><div class="wrap"><div class="head"><h2>{"Czytaj również" if P else "Keep reading"}</h2></div><div class="grid2x">{art_cards(l, a["id"])}</div></div></section>'
    return hero + f'<section><div class="wrap art">{body}{links}</div></section>' + more + cta(l)

BODIES["articles"] = body_articles
for _k in ART_BY_KEY:
    BODIES[_k] = (lambda kk: (lambda l: body_article(kk, l)))(_k)

_home_orig = body_home
def body_home_x(l):
    P = l == "pl"
    h = _home_orig(l)
    teaser = (f'<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">{"Artykuły" if P else "Articles"}</span>'
              f'<h2>{"Z naszego poradnika" if P else "From our guide"}</h2></div><div class="grid2x">{art_cards(l)}</div>'
              f'<p class="center" style="margin-top:28px"><a class="btn btn-line" href="{url("articles", l)}">{"Wszystkie artykuły" if P else "All articles"}</a></p></div></section>')
    i = h.rfind('<section class="cta">')
    return h[:i] + teaser + h[i:] if i != -1 else h + teaser
BODIES["home"] = body_home_x

def crumbs(key, l):
    P = l == "pl"
    items = [("Dobrani", DOMAIN + url("home", l))]
    if key.startswith("art_"):
        items.append(("Artykuły" if P else "Articles", DOMAIN + url("articles", l)))
    if key != "home":
        items.append((META[key][l][0].split(" | ")[0], DOMAIN + url(key, l)))
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

OG_IMG = DOMAIN + "/assets/og-image.png"

def jsonld(key, l):
    graph = []
    if key == "home":
        graph.append({
            "@type": "ProfessionalService", "@id": DOMAIN + "/#org", "name": "Dobrani", "alternateName": ["Dobrani by Ania", "Polish Matchmaker"], "url": DOMAIN + "/",
            "description": META["home"][l][1], "inLanguage": ["pl", "en"], "email": EMAIL,
            "areaServed": [{"@type": "AdministrativeArea", "name": "London"}, {"@type": "Country", "name": "United Kingdom"}],
            "parentOrganization": {"@type": "Organization", "name": COMPANY, "url": SC_URL},
            "founder": {"@type": "Person", "name": "Anna", "alternateName": "Ania", "jobTitle": "Founder and Lead Matchmaker"},
            "sameAs": [SC_URL, INSTA, FB, LI]})
        graph.append({
            "@type": "FAQPage", "inLanguage": l,
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items(l)]})
        graph.append({"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Dobrani - Polish Matchmaker", "inLanguage": ["pl", "en"], "publisher": {"@id": DOMAIN + "/#org"}})
        graph.append({"@type": "Person", "@id": DOMAIN + "/#ania", "name": "Anna (Ania)", "jobTitle": "Founder and Lead Matchmaker", "worksFor": {"@id": DOMAIN + "/#org"}, "image": PHOTO, "knowsLanguage": ["pl", "en"]})
    else:
        graph.append({"@type": "WebPage", "@id": DOMAIN + url(key, l) + "#page", "url": DOMAIN + url(key, l), "name": META[key][l][0], "description": META[key][l][1], "inLanguage": l, "isPartOf": {"@id": DOMAIN + "/#site"}})
        graph.append(crumbs(key, l))
    if key in ART_BY_KEY:
        a = ART_BY_KEY[key]
        graph.append({"@type": "Article", "headline": a[l]["title"], "description": a[l]["desc"], "inLanguage": l, "datePublished": a["date"], "dateModified": a["date"],
                      "mainEntityOfPage": DOMAIN + url(key, l), "image": OG_IMG,
                      "author": {"@type": "Person", "name": "Anna (Ania)", "url": DOMAIN + url("about", l)},
                      "publisher": {"@type": "Organization", "name": "Dobrani - Polish Matchmaker", "url": DOMAIN + "/", "parentOrganization": {"@type": "Organization", "name": COMPANY, "url": SC_URL}}})
    return ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>') if graph else ""

def page(key, l):
    P = l == "pl"
    title, desc = META[key][l]
    me = DOMAIN + url(key, l)
    pl_u, en_u = DOMAIN + url(key, "pl"), DOMAIN + url(key, "en")
    other = "en" if P else "pl"
    CUR = ' aria-current="page"'
    nav = "".join(f'<li><a href="{url(k, l)}"{CUR if k == key else ""}>{n}</a></li>' for k, n in NAV[l])
    def gb(n): return FLAG_GB.replace('id="fs"', f'id="fs{n}"').replace('id="ft"', f'id="ft{n}"').replace('url(#fs)', f'url(#fs{n})').replace('url(#ft)', f'url(#ft{n})')
    def pl_(n): return FLAG_PL
    def switch(n, cls):
        lab = "Język" if P else "Language"
        if P:
            inner = f'<span aria-current="true">{pl_(n)}PL</span><a href="{url(key,"en")}" hreflang="en" lang="en">{gb(n)}EN</a>'
        else:
            inner = f'<a href="{url(key,"pl")}" hreflang="pl" lang="pl">{pl_(n)}PL</a><span aria-current="true">{gb(n)}EN</span>'
        return f'<div class="lang {cls}" aria-label="{lab}">{inner}</div>'
    sw = f'<li class="lang-li">{switch("d", "lang-d")}</li>'
    sw_m = switch("m", "lang-m")
    ga = f'<script>window.PM_GA="{GA_ID}";</script>' if GA_ID else ""
    cc = ""
    if GA_ID:
        cc = (f'<div id="cc" role="dialog" aria-label="Cookies"><p>{"Używamy plików cookie analitycznych, aby rozumieć, jak odwiedzający korzystają ze strony. Żadne pliki cookie nie są ustawiane, dopóki Pan/Pani nie wybierze opcji. Szczegóły w" if P else "We use analytics cookies to understand how visitors use this site. No cookies are set until you choose. See our"} '
              f'<a href="{PRIVACY}" target="_blank" rel="noopener">{"Polityce prywatności (po angielsku)" if P else "Privacy Notice"}</a>.</p>'
              f'<div class="row"><button class="y" type="button">{"Akceptuję" if P else "Accept"}</button><button class="n" type="button">{"Odrzucam" if P else "Reject"}</button></div></div>')
    TOPBAR = f'''<div class="topbar"><span class="tb-m">Polish Matchmaker</span><a class="pw" href="{SC_URL}" target="_blank" rel="noopener" aria-label="{"W partnerstwie z" if P else "In Partnership with"} Sparked Connection"><span>{"W partnerstwie z" if P else "In Partnership with"}</span><img src="/assets/sparked-badge.svg" alt="Sparked Connection" width="48" height="48"></a></div>'''
    head = f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{me}">
<link rel="alternate" hreflang="pl" href="{pl_u}">
<link rel="alternate" hreflang="en" href="{en_u}">
<link rel="alternate" hreflang="x-default" href="{en_u}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{"article" if key.startswith("art_") else "website"}"><meta property="og:site_name" content="Dobrani - Polish Matchmaker">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{me}"><meta property="og:locale" content="{"pl_PL" if P else "en_GB"}"><meta property="og:locale:alternate" content="{"en_GB" if P else "pl_PL"}">
<meta property="og:image" content="{OG_IMG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Dobrani by Ania - Polish Matchmaker">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{OG_IMG}">
{f'<meta property="article:published_time" content="{ART_BY_KEY[key]["date"]}"><meta property="article:author" content="Ania">' if key.startswith("art_") else ""}
<meta name="theme-color" content="#1E3151">
<link rel="icon" href="/assets/favicon.svg?v=2" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png?v=2" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&family=Josefin+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{jsonld(key, l)}
</head>
<body>
<a class="skip" href="#main">{"Przejdź do treści" if P else "Skip to content"}</a>
{TOPBAR if key != "home" else ""}
<header class="site-header"><div class="wrap nav">
<a class="brand" href="{url("home", l)}" aria-label="Dobrani by Ania - Polish Matchmaker"><img src="/assets/logo.svg" alt="Dobrani by Ania" width="{LOGO_W}" height="{LOGO_H}"><span class="rule" aria-hidden="true"></span><span class="desc">Polish<br>Matchmaker</span></a>
{sw_m}<button class="burger" type="button" aria-label="{"Menu" if P else "Menu"}" aria-expanded="false" aria-controls="menu"><svg width="22" height="16" viewBox="0 0 22 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 2h20M1 8h20M1 14h20"/></svg></button>
<ul class="menu" id="menu">{nav}{sw}</ul>
</div></header>
<main id="main">
'''
    foot = f'''
</main>
<footer class="site-footer"><div class="wrap">
<div class="fgrid">
<div class="fbrand"><img class="flogo" src="/assets/logo-stacked-reversed.svg" alt="Dobrani by Ania - Polish Matchmaker" width="{STK_W}" height="{STK_H}"><p>{"Prywatny matchmaking po polsku i po angielsku w Londynie i w całej Wielkiej Brytanii." if P else "Private matchmaking in Polish and English in London and across the UK."}</p>{partner(l)}</div>
<div><h4>{"Strony" if P else "Pages"}</h4><ul>{"".join(f'<li><a href="{url(k,l)}">{n}</a></li>' for k,n in NAV[l])}</ul></div>
<div><h4>{"Informacje prawne" if P else "Legal"}</h4><ul>
<li><a href="{PRIVACY}" target="_blank" rel="noopener">{"Polityka prywatności" if P else "Privacy Notice"}</a></li>
<li><a href="{TERMS}" target="_blank" rel="noopener">{"Regulamin" if P else "Terms &amp; Conditions"}</a></li>
<li><a href="{REFUND}" target="_blank" rel="noopener">{"Zwroty i rezygnacja" if P else "Refund &amp; Cancellation"}</a></li>
<li><a href="{ACCESS}" target="_blank" rel="noopener">{"Dostępność" if P else "Accessibility"}</a></li></ul></div>
<div><h4>{"Kontakt" if P else "Contact"}</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li><li><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></li></ul></div>
</div>
<div class="legal">
<p>{f"Dobrani (Polish Matchmaker) jest nazwą handlową {COMPANY}. Spółka zarejestrowana w Anglii i Walii, nr {CO_NO}. Siedziba: {REG_ADDR}. Numer rejestracji ICO: {ICO}. Agencja zarejestrowana i zatwierdzona przez ABIA." if P else f"Dobrani (Polish Matchmaker) is a trading name of {COMPANY}. Registered in England and Wales, company no. {CO_NO}. Registered office: {REG_ADDR}. ICO registration no. {ICO}. ABIA registered and approved."}</p>
<p>{"Dokumenty prawne dostępne są w języku angielskim; w razie rozbieżności wiążąca jest wersja angielska." if P else "Legal documents are provided in English."}</p>
<p>© 2026 {COMPANY}. {"Wszelkie prawa zastrzeżone." if P else "All rights reserved."}</p>
</div></div></footer>
{cc}{ga}
<script src="/assets/main.js" defer></script>
</body></html>
'''
    return head + BODIES[key](l) + foot

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    if full.endswith("/"): full = os.path.join(full, "index.html")
    content = re.sub(r'<p class="aka"[^>]*></p>\s*', "", content)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

def main():
    import shutil
    # clear output of earlier layouts (Polish at /, English at /en/) so no stale pages remain
    for d in ("jak-to-dziala", "oferta", "o-mnie", "kontakt", "artykuly", "en"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for key in URLS:
        for l in ("pl", "en"):
            write(url(key, l), page(key, l))
    # tiny redirect stubs for the earlier URL layout (the site had just launched)
    for key in URLS:
        for l in ("pl", "en"):
            new_u = url(key, l)
            old_u = new_u[3:] if l == "pl" else "/en" + new_u
            if old_u in ("/", "") or old_u == new_u: continue
            tgt = DOMAIN + new_u
            write(old_u, f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><title>Redirecting</title><meta name="robots" content="noindex"><link rel="canonical" href="{tgt}"><meta http-equiv="refresh" content="0;url={new_u}"></head><body><a href="{new_u}">{new_u}</a></body></html>')
    # sitemap with hreflang alternates
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in URLS:
        for l in ("pl", "en"):
            sm.append(f'<url><loc>{DOMAIN}{url(key,l)}</loc>'
                      f'<xhtml:link rel="alternate" hreflang="pl" href="{DOMAIN}{url(key,"pl")}"/>'
                      f'<xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{url(key,"en")}"/>'
                      f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{url(key,"en")}"/></url>')
    sm.append('</urlset>')
    write("/sitemap.xml", "\n".join(sm))
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    llm = ["# Dobrani by Ania - Polish Matchmaker", "", "> Private matchmaking in Polish and English for Poles in London and across the UK. Delivered by Sparked Connection Ltd (UK, ABIA registered).", "", "## Pages"]
    for key in URLS:
        llm.append(f"- [{META[key]['en'][0]}]({DOMAIN}{url(key,'en')}): {META[key]['en'][1]}")
    llm += ["", "## Strony po polsku"]
    for key in URLS:
        llm.append(f"- [{META[key]['pl'][0]}]({DOMAIN}{url(key,'pl')})")
    write("/llms.txt", "\n".join(llm) + "\n")
    write("/CNAME", DOMAIN.replace("https://", "") + "\n")
    write("/.nojekyll", "")
    write("/assets/favicon.svg?v=2", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#1E3151"/><circle cx="23" cy="27" r="6.5" fill="#CE7E98"/><circle cx="41" cy="27" r="6.5" fill="#E6A961"/><path d="M15 46c2-7 8-11 17-11s15 4 17 11" stroke="#E6A961" stroke-width="3" stroke-linecap="round" fill="none"/></svg>')
    write("/404.html", '''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 | Dobrani - Polish Matchmaker</title><meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Inter:wght@400&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/style.css"></head>
<body><main class="wrap center" style="padding:120px 24px"><span class="eyebrow">404</span><h1>Nie znaleziono strony / Page not found</h1>
<div class="btns" style="justify-content:center"><a class="btn btn-navy" href="/">Home</a><a class="btn btn-line" href="/pl/">Strona główna (po polsku)</a></div></main></body></html>''')
    print("built", len(URLS) * 2, "pages")

if __name__ == "__main__":
    main()
