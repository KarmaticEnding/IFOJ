(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.IFOJScoreColors = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Each shared boundary belongs to the following interval.
  var bands = [
    { min: 0, max: 10, from: '#FF0000', to: '#FF0000' },
    { min: 10, max: 25, from: '#FF0000', to: '#FFA900' },
    { min: 25, max: 50, from: '#FFA900', to: '#FFD800' },
    { min: 50, max: 75, from: '#FFD800', to: '#228B22' },
    { min: 75, max: 100, from: '#228B22', to: '#0000FF' }
  ];

  function normalize(value) {
    var score = Number(value);
    return Number.isFinite(score) ? Math.max(0, Math.min(100, score)) : 0;
  }

  function band(value) {
    var score = normalize(value);
    for (var i = 0; i < bands.length - 1; i++) if (score < bands[i].max) return i;
    return bands.length - 1;
  }

  function color(value) {
    var score = normalize(value), interval = bands[band(score)];
    var ratio = (score - interval.min) / (interval.max - interval.min);
    var result = '#';
    for (var offset = 1; offset < 7; offset += 2) {
      var from = parseInt(interval.from.slice(offset, offset + 2), 16);
      var to = parseInt(interval.to.slice(offset, offset + 2), 16);
      result += Math.round(from + (to - from) * ratio).toString(16).padStart(2, '0');
    }
    return result.toUpperCase();
  }

  return Object.freeze({ color: color, band: band, normalize: normalize });
}));
