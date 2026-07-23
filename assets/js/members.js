/* 會員名錄：從 assets/data/members.json 載入，客戶端搜尋＋篩選＋分頁。
   未來搬 Supabase 時，只需把 fetch 的 URL 換成 API endpoint（回應格式相同，見 docs/ARCHITECTURE.md）。 */
(function () {
  "use strict";
  var DATA_URL = "assets/data/members.json";
  var PAGE_SIZE = 50;

  var state = { q: "", district: "", scope: "", page: 1, all: [] };

  var rowsEl = document.getElementById("mRows");
  var pagerEl = document.getElementById("mPager");
  var countEl = document.getElementById("mCount");
  var searchEl = document.getElementById("mSearch");
  var districtEl = document.getElementById("mDistrict");
  var scopeEl = document.getElementById("mScope");
  if (!rowsEl) return;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function filtered() {
    var q = state.q.trim().toLowerCase();
    return state.all.filter(function (m) {
      if (state.district && m.district !== state.district) return false;
      if (state.scope && m.scope !== state.scope) return false;
      if (!q) return true;
      return (m.name + " " + (m.name_en || "") + " " + (m.boss || "") + " " + (m.rep || "") + " " + (m.phone || "") + " " + (m.address || ""))
        .toLowerCase().indexOf(q) !== -1;
    });
  }

  function render() {
    var list = filtered();
    var pages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
    if (state.page > pages) state.page = pages;
    var start = (state.page - 1) * PAGE_SIZE;
    var slice = list.slice(start, start + PAGE_SIZE);

    countEl.textContent = "共 " + list.length.toLocaleString() + " 家（第 " + state.page + " / " + pages + " 頁）";

    if (!slice.length) {
      rowsEl.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:2.5rem">查無符合的會員資料</td></tr>';
    } else {
      rowsEl.innerHTML = slice.map(function (m) {
        var site = m.website
          ? '<a href="https://' + esc(m.website.replace(/^https?:\/\//, "")) + '" target="_blank" rel="noopener">' + esc(m.website) + "</a>"
          : '<span style="color:var(--muted)">—</span>';
        return "<tr>" +
          '<td><span class="m-name">' + esc(m.name) + "</span>" + (m.rep ? '<span class="m-sub">' + esc(m.rep) + "</span>" : "") + "</td>" +
          "<td>" + esc(m.district) + "</td>" +
          "<td>" + esc(m.scope) + "</td>" +
          '<td style="white-space:nowrap">' + esc(m.phone) + "</td>" +
          '<td style="white-space:nowrap">' + esc(m.join_date) + "</td>" +
          "<td>" + site + "</td>" +
          "</tr>";
      }).join("");
    }

    var btns = [];
    btns.push('<button type="button" data-p="prev"' + (state.page === 1 ? " disabled" : "") + ">‹ 上一頁</button>");
    var lo = Math.max(1, state.page - 3), hi = Math.min(pages, state.page + 3);
    for (var p = lo; p <= hi; p++) {
      btns.push('<button type="button" data-p="' + p + '"' + (p === state.page ? ' class="is-active"' : "") + ">" + p + "</button>");
    }
    btns.push('<button type="button" data-p="next"' + (state.page === pages ? " disabled" : "") + ">下一頁 ›</button>");
    pagerEl.innerHTML = btns.join("");
  }

  pagerEl.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b || b.disabled) return;
    var pages = Math.max(1, Math.ceil(filtered().length / PAGE_SIZE));
    if (b.dataset.p === "prev") state.page = Math.max(1, state.page - 1);
    else if (b.dataset.p === "next") state.page = Math.min(pages, state.page + 1);
    else state.page = parseInt(b.dataset.p, 10);
    render();
    window.scrollTo({ top: document.querySelector(".members-toolbar").getBoundingClientRect().top + window.scrollY - 120, behavior: "smooth" });
  });

  var debounce;
  searchEl.addEventListener("input", function () {
    clearTimeout(debounce);
    debounce = setTimeout(function () { state.q = searchEl.value; state.page = 1; render(); }, 200);
  });
  districtEl.addEventListener("change", function () { state.district = districtEl.value; state.page = 1; render(); });
  scopeEl.addEventListener("change", function () { state.scope = scopeEl.value; state.page = 1; render(); });

  fetch(DATA_URL)
    .then(function (r) { return r.json(); })
    .then(function (data) {
      state.all = data.members || [];
      var districts = {}, scopes = {};
      state.all.forEach(function (m) {
        if (m.district) districts[m.district] = (districts[m.district] || 0) + 1;
        if (m.scope) scopes[m.scope] = (scopes[m.scope] || 0) + 1;
      });
      Object.keys(districts).sort(function (a, b) { return districts[b] - districts[a]; })
        .forEach(function (d) { districtEl.insertAdjacentHTML("beforeend", "<option>" + esc(d) + "（" + districts[d] + "）</option>"); districtEl.lastChild.value = d; });
      Object.keys(scopes).sort(function (a, b) { return scopes[b] - scopes[a]; })
        .forEach(function (s) { scopeEl.insertAdjacentHTML("beforeend", "<option>" + esc(s) + "（" + scopes[s] + "）</option>"); scopeEl.lastChild.value = s; });
      render();
    })
    .catch(function () {
      rowsEl.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:2.5rem">名錄載入失敗（本頁需透過 http 伺服器開啟，直接雙擊檔案會被瀏覽器擋下）</td></tr>';
    });
})();
