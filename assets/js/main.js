/* ============================================================
   TATA 官網重新設計提案 — main.js
   原則：所有內容預設可見，GSAP 只做增強；prefers-reduced-motion 全部略過。
   ============================================================ */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 主導覽捲動狀態（rAF 節流） ---------- */
  var header = document.getElementById("siteHeader");
  var scrollTicking = false;
  function onScroll() {
    if (scrollTicking) return;
    scrollTicking = true;
    window.requestAnimationFrame(function () {
      header.classList.toggle("is-scrolled", window.scrollY > 80);
      scrollTicking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  header.classList.toggle("is-scrolled", window.scrollY > 80);

  /* ---------- 手機版選單 ---------- */
  var toggle = document.getElementById("menuToggle");
  var mobileNav = document.getElementById("mobileNav");
  function closeMenu() {
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "開啟選單");
    mobileNav.hidden = true;
    document.body.style.overflow = "";
    document.body.classList.remove("menu-open");
  }
  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") === "true";
    if (open) {
      closeMenu();
    } else {
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "關閉選單");
      mobileNav.hidden = false;
      document.body.style.overflow = "hidden";
      document.body.classList.add("menu-open");
    }
  });
  mobileNav.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", closeMenu);
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1100) closeMenu();
  });

  /* ---------- 活動倒數（真實日期計算） ---------- */
  document.querySelectorAll(".event-row__count").forEach(function (el) {
    var start = new Date(el.dataset.start + "T00:00:00+08:00");
    var end = new Date(el.dataset.end + "T23:59:59+08:00");
    var now = new Date();
    if (now < start) {
      var days = Math.ceil((start - now) / 86400000);
      el.textContent = "距離活動還有 " + days + " 天";
    } else if (now <= end) {
      el.textContent = "活動進行中";
    } else {
      el.textContent = "已圓滿落幕";
      el.classList.add("is-ended");
    }
  });

  /* ---------- 報名進度條：無 JS 時顯示完整比例，有 JS 時由 0 長出 ---------- */
  var bars = document.querySelectorAll(".progress");
  bars.forEach(function (bar) {
    var pct = Math.min(100, Math.max(0, parseFloat(bar.dataset.progress) || 0)) / 100;
    bar.querySelector(".progress__fill").style.setProperty("--p", pct);
  });

  /* ---------- AI 展示段：卡片滑入（IO，無 JS 時保持可見） ---------- */
  var aiCards = document.querySelectorAll(".ai-card");
  if (aiCards.length && "IntersectionObserver" in window && !reduced) {
    aiCards.forEach(function (c) { c.classList.add("ai-card--pre"); });
    var cardIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          cardIO.unobserve(en.target);
        }
      });
    }, { threshold: 0.2 });
    aiCards.forEach(function (c) { cardIO.observe(c); });
  }

  /* AI 段左欄導航：點擊平滑滾動＋滾動時高亮對應按鈕 */
  var aiNavBtns = document.querySelectorAll(".ai__nav button");
  aiNavBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.getElementById(btn.dataset.target);
      if (target) target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
    });
  });
  if (aiCards.length && aiNavBtns.length && "IntersectionObserver" in window) {
    var navIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        aiNavBtns.forEach(function (b) {
          b.classList.toggle("is-active", b.dataset.target === en.target.id);
        });
      });
    }, { rootMargin: "-40% 0px -40% 0px" });
    aiCards.forEach(function (c) { navIO.observe(c); });
  }

  /* ---------- 以下為動效增強；reduced-motion 或 GSAP 未載入時全部略過 ---------- */
  if (reduced || !window.gsap) return;
  gsap.registerPlugin(window.ScrollTrigger);

  /* Hero 進場：疊層淡入＋主標逐字（30ms/字）＋副標與 CTA 延遲淡入 */
  var heroTl = gsap.timeline({ defaults: { ease: "power2.out" } });
  heroTl
    .from(".hero__overlay", { autoAlpha: 0, duration: 0.6 }, 0)
    .from(".hero__chars .ch", { autoAlpha: 0, x: -18, duration: 0.5, stagger: 0.03 }, 0.2)
    .from("[data-hero-fade]", { autoAlpha: 0, y: 20, duration: 0.7, stagger: 0.2 }, 0.8)
    .from(".hero__stats .stat", { autoAlpha: 0, y: 18, duration: 0.6, stagger: 0.08, ease: "expo.out" }, 1.2);

  /* 段落 reveal：預設可見，進場時輕浮上 */
  gsap.utils.toArray("[data-reveal]").forEach(function (el) {
    gsap.from(el, {
      autoAlpha: 0,
      y: 28,
      duration: 0.9,
      ease: "expo.out",
      scrollTrigger: { trigger: el, start: "top 88%", once: true }
    });
  });

  /* 統計數字 count-up（1969 年份不動） */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseInt(el.dataset.count, 10);
    var obj = { val: 0 };
    gsap.to(obj, {
      val: target,
      duration: 1.6,
      ease: "expo.out",
      scrollTrigger: { trigger: el, start: "top 92%", once: true },
      onUpdate: function () {
        el.textContent = Math.round(obj.val).toLocaleString("en-US");
      }
    });
  });

  /* 進度條金線由左長出（transform，不動 layout） */
  bars.forEach(function (bar) {
    var fill = bar.querySelector(".progress__fill");
    gsap.from(fill, {
      scaleX: 0,
      duration: 1.2,
      ease: "expo.out",
      scrollTrigger: { trigger: bar, start: "top 90%", once: true }
    });
  });

  /* 團隊卡：依序淡入上移（stagger 80ms）；手風琴互動本身為純 CSS */
  if (document.querySelector(".team__row")) {
    gsap.from(".team-card", {
      autoAlpha: 0,
      y: 24,
      duration: 0.7,
      ease: "expo.out",
      stagger: 0.08,
      scrollTrigger: { trigger: ".team__row", start: "top 85%", once: true }
    });
  }

  /* Livo 風逐字進場：data-split-chars 的標題（保留 .text-gold 等內層標記） */
  function splitChars(el) {
    var nodes = Array.prototype.slice.call(el.childNodes);
    nodes.forEach(function (node) {
      if (node.nodeType === Node.TEXT_NODE) {
        var frag = document.createDocumentFragment();
        node.textContent.split("").forEach(function (chr) {
          if (chr.trim() === "") { frag.appendChild(document.createTextNode(chr)); return; }
          var s = document.createElement("span");
          s.className = "ch-w";
          s.textContent = chr;
          frag.appendChild(s);
        });
        el.replaceChild(frag, node);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        splitChars(node);
      }
    });
  }
  document.querySelectorAll("[data-split-chars]").forEach(function (el) {
    splitChars(el);
    gsap.from(el.querySelectorAll(".ch-w"), {
      autoAlpha: 0,
      y: 10,
      filter: "blur(8px)",
      duration: 0.6,
      ease: "back.out(1.6)",
      stagger: 0.045,
      scrollTrigger: { trigger: el, start: "top 88%", once: true }
    });
  });
  /* ---------- Hero 世界地圖：弧線描繪＋城市浮現＋統計卡進場 ---------- */
  var worldArcs = document.querySelector(".hero__world-arcs");
  if (worldArcs && reduced && worldArcs.pauseAnimations) worldArcs.pauseAnimations();
  if (worldArcs && !reduced && typeof gsap !== "undefined") {
    var baseArcs = worldArcs.querySelectorAll(".arcs-base path");
    baseArcs.forEach(function (pt) {
      var L = pt.getTotalLength();
      pt.style.strokeDasharray = L;
      pt.style.strokeDashoffset = L;
    });
    var atl = gsap.timeline({ delay: 0.9 });
    atl.to(baseArcs, { strokeDashoffset: 0, duration: 1.2, stagger: 0.15, ease: "power2.out" })
      .from(worldArcs.querySelectorAll(".arcs-cities .city"), { autoAlpha: 0, scale: 0.3, transformOrigin: "center", stagger: 0.1, duration: 0.4, ease: "back.out(2)" }, "-=0.5")
      .from(worldArcs.querySelectorAll(".arcs-labels .lbl"), { autoAlpha: 0, y: 4, stagger: 0.08, duration: 0.4 }, "-=0.3")
      .from(worldArcs.querySelectorAll(".arcs-movers circle"), { autoAlpha: 0, duration: 0.6 }, "-=0.2")
      .from(document.querySelectorAll(".hchip"), { y: 14, autoAlpha: 0, stagger: 0.1, duration: 0.5, ease: "power3.out" }, "-=0.4");
  }
})();
