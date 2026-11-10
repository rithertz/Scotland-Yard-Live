import {
  containRect,
  displayToPixel,
  isInBounds,
  nextCorrespondenceId,
  normalizeRotation,
  originalToRotated,
  rotatedDimensions,
  rotatedToOriginal,
} from './coordinate-utils.mjs';
import { RAW_PHOTOS } from './photo-manifest.mjs';

const PHOTO_MAP = new Map(RAW_PHOTOS.map((photo) => [photo.filename, photo]));
const PAIRS = [...'ABCD']
  .flatMap((row) => [1, 2, 3].map((col) => [`${row}${col}.jpg`, `${row}${col + 1}.jpg`]))
  .concat(
    [1, 2, 3, 4].flatMap((col) =>
      ['A', 'B', 'C'].map((row) => [
        `${row}${col}.jpg`,
        `${String.fromCharCode(row.charCodeAt(0) + 1)}${col}.jpg`,
      ]),
    ),
  );
const INSUFFICIENT = new Set(['A2-A3', 'B1-C1', 'B2-C2', 'B3-C3']);
const STORAGE_KEY = 'scotland-yard-live-phase-3f2-3-control-points';
const state = {
  pairIndex: 0,
  selectedPoint: null,
  pendingLeft: null,
  pairs: new Map(),
  views: {
    left: { zoom: 1, panX: 0, panY: 0, rotation: 0 },
    right: { zoom: 1, panX: 0, panY: 0, rotation: 0 },
  },
  history: [],
  sync: true,
  pairAudit: new Map(),
};

const $ = (id) => document.getElementById(id);
const pairId = (pair) => `${pair[0].slice(0, -4)}-${pair[1].slice(0, -4)}`;
const currentPair = () => PAIRS[state.pairIndex];
const photoPath = (filename) => PHOTO_MAP.get(filename);

function snapshot() {
  return JSON.stringify([...state.pairs.entries()]);
}
function pushHistory() {
  state.history.push(snapshot());
  if (state.history.length > 30) state.history.shift();
}
function currentPoints() {
  return state.pairs.get(pairId(currentPair())) ?? [];
}
function ensurePair(pair) {
  if (!state.pairs.has(pairId(pair))) state.pairs.set(pairId(pair), []);
  return state.pairs.get(pairId(pair));
}

function pairStatus(pair) {
  const points = state.pairs.get(pairId(pair)) ?? [];
  if (!points.length) return 'draft';
  if (points.some((point) => point.reviewStatus === 'accepted')) return 'accepted';
  if (points.some((point) => point.reviewStatus === 'reviewed')) return 'reviewed';
  return 'draft';
}

function renderLists() {
  $('photo-list').innerHTML = RAW_PHOTOS.map(
    (photo) =>
      `<button data-photo="${photo.filename}"><span>${photo.filename}</span><span class="pair-meta">${photo.width}×${photo.height}</span></button>`,
  ).join('');
  $('pair-list').innerHTML = PAIRS.map((pair, index) => {
    const id = pairId(pair);
    const insufficient = INSUFFICIENT.has(id);
    return `<button class="${index === state.pairIndex ? 'active ' : ''}${insufficient ? 'insufficient' : ''}" data-pair-index="${index}"><span>${id}</span><span class="pair-meta">${pairStatus(pair)} · ${(state.pairs.get(id) ?? []).length}</span></button>`;
  }).join('');
  $('pair-count').textContent = `(${PAIRS.length})`;
  document.querySelectorAll('[data-pair-index]').forEach((button) =>
    button.addEventListener('click', () => {
      state.pairIndex = Number(button.dataset.pairIndex);
      state.selectedPoint = null;
      state.pendingLeft = null;
      resetViews();
      render();
    }),
  );
  document.querySelectorAll('[data-photo]').forEach((button) =>
    button.addEventListener('click', () => {
      const index = PAIRS.findIndex((pair) => pair.includes(button.dataset.photo));
      if (index >= 0) {
        state.pairIndex = index;
        state.selectedPoint = null;
        state.pendingLeft = null;
        resetViews();
        render();
      }
    }),
  );
}

function renderPair() {
  const pair = currentPair();
  const left = photoPath(pair[0]);
  const right = photoPath(pair[1]);
  $('selected-pair').textContent = pairId(pair);
  $('pair-status').textContent = INSUFFICIENT.has(pairId(pair))
    ? 'INSUFFICIENT EVIDENCE'
    : pairStatus(pair);
  $('left-title').textContent = left.filename;
  $('right-title').textContent = right.filename;
  $('left-dimensions').textContent = `${left.width}×${left.height} · EXIF ${left.exifOrientation}`;
  $('right-dimensions').textContent =
    `${right.width}×${right.height} · EXIF ${right.exifOrientation}`;
  for (const side of ['left', 'right']) {
    const photo = side === 'left' ? left : right;
    const image = $(`${side}-image`);
    image.src = photo.src;
    image.width = photo.width;
    image.height = photo.height;
    image.style.imageOrientation = 'none';
  }
  requestAnimationFrame(() => {
    resetViews();
    renderOverlays();
  });
}

