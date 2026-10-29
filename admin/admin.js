(() => {
  'use strict';

  const OWNER = 'su92-bsaim-f24-127-hue';
  const REPO = 'ai-tools-zone';
  const BRANCH = 'main';
  const API = 'https://api.github.com';
  const FILES = ['data/catalog.json', 'assets/product-logo-sources.json', 'data/site-settings.json', 'data/seo-contract.json', 'data/seo-content.json', 'data/blog-content.json'];
  const $ = (query, root = document) => root.querySelector(query);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const money = value => `PKR ${Number(value || 0).toLocaleString('en-PK')}`;
  const phoneDigits = value => String(value || '').replace(/\D/g, '');
  const formatPhone = value => {
    const digits = phoneDigits(value);
    return digits.startsWith('92') && digits.length === 12 ? `+92 ${digits.slice(2,5)} ${digits.slice(5,8)} ${digits.slice(8)}` : `+${digits}`;
  };
  const safeURL = value => {
    try { const url = new URL(value); return url.protocol === 'https:' && url.hostname.includes('.') ? url.href : ''; }
    catch { return ''; }
  };

  let token = '';
  let baseSha = '';
  let data = null;
  let activePanel = 'overview';
  let dirty = false;
  let pendingDeletes = new Set();
  let toastTimer = 0;

  function showToast(message, isError = false) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.classList.toggle('error', isError);
    toast.hidden = false;
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => { toast.hidden = true; }, 4200);
  }

  function showLoginError(message) {
    const error = $('#login-error');
    error.textContent = message;
    error.hidden = false;
  }

  async function github(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: `Bearer ${token}`,
        'X-GitHub-Api-Version': '2022-11-28',
        ...(options.body ? {'Content-Type': 'application/json'} : {}),
        ...options.headers,
      },
    });
    const raw = await response.text();
    let payload = {};
    try { payload = raw ? JSON.parse(raw) : {}; } catch { payload = {message: raw}; }
    if (!response.ok) {
      const reason = response.status === 401 || response.status === 403
        ? 'GitHub rejected this token or it does not have Contents read/write permission for this repository.'
        : (payload.message || `GitHub returned HTTP ${response.status}.`);
      throw new Error(reason);
    }
    return payload;
  }

  function decodeFile(content) {
    const binary = atob(String(content || '').replace(/\s/g, ''));
    const bytes = Uint8Array.from(binary, char => char.charCodeAt(0));
    return JSON.parse(new TextDecoder().decode(bytes));
  }

  async function loadFile(path) {
    const file = await github(`/repos/${OWNER}/${REPO}/contents/${path}?ref=${encodeURIComponent(baseSha)}`);
    return decodeFile(file.content);
  }

  async function connect(githubToken) {
    token = githubToken.trim();
    if (!token) throw new Error('Paste a fine-grained GitHub token to connect.');
    const repo = await github(`/repos/${OWNER}/${REPO}`);
    if (repo.default_branch !== BRANCH) throw new Error(`Expected repository branch ${BRANCH}; found ${repo.default_branch}.`);
    const ref = await github(`/repos/${OWNER}/${REPO}/git/ref/heads/${BRANCH}`);
    baseSha = ref.object.sha;
    const values = await Promise.all(FILES.map(loadFile));
    data = {
      products: values[0],
      logos: values[1],
      settings: values[2],
      contract: values[3],
      seoContent: values[4],
      blogContent: values[5],
      activeCategories: [...new Set(values[0].map(product => product.category))].sort((a,b) => a.localeCompare(b)),
    };
    validateLoadedData();
    $('#repo-label').textContent = `${OWNER}/${REPO} · ${BRANCH}`;
    $('#login-shell').hidden = true;
    $('#workspace').hidden = false;
    renderAll();
    showToast('Connected. No changes have been published yet.');
  }

  function validateLoadedData() {
    if (!Array.isArray(data.products) || !data.products.length) throw new Error('The repository catalog is empty or has an unsupported format.');
    if (!data.logos || !data.settings || !data.contract || !Array.isArray(data.contract.routes)) throw new Error('A required admin source file has an unsupported format.');
    for (const product of data.products) {
      if (!data.logos[product.id]?.path || !data.logos[product.id]?.website) throw new Error(`The logo/vendor mapping for ${product.name || product.id} is missing.`);
    }
  }

  function activeProducts() { return data.products.filter(product => product.active !== false); }
  function markDirty(message = 'Unsaved changes') {
    dirty = true;
    $('#publish-bar').hidden = false;
    $('#dirty-label').textContent = message;
  }

  function renderAll() {
    renderOverview();
    renderProductTable();
    renderSettings();
    $('#nav-product-count').textContent = String(activeProducts().length);
    showPanel(activePanel);
  }

  function renderOverview() {
    const active = activeProducts();
    const archived = data.products.length - active.length;
    const values = [
      ['Active listings', active.length, 'Visible in the storefront', '◈'],
      ['Archived', archived, 'Old routes remain available', '↗'],
      ['Catalog categories', new Set(active.map(product => product.category)).size, 'Active categories', '▧'],
      ['Listed value', money(active.reduce((sum, product) => sum + Number(product.price || 0), 0)), 'Sum of active listing prices', '₨'],
    ];
    $('#stats-grid').innerHTML = values.map(([label,value,caption,icon]) => `<article class="stat-card"><div class="stat-top"><span>${esc(label)}</span><span class="stat-icon" aria-hidden="true">${esc(icon)}</span></div><b class="stat-value">${esc(value)}</b><small class="stat-caption">${esc(caption)}</small></article>`).join('');
    $('#recent-list').innerHTML = [...data.products].slice(-5).reverse().map(product => `<div class="recent-item"><div><b>${esc(product.name)}</b><small>${esc(product.category)} · ${esc(product.duration)}</small></div><span class="amount">${money(product.price)}</span><span class="status-pill ${product.active === false ? 'archived' : ''}">${product.active === false ? 'Archived' : 'Active'}</span></div>`).join('') || '<p class="empty-state">No listings yet.</p>';
  }

  function priceCells(product) {
    const regular = Number(product.regularPrice);
    const prior = Number.isInteger(regular) && regular > Number(product.price) ? `<del>${money(regular)}</del>` : '';
    return `<span class="price-cell"><b>${money(product.price)}</b>${prior}</span>`;
  }

  function renderProductTable() {
    if (!data) return;
    const query = ($('#product-search')?.value || '').trim().toLowerCase();
    const status = $('#status-filter')?.value || 'all';
    const filtered = [...data.products].filter(product => {
      const isActive = product.active !== false;
      const statusMatch = status === 'all' || (status === 'active' ? isActive : !isActive);
      return statusMatch && `${product.name} ${product.id} ${product.category} ${product.slug}`.toLowerCase().includes(query);
    }).sort((a,b) => Number(b.active !== false) - Number(a.active !== false) || a.name.localeCompare(b.name));
    $('#products-table').innerHTML = filtered.map(product => {
      const logo = data.logos[product.id];
      const discount = Number.isInteger(Number(product.regularPrice)) && Number(product.regularPrice) > Number(product.price)
        ? ` · ${Math.round((product.regularPrice-product.price)*100/product.regularPrice)}% off` : '';
      return `<tr><td><div class="product-cell"><img src="../${esc(logo.path)}" alt="" width="35" height="35"><div><b>${esc(product.name)}</b><small>${esc(product.id)} · /${esc(product.slug)}/</small></div></div></td><td>${esc(product.category)}</td><td><span class="plan-cell"><b>${esc(product.duration)}</b><small>${esc(product.access)} · ${esc(product.delivery)}</small></span></td><td>${priceCells(product)}<small>${esc(discount)}</small></td><td><span class="status-pill ${product.active === false ? 'archived' : ''}">${product.active === false ? 'Archived' : 'Active'}</span></td><td><div class="row-actions"><button class="icon-action" type="button" data-action="edit-product" data-id="${esc(product.id)}" aria-label="Edit ${esc(product.name)}" title="Edit listing">✎</button><button class="icon-action danger" type="button" data-action="delete-product" data-id="${esc(product.id)}" aria-label="Delete ${esc(product.name)}" title="Delete listing">×</button></div></td></tr>`;
    }).join('');
    $('#empty-products').hidden = filtered.length !== 0;
  }

  function renderSettings() {
    const input = $('#whatsapp-number');
    if (document.activeElement !== input) input.value = data.settings.whatsappNumber || '';
    $('#phone-preview').textContent = formatPhone(input.value || data.settings.whatsappNumber);
  }

  function showPanel(name) {
    activePanel = name;
    for (const panel of ['overview','products','settings']) $(`#${panel}-panel`).hidden = panel !== name;
    for (const button of document.querySelectorAll('[data-panel]')) button.classList.toggle('is-current', button.dataset.panel === name && button.classList.contains('nav-item'));
    $('#page-title').textContent = ({overview:'Overview',products:'Products & plans',settings:'Contact settings'})[name] || 'Overview';
  }

  function inputField(id,label,value,type='text',opts={}) {
    const wide = opts.wide ? ' wide' : '';
    const help = opts.help ? `<small>${opts.help}</small>` : '';
    const req = opts.required ? ' required' : '';
    const min = opts.min != null ? ` min="${opts.min}"` : '';
    const max = opts.max != null ? ` max="${opts.max}"` : '';
    const readOnly = opts.readOnly ? ' readonly' : '';
    return `<div class="field${wide}"><label for="${esc(id)}">${esc(label)}</label><input id="${esc(id)}" name="${esc(id)}" type="${esc(type)}" value="${esc(value)}"${req}${min}${max}${readOnly}>${help}</div>`;
  }

  function textArea(id,label,value,help='') {
    return `<div class="field wide"><label for="${esc(id)}">${esc(label)}</label><textarea id="${esc(id)}" name="${esc(id)}" rows="3">${esc((value || []).join('\n'))}</textarea>${help ? `<small>${esc(help)}</small>` : ''}</div>`;
  }

  function openProductEditor(id = '') {
    const existing = Boolean(id);
    const product = existing ? data.products.find(item => item.id === id) : {
      id:'', name:'', category:data.activeCategories[0] || '', description:'', price:'', duration:'1 Month', access:'Private', delivery:'15–30 min', warranty:'7 Days', badge:'', bestFor:[], features:[], intent:[], slug:'', active:true,
    };
    const logo = existing ? data.logos[id] : {website:'',source:'assets/brand-icon.webp',path:'assets/brand-icon.webp',bytes:0};
    const categories = [...new Set([...data.activeCategories, product.category].filter(Boolean))];
    const logoPaths = [...new Set(['assets/brand-icon.webp', ...Object.values(data.logos).map(item => item.path), logo.path].filter(Boolean))].sort();
    const deleteSafe = existing && canDelete(product);
    const dialog = $('#product-dialog');
    const form = $('#product-form');
    const categoryOptions = categories.map(category => `<option value="${esc(category)}" ${category === product.category ? 'selected' : ''}>${esc(category)}</option>`).join('');
    const logoOptions = logoPaths.map(path => `<option value="${esc(path)}" ${path === logo.path ? 'selected' : ''}>${esc(path)}</option>`).join('');
    const regular = product.regularPrice || '';
    form.innerHTML = `<div class="dialog-head"><div><h2 id="dialog-title">${existing ? 'Edit listing' : 'Add a product listing'}</h2><small>${existing ? 'Product identity and URL are stable; edit the offer details below.' : 'One catalog entry is one seller-listed plan.'}</small></div><button class="icon-action" type="button" data-action="close-editor" aria-label="Close editor">×</button></div>
      <div class="dialog-body"><div class="form-grid">
        ${inputField('id','Product ID',product.id,'text',{required:true,readOnly:existing,help:'Lowercase letters and numbers; permanent identifier.'})}
        ${inputField('slug','URL slug',product.slug,'text',{required:true,readOnly:existing,help:'Keep existing product URLs stable.'})}
        ${inputField('name','Product / plan name',product.name,'text',{required:true})}
        <div class="field"><label for="category">Category</label><select id="category" name="category" required>${categoryOptions}</select><small>Use an existing site category.</small></div>
        ${inputField('price','Current listed price (PKR)',product.price,'number',{required:true,min:1})}
        ${inputField('regularPrice','Regular price before discount (PKR)',regular,'number',{min:1,help:'Leave blank without a real, verified regular price. Never invent a crossed-out price.'})}
        <div id="discount-preview" class="discount-preview field wide" aria-live="polite"></div>
        ${inputField('duration','Duration / allowance',product.duration,'text',{required:true})}
        <div class="field"><label for="access">Access type</label><select id="access" name="access"><option ${product.access==='Private'?'selected':''}>Private</option><option ${product.access==='Shared'?'selected':''}>Shared</option><option ${product.access==='Invitation'?'selected':''}>Invitation</option><option ${product.access==='License Key'?'selected':''}>License Key</option></select></div>
        ${inputField('delivery','Delivery estimate',product.delivery,'text',{required:true})}
        ${inputField('warranty','Replacement coverage',product.warranty,'text',{required:true})}
        ${inputField('badge','Badge (optional)',product.badge || '')}
        ${inputField('vendor','Official vendor URL',logo.website,'url',{required:true,help:'HTTPS provider page. The listing does not imply affiliation.'})}
        <div class="field"><label for="logoPath">Local logo asset</label><select id="logoPath" name="logoPath">${logoOptions}</select><small>New image files must be added to the repository before selecting them here.</small></div>
        ${inputField('logoSource','Logo source URL or asset',logo.source || logo.path,'text',{required:true})}
        ${inputField('description','Product description',product.description,'text',{required:true,wide:true})}
        ${textArea('bestFor','Best for',product.bestFor,'One audience or use case per line.')}
        ${textArea('features','Included plan features',product.features,'Only list offer details the owner can verify.')}
        ${textArea('intent','Search / finder terms',product.intent,'One short term per line; these power catalog search and the tool finder.')}
        <div class="field wide"><div class="field-check"><input id="active" name="active" type="checkbox" ${product.active === false ? '' : 'checked'}><label for="active">Active in the public storefront</label></div><small>Turning this off archives the listing, removes it from the sitemap and keeps its old URL with a noindex page.</small></div>
      </div></div>
      <div class="dialog-actions"><div class="actions-left">${existing ? `<button class="button danger-button" type="button" data-action="delete-from-editor" data-id="${esc(id)}" ${deleteSafe ? '' : 'disabled'} title="${deleteSafe ? 'Permanently delete this unreferenced listing' : 'This listing is referenced by editorial content. Archive it instead.'}">Delete permanently</button>` : '<span></span>'}</div><div class="actions-right"><button class="button button-secondary" type="button" data-action="close-editor">Cancel</button><button class="button button-primary" type="submit">${existing ? 'Save listing' : 'Add listing'}</button></div></div>`;
    form.dataset.editId = existing ? id : '';
    dialog.showModal();
    updateDiscountPreview();
  }

  function formProduct(form) {
    const formData = new FormData(form);
    const splitLines = key => String(formData.get(key) || '').split(/\n|,/).map(value => value.trim()).filter(Boolean);
    const price = Number(formData.get('price'));
    const regularPriceRaw = String(formData.get('regularPrice') || '').trim();
    const product = {
      id:String(formData.get('id') || '').trim().toLowerCase(),
      slug:String(formData.get('slug') || '').trim().toLowerCase(),
      name:String(formData.get('name') || '').trim(),
      category:String(formData.get('category') || '').trim(),
      description:String(formData.get('description') || '').trim(),
      price,
      duration:String(formData.get('duration') || '').trim(),
      access:String(formData.get('access') || '').trim(),
      delivery:String(formData.get('delivery') || '').trim(),
      warranty:String(formData.get('warranty') || '').trim(),
      badge:String(formData.get('badge') || '').trim(),
      bestFor:splitLines('bestFor'),
      features:splitLines('features'),
      intent:splitLines('intent'),
      active:formData.get('active') === 'on',
      logoPath:String(formData.get('logoPath') || ''),
      logoSource:String(formData.get('logoSource') || '').trim(),
      vendor:String(formData.get('vendor') || '').trim(),
    };
    if (regularPriceRaw) product.regularPrice = Number(regularPriceRaw);
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(product.id)) throw new Error('Product ID must use lowercase letters, numbers and hyphens.');
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(product.slug)) throw new Error('URL slug must use lowercase letters, numbers and hyphens.');
    if (!product.name || !product.description || !product.category || !product.duration || !product.delivery || !product.warranty) throw new Error('Complete all required listing fields.');
    if (!Number.isSafeInteger(price) || price < 1) throw new Error('Enter a positive whole-number PKR price.');
    if (product.regularPrice != null && (!Number.isSafeInteger(product.regularPrice) || product.regularPrice <= price)) throw new Error('Regular price must be a whole number greater than the current listed price.');
    if (!safeURL(product.vendor)) throw new Error('Vendor URL must be a valid HTTPS URL.');
    if (!product.logoPath.startsWith('assets/') || !product.logoSource) throw new Error('Choose an existing local logo asset and provide its source.');
    return product;
  }

  function productLogo(product) {
    return {website:product.vendor,source:product.logoSource,path:product.logoPath,bytes:data.logos[product.id]?.bytes || 0};
  }

  function saveProductForm(event) {
    event.preventDefault();
    const form = event.currentTarget;
    try {
      const product = formProduct(form);
      const oldId = form.dataset.editId;
      const existing = oldId ? data.products.find(item => item.id === oldId) : null;
      if (existing && product.slug !== existing.slug) throw new Error('Changing an existing URL is disabled to protect its search and customer links.');
      if (data.products.some(item => item.id === product.id && item.id !== oldId)) throw new Error('That product ID is already in use.');
      if (data.products.some(item => item.slug === product.slug && item.id !== oldId)) throw new Error('That URL slug is already in use.');
      if (!data.activeCategories.includes(product.category)) throw new Error('Choose one of the existing catalog categories.');
      if (existing && existing.active !== false && !product.active && activeProducts().filter(item => item.category === existing.category).length <= 1) throw new Error('Keep at least one active listing in this category. Archive other category listings first.');
      if (existing) {
        if (product.regularPrice == null) delete existing.regularPrice;
        Object.assign(existing, product);
        data.logos[oldId] = productLogo({...product,id:oldId});
      } else {
        data.products.push(product);
        data.logos[product.id] = productLogo(product);
      }
      $('#product-dialog').close();
      markDirty(existing ? 'Listing changes are ready to publish' : 'New listing is ready to publish');
      renderAll();
      showToast(existing ? 'Listing updated in this session.' : 'Listing added to this session.');
    } catch (error) { showToast(error.message, true); }
  }

  function updateDiscountPreview() {
    const price = Number($('#product-form [name="price"]')?.value || 0);
    const regular = Number($('#product-form [name="regularPrice"]')?.value || 0);
    const output = $('#discount-preview');
    if (!output) return;
    output.textContent = Number.isInteger(regular) && regular > price && price > 0
      ? `Displayed discount: ${Math.round((regular-price)*100/regular)}% off (${money(regular)} → ${money(price)}).`
      : 'No discount will display unless a higher verified regular price is entered.';
  }

  function exactReference(value, id) {
    if (typeof value === 'string') return value === id;
    if (Array.isArray(value)) return value.some(item => exactReference(item,id));
    if (value && typeof value === 'object') return Object.values(value).some(item => exactReference(item,id));
    return false;
  }

  function canDelete(product) {
    const referenced = [product.id,product.slug].some(key => exactReference(data.seoContent,key) || exactReference(data.blogContent,key));
    const finalCategoryListing = product.active !== false && activeProducts().filter(item => item.category === product.category).length <= 1;
    return !referenced && !finalCategoryListing;
  }

  function deleteProduct(id) {
    const product = data.products.find(item => item.id === id);
    if (!product) return;
    if (!canDelete(product)) {
      showToast('This listing is referenced by a guide/comparison or is the last active item in its category. Archive it instead.', true);
      return;
    }
    if (!window.confirm(`Permanently delete ${product.name}? This removes its catalog record and URL from the next published build.`)) return;
    pendingDeletes.add(`products/${product.slug}/index.html`);
    data.products = data.products.filter(item => item.id !== id);
    delete data.logos[id];
    markDirty('A listing is marked for permanent removal');
    $('#product-dialog').close();
    renderAll();
    showToast('Listing removed from this session.');
  }

  function validateCatalog() {
    const ids = data.products.map(product => product.id);
    const slugs = data.products.map(product => product.slug);
    if (new Set(ids).size !== ids.length) throw new Error('Duplicate product IDs found.');
    if (new Set(slugs).size !== slugs.length) throw new Error('Duplicate product URL slugs found.');
    const counts = new Map();
    for (const product of activeProducts()) counts.set(product.category,(counts.get(product.category)||0)+1);
    for (const category of data.activeCategories) if (!counts.get(category)) throw new Error(`Category ${category} needs at least one active listing.`);
    for (const product of data.products) {
      if (!data.logos[product.id]?.website || !data.logos[product.id]?.path) throw new Error(`Logo or vendor details are missing for ${product.name}.`);
      if (!Number.isSafeInteger(Number(product.price)) || Number(product.price) < 1) throw new Error(`Invalid price for ${product.name}.`);
      if (product.regularPrice && Number(product.regularPrice) <= Number(product.price)) throw new Error(`Invalid regular price for ${product.name}.`);
    }
  }

  function publishedFiles() {
    const catalog = data.products.map(product => {
      const saved = {...product};
      delete saved.logo; delete saved.vendor; delete saved.orderMessage;
      delete saved.logoPath; delete saved.logoSource;
      if (saved.active !== false) delete saved.active;
      return saved;
    });
    const contract = structuredClone(data.contract);
    const productRoutePattern = /^\/products\/[^/]+\/$/;
    const activeRoutes = activeProducts().map(product => `/products/${product.slug}/`);
    contract.routes = [...new Set(contract.routes.filter(path => !productRoutePattern.test(path)).concat(activeRoutes))].sort((a,b) => a.localeCompare(b));
    contract.expected_pages = contract.routes.length;
    contract.product_slugs = Object.fromEntries([...data.products].sort((a,b)=>a.id.localeCompare(b.id)).map(product => [product.id,product.slug]));
    contract.reason = `Catalog and listing status maintained through the AI Tools Zone admin on ${new Date().toISOString().slice(0,10)}; existing active routes are preserved.`;
    const settings = {...data.settings,whatsappNumber:phoneDigits(data.settings.whatsappNumber)};
    return {
      'data/catalog.json': JSON.stringify(catalog,null,2)+'\n',
      'assets/product-logo-sources.json': JSON.stringify(data.logos,null,2)+'\n',
      'data/site-settings.json': JSON.stringify(settings,null,2)+'\n',
      'data/seo-contract.json': JSON.stringify(contract,null,2)+'\n',
    };
  }

  async function createCommit(files) {
    const ref = await github(`/repos/${OWNER}/${REPO}/git/ref/heads/${BRANCH}`);
    if (ref.object.sha !== baseSha) throw new Error('The repository changed after you opened this admin. Sign out, reconnect, review the latest values, then try again.');
    const parent = await github(`/repos/${OWNER}/${REPO}/git/commits/${baseSha}`);
    const entries = [];
    for (const [path,content] of Object.entries(files)) {
      const blob = await github(`/repos/${OWNER}/${REPO}/git/blobs`, {method:'POST',body:JSON.stringify({content,encoding:'utf-8'})});
      entries.push({path,mode:'100644',type:'blob',sha:blob.sha});
    }
    for (const path of pendingDeletes) entries.push({path,mode:'100644',type:'blob',sha:null});
    const tree = await github(`/repos/${OWNER}/${REPO}/git/trees`, {method:'POST',body:JSON.stringify({base_tree:parent.tree.sha,tree:entries})});
    const commit = await github(`/repos/${OWNER}/${REPO}/git/commits`, {method:'POST',body:JSON.stringify({message:'Admin: update product catalog and store settings',tree:tree.sha,parents:[baseSha]})});
    await github(`/repos/${OWNER}/${REPO}/git/refs/heads/${BRANCH}`, {method:'PATCH',body:JSON.stringify({sha:commit.sha,force:false})});
    baseSha = commit.sha;
    return commit;
  }

  async function publish() {
    if (!dirty) return showToast('There are no pending changes.');
    try {
      validateCatalog();
      const files = publishedFiles();
      const summary = `${data.products.length} catalog listings, WhatsApp contact, discount prices and route contract.`;
      if (!window.confirm(`Publish ${summary}\n\nGitHub Actions will rebuild the site. Continue?`)) return;
      const button = $('[data-action="publish"]');
      button.disabled = true; button.textContent = 'Committing…';
      const commit = await createCommit(files);
      dirty = false; pendingDeletes = new Set();
      $('#publish-bar').hidden = true;
      showToast(`Committed ${commit.sha.slice(0,7)}. GitHub Pages is rebuilding the site.`);
      renderAll();
    } catch (error) { showToast(error.message, true); }
    finally {
      const button = $('[data-action="publish"]');
      if (button) { button.disabled = false; button.innerHTML = 'Save changes to GitHub <span aria-hidden="true">↗</span>'; }
    }
  }

  function logout() {
    if (dirty && !window.confirm('Discard the unpublished changes in this session and sign out?')) return;
    token = '';
    baseSha = '';
    data = null;
    dirty = false;
    pendingDeletes = new Set();
    $('#workspace').hidden = true;
    $('#login-shell').hidden = false;
    $('#github-token').value = '';
    $('#login-error').hidden = true;
    $('#publish-bar').hidden = true;
    $('#products-table').replaceChildren();
    showToast('Signed out. The GitHub token was cleared from this page.');
  }

  $('#connect-form').addEventListener('submit', async event => {
    event.preventDefault();
    $('#login-error').hidden = true;
    const field = $('#github-token');
    const value = field.value;
    field.value = '';
    const button = event.currentTarget.querySelector('button');
    button.disabled = true; button.firstElementChild.textContent = 'Connecting…';
    try { await connect(value); }
    catch (error) { token = ''; showLoginError(error.message); }
    finally { button.disabled = false; button.firstElementChild.textContent = 'Connect repository'; }
  });

  window.addEventListener('beforeunload',event => {
    if (!dirty) return;
    event.preventDefault();
    event.returnValue = '';
  });

  $('#product-search').addEventListener('input',renderProductTable);
  $('#status-filter').addEventListener('change',renderProductTable);
  $('#product-form').addEventListener('submit',saveProductForm);
  $('#product-form').addEventListener('input',event => {if (event.target.name==='price'||event.target.name==='regularPrice') updateDiscountPreview();});
  $('#settings-form').addEventListener('input',renderSettings);
  $('#settings-form').addEventListener('submit',event => {
    event.preventDefault();
    const number = phoneDigits($('#whatsapp-number').value);
    if (number.length < 8 || number.length > 15) return showToast('Enter an international WhatsApp number with 8–15 digits.',true);
    if (number === phoneDigits(data.settings.whatsappNumber)) return showToast('The WhatsApp number has not changed.');
    data.settings.whatsappNumber = number;
    markDirty('WhatsApp contact change is ready to publish');
    renderSettings();
    showToast('Contact updated in this session.');
  });

  document.addEventListener('click',event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.panel) {showPanel(button.dataset.panel);return;}
    const action = button.dataset.action;
    if (action==='logout') logout();
    if (action==='publish') publish();
    if (action==='new-product') openProductEditor();
    if (action==='edit-product') openProductEditor(button.dataset.id);
    if (action==='delete-product'||action==='delete-from-editor') deleteProduct(button.dataset.id);
    if (action==='close-editor') $('#product-dialog').close();
  });

  $('#product-dialog').addEventListener('click',event => {
    if (event.target === event.currentTarget) event.currentTarget.close();
  });
})();
