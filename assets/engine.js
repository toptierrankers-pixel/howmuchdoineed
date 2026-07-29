/* ============================================================
   HowMuchDoINeed calc engine
   Each page sets window.CALC = { fields:[...], compute(v){...} }
   then calls HowMuchDoINeed.mount(). The engine renders the input
   form, wires live recalculation, and paints the result rail.
   ============================================================ */
(function () {
  "use strict";

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  // numeric helpers available to page configs
  var H = {
    round: function (n, dp) { var f = Math.pow(10, dp || 0); return Math.round(n * f) / f; },
    ceil: function (n) { return Math.ceil(n); },
    fmt: function (n, dp) {
      if (!isFinite(n)) return "0";
      var s = (dp == null ? n : H.round(n, dp));
      return s.toLocaleString("en-US", { maximumFractionDigits: dp == null ? 2 : dp });
    }
  };

  function buildForm(cfg, onChange) {
    var form = el("div");
    form.setAttribute("role", "group");
    cfg.fields.forEach(function (f) {
      var wrap = el("div", "field" + (f.options ? " select" : ""));
      var id = "f_" + f.id;
      var lab = el("label", null, f.label);
      lab.setAttribute("for", id);
      wrap.appendChild(lab);

      var line = el("div", "inputline");
      var input;
      if (f.options) {
        input = el("select");
        f.options.forEach(function (o) {
          var opt = el("option", null, o.label);
          opt.value = o.value;
          if (String(o.value) === String(f.value)) opt.selected = true;
          input.appendChild(opt);
        });
      } else {
        input = el("input");
        input.type = "number";
        input.value = f.value;
        if (f.min != null) input.min = f.min;
        if (f.step != null) input.step = f.step;
        input.inputMode = "decimal";
      }
      input.id = id;
      input.setAttribute("data-field", f.id);
      input.addEventListener("input", onChange);
      input.addEventListener("change", onChange);
      line.appendChild(input);
      if (f.unit) line.appendChild(el("span", "unit", f.unit));
      wrap.appendChild(line);
      form.appendChild(wrap);
    });
    return form;
  }

  function readValues(root, cfg) {
    var v = {};
    cfg.fields.forEach(function (f) {
      var node = root.querySelector('[data-field="' + f.id + '"]');
      var raw = node ? node.value : f.value;
      v[f.id] = f.options ? raw : parseFloat(raw);
      if (!f.options && (isNaN(v[f.id]) || v[f.id] < 0)) v[f.id] = 0;
    });
    return v;
  }

  function paint(rail, out) {
    rail.innerHTML = "";
    rail.appendChild(el("div", "rlabel", out.label || "Estimate"));
    var val = el("div", "rvalue");
    val.innerHTML = out.value + (out.unit ? ' <small>' + out.unit + "</small>" : "");
    rail.appendChild(val);

    if (out.lines && out.lines.length) {
      var brk = el("div", "rbreak");
      out.lines.forEach(function (ln) {
        var row = el("div", "row");
        row.appendChild(el("span", null, ln.label));
        row.appendChild(el("span", null, ln.value));
        brk.appendChild(row);
      });
      rail.appendChild(brk);
    }
    if (out.note) rail.appendChild(el("div", "rnote", out.note));
  }

  var HowMuchDoINeed = {
    helpers: H,
    mount: function () {
      var cfg = window.CALC;
      if (!cfg) return;
      var inputsHost = document.getElementById("calc-inputs");
      var rail = document.getElementById("calc-result");
      if (!inputsHost || !rail) return;

      var run = function () {
        var v = readValues(inputsHost, cfg);
        var out = cfg.compute(v, H);
        var price = parseFloat(v.price);
        if (price > 0) {
          var head = parseFloat(String(out.value).replace(/,/g, ""));
          if (isFinite(head)) {
            out.lines = (out.lines || []).concat([{ label: "Estimated cost", value: "$" + H.fmt(head * price, 2) }]);
          }
        }
        paint(rail, out);
      };
      inputsHost.appendChild(buildForm(cfg, run));
      run();
    }
  };

  window.HowMuchDoINeed = HowMuchDoINeed;
  document.addEventListener("DOMContentLoaded", HowMuchDoINeed.mount);
})();
