(function () {
  var r = document.documentElement;
  try { var t = localStorage.getItem('theme'); if (t) r.dataset.theme = t; } catch (e) {}
  document.getElementById('theme').onclick = function () {
    var dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme:dark)').matches;
    r.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('theme', r.dataset.theme); } catch (e) {}
  };

  /* syntax highlight */
  var KW = {
    python: 'def class return if elif else for while in not and or is None True False import from as with try except finally raise pass break continue lambda yield self',
    php: 'function class return if elseif else foreach for while as new public private protected static array isset empty null true false use namespace try catch throw break continue',
    go: 'func return if else for range var const type struct interface map make append len package import nil true false break continue switch case default go defer chan'
  };
  var COM = { python: '#.*', php: '\\/\\/.*|#.*|\\/\\*[\\s\\S]*?\\*\\/', go: '\\/\\/.*|\\/\\*[\\s\\S]*?\\*\\/' };
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function hl(src, lang) {
    var kw = (KW[lang] || '').split(' ').join('|');
    var re = new RegExp('(' + (COM[lang] || '//.*') + ')|("(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\'|`[^`]*`)|(\\b\\d+(?:\\.\\d+)?\\b)|(\\b(?:' + kw + ')\\b)|(\\b[A-Za-z_]\\w*)(?=\\()', 'g');
    var out = '', last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      var c = m[1] ? 'c' : m[2] ? 's' : m[3] ? 'm' : m[4] ? 'k' : 'f';
      out += '<span class="' + c + '">' + esc(m[0]) + '</span>';
      last = re.lastIndex;
    }
    out += esc(src.slice(last));
    return out.split('\n').map(function (l) { return '<span class="ln">' + (l || ' ') + '</span>'; }).join('');
  }
  document.querySelectorAll('.panel code').forEach(function (c) {
    c.dataset.raw = c.textContent;
    c.innerHTML = hl(c.textContent, c.closest('.panel').dataset.lang);
  });

  /* tab groups (problem editor + topic code examples) */
  var groups = document.querySelectorAll('[data-tabs]');
  var pref; try { pref = localStorage.getItem('lang'); } catch (e) {}

  function updateEditorPanels(g, targetLang, targetMethod) {
    var hasMethods = !!g.querySelector('.panel[data-method]');
    var langTabs = g.querySelectorAll('.ed-bar [role=tab]');

    var curMethod = targetMethod;
    if (hasMethods && curMethod === undefined) {
      var activeMethodBtn = document.querySelector('[data-m][aria-selected="true"]');
      curMethod = activeMethodBtn ? activeMethodBtn.dataset.m : "0";
    }

    var panels = g.querySelectorAll('.panel');
    var availLangs = [];
    panels.forEach(function (p) {
      if (!hasMethods || p.dataset.method === curMethod) {
        if (availLangs.indexOf(p.dataset.lang) === -1) availLangs.push(p.dataset.lang);
      }
    });

    var chosenLang = targetLang;
    if (availLangs.indexOf(chosenLang) === -1) {
      chosenLang = availLangs.length ? availLangs[0] : 'python';
    }

    langTabs.forEach(function (b) {
      var l = b.dataset.lang;
      b.setAttribute('aria-selected', l === chosenLang);
      b.style.display = (availLangs.indexOf(l) > -1) ? '' : 'none';
    });

    panels.forEach(function (p) {
      if (hasMethods) {
        p.hidden = !(p.dataset.method === curMethod && p.dataset.lang === chosenLang);
      } else {
        p.hidden = p.dataset.lang !== chosenLang;
      }
    });

    try { localStorage.setItem('lang', chosenLang); } catch (e) {}
  }

  function pickAll(l) {
    groups.forEach(function (g) {
      updateEditorPanels(g, l);
    });
  }

  groups.forEach(function (g) {
    var tabs = g.querySelectorAll('.ed-bar [role=tab]');
    tabs.forEach(function (b) { b.onclick = function () { pickAll(b.dataset.lang); }; });
    var first = tabs.length ? tabs[0].dataset.lang : null;
    var ok = [].some.call(tabs, function (b) { return b.dataset.lang === pref; });
    var l = ok ? pref : first;
    updateEditorPanels(g, l);

    var c = g.querySelector('.copy');
    if (c) c.onclick = function () {
      var code = g.querySelector('.panel:not([hidden]) code'), label = c.querySelector('span');
      if (!code) return;
      navigator.clipboard.writeText(code.dataset.raw).then(function () {
        label.textContent = 'Nusxalandi';
        setTimeout(function () { label.textContent = 'Nusxalash'; }, 1200);
      });
    };
  });

  /* method switcher (hover and click) */
  var mBtns = document.querySelectorAll('[data-m]');
  if (mBtns.length) {
    function pickMethod(idx) {
      mBtns.forEach(function (b) {
        b.setAttribute('aria-selected', b.dataset.m === idx);
      });
      document.querySelectorAll('.m-view').forEach(function (v) {
        v.hidden = v.dataset.m !== idx;
      });
      var curLang = localStorage.getItem('lang') || 'python';
      groups.forEach(function (g) {
        updateEditorPanels(g, curLang, idx);
      });
    }

    mBtns.forEach(function (b) {
      b.onclick = function () { pickMethod(b.dataset.m); };
      b.onmouseenter = function () { pickMethod(b.dataset.m); };
    });
  }

  /* index filters */
  var q = document.getElementById('q');
  if (q) {
    var rows = document.querySelectorAll('.list .row'), none = document.getElementById('none'),
        count = document.getElementById('count'), st = { d: '', t: '' };
    function apply() {
      var shown = 0, s = q.value.toLowerCase().trim();
      rows.forEach(function (x) {
        var ok = x.dataset.s.indexOf(s) > -1 && (!st.d || x.dataset.d === st.d) &&
                 (!st.t || x.dataset.t.split(' ').indexOf(st.t) > -1);
        x.hidden = !ok; if (ok) shown++;
      });
      none.hidden = shown > 0;
      count.textContent = shown;
    }
    function group(sel, key) {
      var bs = document.querySelectorAll(sel);
      bs.forEach(function (b) {
        b.onclick = function () {
          var on = b.getAttribute('aria-pressed') === 'true' && b.dataset[key];
          st[key] = on ? '' : b.dataset[key];
          bs.forEach(function (o) { o.setAttribute('aria-pressed', (o.dataset[key] || '') === st[key]); });
          apply();
        };
      });
    }
    group('.seg button', 'd');
    group('.tf button', 't');
    q.oninput = apply;
  }

  /* topics search */
  var tq = document.getElementById('tq');
  if (tq) {
    var cards = document.querySelectorAll('.grid .card'), tnone = document.getElementById('tnone');
    tq.oninput = function () {
      var s = tq.value.toLowerCase().trim(), shown = 0;
      cards.forEach(function (c) {
        var ok = c.dataset.s.indexOf(s) > -1;
        c.hidden = !ok; if (ok) shown++;
      });
      tnone.hidden = shown > 0;
    };
  }
})();