function renderOverlays() {
  const pair = currentPair();
  const photos = { left: photoPath(pair[0]), right: photoPath(pair[1]) };
  for (const side of ['left', 'right']) {
    const viewer = $(`${side}-viewer`);
    const canvas = $(`${side}-canvas`);
    const content = $(`${side}-content`);
    const photo = photos[side];
    const dimensions = rotatedDimensions(photo.width, photo.height, state.views[side].rotation);
    const rect = containRect(
      viewer.clientWidth,
      viewer.clientHeight,
      dimensions.width,
      dimensions.height,
    );
    const view = state.views[side];
    // Keep the canvas in source-pixel coordinates and apply the calculated
    // contain scale to the single shared image/overlay surface. A zoom of 1
    // therefore means "fit", rather than native-pixel rendering.
    canvas.style.width = `${dimensions.width}px`;
    canvas.style.height = `${dimensions.height}px`;
    canvas.style.marginLeft = `${-dimensions.width / 2}px`;
    canvas.style.marginTop = `${-dimensions.height / 2}px`;
    canvas.style.transform = `translate(${view.panX}px, ${view.panY}px) scale(${rect.scale * view.zoom})`;
    content.style.width = `${dimensions.width}px`;
    content.style.height = `${dimensions.height}px`;
    content.style.marginLeft = `${-dimensions.width / 2}px`;
    content.style.marginTop = `${-dimensions.height / 2}px`;
    content.style.transform = 'none';
    const image = $(`${side}-image`);
    image.style.width = `${photo.width}px`;
    image.style.height = `${photo.height}px`;
    image.style.left = '50%';
    image.style.top = '50%';
    image.style.right = 'auto';
    image.style.bottom = 'auto';
    image.style.transform = `translate(-50%, -50%) rotate(${view.rotation}deg)`;
    $(`${side}-rotation`).textContent = `ROT ${view.rotation}°`;
    const svg = $(`${side}-overlay`);
    svg.setAttribute('viewBox', `0 0 ${dimensions.width} ${dimensions.height}`);
    svg.innerHTML = currentPoints()
      .map((point, index) => {
        const original = side === 'left' ? point.left : point.right;
        const p = originalToRotated(original, photo.width, photo.height, view.rotation);
        return `<g class="cp-marker ${point.demo ? 'demo' : ''}" data-point-id="${point.id}"><circle cx="${p.x}" cy="${p.y}" r="${Math.max(photo.width, photo.height) / 180}"/><text x="${p.x + Math.max(photo.width, photo.height) / 120}" y="${p.y - Math.max(photo.width, photo.height) / 120}">${index + 1}</text></g>`;
      })
      .join('');
  }
  $('point-count').textContent = currentPoints().length;
  $('annotation-status').textContent = currentPoints().length ? pairStatus(currentPair()) : 'draft';
  $('correspondence-list').innerHTML = currentPoints()
    .map(
      (point, index) =>
        `<div class="correspondence ${point.id === state.selectedPoint ? 'selected ' : ''}${point.demo ? 'demo' : ''}" data-point-id="${point.id}"><strong>${index + 1}. ${point.id}${point.demo ? ' · TEST DATA' : ''}</strong><small>${point.description || 'No description'} · ${point.confidence} · ${point.reviewStatus}</small><small>L (${Math.round(point.left.x)}, ${Math.round(point.left.y)}) ↔ R (${Math.round(point.right.x)}, ${Math.round(point.right.y)})</small></div>`,
    )
    .join('');
  document.querySelectorAll('[data-point-id]').forEach((element) =>
    element.addEventListener('click', (event) => {
      event.stopPropagation();
      state.selectedPoint = element.dataset.pointId;
      fillEditor();
      renderOverlays();
    }),
  );
}

