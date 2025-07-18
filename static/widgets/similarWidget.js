(function () {
  console.log("🔁 Benzer ürün widget başlatıldı...");

  function getProductId() {
    try {
      // JSON-LD'den al
      const script = document.querySelector('script[type="application/ld+json"]');
      const json = JSON.parse(script?.innerText || "{}");

      if (json["@graph"] && Array.isArray(json["@graph"])) {
        const graphItem = json["@graph"].find(item => item.sku);
        return graphItem?.sku || null;
      }

      return json.sku || null;
    } catch (e) {
      console.warn("⚠️ JSON-LD parse hatası:", e);
      return null;
    }
  }

  function startWidget(productId) {
    if (!productId) {
      console.error("❌ product_id bulunamadı, widget durduruldu.");
      return;
    }

    console.log("🟢 Widget başlatılıyor, product_id:", productId);

    fetch(`https://searchprojectdemo.com/api/also-viewed-products/${productId}/`)
      .then(res => res.json())
      .then(data => {
        if (!data || data.length === 0) {
          console.log("🟡 Benzer ürün bulunamadı.");
          return;
        }

        // 👇 Basit örnek UI - kendine göre geliştir
        const container = document.createElement("div");
        container.style.position = "fixed";
        container.style.bottom = "20px";
        container.style.left = "20px";
        container.style.zIndex = "9999";
        container.style.background = "#fff";
        container.style.border = "1px solid #ccc";
        container.style.padding = "10px";
        container.style.boxShadow = "0 0 10px rgba(0,0,0,0.2)";
        container.innerHTML = "<h4>Benzer Ürünler</h4>";

        data.forEach(item => {
          const el = document.createElement("div");
          el.innerHTML = `
            <a href="/product/${item.id}" target="_blank" style="display:block;margin-bottom:8px;">
              <img src="${item.image_url}" alt="${item.name}" style="width:80px;height:auto;">
              <div>${item.name} - ${item.price} TL</div>
            </a>
          `;
          container.appendChild(el);
        });

        document.body.appendChild(container);
      })
      .catch(err => {
        console.error("❌ Widget verisi alınamadı:", err);
      });
  }

  function waitForProductIdAndStart(retries = 10) {
    const productId = getProductId();

    if (productId) {
      startWidget(productId);
    } else if (retries > 0) {
      console.log("⏳ product_id henüz yok, yeniden denenecek...");
      setTimeout(() => waitForProductIdAndStart(retries - 1), 500);
    } else {
      console.error("❌ product_id bulunamadı, widget durduruldu.");
    }
  }

  waitForProductIdAndStart();
})();
