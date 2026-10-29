'use strict';

// Product concepts are intentionally separate from measured research results.
// All internal links resolve beneath either '/' locally or '/simworld/' on Pages.
const base = new URL('.', document.baseURI);
const contentVersion = document.querySelector('meta[name="simworld-content-version"]')?.content || '1';
const byId = id => document.getElementById(id);
const categories = {
  foundation: {label:'Tooling extensions', description:'Closest to the current foundation'},
  physical: {label:'Physical models', description:'Requires validated physical layers'},
  worlds: {label:'Worlds and agents', description:'Long-range research dependencies'},
};
let catalog = null;
let category = 'all';
let selected = new Set();
let lastFocus = null;
let noticeTimer;

function escape(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}
function local(path) { return new URL(path.replace(/^\/+/, ''), base).href; }
function announce(message) {
  const toast = byId('portfolio-message');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(noticeTimer);
  noticeTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}
function phaseLinks(product, clickable=false) {
  const chips = product.phases.map(id => clickable
    ? `<a class="phase-chip" href="${local(`index.html?phase=${id}#roadmap`)}" aria-label="Phase ${id} in the roadmap">${id}</a>`
    : `<span class="phase-chip">${id}</span>`).join('');
  return `<div class="product-phases"><span>PHASES</span>${chips}</div>`;
}
function updateComparison() {
  const products = catalog.products.filter(product => selected.has(product.id));
  byId('compare-tray').hidden = products.length === 0;
  byId('compare-count').textContent = `${products.length} of 3 concepts selected`;
  byId('compare-names').textContent = products.map(product => product.name).join(' · ');
  byId('open-comparison').disabled = products.length < 2;
}
function renderProducts() {
  const query = byId('product-search').value.trim().toLowerCase();
  const products = catalog.products.filter(product => (category === 'all' || product.category === category)
    && [product.name,product.tagline,product.audience,product.problem,product.format].join(' ').toLowerCase().includes(query));
  byId('product-count').textContent = `${products.length} of ${catalog.products.length} product concepts`;
  byId('reset-products').hidden = category === 'all' && !query;
  byId('product-grid').innerHTML = products.length ? products.map(product => {
    const index = catalog.products.findIndex(item => item.id === product.id) + 1;
    return `<article class="product-card" data-category="${product.category}">
      <div class="product-card-top"><span class="product-index">${String(index).padStart(2,'0')}</span><span class="product-tier">${categories[product.category].description}</span></div>
      <div class="product-body"><p class="product-format">${escape(product.format)}</p><h3>${escape(product.name)}</h3><p class="product-tagline">${escape(product.tagline)}</p>
      <dl class="product-audience"><dt>Intended users</dt><dd>${escape(product.audience)}</dd></dl>${phaseLinks(product)}</div>
      <div class="product-footer"><button class="explore-product" data-product="${product.id}" aria-label="Explore ${escape(product.name)}">Explore concept ↗</button>
      <label class="compare-label"><input type="checkbox" data-compare="${product.id}" ${selected.has(product.id)?'checked':''} aria-label="Compare ${escape(product.name)}">Compare</label></div></article>`;
  }).join('') : '<p class="portfolio-empty">No concepts match this search. Try another term or reset the filters.</p>';
  document.querySelectorAll('[data-product]').forEach(button => button.addEventListener('click', () => openProduct(button.dataset.product)));
  document.querySelectorAll('[data-compare]').forEach(input => input.addEventListener('change', () => {
    if (input.checked && selected.size === 3) {
      input.checked = false;
      announce('Compare up to three concepts. Remove one to choose another.');
      return;
    }
    input.checked ? selected.add(input.dataset.compare) : selected.delete(input.dataset.compare);
    updateComparison();
    announce(`${selected.size} concepts selected for comparison`);
  }));
  updateComparison();
}
function openDialog(id) {
  lastFocus = document.activeElement;
  const dialog = byId(id);
  dialog.showModal();
  dialog.scrollTop = 0;
  document.body.style.overflow = 'hidden';
}
function field(title, value) {
  const body = Array.isArray(value) ? `<ul>${value.map(item => `<li>${escape(item)}</li>`).join('')}</ul>` : `<p>${escape(value)}</p>`;
  return `<section class="concept-field"><h3>${title}</h3>${body}</section>`;
}
function openProduct(id) {
  const product = catalog.products.find(item => item.id === id);
  byId('product-dialog-title').textContent = product.name;
  byId('product-dialog-kicker').textContent = `PRODUCT CONCEPT / ${categories[product.category].label.toUpperCase()}`;
  byId('product-dialog-content').innerHTML = `<p class="concept-tagline">${escape(product.tagline)}</p>
    <dl class="concept-meta"><div><dt>Intended users</dt><dd>${escape(product.audience)}</dd></div><div><dt>Possible delivery format</dt><dd>${escape(product.format)}</dd></div></dl>
    <div class="concept-fields">${field('The user problem',product.problem)}${field('First proposed scope',product.firstRelease)}${field('How it could be used',product.experience)}${field('What it would produce',product.output)}${field('Current foundation',product.foundation)}${field('What must be built',product.requirements)}${field('Evidence before release',product.validation)}</div>
    <p class="concept-boundary"><strong>Scope and limits.</strong> ${escape(product.boundary)}</p>
    <div class="concept-links">${phaseLinks(product,true)}<a class="inline-link" href="${local('index.html#downloads')}">Read the research and evidence ↗</a></div>`;
  openDialog('product-dialog');
}
function openComparison() {
  const products = catalog.products.filter(product => selected.has(product.id));
  if (products.length < 2) return;
  const rows = [['Intended users','audience'],['Possible format','format'],['First proposed scope','firstRelease'],['Current foundation','foundation'],['Missing capabilities','requirements'],['Validation gate','validation'],['Scope and limits','boundary']];
  byId('comparison-content').innerHTML = `<p class="comparison-note">All entries are proposed products. Dependency groups do not imply delivery dates. On a small screen, scroll the table horizontally.</p><table class="comparison-table" aria-label="Product concept comparison"><thead><tr><th scope="col">Concept</th>${products.map(product => `<th scope="col">${escape(product.name)}</th>`).join('')}</tr></thead><tbody>
    <tr><th scope="row">Development path</th>${products.map(product => `<td>${categories[product.category].description}</td>`).join('')}</tr>
    ${rows.map(([label,key]) => `<tr><th scope="row">${label}</th>${products.map(product => `<td>${escape(Array.isArray(product[key]) ? product[key].join('; ') : product[key])}</td>`).join('')}</tr>`).join('')}
    <tr><th scope="row">Source phases</th>${products.map(product => `<td>${product.phases.join(', ')}</td>`).join('')}</tr></tbody></table>`;
  openDialog('comparison-dialog');
}
function renderPrintableCatalog() {
  byId('print-catalog').innerHTML = `<h1>SimWorld possible products</h1><p>Concept portfolio · ${escape(catalog.updated)}. All products are proposals. The current release is a research prototype.</p>
    ${catalog.products.map(product => `<article class="print-product"><h2>${escape(product.name)}</h2><p>${escape(product.tagline)}</p><p><strong>Development path:</strong> ${categories[product.category].description}.</p><p><strong>Users:</strong> ${escape(product.audience)}. <strong>Possible format:</strong> ${escape(product.format)}.</p><p><strong>Problem:</strong> ${escape(product.problem)}</p><p><strong>First proposed scope:</strong> ${escape(product.firstRelease)}</p><p><strong>Workflow:</strong> ${escape(product.experience)}</p><p><strong>Output:</strong> ${escape(product.output)}</p><p><strong>Foundation:</strong> ${escape(product.foundation)}</p><p><strong>Needed:</strong> ${escape(product.requirements.join('; '))}</p><p><strong>Validation:</strong> ${escape(product.validation)}</p><p><strong>Limits:</strong> ${escape(product.boundary)}</p><p><strong>Phases:</strong> ${product.phases.join(', ')}.</p></article>`).join('')}`;
}
function resetFilters() {
  category = 'all';
  byId('product-search').value = '';
  document.querySelectorAll('[data-category]').forEach(button => {
    if (button.tagName !== 'BUTTON') return;
    const active = button.dataset.category === 'all';
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  renderProducts();
  byId('product-search').focus();
}
document.querySelectorAll('.portfolio-filters button').forEach(button => button.addEventListener('click', () => {
  category = button.dataset.category;
  document.querySelectorAll('.portfolio-filters button').forEach(item => {
    const active = item === button;
    item.classList.toggle('active',active);
    item.setAttribute('aria-pressed',String(active));
  });
  if (catalog) renderProducts();
}));
byId('product-search').addEventListener('input', () => catalog && renderProducts());
byId('reset-products').addEventListener('click', resetFilters);
byId('clear-comparison').addEventListener('click', () => {
  selected.clear(); renderProducts(); announce('Comparison cleared');
  document.querySelector('.portfolio-filters button[aria-pressed="true"]').focus();
});
byId('open-comparison').addEventListener('click', openComparison);
byId('close-product').addEventListener('click', () => byId('product-dialog').close());
byId('close-comparison').addEventListener('click', () => byId('comparison-dialog').close());
for (const id of ['product-dialog','comparison-dialog']) {
  byId(id).addEventListener('close', () => {
    document.body.style.overflow = '';
    if (lastFocus?.isConnected) lastFocus.focus();
  });
}
byId('print-portfolio').addEventListener('click', () => {
  if (catalog) window.print(); else announce('The catalog is still loading.');
});
const menu = document.querySelector('.menu-toggle');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  byId('navigation').classList.toggle('open', open);
});
fetch(local(`data/products.json?v=${encodeURIComponent(contentVersion)}`))
  .then(response => { if (!response.ok) throw new Error('Could not load the concept catalog.'); return response.json(); })
  .then(data => { catalog=data; renderProducts(); renderPrintableCatalog(); })
  .catch(error => { byId('product-count').textContent='Catalog unavailable'; byId('product-grid').innerHTML='<p class="portfolio-empty">Please refresh the page or download the concept catalog using the link below.</p>'; console.error(error); });