function fillEditor() {
  const point = currentPoints().find((candidate) => candidate.id === state.selectedPoint);
  if (!point) return;
  $('description').value = point.description;
  $('reviewer').value = point.reviewer;
  $('confidence').value = point.confidence;
  $('review-status').value = point.reviewStatus;
}
function resetViews() {
  state.views.left = { zoom: 1, panX: 0, panY: 0, rotation: 0 };
  state.views.right = { zoom: 1, panX: 0, panY: 0, rotation: 0 };
}
function syncZoomAndPan(side) {
  if (!state.sync) return;
  const other = side === 'left' ? 'right' : 'left';
  state.views[other].zoom = state.views[side].zoom;
  state.views[other].panX = state.views[side].panX;
  state.views[other].panY = state.views[side].panY;
}
function updateView(side, action) {
  const view = state.views[side];
  if (action === 'zoomIn') view.zoom = Math.min(view.zoom * 1.3, 12);
  if (action === 'zoomOut') view.zoom = Math.max(view.zoom / 1.3, 0.25);
  if (action === 'fit' || action === 'reset') ((view.zoom = 1), (view.panX = 0), (view.panY = 0));
  syncZoomAndPan(side);
  renderOverlays();
}
function updateRotation(side, amount) {
  state.views[side].rotation =
    amount === 0 ? 0 : normalizeRotation(state.views[side].rotation + amount);
  renderOverlays();
}
function render() {
  renderLists();
  renderPair();
}

function addPoint(side, event) {
  const pair = currentPair();
  const photo = photoPath(side === 'left' ? pair[0] : pair[1]);
  const canvas = $(`${side}-canvas`);
  const rect = canvas.getBoundingClientRect();
  const dimensions = rotatedDimensions(photo.width, photo.height, state.views[side].rotation);
  const rotatedPoint = displayToPixel(
    event.clientX,
    event.clientY,
    rect,
    dimensions.width,
    dimensions.height,
  );
  const point = rotatedToOriginal(
    rotatedPoint,
    photo.width,
    photo.height,
    state.views[side].rotation,
  );
  if (!isInBounds(point, photo.width, photo.height)) return;
  if (side === 'left') {
    state.pendingLeft = point;
    return;
  }
  if (!state.pendingLeft) return;
  pushHistory();
  const points = ensurePair(pair);
  const id = nextCorrespondenceId([...state.pairs.values()].flat().map((item) => item.id));
  points.push({
    id,
    pairId: pairId(pair),
    left: state.pendingLeft,
    right: point,
    leftPhoto: pair[0],
    rightPhoto: pair[1],
    leftDimensions: { width: photoPath(pair[0]).width, height: photoPath(pair[0]).height },
    rightDimensions: { width: photo.width, height: photo.height },
    leftExifOrientation: photoPath(pair[0]).exifOrientation,
    rightExifOrientation: photo.exifOrientation,
    description: '',
    reviewer: '',
    confidence: 'unreviewed',
    reviewStatus: 'draft',
    demo: false,
  });
  state.selectedPoint = id;
  state.pendingLeft = null;
  persistDraft();
  renderOverlays();
  fillEditor();
}

function persistDraft() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(exportDocument()));
}
function exportDocument() {
  return {
    phase: '3F.2.3',
    schemaVersion: 1,
    coordinateConvention:
      'Original decoded pixel coordinates; EXIF orientation is recorded but not applied to stored coordinates.',
    reviewer: $('reviewer').value || '',
    photos: RAW_PHOTOS,
    pairs: PAIRS.map((pair) => ({
      pairId: pairId(pair),
      photoA: pair[0],
      photoB: pair[1],
      status: pairStatus(pair),
      insufficientEvidence: INSUFFICIENT.has(pairId(pair)),
    })),
    correspondences: [...state.pairs.values()].flat(),
  };
}
function loadDocument(document) {
  if (document.phase !== '3F.2.3' || !Array.isArray(document.correspondences))
    throw new Error('Unsupported or malformed Phase 3F.2.3 JSON');
  const next = new Map();
  for (const point of document.correspondences) {
    if (!point.id || next.values().some((items) => items.some((item) => item.id === point.id)))
      throw new Error(`Duplicate correspondence ID: ${point.id}`);
    const pair = PAIRS.find((candidate) => pairId(candidate) === point.pairId);
    if (!pair) throw new Error(`Unknown pair: ${point.pairId}`);
    const left = photoPath(pair[0]);
    const right = photoPath(pair[1]);
    if (
      !isInBounds(point.left, left.width, left.height) ||
      !isInBounds(point.right, right.width, right.height)
    )
      throw new Error(`Out-of-bounds correspondence: ${point.id}`);
    if (!next.has(point.pairId)) next.set(point.pairId, []);
    next.get(point.pairId).push(point);
  }
  state.pairs = next;
  state.selectedPoint = null;
  persistDraft();
  render();
}
function demoPoints() {
  pushHistory();
  const pair = currentPair();
  const left = photoPath(pair[0]);
  const right = photoPath(pair[1]);
  const usedIds = [...state.pairs.values()].flat().map((item) => item.id);
  const points = [
    { x: left.width * 0.35, y: left.height * 0.38 },
    { x: left.width * 0.52, y: left.height * 0.46 },
    { x: left.width * 0.67, y: left.height * 0.56 },
  ].map((p, index) => {
    const id = nextCorrespondenceId(usedIds);
    usedIds.push(id);
    return {
      id,
      pairId: pairId(pair),
      left: p,
      right: { x: right.width * (0.31 + index * 0.17), y: right.height * (0.35 + index * 0.11) },
      leftPhoto: pair[0],
      rightPhoto: pair[1],
      leftDimensions: { width: left.width, height: left.height },
      rightDimensions: { width: right.width, height: right.height },
      leftExifOrientation: left.exifOrientation,
      rightExifOrientation: right.exifOrientation,
      description: `DEMO TEST LANDMARK ${index + 1}`,
      reviewer: 'test data',
      confidence: 'unreviewed',
      reviewStatus: 'draft',
      demo: true,
    };
  });
  ensurePair(pair).push(...points);
  state.selectedPoint = points[0].id;
  persistDraft();
  renderOverlays();
}

