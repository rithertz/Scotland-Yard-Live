export const RAW_PHOTOS = [
  ['A1.jpg',6120,8160,6],['A2.jpg',5844,6628,0],['A3.jpg',6120,6404,0],['A4.jpg',6120,8160,1],
  ['B1.jpg',5240,6772,0],['B2.jpg',6120,8160,3],['B3.jpg',6120,8160,6],['B4.jpg',6120,8160,1],
  ['C1.jpg',6120,8160,1],['C2.jpg',6120,8160,1],['C3.jpg',5420,8160,0],['C4.jpg',5704,8160,3],
  ['D1.jpg',6120,8160,8],['D2.jpg',6120,8160,8],['D3.jpg',5312,8160,0],['D4.jpg',6120,8160,1],
].map(([filename,width,height,exifOrientation]) => ({ filename, width, height, exifOrientation, src: `../../../docs/game/evidence/board-photos/high-resolution/${filename}` }));
