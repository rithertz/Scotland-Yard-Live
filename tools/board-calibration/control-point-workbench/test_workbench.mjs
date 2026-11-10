import assert from 'node:assert/strict';
import { containRect, displayToPixel, isInBounds, nextCorrespondenceId, originalToRotated, pixelToDisplay, rotatedDimensions, rotatedToOriginal } from './coordinate-utils.mjs';
import { RAW_PHOTOS } from './photo-manifest.mjs';

const rect = containRect(800, 600, 1600, 1200);
assert.deepEqual(rect, { left: 0, top: 0, width: 800, height: 600, scale: 0.5 });
const portraitFit = containRect(400, 300, 600, 1200);
assert.deepEqual(portraitFit, { left: 125, top: 0, width: 150, height: 300, scale: 0.25 });
assert.deepEqual(displayToPixel(400, 300, { left: 0, top: 0, width: 800, height: 600 }, 1600, 1200), { x: 800, y: 600 });
assert.deepEqual(pixelToDisplay(800, 600, { left: 0, top: 0, width: 800, height: 600 }, 1600, 1200), { x: 400, y: 300 });
assert.equal(isInBounds({ x: 0, y: 1200 }, 1600, 1200), true);
assert.equal(isInBounds({ x: 1600.1, y: 10 }, 1600, 1200), false);
assert.equal(isInBounds({ x: Number.NaN, y: 10 }, 1600, 1200), false);
assert.equal(nextCorrespondenceId(['CP-001', 'CP-003']), 'CP-002');
assert.equal(nextCorrespondenceId(['CP-001', 'CP-002']), 'CP-003');

const width = 5844;
const height = 6628;
assert.deepEqual(rotatedDimensions(width, height, 0), { width, height });
assert.deepEqual(rotatedDimensions(width, height, 90), { width: height, height: width });
assert.deepEqual(rotatedDimensions(width, height, 180), { width, height });
assert.deepEqual(rotatedDimensions(width, height, 270), { width: height, height: width });
for (const rotation of [0, 90, 180, 270]) {
  for (const point of [{ x: 0, y: 0 }, { x: width, y: 0 }, { x: 0, y: height }, { x: width, y: height }, { x: 1234.5, y: 5678.25 }]) {
    const rotated = originalToRotated(point, width, height, rotation);
    assert.deepEqual(rotatedToOriginal(rotated, width, height, rotation), point);
  }
}
assert.deepEqual(rotatedToOriginal({ x: height, y: 0 }, width, height, 90), { x: 0, y: 0 });
assert.deepEqual(rotatedToOriginal({ x: 0, y: width }, width, height, 270), { x: 0, y: 0 });
const rotatedRect = rotatedDimensions(width, height, 90);
const displayed = { left: 10, top: 20, width: 500, height: 700 };
const displayPoint = pixelToDisplay(height - 5678.25, 1234.5, displayed, rotatedRect.width, rotatedRect.height);
const recoveredRotated = displayToPixel(displayPoint.x, displayPoint.y, displayed, rotatedRect.width, rotatedRect.height);
assert.deepEqual(rotatedToOriginal(recoveredRotated, width, height, 90), { x: 1234.5, y: 5678.25 });
for (const [filename, orientation] of [['A1.jpg', 6], ['B2.jpg', 3], ['D1.jpg', 8]]) {
  assert.equal(RAW_PHOTOS.find((photo) => photo.filename === filename)?.exifOrientation, orientation);
}
console.log('workbench coordinate tests: 27 passed');
