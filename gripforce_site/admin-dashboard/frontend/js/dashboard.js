// ===== DATA FETCHING =====
let currentTab = 'stats';
let commandesData = { items: [], total: 0 };
let commandesOffset = 0;
let commandesFilter = { status: '', search: '' };

async function loadStats() {
  try {
    const data = await api('/api/stats');
    document.getElementById('stat-ca-total').textContent = formatFCFA(data.ca_total);
    document.getElementById('stat-ca-jour').textContent = formatFCFA(data.ca_jour);
    document.getElementById('stat-cmd-total').textContent = data.total_commandes;
    document.getElementById('stat-cmd-jour').textContent = data.commandes_jour;
    document.getElementById('stat-attente').textContent = data.en_attente;
    document.getElementById('stat-livrer').textContent = data.a_livrer;
    document.getElementById('stat-livrees').textContent = data.livrees;
    document.getElementById('stat-cmd-semaine').textContent = data.commandes_semaine;

    // Badge sidebar
    const badge = document.getElementById('nav-badge-attente');
    if (badge) {
      badge.textContent = data.en_attente;
      badge.style.display = data.en_attente > 0 ? 'inline' : 'none';
    }

    renderRecent(data.recentes || []);
  } catch (e) { console.error(e); }
}

async function loadCommandes() {
  const params = new URLSearchParams({ limit: 20, offset: commandesOffset });
  if (commandesFilter.status) params.set('status', commandesFilter.status);
  if (commandesFilter.search) params.set('search', commandesFilter.search);
  try {
    const data = await api(`/api/commandes?${params}`);
    commandesData = data;
    renderCommandesTable();
    renderPagination();
  } catch (e) { console.error(e); }
}

async function loadPaiements() {
  try {
    const data = await api('/api/paiements');
    renderPaiementsTable(data);
  } catch (e) { console.error(e); }
}

async function loadLivraisons() {
  try {
    const data = await api('/api/livraisons');
    renderLivraisonsTable(data);
  } catch (e) { console.error(e); }
}

// ===== RENDERERS =====
function formatFCFA(n) { return n.toLocaleString('fr-FR') + ' F'; }
function formatDate(iso) {
  if (!iso) return '-';
  const d = new Date(iso);
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}
function statusBadge(s) {
  const map = { nouveau: 'badge-new', confirme: 'badge-confirmed', preparation: 'badge-prepa', livre: 'badge-delivered', annule: 'badge-cancelled' };
  return `<span class="badge ${map[s] || ''}">${s}</span>`;
}
function statusLabel(s) {
  const map = { nouveau: 'Nouveau', confirme: 'Confirmé', preparation: 'En préparation', livre: 'Livré', annule: 'Annulé' };
  return map[s] || s;
}

function renderRecent(items) {
  const el = document.getElementById('recent-orders');
  if (!el) return;
  if (!items.length) { el.innerHTML = '<p style="color:var(--ink-500);padding:20px">Aucune commande récente</p>'; return; }
  el.innerHTML = items.map(c => `
    <div class="recent-item">
      <div>
        <div class="recent-client">${c.client_name} · ${c.color} x${c.quantity}</div>
        <div class="recent-meta">${c.client_whatsapp} · ${formatDate(c.created_at)}</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-weight:600">${formatFCFA(c.amount * c.quantity)}</span>
        ${statusBadge(c.status)}
        <button class="icon-btn-sm whatsapp" onclick="openWA('${c.client_whatsapp}')" title="WhatsApp">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.84 12.84 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/></svg>
        </button>
      </div>
    </div>
  `).join('');
}

