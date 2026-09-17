import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_lodging = '''<!-- --- LODGING --- -->
<section class="lodging-section" id="lodging">
  <div class="container">
    <div class="lodging-card">
      <h2>?? Logements — Votez & Choisissez</h2>
      <p class="sub">Votez Oui / Bof / Non. Cliquez les prix pour les modifier. Tout est synchronisé en temps réel ?</p>

      <!-- -- Étape 1: 9?12 oct -- -->
      <div class="lodge-period">
        <span>?? 9 ? 12 Oct · Machico</span>
        <span>3 nuits</span>
      </div>

      <div class="lodge-opt" data-lodge="machico-A">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://fr.airbnb.com/rooms/26884921" target="_blank">Option A (Airbnb)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="230" data-lp="machico-A"> €</div>
            <div class="pp" data-pp="machico-A">76 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://fr.airbnb.com/rooms/26884921" target="_blank" style="display:inline-block; font-size:0.75rem; background:var(--accent); color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Airbnb</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('machico-A','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-A','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-A','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('machico-A','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-A','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-A','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('machico-A','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-A','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-A','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape1','machico-A')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="machico-B">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://www.booking.com/hotel/pt/charming-retreat-machico-5-min-praia-amp-centro-b.fr.html" target="_blank">Option B (Booking)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="250" data-lp="machico-B"> €</div>
            <div class="pp" data-pp="machico-B">83 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://www.booking.com/hotel/pt/charming-retreat-machico-5-min-praia-amp-centro-b.fr.html" target="_blank" style="display:inline-block; font-size:0.75rem; background:#003580; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Booking</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('machico-B','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-B','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-B','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('machico-B','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-B','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-B','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('machico-B','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-B','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-B','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape1','machico-B')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="machico-C">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://www.booking.com/hotel/pt/discovery-i.fr.html" target="_blank">Option C (Booking)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="260" data-lp="machico-C"> €</div>
            <div class="pp" data-pp="machico-C">86 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://www.booking.com/hotel/pt/discovery-i.fr.html" target="_blank" style="display:inline-block; font-size:0.75rem; background:#003580; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Booking</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('machico-C','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-C','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-C','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('machico-C','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-C','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-C','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('machico-C','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-C','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-C','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape1','machico-C')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="machico-D">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://fr.trip.com/hotels/detail/?hotelId=133370350" target="_blank">Option D (Trip.com)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="240" data-lp="machico-D"> €</div>
            <div class="pp" data-pp="machico-D">80 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://fr.trip.com/hotels/detail/?hotelId=133370350" target="_blank" style="display:inline-block; font-size:0.75rem; background:#0f294d; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Trip.com</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('machico-D','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-D','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-D','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('machico-D','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-D','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-D','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('machico-D','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('machico-D','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('machico-D','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape1','machico-D')">? Choisir cette option</button>
      </div>

      <!-- -- Étape 2: 12?15 oct -- -->
      <div class="lodge-period">
        <span>?? 12 ? 15 Oct · Côte Nord</span>
        <span>3 nuits</span>
      </div>

      <div class="lodge-opt" data-lodge="nord-1">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://www.booking.com/hotel/pt/sao-vicente-guest-house.fr.html" target="_blank">Option 01 (São Vicente)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="273" data-lp="nord-1"> €</div>
            <div class="pp" data-pp="nord-1">91 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://www.booking.com/hotel/pt/sao-vicente-guest-house.fr.html" target="_blank" style="display:inline-block; font-size:0.75rem; background:#003580; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Booking</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('nord-1','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-1','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-1','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('nord-1','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-1','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-1','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('nord-1','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-1','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-1','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape2','nord-1')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="nord-2">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://fr.airbnb.com/rooms/5315743" target="_blank">Option 02 (Ponta Delgada)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="254" data-lp="nord-2"> €</div>
            <div class="pp" data-pp="nord-2">85 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://fr.airbnb.com/rooms/5315743" target="_blank" style="display:inline-block; font-size:0.75rem; background:var(--accent); color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Airbnb</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('nord-2','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-2','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-2','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('nord-2','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-2','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-2','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('nord-2','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-2','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-2','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape2','nord-2')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="nord-3">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://www.booking.com/hotel/pt/estalagem-corte-do-norte-ponta-delgada.fr.html" target="_blank">Option 03 (Ponta Delgada)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="273" data-lp="nord-3"> €</div>
            <div class="pp" data-pp="nord-3">91 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://www.booking.com/hotel/pt/estalagem-corte-do-norte-ponta-delgada.fr.html" target="_blank" style="display:inline-block; font-size:0.75rem; background:#003580; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Booking</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('nord-3','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-3','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-3','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('nord-3','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-3','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-3','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('nord-3','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('nord-3','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('nord-3','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape2','nord-3')">? Choisir cette option</button>
      </div>

      <!-- -- Étape 3: 15?16 oct -- -->
      <div class="lodge-period">
        <span>?? 15 ? 16 Oct · Funchal</span>
        <span>1 nuit</span>
      </div>

      <div class="lodge-opt" data-lodge="fun-1">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://www.french.hostelworld.com/pwa/hosteldetails.php/Residencial-Monaco/Funchal/75715" target="_blank">Option 01 (Hostel)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="70" data-lp="fun-1"> €</div>
            <div class="pp" data-pp="fun-1">23 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://www.french.hostelworld.com/pwa/hosteldetails.php/Residencial-Monaco/Funchal/75715" target="_blank" style="display:inline-block; font-size:0.75rem; background:#f26222; color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Hostelworld</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('fun-1','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-1','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-1','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('fun-1','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-1','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-1','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('fun-1','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-1','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-1','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape3','fun-1')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="fun-2">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? <a href="https://fr.airbnb.com/rooms/1637584730331319648" target="_blank">Option 02 (Airbnb)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="108" data-lp="fun-2"> €</div>
            <div class="pp" data-pp="fun-2">36 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://fr.airbnb.com/rooms/1637584730331319648" target="_blank" style="display:inline-block; font-size:0.75rem; background:var(--accent); color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Airbnb</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('fun-2','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-2','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-2','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('fun-2','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-2','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-2','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('fun-2','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-2','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-2','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape3','fun-2')">? Choisir cette option</button>
      </div>

      <div class="lodge-opt" data-lodge="fun-3">
        <div class="lodge-opt-header">
          <div class="lodge-opt-name">??? ?? <a href="https://fr.airbnb.com/rooms/1437146092888977049" target="_blank">Option 03 (Airbnb)</a></div>
          <div class="lodge-price">
            <div class="total"><input type="number" class="price-edit" value="180" data-lp="fun-3"> €</div>
            <div class="pp" data-pp="fun-3">60 € / pers.</div>
          </div>
        </div>
        <div style="margin-bottom: 10px;">
          <a href="https://fr.airbnb.com/rooms/1437146092888977049" target="_blank" style="display:inline-block; font-size:0.75rem; background:var(--accent); color:#fff; padding:4px 10px; border-radius:6px; text-decoration:none; font-weight:600;">??? Voir sur Airbnb</a>
        </div>
        <div class="lodge-votes">
          <span class="vote-label">Vincent</span>
          <button class="vote-btn oui" onclick="vote('fun-3','vincent','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-3','vincent','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-3','vincent','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Momo</span>
          <button class="vote-btn oui" onclick="vote('fun-3','momo','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-3','momo','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-3','momo','non')">Non</button>
          <span style="width:8px"></span>
          <span class="vote-label">Caro</span>
          <button class="vote-btn oui" onclick="vote('fun-3','caro','oui')">Oui</button>
          <button class="vote-btn bof" onclick="vote('fun-3','caro','bof')">Bof</button>
          <button class="vote-btn non" onclick="vote('fun-3','caro','non')">Non</button>
        </div>
        <button class="select-lodge-btn" onclick="selectLodge('etape3','fun-3')">? Choisir cette option</button>
      </div>
    </div>
  </div>
</section>'''

html = re.sub(r'<!-- --- LODGING --- -->.*?<!-- --- BUDGET --- -->', new_lodging + '\n\n<!-- --- BUDGET --- -->', html, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