// Use delegated controls so rotation remains functional even if the controls are
// re-rendered or the workbench is embedded in a host that initializes the DOM
// after this module is evaluated. Explicitly prevent default button behaviour.
document.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action], button[data-rotate]');
  if (!button) return;
  event.preventDefault();
  if (button.dataset.rotate !== undefined)
    updateRotation(button.dataset.viewer, Number(button.dataset.rotate));
  else updateView(button.dataset.viewer, button.dataset.action);
});
for (const side of ['left', 'right']) {
  const viewer = $(`${side}-viewer`);
  let drag = null;
  viewer.addEventListener('click', (event) => {
    if (drag) return;
    addPoint(side, event);
  });
  viewer.addEventListener(
    'wheel',
    (event) => {
      event.preventDefault();
      updateView(side, event.deltaY < 0 ? 'zoomIn' : 'zoomOut');
    },
    { passive: false },
  );
  viewer.addEventListener('pointerdown', (event) => {
    if (event.target.closest('svg')) return;
    drag = {
      x: event.clientX,
      y: event.clientY,
      panX: state.views[side].panX,
      panY: state.views[side].panY,
    };
    viewer.setPointerCapture(event.pointerId);
  });
  viewer.addEventListener('pointermove', (event) => {
    if (!drag) return;
    state.views[side].panX = drag.panX + event.clientX - drag.x;
    state.views[side].panY = drag.panY + event.clientY - drag.y;
    syncZoomAndPan(side);
    renderOverlays();
  });
  viewer.addEventListener('pointerup', () => {
    drag = null;
  });
}
$('sync-toggle').addEventListener('change', (event) => {
  state.sync = event.target.checked;
});
$('demo-button').addEventListener('click', demoPoints);
$('undo-button').addEventListener('click', () => {
  const previous = state.history.pop();
  if (previous) {
    state.pairs = new Map(JSON.parse(previous));
    renderOverlays();
  }
});
$('delete-selected').addEventListener('click', () => {
  if (!state.selectedPoint) return;
  pushHistory();
  state.pairs.set(
    pairId(currentPair()),
    currentPoints().filter((point) => point.id !== state.selectedPoint),
  );
  state.selectedPoint = null;
  persistDraft();
  renderOverlays();
});
$('apply-edit').addEventListener('click', () => {
  const point = currentPoints().find((candidate) => candidate.id === state.selectedPoint);
  if (!point) return;
  pushHistory();
  point.description = $('description').value;
  point.reviewer = $('reviewer').value;
  point.confidence = $('confidence').value;
  point.reviewStatus = $('review-status').value;
  persistDraft();
  renderOverlays();
});
$('clear-selection').addEventListener('click', () => {
  state.selectedPoint = null;
  renderOverlays();
});
$('save-button').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(exportDocument(), null, 2) + '\n'], {
    type: 'application/json',
  });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `phase-3f2-3-control-points-${new Date().toISOString().replaceAll(':', '-')}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});
$('load-input').addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    loadDocument(JSON.parse(await file.text()));
  } catch (error) {
    alert(error.message);
  }
  event.target.value = '';
});
const savedDraft = localStorage.getItem(STORAGE_KEY);
if (savedDraft) {
  try {
    loadDocument(JSON.parse(savedDraft));
  } catch (error) {
    console.warn('Ignoring invalid saved draft:', error.message);
    render();
  }
} else
  fetch('../output/phase_3f2_2_registration/overlap_audit.json')
    .then((response) => response.json())
    .then((audit) =>
      audit.pairs.forEach((pair) =>
        state.pairAudit.set(`${pair.a.slice(0, -4)}-${pair.b.slice(0, -4)}`, pair),
      ),
    )
    .catch(() => {})
    .finally(() => render());
