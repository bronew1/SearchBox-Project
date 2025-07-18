(function () {
  console.log("📦 Benzer ürün widget başlatıldı...");

  var checkCount = 0;
  var interval = setInterval(function () {
    checkCount++;
    if (checkCount > 30) {
      console.log("⏰ Süre doldu, widget durduruldu.");
      clearInterval(interval);
    }

    const productEvent = window.dataLayer?.find(e => e.event === "view_item" && e.product_id);
    let sku = productEvent?.product_id;

    if (!sku) {
      const skuText = document.querySelector("p.product-info-sku")?.textContent;
      if (skuText?.includes("Ürün Kodu:")) {
        sku = skuText.split("Ürün Kodu:")[1].trim();
        console.log("🔁 Fallback ile SKU bulundu:", sku);
      }
    }

    if (!sku) {
      console.log("❌ SKU bulunamadı, widget durduruldu.");
      return;
    }

    console.log("✅ SKU bulundu:", sku);

    clearInterval(interval);

    const apiUrl = "https://searchprojectdemo.com/api/recommendations/similar/" + sku + "/";
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const products = data.products || [];
        console.log("🎯 Benzer ürünler geldi:", products);

        if (products.length === 0) {
          console.log("⚠️ Benzer ürün yok.");
          return;
        }

        const style = document.createElement("style");
        style.innerHTML = `
          #similar-products-slider {
            padding: 20px;
            margin-top: 40px;
            border-top: 1px solid #ccc;
            font-family: sans-serif;
          }
          #similar-products-slider h2 {
            font-size: 20px;
            margin-bottom: 12px;
          }
          .similar-products-grid {
            display: flex;
            overflow-x: auto;
            gap: 12px;
          }
          .similar-product-card {
            flex: 0 0 200px;
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 10px;
            background: #fff;
            text-align: center;
          }
          .similar-product-card img {
            max-width: 100%;
            height: auto;
          }
          .similar-product-card .price {
            font-weight: bold;
            margin-top: 4px;
          }
        `;
        document.head.appendChild(style);

        const container = document.createElement("div");
        container.id = "similar-products-slider";
        container.innerHTML = "<h2>Benzer Ürünler</h2>";

        const grid = document.createElement("div");
        grid.className = "similar-products-grid";

        products.forEach(p => {
          const card = document.createElement("div");
          card.className = "similar-product-card";
          card.innerHTML = `
            <a href="${p.url}">
              <img src="${p.image}" alt="${p.name}" />
              <div>${p.name}</div>
              <div class="price">${p.price} TL</div>
            </a>
          `;
          grid.appendChild(card);
        });

        container.appendChild(grid);

        // 🎯 Hedef: .vertical-tab elementinin sonuna ekle
        const targetEl = document.querySelector(".vertical-tab");
        if (targetEl) {
          targetEl.appendChild(container);
          console.log("✅ Widget .vertical-tab altına eklendi.");
        } else {
          document.body.appendChild(container);
          console.warn("⚠️ .vertical-tab bulunamadı, body'e eklendi.");
        }
      })
      .catch(err => {
        console.error("❌ API hatası:", err);
      });
  }, 300);
})();
