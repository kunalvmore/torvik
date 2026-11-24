// Torvik website: phone menu, "Notify me" form and motion. No tracking, no third-party code.
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------------------------------------------------------------- phone menu
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    });
  }

  // ---------------------------------------------------------------- scroll reveals
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  // ---------------------------------------------------------------- scroll: progress bar, header, parallax
  var header = document.querySelector(".site-header");
  var bar = document.querySelector(".progress-bar");
  var layers = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll(".parallax"));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    var max = root.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
    if (header) header.classList.toggle("scrolled", y > 12);
    var vh = window.innerHeight;
    for (var i = 0; i < layers.length; i++) {
      var r = layers[i].getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) continue;
      var offset = (r.top + r.height / 2 - vh / 2) * -0.06;
      layers[i].style.transform = "translate3d(0," + offset.toFixed(1) + "px,0)";
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();

  // ---------------------------------------------------------------- hero tilt (mouse only)
  var hero = document.querySelector(".hero");
  var tilt = document.querySelector(".tilt");
  var finePointer = window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (hero && tilt && finePointer && !reduce) {
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
    var step = function () {
      cx += (tx - cx) * 0.08;
      cy += (ty - cy) * 0.08;
      tilt.style.transform = "rotateY(" + cx.toFixed(2) + "deg) rotateX(" + cy.toFixed(2) + "deg)";
      raf = (Math.abs(tx - cx) > 0.01 || Math.abs(ty - cy) > 0.01) ? requestAnimationFrame(step) : 0;
    };
    var kick = function () { if (!raf) raf = requestAnimationFrame(step); };
    tilt.style.transition = "none";
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - 0.5) * 12;
      ty = -((e.clientY - r.top) / r.height - 0.5) * 8;
      kick();
    });
    hero.addEventListener("pointerleave", function () { tx = 0; ty = 0; kick(); });
  }

  // ---------------------------------------------------------------- "Notify me" form
  var form = document.querySelector(".notify-form");
  if (!form) return;
  var note = form.parentNode.querySelector(".form-note");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = form.email.value.trim();
    if (!email) return;
    var endpoint = form.getAttribute("data-endpoint");
    if (!endpoint) {
      // No email service connected yet: open a pre-filled email instead.
      var body = encodeURIComponent("Please let me know when the next version of Torvik is out.\n\nMy email: " + email);
      window.location.href = form.getAttribute("data-mailto") + "&body=" + body;
      if (note) note.textContent = "Your email app should open. Send the message and you’re on the list.";
      return;
    }
    fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) {
        if (!r.ok) throw new Error("bad status");
        form.reset();
        if (note) note.textContent = "You’re on the list. We’ll email you once, when it’s out.";
      })
      .catch(function () {
        if (note) note.textContent = "That didn’t go through. Please try again in a moment.";
      });
  });
})();
