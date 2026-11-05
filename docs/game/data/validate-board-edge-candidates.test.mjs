import { deepStrictEqual, equal, ok } from 'node:assert/strict';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import {
  loadCandidateDataset,
  validateCandidateDataset,
} from './validate-board-edge-candidates.mjs';

const dataDir = dirname(fileURLToPath(import.meta.url));
const dataset = loadCandidateDataset(resolve(dataDir, 'board-edge-candidates-1-200.json'));

test('candidate dataset validates while retaining non-canonical conflict warnings', () => {
  const result = validateCandidateDataset(dataset);
  equal(result.valid, true);
  equal(dataset.edges.length, 125);
  ok(result.issues.some((entry) => entry.code === 'conflicting-transport-classification'));
  equal(dataset.metadata.canonicalStatus, 'non-canonical');
  equal(dataset.metadata.playable, false);
});

test('station 200 is allowed as observed evidence without becoming canonical', () => {
  const edge = dataset.edges.find((entry) => entry.to === 200);
  ok(edge);
  equal(validateCandidateDataset({ ...dataset, edges: [edge] }).valid, true);
});

test('legitimate multi-modal and unresolved boat records remain valid candidates', () => {
  const multiModal = dataset.edges.filter((entry) => entry.from === 11 && entry.to === 22);
  const boats = dataset.edges.filter((entry) => entry.transport === 'boat');
  equal(multiModal.length, 2);
  equal(boats.length, 4);
  ok(boats.every((entry) => entry.verificationStatus === 'unresolved'));
  equal(validateCandidateDataset({ ...dataset, edges: [...multiModal, ...boats] }).valid, true);
});

test('validator rejects malformed and duplicate candidates', () => {
  const edge = dataset.edges[0];
  const malformed = {
    ...dataset,
    edges: [
      { ...edge, edgeId: 'E-999', from: 4, to: 4 },
      { ...edge, edgeId: 'E-999', from: 8, to: 1, transport: 'tram', evidence: [] },
      { ...edge, edgeId: 'E-1000', from: 1, to: 8 },
      { ...edge, edgeId: 'E-1001', from: 1, to: 8 },
    ],
  };
  const result = validateCandidateDataset(malformed);
  const codes = result.issues.map((entry) => entry.code);
  ok(codes.includes('self-loop'));
  ok(codes.includes('duplicate-edge-id'));
  ok(codes.includes('non-canonical-endpoint-order'));
  ok(codes.includes('invalid-transport'));
  ok(codes.includes('missing-evidence'));
  ok(codes.includes('duplicate-undirected-edge'));
});

test('validator detects missing evidence files and empty explanations', () => {
  const edge = dataset.edges[0];
  const result = validateCandidateDataset({
    ...dataset,
    edges: [{ ...edge, evidence: [{ file: 'missing.jpeg', region: '' }], visualExplanation: ' ' }],
  });
  const codes = result.issues.map((entry) => entry.code);
  ok(codes.includes('missing-evidence'));
  ok(codes.includes('missing-evidence-region'));
  ok(codes.includes('empty-explanation'));
});

test('validator rejects invalid confidence and verification status values', () => {
  const edge = dataset.edges[0];
  const result = validateCandidateDataset({
    ...dataset,
    edges: [{ ...edge, confidence: 'certain', verificationStatus: 'verified' }],
  });
  const codes = result.issues.map((entry) => entry.code);
  ok(codes.includes('invalid-confidence'));
  ok(codes.includes('invalid-verification-status'));
});

test('validator rejects canonical or playable metadata', () => {
  const result = validateCandidateDataset({
    ...dataset,
    metadata: { ...dataset.metadata, canonicalStatus: 'canonical', playable: true },
  });
  ok(result.issues.some((entry) => entry.code === 'inconsistent-metadata'));
});