function renderCommandesTable() {
  const el = document.getElementById('commandes-tbody');
  if (!el) return;
  if (!commandesData.items.length) {
    el.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--ink-500);padding:40px">Aucune commande trouvée</td></tr>';
    return;
  }
  el.innerHTML = commandesData.items.map(c => `
    <tr>
      <td style="font-family:var(--font-mono);font-size:12px">#${c.id}</td>
      <td><strong>${c.client_name}</strong><br><span style="font-size:12px;color:var(--ink-400)">${c.client_whatsapp}</span></td>
      <td>${c.color}</td>
      <td>${c.quantity}</td>
      <td>${formatFCFA(c.amount * c.quantity)}</td>
      <td>${statusBadge(c.status)}</td>
      <td style="font-size:12px">${formatDate(c.created_at)}</td>
      <td style="display:flex;gap:6px">
        <button class="icon-btn-sm whatsapp" onclick="openWA('${c.client_whatsapp}')" title="WhatsApp">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.84 12.84 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/></svg>
        </button>
        <button class="icon-btn-sm" onclick="openEditCommande(${c.id})" title="Modifier">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
        </button>
        <button class="icon-btn-sm" onclick="changeStatus(${c.id})" title="Changer statut" style="color:var(--volt-400)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
        </button>
      </td>
    </tr>
  `).join('');
}

function renderPaiementsTable(data) {
  const el = document.getElementById('paiements-tbody');
  if (!el) return;
  if (!data.length) { el.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--ink-500);padding:40px">Aucun paiement</td></tr>'; return; }
  el.innerHTML = data.map(p => `
    <tr>
      <td style="font-family:var(--font-mono);font-size:12px">#${p.id}</td>
      <td>Commande #${p.commande_id}</td>
      <td style="text-transform:capitalize">${p.methode.replace('_',' ')}</td>
      <td>${formatFCFA(p.montant)}</td>
      <td><span class="badge ${p.statut === 'recu' ? 'badge-paid' : 'badge-pending'}">${p.statut === 'recu' ? 'Reçu' : 'En attente'}</span></td>
      <td style="font-size:12px">${formatDate(p.created_at)}</td>
      <td>
        ${p.statut !== 'recu' ? `<button class="btn btn-success btn-sm" onclick="confirmPayment(${p.id})">Confirmer</button>` : ''}
        ${p.preuve_url ? `<a href="${p.preuve_url}" target="_blank" class="btn btn-outline btn-sm">Preuve</a>` : ''}
      </td>
    </tr>
  `).join('');
}

function renderLivraisonsTable(data) {
  const el = document.getElementById('livraisons-tbody');
  if (!el) return;
  if (!data.length) { el.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--ink-500);padding:40px">Aucune livraison</td></tr>'; return; }
  el.innerHTML = data.map(l => `
    <tr>
      <td style="font-family:var(--font-mono);font-size:12px">#${l.id}</td>
      <td>Commande #${l.commande_id}</td>
      <td>${l.zone || '-'}</td>
      <td><span class="badge ${l.statut === 'livre' ? 'badge-delivered' : l.statut === 'en_cours' ? 'badge-confirmed' : 'badge-pending'}">${l.statut === 'livre' ? 'Livré' : l.statut === 'en_cours' ? 'En cours' : 'En attente'}</span></td>
      <td style="font-size:12px">${l.adresse_complete || '-'}</td>
      <td>
        <button class="btn btn-outline btn-sm" onclick="openEditLivraison(${l.id})">Modifier</button>
      </td>
    </tr>
  `).join('');
}

function renderPagination() {
  const el = document.getElementById('pagination-info');
  if (!el) return;
  el.innerHTML = `
    <span class="pagination-info">${commandesData.total} commande(s)</span>
    <div class="pagination-btns">
      <button class="btn btn-outline btn-sm" onclick="commandesOffset=Math.max(0,commandesOffset-20);loadCommandes()" ${commandesOffset === 0 ? 'disabled' : ''}>← Précédent</button>
      <button class="btn btn-outline btn-sm" onclick="commandesOffset+=20;loadCommandes()" ${commandesOffset + 20 >= commandesData.total ? 'disabled' : ''}>Suivant →</button>
    </div>
  `;
}

// ===== ACTIONS =====
function openWA(number) {
  window.open(`https://wa.me/${number.replace(/\D/g,'')}`, '_blank');
}

async function openCreateCommande() {
  document.getElementById('modal-create').classList.remove('hidden');
}

function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}

