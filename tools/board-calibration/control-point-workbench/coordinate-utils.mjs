export function containRect(viewportWidth, viewportHeight, imageWidth, imageHeight) {
  const scale = Math.min(viewportWidth / imageWidth, viewportHeight / imageHeight);
  const width = imageWidth * scale;
  const height = imageHeight * scale;
  return {
    left: (viewportWidth - width) / 2,
    top: (viewportHeight - height) / 2,
    width,
    height,
    scale,
  };
}

export function displayToPixel(clientX, clientY, canvasRect, imageWidth, imageHeight) {
  return {
    x: ((clientX - canvasRect.left) / canvasRect.width) * imageWidth,
    y: ((clientY - canvasRect.top) / canvasRect.height) * imageHeight,
  };
}

export function pixelToDisplay(x, y, canvasRect, imageWidth, imageHeight) {
  return {
    x: canvasRect.left + (x / imageWidth) * canvasRect.width,
    y: canvasRect.top + (y / imageHeight) * canvasRect.height,
  };
}

export function isInBounds(point, width, height) {
  return (
    Number.isFinite(point.x) &&
    Number.isFinite(point.y) &&
    point.x >= 0 &&
    point.x <= width &&
    point.y >= 0 &&
    point.y <= height
  );
}

export function nextCorrespondenceId(existingIds) {
  const used = new Set(existingIds);
  let index = 1;
  while (used.has(`CP-${String(index).padStart(3, '0')}`)) index += 1;
  return `CP-${String(index).padStart(3, '0')}`;
}

export function normalizeRotation(degrees) {
  return ((degrees % 360) + 360) % 360;
}

export function rotatedDimensions(width, height, rotation) {
  return normalizeRotation(rotation) % 180 === 0
    ? { width, height }
    : { width: height, height: width };
}

export function originalToRotated(point, width, height, rotation) {
  switch (normalizeRotation(rotation)) {
    case 90:
      return { x: height - point.y, y: point.x };
    case 180:
      return { x: width - point.x, y: height - point.y };
    case 270:
      return { x: point.y, y: width - point.x };
    default:
      return { x: point.x, y: point.y };
  }
}

export function rotatedToOriginal(point, width, height, rotation) {
  switch (normalizeRotation(rotation)) {
    case 90:
      return { x: point.y, y: height - point.x };
    case 180:
      return { x: width - point.x, y: height - point.y };
    case 270:
      return { x: width - point.y, y: point.x };
    default:
      return { x: point.x, y: point.y };
  }
}
