(() => {
  'use strict';
  const products = window.PRODUCTS;
  const WA = '923136726285';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const money = n => 'PKR ' + n.toLocaleString('en-PK');
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const marks = {chatgpt:'✳',gemini:'✧',veo:'▷',leonardo:'◈',elevenlabs:'Ⅱ',canva:'C',figma:'◒',capcut:'⋈',adobe:'A',lovable:'♥',gamma:'G',replit:'⊞',n8n:'⌘',notion:'N',nordvpn:'⌁',surfshark:'S',youtube:'▶',netflix:'N',linkedin:'in',windows:'⊞'};
  const categoryIcons = {'AI Assistants':'✳','AI Video':'▷',Design:'◈',Development:'⌘',Productivity:'▤','AI Voice':'∿','VPN & Security':'◇',Entertainment:'▶',Business:'↗',Software:'⊞'};
  const categories = [...new Set(products.map(p => p.category))];
  let cart = {};
  try { const stored = JSON.parse(localStorage.getItem('atz-cart-v1') || '{}'); if (stored && typeof stored === 'object' && !Array.isArray(stored)) products.forEach(p => {if(Number.isInteger(stored[p.id]) && stored[p.id] > 0) cart[p.id] = Math.min(99, stored[p.id]);}); } catch (_) {}
  const selected = new Set();
  let category = 'All tools', expanded = false, toastTimer, lastFocus;
  const modalHistory = [];
  let finderChoices = {intent:'writing', budget:'3000', access:'all'};
  const modal = $('#modal'), content = $('#modal-content');
  const mark = p => `<span class="tool-mark mark-${p.id}" aria-hidden="true">${marks[p.id] || '✳'}</span>`;
  const waUrl = text => `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;
  const singleMessage = p => `Assalam-o-Alaikum AI Tools Zone!\nI would like to order:\n\n${p.name}\nListed price: ${money(p.price)}\nDuration: ${p.duration}\nAccess: ${p.access}\nDelivery estimate: ${p.delivery}\nReplacement warranty: ${p.warranty}\n\nPlease confirm availability, plan limits, final price and payment details.`;
  const waLink = (message, text, classes = 'button button-lime') => `<a class="${classes}" href="${escape(waUrl(message))}" target="_blank" rel="noopener noreferrer">${text} <span>↗</span></a>`;
  $$('[data-wa]').forEach(a => {a.href = waUrl(a.dataset.wa);a.target = '_blank';a.rel = 'noopener noreferrer';});
  $('#year').textContent = new Date().getFullYear();
  const backButton = document.createElement('button');
  backButton.className = 'modal-back';
  backButton.dataset.modalBack = '';
  backButton.textContent = '← Back';
  backButton.hidden = true;
  $('.modal-top').prepend(backButton);
  const modalStatus = document.createElement('div');
  modalStatus.className = 'modal-status';
  modalStatus.setAttribute('role','status');
  modalStatus.setAttribute('aria-live','polite');
  modal.append(modalStatus);
  function toast(message) {
    clearTimeout(toastTimer);
    if(modal.open) {modalStatus.textContent=message;$('#toast').classList.remove('visible');modalStatus.scrollIntoView({block:'nearest'});}
    else {$('#toast').textContent=message;$('#toast').classList.add('visible');}
    toastTimer=setTimeout(()=>{$('#toast').classList.remove('visible');},2700);
  }
  function persist() {try {localStorage.setItem('atz-cart-v1', JSON.stringify(cart));} catch (_) {} $$('.cart-count').forEach(el => el.textContent = Object.values(cart).reduce((a,b) => a+b,0));}
  function add(id, silent = false) {if (!products.some(p => p.id === id)) return;if(cart[id]>=99){if(!silent)toast('Maximum 99 of each tool per order');return;} cart[id] = (cart[id] || 0)+1;persist();if(!silent) toast(`${products.find(p => p.id === id).name} added to your bag`);}
  function openModal(html, type = '', remember = false) {
    if (!modal.open) {lastFocus=document.activeElement;modalHistory.length=0;}
    else if(remember) modalHistory.push({html:content.innerHTML,type:modal.className,scroll:modal.scrollTop});
    modal.className=type;content.innerHTML=html;modalStatus.textContent='';backButton.hidden=!modalHistory.length;
    if(!modal.open)modal.showModal();document.body.style.overflow='hidden';modal.scrollTop=0;
    const title=$('#modal-title');if(title){title.tabIndex=-1;title.focus({preventScroll:true});}
  }
  function closeModal() {modal.close();}
  modal.addEventListener('close', () => {document.body.style.overflow = '';modalHistory.length=0;modalStatus.textContent='';lastFocus?.focus?.({preventScroll:true});});
  $('.close-modal').addEventListener('click', closeModal);
  modal.addEventListener('click', e => {if(e.target === modal){const r = modal.getBoundingClientRect();if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) closeModal();}});
  function renderTabs() {const focused=document.activeElement?.dataset.category;$('#category-tabs').innerHTML = ['All tools',...categories].map(c => `<button data-category="${escape(c)}" class="${category === c ? 'active' : ''}" aria-pressed="${category === c}">${escape(c)}</button>`).join('');if(focused)$$('[data-category]').find(el=>el.dataset.category===focused)?.focus({preventScroll:true});}
  function card(p) {return `<article class="product-card" data-product="${p.id}"><div class="product-card-top">${mark(p)}<span class="badge ${['Best Seller','Best Value','Trending'].includes(p.badge)?'accent':''}">${escape(p.badge)}</span></div><div class="product-category">${escape(p.category)}</div><h3><button data-detail="${p.id}">${escape(p.name)}</button></h3><p>${escape(p.description)}</p><div class="plan-meta"><span>${escape(p.duration)}</span><span>${escape(p.access)}</span></div><div class="card-price"><small>PKR</small> ${p.price.toLocaleString('en-PK')}<del aria-label="Previously ${money(p.oldPrice)}">${p.oldPrice.toLocaleString('en-PK')}</del></div><div class="card-actions"><button class="button" data-add="${p.id}" aria-label="Add ${escape(p.name)} to bag">Add to bag <span>＋</span></button><button class="details-button" data-detail="${p.id}" aria-label="View ${escape(p.name)} details">↗</button></div><label class="card-compare"><input type="checkbox" data-compare="${p.id}" ${selected.has(p.id)?'checked':''}> Compare tool</label></article>`;}
  function renderProducts() {
    const query = $('#search').value.trim().toLowerCase(), access = $('#access-filter').value;
    const budget = $('#budget-filter').value === '' ? Infinity : Math.max(0, Number($('#budget-filter').value));
    let results = products.filter(p => (category === 'All tools' || p.category === category) && (access === 'all' || p.access === access) && p.price <= budget && `${p.name} ${p.category} ${p.description} ${p.bestFor.join(' ')}`.toLowerCase().includes(query));
    const sort = $('#sort').value;
    if(sort === 'price-low') results.sort((a,b)=>a.price-b.price);
    if(sort === 'price-high') results.sort((a,b)=>b.price-a.price);
    if(sort === 'name') results.sort((a,b)=>a.name.localeCompare(b.name));
    const filtered = query || category !== 'All tools' || access !== 'all' || budget !== Infinity || sort !== 'featured';
    const visible = expanded || filtered ? results : results.slice(0,8);
    $('#result-count').textContent = `Showing ${visible.length} of ${results.length} tools`;
    $('#product-grid').innerHTML = visible.length ? visible.map(card).join('') : `<div class="empty-state"><div class="empty-icon">⌕</div><h3>No tools found. New possibilities await.</h3><p>Try another search or reset your filters.</p><button class="button button-outline" data-reset>Reset all filters ↺</button></div>`;
    $('#show-more').hidden = filtered || results.length <= 8;
    $('#show-more').innerHTML = expanded ? 'Show featured tools <span>↑</span>' : 'Explore all 20 tools <span>↗</span>';
  }
  function resetFilters() {category='All tools';$('#search').value='';$('#sort').value='featured';$('#access-filter').value='all';$('#budget-filter').value='';expanded=false;renderTabs();renderProducts();}
  function chooseCategory(c) {category=c;renderTabs();renderProducts();}
  function details(id) {
    const p = products.find(p=>p.id===id);if(!p)return;
    openModal(`<div class="detail-heading">${mark(p)}<div><div class="eyebrow">${escape(p.category)}</div><h2 id="modal-title">${escape(p.name)}</h2></div></div><p>${escape(p.description)}</p><div class="detail-price">${money(p.price)} <small>for ${escape(p.duration)}</small></div><div class="detail-specs"><div><small>ACCESS TYPE</small><b>${escape(p.access)}</b></div><div><small>DURATION / ALLOWANCE</small><b>${escape(p.duration)}</b></div><div><small>DELIVERY ESTIMATE</small><b>${escape(p.delivery)}</b></div><div><small>REPLACEMENT WARRANTY</small><b>${escape(p.warranty)}</b></div></div><h3>What’s in your toolkit</h3><ul class="feature-list">${p.features.map(f=>`<li>${escape(f)}</li>`).join('')}</ul><p class="modal-note">Plan features and usage limits are subject to the selected offer. Confirm the current limits, eligibility and availability with us before payment.</p><div class="modal-actions">${waLink(singleMessage(p),'Order on WhatsApp')}<button class="button button-outline" data-add="${p.id}">Add to bag ＋</button><button class="button button-outline" data-cart>View bag ↗</button></div>`, '', modal.open);
  }
  function renderCart(remember = false) {
    const entries = products.filter(p=>cart[p.id]);
    const total = entries.reduce((n,p)=>n+p.price*cart[p.id],0);
    const message = `Assalam-o-Alaikum AI Tools Zone!\nI would like to order:\n\n${entries.map(p=>`${cart[p.id]} × ${p.name} — ${money(p.price*cart[p.id])}\n${p.duration} | ${p.access} | Warranty: ${p.warranty}`).join('\n\n')}\n\nEstimated total: ${money(total)}\nPlease confirm availability, final price, plan limits and payment details.`;
    openModal(`<h2 id="modal-title">Your creative stack.</h2><p>A few good tools. A lot of possibilities.</p>${entries.length ? `<div class="cart-items">${entries.map(p=>`<article class="cart-item">${mark(p)}<div class="cart-item-details"><h3>${escape(p.name)}</h3><small>${escape(p.duration)} · ${escape(p.access)}</small><div class="quantity"><button data-quantity="${p.id}" data-change="-1" aria-label="Decrease ${escape(p.name)} quantity">−</button><span>${cart[p.id]}</span><button data-quantity="${p.id}" data-change="1" aria-label="Increase ${escape(p.name)} quantity" ${cart[p.id]>=99?'disabled':''}>+</button><button class="remove-item" data-remove="${p.id}">Remove</button></div></div><span class="cart-item-price">${money(p.price*cart[p.id])}</span></article>`).join('')}</div><div class="cart-total"><span>Estimated total</span><strong>${money(total)}</strong></div>${waLink(message,'Order on WhatsApp','button button-lime cart-checkout')}<p class="modal-note">WhatsApp opens with your order ready to review and send. Final availability, price and payment are confirmed in chat. No payment is taken here.</p><button class="inline-button" data-explore>Continue exploring ↗</button>` : `<div class="empty-state"><div class="empty-icon">＋</div><h3>Your next big thing starts here.</h3><p>Your bag is empty. Explore the tools and add your favorites.</p><button class="button button-lime" data-explore>Explore the tools ↗</button></div>`}`, 'cart-dialog', remember);
  }
  function refreshCart(selector) {
    const scroll=modal.scrollTop;renderCart();
    const control=$(selector,content)||$('[data-quantity]',content)||$('[data-explore]',content);
    if(control && !control.disabled)control.focus({preventScroll:true});
    else $('#modal-title')?.focus({preventScroll:true});
    modal.scrollTop=scroll;
  }
  function exploreAll() {
    resetFilters();expanded=true;renderProducts();
    const go=()=>{$('#marketplace').scrollIntoView();$('#search').focus({preventScroll:true});};
    if(modal.open){modal.addEventListener('close',go,{once:true});closeModal();}else go();
  }
  function updateCompare() {
    $('#compare-bar').hidden=!selected.size;$('#compare-count').textContent=selected.size;
    $$('[data-compare]').forEach(input=>input.checked=selected.has(input.dataset.compare));
    const count=$('#picker-count'),run=$('#picker-run');
    if(count)count.textContent=`${selected.size} of 3 selected`;
    if(run)run.disabled=selected.size<2;
  }
  function comparePicker() {
    openModal(`<h2 id="modal-title">Choose your contenders.</h2><p>Select 2 or 3 tools to compare prices, access and features.</p><div class="compare-picker">${products.map(p=>`<label class="compare-choice">${mark(p)}<span><b>${escape(p.name)}</b><small>${money(p.price)} · ${escape(p.duration)}</small></span><input type="checkbox" data-compare="${p.id}" aria-label="Compare ${escape(p.name)}" ${selected.has(p.id)?'checked':''}></label>`).join('')}</div><div class="picker-actions"><span id="picker-count" aria-live="polite"></span><button class="button button-lime" id="picker-run" data-open-compare>Compare selected ↗</button></div>`);
    updateCompare();
  }
  function renderCompare() {
    const list=products.filter(p=>selected.has(p.id));
    if(list.length<2){comparePicker();return;}
    const row=(label,fn)=>`<tr><td>${label}</td>${list.map(p=>`<td>${fn(p)}</td>`).join('')}</tr>`;
    openModal(`<h2 id="modal-title">Find your best fit.</h2><p>Your selected tools, side by side. Different durations are shown so you can compare fairly.</p><button class="button button-outline button-small" data-edit-compare>Change tools</button><div class="compare-table-wrap"><table class="compare-table"><thead><tr><th scope="col">The details</th>${list.map(p=>`<th scope="col">${mark(p)}<br>${escape(p.name)}</th>`).join('')}</tr></thead><tbody>${row('Listed price',p=>money(p.price))}${row('Duration / allowance',p=>escape(p.duration))}${row('Access',p=>escape(p.access))}${row('Best for',p=>escape(p.bestFor.join(', ')))}${row('Delivery estimate',p=>escape(p.delivery))}${row('Replacement warranty',p=>escape(p.warranty))}${row('Features',p=>p.features.map(escape).join('<br>'))}${row('Your next step',p=>`<button class="button button-lime" data-detail="${p.id}">View plan ↗</button>`)}</tbody></table></div>`, 'wide');
  }
  function finder() {
    openModal(`<h2 id="modal-title">Let’s find your zone.</h2><p>Three choices. A toolkit that fits the way you work.</p><form id="finder-form"><div class="finder-fields"><label><span><b>01</b> What do you want to do?</span><select name="intent"><option value="writing">Write & create content</option><option value="video">Make & edit videos</option><option value="design">Design & generate images</option><option value="code">Build apps & websites</option><option value="study">Study & research</option><option value="voice">Create voices & audio</option><option value="automation">Automate my workflow</option><option value="business">Grow my business</option><option value="entertainment">Stream & unwind</option><option value="vpn">Browse privately</option></select></label><label><span><b>02</b> Your total budget for one plan?</span><select name="budget"><option value="1500">Up to PKR 1,500</option><option value="3000" selected>Up to PKR 3,000</option><option value="7000">Up to PKR 7,000</option><option value="any">Any budget</option></select></label><label><span><b>03</b> Your preferred access?</span><select name="access"><option value="all">Show me all options</option><option value="Private">Private access only</option><option value="Invitation">Invitation / team access</option><option value="Shared">Shared access</option></select></label></div><button class="button button-lime" type="submit">Find my tools <span>✳</span></button></form>`);
  }
  content.addEventListener('submit',e=>{
    if(e.target.id!=='finder-form')return;e.preventDefault();
    const data=new FormData(e.target),intent=data.get('intent'),budget=data.get('budget')==='any'?Infinity:Number(data.get('budget')),access=data.get('access');
    finderChoices={intent,budget:data.get('budget'),access};
    const result=products.filter(p=>p.intent.includes(intent)&&(intent!=='video'||p.category!=='Entertainment')&&p.price<=budget&&(access==='all'||p.access===access)).sort((a,b)=>a.price-b.price).slice(0,4);
    openModal(`<h2 id="modal-title">${result.length?'Welcome to your zone.':'Let’s widen the possibilities.'}</h2><p>${result.length?'These tools match your workflow, access preference and total plan budget.':'No tools match all three choices. Try a higher budget or another access type.'}</p>${result.map(p=>`<div class="finder-result">${mark(p)}<div><h3>${escape(p.name)}</h3><small>${money(p.price)} · ${escape(p.duration)} · ${escape(p.access)}</small></div><button class="button button-outline" data-detail="${p.id}">View ↗</button></div>`).join('')}<div class="modal-actions"><button class="button button-outline" data-finder>Try again ↺</button>${waLink('Hi AI Tools Zone! Please help me choose a tool for '+intent+(budget===Infinity?' with no fixed budget.':' with a total plan budget of '+money(budget)+'.'),'Ask a human')}</div>`);
  });
  $('#category-grid').innerHTML=categories.map(c=>`<button class="category-card" data-browse-category="${escape(c)}"><span class="category-icon">${categoryIcons[c]}</span><h3>${escape(c)}</h3><small>${products.filter(p=>p.category===c).length} tools</small><span aria-hidden="true">↗</span></button>`).join('');
  document.addEventListener('click',e=>{
    const target=e.target.closest('button,a');if(!target)return;
    if(target.hasAttribute('data-add'))add(target.dataset.add);
    if(target.hasAttribute('data-detail'))details(target.dataset.detail);
    if(target.hasAttribute('data-cart'))renderCart(modal.open && modal.className !== 'cart-dialog');
    if(target.hasAttribute('data-finder')){finder();Object.entries(finderChoices).forEach(([name,value])=>{$(`[name="${name}"]`,content).value=value;});}
    if(target.hasAttribute('data-open-compare'))renderCompare();
    if(target.hasAttribute('data-edit-compare'))comparePicker();
    if(target.hasAttribute('data-modal-back')){
      const previous=modalHistory.pop();if(previous){openModal(previous.html,previous.type);modal.scrollTop=previous.scroll;updateCompare();}
    }
    if(target.hasAttribute('data-explore'))exploreAll();
    if(target.matches('footer a[href="#marketplace"]')){e.preventDefault();exploreAll();}
    if(target.matches('a[href="#refund-policy"]'))$('#refund-policy').open=true;
    if(target.hasAttribute('data-close'))closeModal();
    if(target.hasAttribute('data-reset'))resetFilters();
    if(target.hasAttribute('data-category'))chooseCategory(target.dataset.category);
    if(target.hasAttribute('data-browse-category')){resetFilters();chooseCategory(target.dataset.browseCategory);$('#marketplace').scrollIntoView();}
    if(target.hasAttribute('data-quantity')){const id=target.dataset.quantity,change=target.dataset.change;cart[id]=Math.max(0,Math.min(99,(cart[id]||0)+Number(change)));if(!cart[id])delete cart[id];persist();refreshCart(`[data-quantity="${id}"][data-change="${change}"]`);}
    if(target.hasAttribute('data-remove')){delete cart[target.dataset.remove];persist();refreshCart('[data-remove]');}
    if(target.hasAttribute('data-privacy'))openModal(`<h2 id="modal-title">Your privacy matters.</h2><p>This site stores your shopping bag in your browser’s local storage so it can be restored on your next visit. It does not collect payments, passwords or account details through a website form.</p><p>Google Fonts may receive your IP address when fonts load. When you open a WhatsApp link, your selected order information is included in the link. You choose whether to send the message. WhatsApp processes that interaction under its own privacy policy.</p><p>Information you send in a support conversation is used to discuss and fulfill your request. For privacy questions, contact AI Tools Zone at +92 313 6726285.</p><button class="button button-outline" id="clear-local">Clear saved shopping bag</button>`);
    if(target.id==='clear-local'){cart={};persist();toast('Your saved shopping bag has been cleared');}
  });
  document.addEventListener('change',e=>{if(!e.target.matches('[data-compare]'))return;const id=e.target.dataset.compare;if(e.target.checked){if(selected.size>=3){e.target.checked=false;toast('Compare up to 3 tools at a time');return;}selected.add(id);}else selected.delete(id);updateCompare();});
  $('#search').addEventListener('input',renderProducts);
  $('#budget-filter').addEventListener('input',renderProducts);
  $('#sort').addEventListener('change',renderProducts);
  $('#access-filter').addEventListener('change',renderProducts);
  $('#reset-filters').addEventListener('click',resetFilters);
  $('#filter-toggle').addEventListener('click',()=>{const open=$('#advanced-filters').hidden;$('#advanced-filters').hidden=!open;$('#filter-toggle').setAttribute('aria-expanded',open);});
  $('#show-more').addEventListener('click',()=>{expanded=!expanded;renderProducts();if(!expanded)$('#marketplace').scrollIntoView();});
  $('#clear-compare').addEventListener('click',()=>{selected.clear();updateCompare();});
  $('#add-stack').addEventListener('click',()=>{['chatgpt','canva','capcut','elevenlabs'].forEach(id=>add(id,true));renderCart();toast('Your creator stack is ready');});
  function setMenu(open) {$('#main-nav').classList.toggle('open',open);$('#menu-toggle').setAttribute('aria-expanded',String(open));$('#menu-toggle').setAttribute('aria-label',open?'Close menu':'Open menu');$('#menu-toggle').textContent=open?'×':'☰';}
  $('#menu-toggle').addEventListener('click',()=>setMenu(!$('#main-nav').classList.contains('open')));
  $$('#main-nav a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
  document.addEventListener('click',e=>{if(!e.target.closest('#main-nav,#menu-toggle'))setMenu(false);});
  matchMedia('(max-width: 640px)').addEventListener('change',()=>setMenu(false));
  document.addEventListener('keydown',e=>{if(e.key==='/' && !modal.open && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('#marketplace').scrollIntoView();$('#search').focus({preventScroll:true});}if(e.key==='Escape'){const wasOpen=$('#main-nav').classList.contains('open');setMenu(false);if(wasOpen)$('#menu-toggle').focus();}});
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  $('#product-grid').addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||reduced.matches)return;const card=e.target.closest('.product-card');if(!card)return;const r=card.getBoundingClientRect();card.style.transform=`perspective(850px) rotateX(${-(e.clientY-r.top-r.height/2)/r.height*5}deg) rotateY(${(e.clientX-r.left-r.width/2)/r.width*5}deg) translateY(-4px)`;});
  $('#product-grid').addEventListener('pointerout',e=>{const card=e.target.closest('.product-card');if(card&&!card.contains(e.relatedTarget))card.style.transform='';});
  // Open policy disclosures when arriving from the footer or a bookmarked link.
  function openHash(){if(location.hash==='#refund-policy')$('#refund-policy').open=true;}
  window.addEventListener('hashchange',openHash);openHash();
  persist();renderTabs();renderProducts();
})();