async function submitCommande(e) {
  e.preventDefault();
  const data = {
    client_name: document.getElementById('cmd-name').value,
    client_whatsapp: document.getElementById('cmd-wa').value,
    client_address: document.getElementById('cmd-address').value,
    color: document.getElementById('cmd-color').value,
    quantity: parseInt(document.getElementById('cmd-qty').value),
    amount: parseInt(document.getElementById('cmd-amount').value),
    notes: document.getElementById('cmd-notes').value
  };
  try {
    await api('/api/commandes', { method: 'POST', body: JSON.stringify(data) });
    closeModal('modal-create');
    loadCommandes();
    loadStats();
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function openEditCommande(id) {
  try {
    const c = await api(`/api/commandes/${id}`);
    document.getElementById('edit-id').value = c.id;
    document.getElementById('edit-name').value = c.client_name;
    document.getElementById('edit-wa').value = c.client_whatsapp;
    document.getElementById('edit-address').value = c.client_address || '';
    document.getElementById('edit-color').value = c.color;
    document.getElementById('edit-qty').value = c.quantity;
    document.getElementById('edit-amount').value = c.amount;
    document.getElementById('edit-status').value = c.status;
    document.getElementById('edit-notes').value = c.notes || '';
    document.getElementById('modal-edit').classList.remove('hidden');
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function submitEditCommande(e) {
  e.preventDefault();
  const id = document.getElementById('edit-id').value;
  const data = {
    client_name: document.getElementById('edit-name').value,
    client_whatsapp: document.getElementById('edit-wa').value,
    client_address: document.getElementById('edit-address').value,
    color: document.getElementById('edit-color').value,
    quantity: parseInt(document.getElementById('edit-qty').value),
    amount: parseInt(document.getElementById('edit-amount').value),
    status: document.getElementById('edit-status').value,
    notes: document.getElementById('edit-notes').value
  };
  try {
    await api(`/api/commandes/${id}`, { method: 'PUT', body: JSON.stringify(data) });
    closeModal('modal-edit');
    loadCommandes();
    loadStats();
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function changeStatus(id) {
  const statuses = ['nouveau', 'confirme', 'preparation', 'livre', 'annule'];
  const current = prompt('Nouveau statut :\n' + statuses.join(' | '));
  if (!current || !statuses.includes(current)) return;
  try {
    await api(`/api/commandes/${id}`, { method: 'PUT', body: JSON.stringify({ status: current }) });
    loadCommandes();
    loadStats();
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function confirmPayment(id) {
  if (!confirm('Confirmer ce paiement comme reçu ?')) return;
  try {
    await api(`/api/paiements/${id}?statut=recu`, { method: 'PUT' });
    loadPaiements();
    loadStats();
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function openEditLivraison(id) {
  try {
    const items = await api('/api/livraisons');
    const l = items.find(x => x.id === id);
    if (!l) return;
    document.getElementById('liv-id').value = l.id;
    document.getElementById('liv-zone').value = l.zone || '';
    document.getElementById('liv-adresse').value = l.adresse_complete || '';
    document.getElementById('liv-statut').value = l.statut;
    document.getElementById('liv-notes').value = l.tracking_notes || '';
    document.getElementById('modal-livraison').classList.remove('hidden');
  } catch (e) { alert('Erreur: ' + e.message); }
}

async function submitLivraison(e) {
  e.preventDefault();
  const id = document.getElementById('liv-id').value;
  const data = {
    zone: document.getElementById('liv-zone').value,
    adresse_complete: document.getElementById('liv-adresse').value,
    statut: document.getElementById('liv-statut').value,
    tracking_notes: document.getElementById('liv-notes').value
  };
  try {
    await api(`/api/livraisons/${id}`, { method: 'PUT', body: JSON.stringify(data) });
    closeModal('modal-livraison');
    loadLivraisons();
    loadStats();
  } catch (e) { alert('Erreur: ' + e.message); }
}

// ===== NAVIGATION =====
function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
  document.getElementById(`tab-${tab}`).classList.remove('hidden');
  document.getElementById(`nav-${tab}`).classList.add('active');
  document.title = `GripForce Admin · ${tab.charAt(0).toUpperCase() + tab.slice(1)}`;

  if (tab === 'stats') loadStats();
  if (tab === 'commandes') loadCommandes();
  if (tab === 'paiements') loadPaiements();
  if (tab === 'livraisons') loadLivraisons();
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  const user = getUser();
  if (!user) return;
  document.getElementById('sidebar-user-name').textContent = user.full_name || user.username;
  loadStats();
});
