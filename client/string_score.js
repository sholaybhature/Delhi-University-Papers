// String Scoring Algorithm 0.1.22 | (c) 2009-2015 Joshaven Potter <yourtech@gmail.com>
// MIT License: http://opensource.org/licenses/MIT | https://github.com/joshaven/string_score
String.prototype.score = function (e, f) {
  if (this === e) return 1;
  if ("" === e) return 0;
  var d = 0,
    a,
    g = this.toLowerCase(),
    n = this.length,
    h = e.toLowerCase(),
    k = e.length,
    b;
  a = 0;
  var l = 1,
    m,
    c;
  f && (m = 1 - f);
  if (f)
    for (c = 0; c < k; c += 1)
      (b = g.indexOf(h[c], a)),
        -1 === b
          ? (l += m)
          : (a === b
              ? (a = 0.7)
              : ((a = 0.1), " " === this[b - 1] && (a += 0.8)),
            this[b] === e[c] && (a += 0.1),
            (d += a),
            (a = b + 1));
  else
    for (c = 0; c < k; c += 1) {
      b = g.indexOf(h[c], a);
      if (-1 === b) return 0;
      a === b ? (a = 0.7) : ((a = 0.1), " " === this[b - 1] && (a += 0.8));
      this[b] === e[c] && (a += 0.1);
      d += a;
      a = b + 1;
    }
  d = (0.5 * (d / n + d / k)) / l;
  h[0] === g[0] && 0.85 > d && (d += 0.15);
  return d;
};
