import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const TRANSPORTS = new Set(['taxi', 'bus', 'underground', 'boat']);
export const CONFIDENCES = new Set(['high', 'medium', 'low']);
export const STATUSES = new Set(['provisional', 'unresolved']);
export const EVIDENCE_FILES = new Set([
  'complete.jpeg',
  'top-left.jpeg',
  'top-right.jpeg',
  'bottom-left.jpeg',
  'bottom-right.jpeg',
]);

function issue(code, message, severity = 'error', edgeId) {
  return { code, message, severity, ...(edgeId ? { edgeId } : {}) };
}

export function validateCandidateDataset(dataset, options = {}) {
  const issues = [];
  const repoRoot =
    options.repoRoot ?? resolve(fileURLToPath(new URL('.', import.meta.url)), '../../..');

  if (!dataset || typeof dataset !== 'object') {
    return { valid: false, issues: [issue('invalid-dataset', 'Dataset must be an object.')] };
  }

  const metadata = dataset.metadata;
  if (!metadata || metadata.canonicalStatus !== 'non-canonical' || metadata.playable !== false) {
    issues.push(
      issue(
        'inconsistent-metadata',
        'Candidate data must be explicitly non-canonical and non-playable.',
      ),
    );
  }
  if (!metadata?.datasetVersion || !metadata?.sourceTranscriptionPhase) {
    issues.push(
      issue(
        'inconsistent-metadata',
        'Dataset version and source transcription phase are required.',
      ),
    );
  }
  if (
    !Number.isInteger(metadata?.stationRange?.minObserved) ||
    metadata.stationRange.minObserved < 1
  ) {
    issues.push(
      issue('inconsistent-metadata', 'stationRange.minObserved must be a positive integer.'),
    );
  }
  if (
    !Number.isInteger(metadata?.stationRange?.maxObserved) ||
    metadata.stationRange.maxObserved < metadata.stationRange.minObserved
  ) {
    issues.push(
      issue('inconsistent-metadata', 'stationRange.maxObserved must be at least minObserved.'),
    );
  }

  if (!Array.isArray(dataset.edges)) {
    issues.push(issue('invalid-edges', 'edges must be an array.'));
    return { valid: false, issues };
  }

  const ids = new Set();
  const exactEdges = new Set();
  const endpointTransports = new Map();

  for (const edge of dataset.edges) {
    const edgeId = edge?.edgeId;
    if (typeof edgeId !== 'string' || !/^E-[0-9]{3,}$/.test(edgeId)) {
      issues.push(issue('invalid-edge-id', 'Edge ID must match E-NNN.', 'error', edgeId));
    } else if (ids.has(edgeId)) {
      issues.push(issue('duplicate-edge-id', `Edge ID ${edgeId} is duplicated.`, 'error', edgeId));
    } else {
      ids.add(edgeId);
    }

    const from = edge?.from;
    const to = edge?.to;
    if (!Number.isInteger(from) || !Number.isInteger(to) || from < 1 || to < 1) {
      issues.push(
        issue(
          'invalid-endpoint',
          'Endpoints must be positive integers; no canonical upper bound is applied.',
          'error',
          edgeId,
        ),
      );
    } else {
      if (from === to)
        issues.push(issue('self-loop', `Edge ${from}-${to} is a self-loop.`, 'error', edgeId));
      if (from > to)
        issues.push(
          issue(
            'non-canonical-endpoint-order',
            `Edge ${from}-${to} is not stored with from < to.`,
            'error',
            edgeId,
          ),
        );
    }

    if (!TRANSPORTS.has(edge?.transport))
      issues.push(
        issue(
          'invalid-transport',
          `Unsupported transport ${String(edge?.transport)}.`,
          'error',
          edgeId,
        ),
      );
    if (!CONFIDENCES.has(edge?.confidence))
      issues.push(
        issue(
          'invalid-confidence',
          `Unsupported confidence ${String(edge?.confidence)}.`,
          'error',
          edgeId,
        ),
      );
    if (!STATUSES.has(edge?.verificationStatus))
      issues.push(
        issue(
          'invalid-verification-status',
          `Unsupported verification status ${String(edge?.verificationStatus)}.`,
          'error',
          edgeId,
        ),
      );
    if (!Array.isArray(edge?.evidence) || edge.evidence.length === 0) {
      issues.push(
        issue('missing-evidence', 'At least one evidence reference is required.', 'error', edgeId),
      );
    } else {
      for (const reference of edge.evidence) {
        if (!reference?.file || !EVIDENCE_FILES.has(reference.file)) {
          issues.push(
            issue(
              'missing-evidence',
              `Unknown or missing evidence file ${String(reference?.file)}.`,
              'error',
              edgeId,
            ),
          );
        } else if (
          !existsSync(resolve(repoRoot, 'docs/game/evidence/board-photos', reference.file))
        ) {
          issues.push(
            issue(
              'missing-evidence',
              `Evidence file ${reference.file} does not exist in the repository.`,
              'error',
              edgeId,
            ),
          );
        }
        if (!reference?.region?.trim())
          issues.push(
            issue('missing-evidence-region', 'Evidence region is required.', 'error', edgeId),
          );
      }
    }
    if (!edge?.approximateImageRegion?.trim())
      issues.push(
        issue('missing-region', 'Approximate image region is required.', 'error', edgeId),
      );
    if (!edge?.visualExplanation?.trim())
      issues.push(issue('empty-explanation', 'Visual explanation is required.', 'error', edgeId));

    if (Number.isInteger(from) && Number.isInteger(to) && TRANSPORTS.has(edge?.transport)) {
      const key = `${from}-${to}-${edge.transport}`;
      if (exactEdges.has(key))
        issues.push(
          issue(
            'duplicate-undirected-edge',
            `Duplicate undirected candidate ${key}.`,
            'error',
            edgeId,
          ),
        );
      exactEdges.add(key);
      const endpointKey = `${from}-${to}`;
      const observed = endpointTransports.get(endpointKey) ?? new Map();
      observed.set(edge.transport, [...(observed.get(edge.transport) ?? []), edgeId]);
      endpointTransports.set(endpointKey, observed);
    }
  }

  for (const [endpointKey, transportMap] of endpointTransports) {
    if (transportMap.size > 1) {
      issues.push(
        issue(
          'conflicting-transport-classification',
          `Endpoint pair ${endpointKey} has multiple observed transport classifications: ${[...transportMap.keys()].join(', ')}.`,
          'warning',
        ),
      );
    }
  }

  return { valid: issues.every((entry) => entry.severity !== 'error'), issues };
}

export function loadCandidateDataset(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}
